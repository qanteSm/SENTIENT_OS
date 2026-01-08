from typing import Dict, Any, Callable, List
import threading

class EventBus:
    """
    The Nervous System of Sentient OS.
    Pure Python implementation to avoid QApplication initialization issues.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(EventBus, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._subscribers: Dict[str, List[Callable]] = {}
            self._initialized = True
            print("[EVENT_BUS] Nervous System Online (Pure Python).")

    def publish(self, event_name: str, data: Dict[str, Any] = None):
        """Broadcast an event to all subscribers."""
        data = data or {}
        # print(f"[EVENT_BUS] Publishing: {event_name}")
        
        # Defensive copy of subscribers to avoid issues if a callback subscribes/unsubscribes
        with self._lock:
            callbacks = self._subscribers.get(event_name, []).copy()
            wildcards = self._subscribers.get("*", []).copy()

        for callback in callbacks:
            try:
                callback(data)
            except Exception as e:
                print(f"[EVENT_BUS] Error in callback for {event_name}: {e}")
                
        for callback in wildcards:
            try:
                callback({"event": event_name, "data": data})
            except Exception as e:
                print(f"[EVENT_BUS] Error in wildcard callback: {e}")

    def subscribe(self, event_name: str, callback: Callable[[Dict[str, Any]], None]):
        """Subscribe to a specific event."""
        with self._lock:
            if event_name not in self._subscribers:
                self._subscribers[event_name] = []
            if callback not in self._subscribers[event_name]:
                self._subscribers[event_name].append(callback)

# Global singleton instance
bus = EventBus()
