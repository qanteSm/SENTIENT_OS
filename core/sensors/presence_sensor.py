import time
from PyQt6.QtCore import QThread, pyqtSignal
from core.event_bus import bus

class PresenceSensor(QThread):
    """
    Monitors user input activity to detect engagement levels.
    """
    def __init__(self):
        super().__init__()
        self.is_running = True
        self.last_mouse_pos = None

    def run(self):
        print("[SENSOR] Presence Sensor Active.")
        try:
            import pyautogui
        except ImportError:
            print("[SENSOR] pyautogui not found, PresenceSensor will be limited.")
            return

        while self.is_running:
            try:
                current_pos = pyautogui.position()
                if current_pos != self.last_mouse_pos:
                    # User moved the mouse
                    bus.publish("ui.user_activity", {"type": "mouse_move", "pos": current_pos})
                    self.last_mouse_pos = current_pos
                    
                time.sleep(1.0) # Check every second
            except Exception:
                time.sleep(5.0)

    def stop(self):
        self.is_running = False
        self.wait()
