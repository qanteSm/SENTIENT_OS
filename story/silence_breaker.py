"""
Silence Breaker - Emergency tension maintainer.

Triggers mini-events after prolonged silence to prevent user
from feeling like game has frozen or stopped working.
"""

import time
import random
from PyQt6.QtCore import QObject, QTimer


class SilenceBreaker(QObject):
    """
    Monitors time since last significant event.
    Triggers subtle horror effects if silence exceeds threshold.
    """
    
    SILENCE_THRESHOLD = 45  # seconds
    CHECK_INTERVAL = 5  # Check every 5 seconds
    
    # Mini events to break silence (subtle, not jarring)
    MINI_EVENTS = [
        ("OVERLAY_TEXT", {"text": "..."}),
        ("OVERLAY_TEXT", {"text": "Orada olduğunu biliyorum..."}),
        ("AUDIO_GLITCH", {}),
        ("MOUSE_SHAKE", {"duration": 0.3}),
        ("FLASH_COLOR", {"color": "#000000", "opacity": 0.08, "duration": 150}),
        ("GDI_STATIC", {"duration": 200, "density": 0.005}),
    ]
    
    def __init__(self, dispatcher):
        super().__init__()
        self.dispatcher = dispatcher
        self.last_event_time = time.time()
        self._running = False
        
        # Timer to check silence
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self._check_silence)
    
    def start(self):
        """Start monitoring for silence"""
        self._running = True
        self.last_event_time = time.time()
        self.check_timer.start(self.CHECK_INTERVAL * 1000)
        print(f"[SILENCE_BREAKER] Started (threshold: {self.SILENCE_THRESHOLD}s)")
    
    def stop(self):
        """Stop monitoring"""
        self._running = False
        self.check_timer.stop()
        print("[SILENCE_BREAKER] Stopped")
    
    def reset(self):
        """Reset silence timer (call after any significant event)"""
        self.last_event_time = time.time()
    
    def _check_silence(self):
        """Check if silence threshold exceeded"""
        if not self._running:
            return
        
        elapsed = time.time() - self.last_event_time
        
        if elapsed > self.SILENCE_THRESHOLD:
            print(f"[SILENCE_BREAKER] Silence detected ({elapsed:.0f}s), breaking...")
            self._break_silence()
            self.reset()
    
    def _break_silence(self):
        """Trigger a subtle event to maintain tension"""
        action, params = random.choice(self.MINI_EVENTS)
        
        self.dispatcher.dispatch({
            "action": action,
            "params": params,
            "speech": ""
        })
        
        print(f"[SILENCE_BREAKER] Triggered: {action}")
