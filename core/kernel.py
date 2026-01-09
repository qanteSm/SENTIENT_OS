import sys
import time
import os
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
from core.resource_guard import ResourceGuard
from core.sensors.panic_sensor import PanicSensor
from visual.ambient_horror import AmbientHorror
from visual.ui.onboarding_manager import OnboardingManager
from story.silence_breaker import SilenceBreaker
from hardware.drone_audio import get_drone_audio

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
            self.resilience = None
            
            # Sensors
            self.presence_sensor = None
            self.window_sensor = None
            
            # Safety Sensors
            self.resource_guard = None
            self.panic_sensor = None
            
            # Ambient Horror (Background effects)
            self.ambient_horror = None
            
            # Silence Breaker
            self.silence_breaker = None
            
            # Drone Audio
            self.drone_audio = None
            
            # Onboarding (replaces simple consent)
            self.onboarding_manager = None

    def boot(self):
        """Initializes the application and shows the mandatory consent screen."""
        print(f"\n[KERNEL] Booting {Config().get('APP_NAME', 'SENTIENT_OS')} v{Config().get('VERSION', '0.8.0')}...")
        
        # 1. Initialize Qt Application
        self.app = QApplication(self.app_argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 2. Critical Backup (Safety) - These don't change system state yet
        
        # Save initial state before any manipulation
        BrightnessOps.save_brightness()
        WallpaperOps.save_current_wallpaper()
        IconOps.save_icon_positions()
        
        # 3. Show Onboarding Flow (Welcome -> Calibration -> Consent)
        # No horror effects or        # Check if DEV_MODE - skip onboarding for faster testing
        dev_mode_file = os.path.join(os.path.dirname(__file__), "..", "DEV_MODE.txt")
        if os.path.exists(dev_mode_file):
            print("[DEV] Skipping onboarding - starting game directly...")
            self.init_core_systems()
        else:
            # Onboarding (replaces simple consent)
            from visual.ui.onboarding_manager import OnboardingManager
            self.onboarding_manager = OnboardingManager()
            self.onboarding_manager.onboarding_complete.connect(self.init_core_systems)
            self.onboarding_manager.start_onboarding()
        
        try:
            sys.exit(self.app.exec())
        except Exception as e:
            log_error(f"Kernel Panic: {e}", "KERNEL")
            self.shutdown()
            raise

    def init_core_systems(self):
        """Rest of the boot logic, triggered after consent is granted."""
        log_info("Consent granted. Completing system boot...", "KERNEL")
        
        # 1. Hardware Initialization (Safety Net)
        if BrightnessOps.check_and_restore_on_startup():
            log_info("Brightness recovered from previous crash", "BOOT")
        
        self.safety = SafetyNet()
        self.safety.start_monitoring()
        
        # 2. Resilience Engine (Ghost)
        self.resilience = ResilienceManager(self)
        if not Config().IS_MOCK:
            # Note: This is now session-locked, controlled by SafetyNet
            self.resilience.spawn_watchdog()
        
        # 3. Core Engine Initialization
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
        
        # 4. Sensors & Autonomy
        log_info("Initializing Sensors...", "KERNEL")
        self.presence_sensor = PresenceSensor()
        self.window_sensor = WindowSensor()
        
        self.heartbeat = Heartbeat(self.anger, self.brain, self.dispatcher)
        self.dispatcher.heartbeat = self.heartbeat
        
        # 4.1 Initialize Glitch Logic (Autonomous Visuals)
        self.glitch_logic = GlitchLogic(self.dispatcher)
        
        # 5. Check for crash recovery
        recovery_reason = self.state_manager.check_for_recovery(self.dispatcher)
        if recovery_reason:
            self.resilience.handle_recovery("crash")
        
        # 6. Start Autonomous Threads
        self.presence_sensor.start()
        self.window_sensor.start()
        self.heartbeat.start()
        
        # 6.1 Start Resource Guard & Panic Sensor (Safety)
        self.resource_guard = ResourceGuard()
        self.resource_guard.start()
        
        self.panic_sensor = PanicSensor()
        self.panic_sensor.start()
        
        # 7. Story Engine
        log_info("Initializing Story Engine...", "KERNEL")
        self.story_manager = StoryManager(self.dispatcher, self.memory, self.brain)
        
        # 7.1 Initialize Ambient Horror
        self.ambient_horror = AmbientHorror(self.dispatcher)
        # Connect to story manager for intensity control
        if hasattr(self.story_manager, 'set_ambient_horror'):
            self.story_manager.set_ambient_horror(self.ambient_horror)
        
        # 7.2 Initialize Silence Breaker
        self.silence_breaker = SilenceBreaker(self.dispatcher)
        self.silence_breaker.start()
        
        # 7.3 Initialize Drone Audio
        self.drone_audio = get_drone_audio()
        # Story manager will control drone per Act
        if hasattr(self.story_manager, 'set_drone_audio'):
            self.story_manager.set_drone_audio(self.drone_audio)
        
        QTimer.singleShot(1000, self.story_manager.start_story)
        
        # 8. Event Bus Subscriptions
        self._setup_global_subscriptions()
        
        # Connect heartbeat signals to Event Bus
        self.heartbeat.pulse_signal.connect(lambda action: bus.publish("system.pulse", {"action": action}))
        
        log_info("SENTIENT_OS Kernel Active and Observant.", "KERNEL")
        bus.publish("system.boot_complete")

    def _setup_global_subscriptions(self):
        """Setup system-wide event handlers."""
        bus.subscribe("system.shutdown", lambda _: self.shutdown())
        bus.subscribe("ui.user_activity", lambda _: self.heartbeat.update_activity())
        
        # Route machine pulses to dispatcher
        bus.subscribe("system.pulse", lambda data: self.dispatcher.dispatch({"action": data["action"]}))
        
        # Example: Real-time reaction to critical state changes
        bus.subscribe("anger.escalated", lambda data: log_warning(f"AI Anger level increased: {data.get('level')}", "KERNEL"))

    def shutdown(self):
        """Graceful and robust shutdown of all systems."""
        log_info("Initiating System Shutdown...", "CLEANUP")
        
        # Disable future signals to avoid recursion if something fails during cleanup
        try:
            bus.unsubscribe("system.shutdown")
        except: pass

        try:
            # 0. Cleanup Resilience Session (Signals guard to stop)
            if self.resilience:
                self.resilience.cleanup_session()
                
            # 1. STOP ALL AUTONOMY (Threads first)
            if self.silence_breaker:
                self.silence_breaker.stop()
            
            if self.ambient_horror:
                self.ambient_horror.stop()
            
            if self.drone_audio:
                self.drone_audio.stop()
            
            if self.resource_guard:
                self.resource_guard.stop()
                
            if self.panic_sensor:
                self.panic_sensor.stop()
            
            if self.heartbeat:
                self.heartbeat.stop()
            
            if self.presence_sensor:
                self.presence_sensor.stop()
            
            if self.window_sensor:
                self.window_sensor.stop()

            # 2. HARDWARE RESTORE (Critical)
            log_info("Restoring system hardware state...", "CLEANUP")
            WindowOps.restore_all_windows()
            IconOps.restore_icon_positions()
            BrightnessOps.restore_brightness()
            WallpaperOps.restore_wallpaper()
            
            # 3. Component Cleanup
            if self.state_manager:
                self.state_manager.clear_all()
            
            if self.memory:
                self.memory.shutdown()
                
            print("[CLEANUP] All subsystems stabilized.")
        except Exception as e:
            log_error(f"Error during shutdown: {e}", "CLEANUP")
        
        if self.app:
            self.app.quit()

# Global exception hook to ensure cleanup on crash
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    log_error(f"UNHANDLED EXCEPTION: {exc_value}", "CRITICAL")
    kernel = SentientKernel()
    if kernel:
        kernel.shutdown()
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = handle_exception

# Convenience function for main.py
def boot_system():
    kernel = SentientKernel()
    kernel.boot()
