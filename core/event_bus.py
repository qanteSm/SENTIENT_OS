"""
Event Bus System for SENTIENT_OS
Global event distribution system for component communication.
"""
from typing import Dict, Any, Callable, List
import threading

class EventBus:
    """
    The Nervous System of Sentient OS.
    
    Provides a centralized publish-subscribe event system for decoupled component communication.
    Pure Python implementation to avoid QApplication initialization issues.
    
    Features:
        - Thread-safe event publishing and subscription
        - Wildcard subscriptions with "*" event name
        - Singleton pattern for global event bus
        
    Example:
        >>> from core.event_bus import bus
        >>> def handler(data):
        ...     print(f"Received: {data}")
        >>> bus.subscribe("user.action", handler)
        >>> bus.publish("user.action", {"type": "click"})
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
        """
        Broadcast an event to all subscribers.
        
        Args:
            event_name: Name of the event to publish
            data: Optional event data dictionary
            
        Example:
            >>> bus.publish("system.boot_complete", {"timestamp": time.time()})
        """
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
        """
        Subscribe to a specific event.
        
        Args:
            event_name: Name of event to subscribe to (use "*" for all events)
            callback: Function to call when event is published
            
        Example:
            >>> def on_boot(data):
            ...     print("System booted!")
            >>> bus.subscribe("system.boot_complete", on_boot)
        """
        with self._lock:
            if event_name not in self._subscribers:
                self._subscribers[event_name] = []
            if callback not in self._subscribers[event_name]:
                self._subscribers[event_name].append(callback)
    
    def unsubscribe(self, event_name: str, callback: Callable[[Dict[str, Any]], None] = None):
        """
        Unsubscribe from an event.
        
        Args:
            event_name: Name of event to unsubscribe from
            callback: Specific callback to remove (if None, removes all for event)
        """
        with self._lock:
            if event_name in self._subscribers:
                if callback is None:
                    del self._subscribers[event_name]
                elif callback in self._subscribers[event_name]:
                    self._subscribers[event_name].remove(callback)

# Global singleton instance
bus = EventBus()
