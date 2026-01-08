import time
from PyQt6.QtCore import QThread
from core.event_bus import bus
from config import Config

try:
    if Config.IS_MOCK:
        raise ImportError("Mock Mode")
    import win32gui
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

class WindowSensor(QThread):
    """
    Monitors active window changes and alerts the system.
    """
    def __init__(self):
        super().__init__()
        self.is_running = True
        self.last_window_title = None

    def run(self):
        print("[SENSOR] Window Sensor Active.")
        if not HAS_WIN32:
            print("[SENSOR] Win32 not available, WindowSensor disabled.")
            return

        while self.is_running:
            try:
                window = win32gui.GetForegroundWindow()
                title = win32gui.GetWindowText(window)
                
                if title != self.last_window_title:
                    bus.publish("ui.window_changed", {"new_title": title, "old_title": self.last_window_title})
                    self.last_window_title = title
                    
                time.sleep(2.0) # Check every 2 seconds
            except Exception:
                time.sleep(5.0)

    def stop(self):
        self.is_running = False
        self.wait()
