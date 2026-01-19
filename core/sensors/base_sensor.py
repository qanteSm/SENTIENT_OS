# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Base Sensor - Thread-safe sensor base class with QMutex.

All sensors should inherit from this class to ensure thread safety
when communicating with the Qt main thread.

FEATURES:
- QMutex for thread-safe operations
- Standard start/stop interface
- Signal-based communication with main thread
- Automatic error handling
"""

from PyQt6.QtCore import QObject, pyqtSignal, QMutex, QTimer
from abc import ABC, abstractmethod
from typing import Dict, Any
import threading
import time

# Combined metaclass to resolve QObject + ABC conflict
class QABCMeta(type(QObject), type(ABC)):
    """Combined metaclass for QObject and ABC"""
    pass

class BaseSensor(QObject, ABC, metaclass=QABCMeta):
    """
    Thread-safe base class for all sensors.
    
    Sensors run in background threads and need to communicate
    safely with the Qt main thread via signals.
    """
    
    # Signal emitted when sensor detects something
    sensor_data = pyqtSignal(dict)
    
    # Signal emitted on errors
    sensor_error = pyqtSignal(str)
    
    def __init__(self, poll_interval: float = 1.0):
        """
        Args:
            poll_interval: How often to check sensor (in seconds)
        """
        super().__init__()
        self._mutex = QMutex()
        self._running = False
        self._thread = None
        self._poll_interval = poll_interval
        self._last_data = {}
    
    @abstractmethod
    def collect_data(self) -> Dict[str, Any]:
        """
        Override this to collect sensor-specific data.
        This will be called from the background thread.
        
        Returns:
            dict: Sensor data to emit
        """
        pass
    
    def start(self):
        """Start the sensor in a background thread"""
        if self._running:
            print(f"[{self.__class__.__name__}] Already running")
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        print(f"[{self.__class__.__name__}] Started")
    
    def stop(self):
        """Stop the sensor"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        print(f"[{self.__class__.__name__}] Stopped")
    
    def _run_loop(self):
        """Main sensor loop - runs in background thread"""
        while self._running:
            try:
                data = self.collect_data()
                
                # Only emit if data changed (avoid spam)
                if data != self._last_data:
                    self.safe_publish(data)
                    self._last_data = data
                
            except Exception as e:
                self._handle_error(f"Error collecting data: {e}")
            
            time.sleep(self._poll_interval)
    
    def safe_publish(self, data: Dict[str, Any]):
        """
        Thread-safe data publication to Qt main thread.
        
        Args:
            data: Dictionary to emit
        """
        self._mutex.lock()
        try:
            self.sensor_data.emit(data)
        finally:
            self._mutex.unlock()
    
    def _handle_error(self, error_msg: str):
        """Handle sensor errors gracefully"""
        print(f"[{self.__class__.__name__}] ERROR: {error_msg}")
        self._mutex.lock()
        try:
            self.sensor_error.emit(error_msg)
        finally:
            self._mutex.unlock()
    
    def is_running(self) -> bool:
        """Check if sensor is running"""
        return self._running
    
    def set_poll_interval(self, interval: float):
        """Change polling interval at runtime"""
        self._poll_interval = max(0.1, interval)  # Minimum 100ms
        print(f"[{self.__class__.__name__}] Poll interval set to {interval}s")
