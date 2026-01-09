from typing import Dict, Any
from core.sensors.base_sensor import BaseSensor
from core.event_bus import bus

class PresenceSensor(BaseSensor):
    """
    Monitors user input activity to detect engagement levels.
    
    IMPROVED:
    - Inherits from BaseSensor for thread safety
    - Uses QMutex for safe event publishing
    - Automatic error handling
    """
    def __init__(self):
        super().__init__(poll_interval=1.0)  # Check every second
        self.last_mouse_pos = None
        self._pyautogui = None
    
    def collect_data(self) -> Dict[str, Any]:
        """Collect mouse position data"""
        # Lazy import pyautogui
        if self._pyautogui is None:
            try:
                import pyautogui
                self._pyautogui = pyautogui
            except ImportError:
                print("[SENSOR] pyautogui not found, PresenceSensor disabled")
                return {}
        
        try:
            current_pos = self._pyautogui.position()
            
            if current_pos != self.last_mouse_pos:
                # User moved the mouse
                self.last_mouse_pos = current_pos
                
                # Publish to event bus (already thread-safe via safe_publish)
                data = {"type": "mouse_move", "pos": current_pos}
                bus.publish("ui.user_activity", data)
                
                return data
            
            return {}  # No change
            
        except Exception as e:
            self._handle_error(f"Error getting mouse position: {e}")
            return {}
