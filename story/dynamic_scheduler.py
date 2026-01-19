# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Dynamic Event Scheduler - Adaptive event timing based on user activity.

Replaces fixed timers with intelligent scheduling that responds to
user idle time and engagement level.
"""

import time
import random
from typing import List, Tuple, Callable
from PyQt6.QtCore import QObject, QTimer


class DynamicEventScheduler(QObject):
    """
    Context-aware event scheduler.
    
    Compresses event delays when user is idle to maintain engagement.
    """
    
    def __init__(self):
        super().__init__()
        self.events = []  # [(min_delay, max_delay, callback)]
        self.user_idle_time = 0  # Seconds since last activity
        self.last_event_time = time.time()
        self._scheduled_timers = []
        
        # Idle tracking timer
        self._idle_timer = QTimer()
        self._idle_timer.timeout.connect(self._update_idle_time)
        self._idle_timer.start(1000)  # Check every second
    
    def add_events(self, events: List[Tuple[int, int, Callable]]):
        """
        Add events to schedule.
        
        Args:
            events: List of (min_delay_ms, max_delay_ms, callback)
        """
        self.events = events
        print(f"[SCHEDULER] Added {len(events)} events")
    
    def start(self):
        """Start scheduling events"""
        print("[SCHEDULER] Starting dynamic event scheduling")
        self._schedule_all()
    
    def stop(self):
        """Stop all scheduled events"""
        for timer in self._scheduled_timers:
            timer.stop()
            timer.deleteLater()
        self._scheduled_timers.clear()
        self._idle_timer.stop()
        print("[SCHEDULER] Stopped")
    
    def on_user_activity(self):
        """Call this when user shows activity (mouse, keyboard, etc.)"""
        self.user_idle_time = 0
    
    def _update_idle_time(self):
        """Increment idle time counter"""
        self.user_idle_time += 1
    
    def _schedule_all(self):
        """Schedule all events with adaptive delays"""
        cumulative_delay = 0
        
        for min_delay, max_delay, callback in self.events:
            # Calculate adaptive delay
            actual_delay = self._calculate_adaptive_delay(min_delay, max_delay)
            cumulative_delay += actual_delay
            
            # Create timer
            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(callback)
            timer.start(cumulative_delay)
            
            self._scheduled_timers.append(timer)
    
    def _calculate_adaptive_delay(self, min_delay: int, max_delay: int) -> int:
        """
        Calculate delay based on user idle time.
        
        Idle factor:
        - 0s idle: Use full range (slow)
        - 30s idle: Use minimum delays (fast)
        """
        # Idle factor from 0.0 (active) to 1.0 (idle 30s+)
        idle_factor = min(self.user_idle_time / 30.0, 1.0)
        
        # Compress delay range as idle time increases
        # At 0% idle: Random between min and max
        # At 100% idle: Always use min (fastest)
        compression = 1.0 - (idle_factor * 0.6)  # 60% compression max
        
        delay_range = max_delay - min_delay
        compressed_range = delay_range * compression
        
        actual_delay = min_delay + random.uniform(0, compressed_range)
        
        return int(actual_delay)
