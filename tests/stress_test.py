import sys
import os
import time
import random
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QThread, QMetaObject, Qt, Q_ARG

# Path setup to import from core
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir)) if "tests" in current_dir else os.path.dirname(current_dir)
sys.path.append(project_root)

from core.kernel import SentientKernel
from core.logger import log_info, log_error
from config import Config

# Overwrite config for stress testing
Config().IS_MOCK = True
Config().AI_SAFETY_CHECK = False

class ChaosThread(QThread):
    def run(self):
        time.sleep(5) 
        log_info("CHAOS THREAD STARTED", "STRESS")
        
        actions = [
            {"action": "MOUSE_SHAKE", "params": {"duration": 0.1}},
            {"action": "PLAY_SOUND", "params": {"sound": "error.wav"}},
        ]
        
        for i in range(50):
            if self.isInterruptionRequested(): break
            
            # Use event bus to trigger actions safely
            from core.event_bus import bus
            action = random.choice(actions)
            bus.publish("system.pulse", action)
            
            time.sleep(random.uniform(0.1, 0.3))

def run_stress_test():
    import faulthandler
    faulthandler.enable()
    
    log_info("=== STRESS TEST STARTED ===", "STRESS")
    
    # Bypass onboarding
    with open("DEV_MODE.txt", "w") as f:
        f.write("1")

    try:
        # Create kernel -> creates QApplication
        kernel = SentientKernel()
        
        # Inject Chaos AFTER boot starts the event loop
        # We use a QTimer singleShot scheduled *before* boot() blocks
        
        def start_chaos_logic():
            log_info("Injecting Chaos...", "STRESS")
            # We must attach it to kernel to keep reference
            kernel.chaos = ChaosThread()
            kernel.chaos.start()
            
            # Auto-kill after 15s
            QTimer.singleShot(15000, kernel.app.quit)

        # We need to manually initialize app if not already done by kernel.__init__?
        # Check kernel implementation: kernel.boot() creates QApplication.
        # But we can't schedule QTimer before QApplication exists.
        
        # FIX: Manually create QApplication first if kernel doesn't do it in __init__
        if not QApplication.instance():
             app = QApplication(sys.argv)
             kernel.app = app # Inject it into kernel
        
        QTimer.singleShot(2000, start_chaos_logic)
        
        kernel.boot()
        
    except Exception as e:
        log_error(f"TEST FAILED: {e}", "STRESS")
    finally:
        if os.path.exists("DEV_MODE.txt"):
            os.remove("DEV_MODE.txt")
        log_info("=== STRESS TEST FINISHED ===", "STRESS")

if __name__ == "__main__":
    run_stress_test()
