import time
import threading
from core.event_bus import bus
from config import Config

try:
    if Config.IS_MOCK:
        raise ImportError("Mock Mode")
    import win32api
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

class PanicSensor(threading.Thread):
    """
    Hardware-level 'Hot Corner' panic detection.
    If the mouse stays at (0,0) for 3 consecutive seconds, triggers emergency shutdown.
    This works even if keyboard drivers fail or input is locked.
    """
    def __init__(self):
        super().__init__(daemon=True)
        self.is_running = False
        self.corner_timer = 0
        self.trigger_threshold = 3.0 # 3 seconds

    def run(self):
        if not HAS_WIN32:
            print("[PANIC_SENSOR] Not active (MOCK or non-Windows)")
            return

        self.is_running = True
        print("[PANIC_SENSOR] Monitoring Hot Corner (0,0) for safety.")
        
        while self.is_running:
            x, y = win32api.GetCursorPos()
            
            # Check if mouse is in the exact top-left corner
            if x <= 1 and y <= 1:
                if self.corner_timer == 0:
                    self.corner_timer = time.time()
                
                elapsed = time.time() - self.corner_timer
                if elapsed >= self.trigger_threshold:
                    print("\n🚨 [PANIC_SENSOR] HOT CORNER TRIGGERED! Shutting down...")
                    bus.publish("system.shutdown", {"reason": "panic_corner"})
                    
                    # Force kill via safety net if kernel doesn't react fast enough
                    from core.safety_net import SafetyNet
                    sn = SafetyNet()
                    sn.emergency_cleanup()
                    break
            else:
                self.corner_timer = 0 # Reset if mouse moves away
            
            time.sleep(0.1) # Fast sampling

    def stop(self):
        self.is_running = False
