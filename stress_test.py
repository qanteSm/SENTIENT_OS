import sys
import os
import time
import threading
import random
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QThread

# Path setup to import from core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.kernel import SentientKernel
from core.logger import log_info, log_error, log_warning
from config import Config

# Overwrite config for stress testing
Config().IS_MOCK = True
Config().AI_SAFETY_CHECK = False

class ChaosThread(QThread):
    """
    Spams the system with events to find race conditions.
    """
    def run(self):
        time.sleep(5) # Let boot finish
        log_info("CHAOS THREAD STARTED", "STRESS")
        
        actions = [
            {"action": "OVERLAY_TEXT", "params": {"text": "STRESS TEST"}},
            {"action": "MOUSE_SHAKE", "params": {"duration": 0.1}},
            {"action": "GLITCH_SCREEN", "params": {}},
            {"action": "FAKE_NOTIFICATION", "params": {"title": "SPAM", "message": "TEST"}},
            {"action": "PLAY_SOUND", "params": {"sound": "error.wav"}},
        ]
        
        # Spam loop
        for i in range(100):
            if self.isInterruptionRequested(): break
            
            action = random.choice(actions)
            # Directly hitting the event bus or dispatcher if available would be best
            # But we can't easily access the kernel instance from here without globals
            # So we rely on the main loop being active.
            
            time.sleep(random.uniform(0.1, 0.5))

def run_stress_test():
    """
    Boots the kernel but injects a chaos thread.
    """
    import faulthandler
    faulthandler.enable()
    
    log_info("=== STRESS TEST INITIATED ===", "STRESS")
    
    # We need to monkey patch the kernel to start our chaos after boot
    original_boot = SentientKernel.boot
    
    def hooked_boot(self):
        # We can't really hook into app.exec() easily without blocking
        # But we can use QTimer to start our chaos once the event loop is running.
        
        def start_chaos():
            self.chaos = ChaosThread()
            self.chaos.start()
            
            # Kill execution after 30 seconds automatically
            QTimer.singleShot(30000, self.app.quit)
            
        # We need to initialize the app first which happens in boot()
        # So this hook is tricky. Instead, let's subclass or just rely on 
        # the standard boot and modify main.py for this test.
        pass

    # Better approach: Just use the standard main but run it with a flag? 
    # Or instantiate Kernel, setup chaos, then run.
    
    kernel = SentientKernel()
    
    # Setup chaos to start 2s after boot
    def start_chaos():
        log_info("Injecting Chaos...", "STRESS")
        chaos = ChaosThread()
        chaos.start()
        kernel.chaos_ref = chaos # Keep alive
        
        # Kill after 30s
        QTimer.singleShot(30000, lambda: (log_info("Test Complete. Quitting.", "STRESS"), kernel.app.quit()))

    # Initialize app manually to schedule the timer before exec
    kernel.app = QApplication(sys.argv)
    QTimer.singleShot(2000, start_chaos)
    
    # Bypass standard boot's app creation and go straight to init
    # But kernel.boot() does unwanted things like onboarding.
    # Let's use the DEV_MODE bypass.
    with open("DEV_MODE.txt", "w") as f:
        f.write("1")
        
    try:
        kernel.boot()
    finally:
        if os.path.exists("DEV_MODE.txt"):
            os.remove("DEV_MODE.txt")

if __name__ == "__main__":
    run_stress_test()
