# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Dynamic Difficulty System - Scales horror experience based on player behavior.

Monitors:
- Typing speed in chat
- Reaction time to scary events
- Frequency of swearing/aggression
- System activity

Adjusts:
- Ambient horror intensity
- AI persona 'aggression' level
- Event frequency
"""

import time
from PyQt6.QtCore import QObject, QTimer
from core.logger import log_info, log_debug
from core.memory import Memory

class DynamicDifficulty(QObject):
    def __init__(self, memory: Memory, story_manager):
        super().__init__()
        self.memory = memory
        self.story_manager = story_manager
        
        # Difficulty state
        self.fear_score = 50  # 0-100 scale
        self.skill_score = 50 # 0-100 scale (high = fast typer/stable)
        
        # Tracking metrics
        self.last_action_time = time.time()
        self.reaction_times = []
        self.typing_speeds = []
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._recalculate_difficulty)
        self.update_timer.start(30000) # Every 30 seconds
        
    def report_reaction_time(self, ms: int):
        """Called when user dismisses a scare or interacts with the system."""
        self.reaction_times.append(ms)
        if len(self.reaction_times) > 10:
            self.reaction_times.pop(0)
        
        # Lower reaction time = higher skill
        log_debug(f"Reaction time reported: {ms}ms", "DIFF")
        
    def report_typing(self, char_count: int, time_spent: float):
        """Called after user sends a chat message."""
        wpm = (char_count / 5) / (time_spent / 60) if time_spent > 0 else 0
        self.typing_speeds.append(wpm)
        if len(self.typing_speeds) > 10:
            self.typing_speeds.pop(0)
            
        log_debug(f"Typing speed reported: {wpm:.1f} WPM", "DIFF")

    def _recalculate_difficulty(self):
        """Analyze metrics and update system intensity."""
        # 1. Calculate Skill
        if self.typing_speeds:
            avg_wpm = sum(self.typing_speeds) / len(self.typing_speeds)
            # 80+ WPM is high skill
            self.skill_score = min(100, (avg_wpm / 80) * 100)
            
        # 2. Calculate Fear (Inverse of skill + based on behavior)
        behavior = self.memory.data.get("user_profile", {}).get("behavior_stats", {})
        swear_intensity = behavior.get("swear_count", 0) * 10
        
        # High skill often means lower fear (not always, but a good proxy for 'mastery')
        # High swearing means low fear (defiance)
        defiance_score = (self.skill_score * 0.5) + (swear_intensity * 0.5)
        self.fear_score = max(0, 100 - defiance_score)
        
        log_info(f"Difficulty Adjusted - Fear: {self.fear_score:.1f}, Skill: {self.skill_score:.1f}", "DIFF")
        
        # 3. Apply changes to Ambient Horror via StoryManager
        if self.story_manager and self.story_manager.ambient_horror:
            # We want to maintain tension.
            # If fear is low (high defiance), increase intensity to provoke.
            # If fear is very high, maybe tone it down slightly to avoid 'numbing'.
            
            target_intensity = 5 # Default
            if self.fear_score < 30: # Bored or defiant
                target_intensity = 8
            elif self.fear_score < 60:
                target_intensity = 6
            elif self.fear_score > 90: # Panic
                target_intensity = 4 # Mercy
                
            self.story_manager.ambient_horror.set_intensity(target_intensity)
            
        # 4. Update Memory
        self.memory.update_user_profile("fear_level", self.fear_score)

    def stop(self):
        self.update_timer.stop()
        log_info("Dynamic Difficulty system stopped.", "DIFF")
