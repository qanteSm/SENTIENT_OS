# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Silence Breaker - Emergency tension maintainer.

Triggers mini-events after prolonged silence to prevent user
from feeling like game has frozen or stopped working.
"""

import time
import random
from PyQt6.QtCore import QObject, QTimer
from core.logger import log_info, log_error, log_debug


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
        ("CAPSLOCK_TOGGLE", {}),
        ("FAKE_NOTIFICATION", {"title": "Sistem", "message": "Gereksiz dosyalar temizleniyor..."}),
        ("SCREEN_INVERT", {"duration": 100}),
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
        log_info(f"Started (threshold: {self.SILENCE_THRESHOLD}s)", "SILENCE_BREAKER")
    
    def stop(self):
        """Stop monitoring"""
        self._running = False
        self.check_timer.stop()
        log_info("Stopped", "SILENCE_BREAKER")
    
    def reset(self):
        """Reset silence timer (call after any significant event)"""
        self.last_event_time = time.time()
    
    def _check_silence(self):
        """Check if silence threshold exceeded"""
        if not self._running:
            return
        
        elapsed = time.time() - self.last_event_time
        
        if elapsed > self.SILENCE_THRESHOLD:
            log_info(f"Silence detected ({elapsed:.0f}s), breaking...", "SILENCE_BREAKER")
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
        
        log_debug(f"Triggered: {action}", "SILENCE_BREAKER")
