import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, QTimer

from config import Config
from core.event_bus import bus
from core.logger import log_info, log_error, log_warning
from core.state_manager import StateManager
from core.memory import Memory
from core.anger_engine import AngerEngine
from core.heartbeat import Heartbeat
from core.function_dispatcher import FunctionDispatcher
from core.gemini_brain import GeminiBrain
from story.story_manager import StoryManager
from core.safety_net import SafetyNet
from hardware.brightness_ops import BrightnessOps
from hardware.window_ops import WindowOps
from visual.icon_ops import IconOps
from core.sensors.presence_sensor import PresenceSensor
from core.sensors.window_sensor import WindowSensor
from core.resilience_manager import ResilienceManager
from hardware.wallpaper_ops import WallpaperOps
from visual.glitch_logic import GlitchLogic

class SentientKernel:
    """
    The Sentient Kernel - Central management unit of SENTIENT_OS.
    Handles lifecycle, component orchestration, and system health.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SentientKernel, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, app_argv=None):
        if not self._initialized:
            self._initialized = True
            self.app_argv = app_argv or sys.argv
            self.app = None
            
            # Core Components
            self.state_manager = None
            self.memory = None
            self.anger = None
            self.dispatcher = None
            self.brain = None
            self.heartbeat = None
            self.story_manager = None
            self.safety = None
            
            # Sensors
            self.presence_sensor = None
            self.window_sensor = None
            
            # Resilience
            self.resilience = None

    def boot(self):
        """Initializes all systems and starts the application loop."""
        print(f"\n[KERNEL] Booting {Config.APP_NAME} v{Config.VERSION}...")
        
        # 1. Initialize Qt Application
        self.app = QApplication(self.app_argv)
        
        # 2. Hardware Restoration & Safety
        if BrightnessOps.check_and_restore_on_startup():
            log_info("Brightness recovered from previous crash", "BOOT")
        
        BrightnessOps.save_brightness()
        WallpaperOps.save_current_wallpaper()
        
        self.safety = SafetyNet()
        self.safety.start_monitoring()
        
        # 3. Resilience Engine (Ghost)
        self.resilience = ResilienceManager(self)
        if not Config.IS_MOCK:
            self.resilience.spawn_watchdog()
        
        # 4. Core Engine Initialization
        log_info("Initializing Core Engines...", "KERNEL")
        self.state_manager = StateManager()
        self.memory = Memory()
        self.anger = AngerEngine()
        self.dispatcher = FunctionDispatcher()
        self.brain = GeminiBrain()
        
        # Link systems
        self.brain.set_memory(self.memory)
        SafetyNet.set_memory(self.memory)
        self.dispatcher.memory = self.memory
        self.dispatcher.brain = self.brain
        
        # 5. Sensors & Autonomy
        log_info("Initializing Sensors...", "KERNEL")
        self.presence_sensor = PresenceSensor()
        self.window_sensor = WindowSensor()
        
        self.heartbeat = Heartbeat(self.anger, self.brain, self.dispatcher)
        self.dispatcher.heartbeat = self.heartbeat
        
        # 5.1 Initialize Glitch Logic (Autonomous Visuals)
        self.glitch_logic = GlitchLogic(self.dispatcher)
        
        # 6. Check for crash recovery
        recovery_reason = self.state_manager.check_for_recovery(self.dispatcher)
        if recovery_reason:
            self.resilience.handle_recovery("crash")
        
        # 7. Start Autonomous Threads
        self.presence_sensor.start()
        self.window_sensor.start()
        self.heartbeat.start()
        
        # 8. Story Engine
        log_info("Initializing Story Engine...", "KERNEL")
        self.story_manager = StoryManager(self.dispatcher, self.memory, self.brain)
        QTimer.singleShot(1000, self.story_manager.start_story)
        
        # 9. Event Bus Subscriptions
        self._setup_global_subscriptions()
        
        # Connect heartbeat signals to Event Bus
        self.heartbeat.pulse_signal.connect(lambda action: bus.publish("system.pulse", {"action": action}))
        
        log_info("SENTIENT_OS Kernel Active and Observant.", "KERNEL")
        bus.publish("system.boot_complete")
        
        try:
            sys.exit(self.app.exec())
        except Exception as e:
            log_error(f"Kernel Panic: {e}", "KERNEL")
            self.shutdown()
            raise

    def _setup_global_subscriptions(self):
        """Setup system-wide event handlers."""
        bus.subscribe("system.shutdown", lambda _: self.shutdown())
        bus.subscribe("ui.user_activity", lambda _: self.heartbeat.update_activity())
        
        # Route machine pulses to dispatcher
        bus.subscribe("system.pulse", lambda data: self.dispatcher.dispatch({"action": data["action"]}))
        
        # Example: Real-time reaction to critical state changes
        bus.subscribe("anger.escalated", lambda data: log_warning(f"AI Anger level increased: {data.get('level')}", "KERNEL"))

    def shutdown(self):
        """Graceful shutdown of all systems."""
        log_info("Initiating System Shutdown...", "CLEANUP")
        
        try:
            # Call the old cleanup logic via Kernel
            WindowOps.restore_all_windows()
            IconOps.restore_icon_positions()
            BrightnessOps.restore_brightness()
            WallpaperOps.restore_wallpaper()
            
            if self.state_manager:
                self.state_manager.clear_all()
            
            if self.memory:
                self.memory.shutdown()
                
            if self.heartbeat:
                self.heartbeat.stop()
            
            if self.presence_sensor:
                self.presence_sensor.stop()
            
            if self.window_sensor:
                self.window_sensor.stop()
                
            print("[CLEANUP] System restored successfully")
        except Exception as e:
            print(f"[CLEANUP] Error during shutdown: {e}")
        
        if self.app:
            self.app.quit()

# Convenience function for main.py
def boot_system():
    kernel = SentientKernel()
    kernel.boot()
