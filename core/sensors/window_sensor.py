from typing import Dict, Any
from core.sensors.base_sensor import BaseSensor
from core.event_bus import bus
from config import Config

class WindowSensor(BaseSensor):
    """
    Monitors which application is currently in focus.
    
    IMPROVED:
    - Inherits from BaseSensor for thread safety
    - Uses QMutex for safe event publishing
    - Automatic error handling
    """
    def __init__(self):
        super().__init__(poll_interval=2.0)  # Check every 2 seconds
        self.last_window = None
        self._win32gui = None
        self._init_win32()
    
    def _init_win32(self):
        """Lazy import win32gui"""
        if Config().IS_MOCK:
            return
        
        try:
            import win32gui
            self._win32gui = win32gui
        except ImportError:
            print("[SENSOR] win32gui not found, WindowSensor disabled")
    
    def collect_data(self) -> Dict[str, Any]:
        """Collect active window data"""
        if self._win32gui is None:
            return {}
        
        try:
            hwnd = self._win32gui.GetForegroundWindow()
            window_title = self._win32gui.GetWindowText(hwnd)
            
            if window_title != self.last_window:
                self.last_window = window_title
                
                # Publish to event bus
                data = {"window_title": window_title, "hwnd": hwnd}
                bus.publish("window.focus_changed", data)
                
                return data
            
            return {}  # No change
            
        except Exception as e:
            self._handle_error(f"Error getting window: {e}")
            return {}
