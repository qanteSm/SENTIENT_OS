"""
Ambient Horror - Background horror effects to maintain tension.

This system provides subtle, randomized horror effects that run in the
background to prevent long periods of inactivity that could break immersion.

FEATURES:
- Adjustable intensity (1-10)
- Random timing (8-15 seconds between effects)
- Context-aware effect selection
- Integrates seamlessly with FunctionDispatcher
"""

from PyQt6.QtCore import QObject, QTimer
import random
from config import Config


class AmbientHorror(QObject):
    """
    Provides subtle ambient horror effects during quiet moments.
    
    The intensity increases automatically as the game progresses (via Acts),
    ensuring the user never feels completely safe.
    """
    
    def __init__(self, dispatcher):
        super().__init__()
        self.dispatcher = dispatcher
        self.intensity = 1  # 1-10 scale
        self._running = False
        
        # Timer for randomized effects
        self.timer = QTimer()
        self.timer.timeout.connect(self._trigger_ambient)
        
        # Effect pools by intensity level
        self.effects = {
            # Level 1-3: Very subtle
            "low": [
                ("FLASH_COLOR", {"color": "#FF0000", "opacity": 0.03, "duration": 100}),
                ("GDI_STATIC", {"duration": 150, "density": 0.003}),
                ("CAPSLOCK_TOGGLE", {}),
            ],
            # Level 4-7: Noticeable but not jarring
            "medium": [
                ("FLASH_COLOR", {"color": "#FF0000", "opacity": 0.08, "duration": 200}),
                ("GDI_STATIC", {"duration": 300, "density": 0.008}),
                ("AUDIO_GLITCH", {}),
                ("MOUSE_SHAKE", {"duration": 0.2}),
                ("GDI_FLASH", {}),
                ("SCREEN_INVERT", {"duration": 50}),
            ],
            # Level 8-10: Intense
            "high": [
                ("FLASH_COLOR", {"color": "#000000", "opacity": 0.15, "duration": 300}),
                ("GDI_STATIC", {"duration": 500, "density": 0.015}),
                ("AUDIO_GLITCH", {}),
                ("MOUSE_SHAKE", {"duration": 0.5}),
                ("OVERLAY_TEXT", {"text": "BURADAYIM", "duration": 800}),
                ("OVERLAY_TEXT", {"text": "KAÇIŞ YOK", "duration": 800}),
                ("GDI_LINE", {"color": 0x0000FF, "thickness": 1}),
                ("GDI_FLASH", {}),
                ("SCREEN_INVERT", {"duration": 100}),
                ("DIGITAL_GLITCH_SURGE", {}),
            ],
        }
    
    def start(self):
        """Start ambient horror effects"""
        if self._running:
            return
        
        self._running = True
        self._schedule_next()
        print(f"[AMBIENT] Ambient Horror started (intensity: {self.intensity})")
    
    def stop(self):
        """Stop ambient horror effects"""
        self._running = False
        self.timer.stop()
        print("[AMBIENT] Ambient Horror stopped")
    
    def set_intensity(self, level: int):
        """
        Set intensity level (1-10).
        
        Args:
            level: 1 (barely noticeable) to 10 (constant dread)
        """
        self.intensity = max(1, min(10, level))
        print(f"[AMBIENT] Intensity set to {self.intensity}")
    
    def _schedule_next(self):
        """Schedule the next ambient effect"""
        if not self._running:
            return
        
        # Random interval between 8-15 seconds
        # Lower intensity = longer intervals
        base_min = 8000 + (10 - self.intensity) * 500
        base_max = 15000 + (10 - self.intensity) * 1000
        
        interval = random.randint(base_min, base_max)
        self.timer.start(interval)
    
    def _trigger_ambient(self):
        """Trigger a random ambient effect"""
        if not self._running:
            return
        
        # Select effect pool based on intensity
        if self.intensity <= 3:
            pool = self.effects["low"]
        elif self.intensity <= 7:
            pool = self.effects["medium"]
        else:
            pool = self.effects["high"]
        
        # Randomly skip some effects (20% chance) to maintain unpredictability
        if random.random() < 0.2:
            self._schedule_next()
            return
        
        # Select and dispatch random effect
        action, params = random.choice(pool)
        
        print(f"[AMBIENT] Triggering: {action}")
        self.dispatcher.dispatch({
            "action": action,
            "params": params,
            "speech": ""
        })
        
        # Schedule next
        self._schedule_next()
    
    def is_running(self) -> bool:
        """Check if ambient horror is active"""
        return self._running
