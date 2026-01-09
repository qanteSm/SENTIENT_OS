"""
Drone Audio Layer - Atmospheric background sounds.

Provides continuous low-frequency ambient sounds that create
subconscious tension and unease.

FEATURES:
- Multiple drone types (infrasound, static, whispers, etc.)
- Volume modulation based on horror intensity
- Smooth crossfading between drones
- Act-aware audio progression
"""

import os
from pathlib import Path

try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False
    print("[DRONE_AUDIO] pygame not found. Install with: pip install pygame")


class DroneAudioLayer:
    """
    Continuous atmospheric drone audio system.
    
    Creates subliminal unease through low-frequency sounds.
    """
    
    # Drone sound files (to be created/added)
    DRONES = {
        "silence": None,  # No drone
        "fan": "fan_rumble.wav",
        "static": "tv_static.wav",
        "whisper": "distant_whispers.wav",
        "infrasound": "infrasound_20hz.wav",
        "heartbeat": "slow_heartbeat.wav",
        "machinery": "industrial_hum.wav",
    }
    
    def __init__(self, assets_dir="assets/audio/drones"):
        if not HAS_PYGAME:
            self.enabled = False
            return
        
        self.enabled = True
        self.assets_dir = Path(assets_dir)
        self.current_drone = None
        self.current_sound = None
        self.volume = 0.3
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init(frequency=22050, channels=2, buffer=512)
            print("[DRONE_AUDIO] Initialized")
        except Exception as e:
            print(f"[DRONE_AUDIO] Init failed: {e}")
            self.enabled = False
    
    def start_drone(self, drone_type="fan"):
        """
        Start playing a drone sound.
        
        Args:
            drone_type: Type of drone (silence, fan, static, whisper, etc.)
        """
        if not self.enabled:
            return
        
        # Check config
        from config import Config
        if not Config().get("audio.enable_drone", True):
            print("[DRONE_AUDIO] Disabled in config")
            return
        
        # Stop current if playing
        if self.current_sound:
            self.stop()
        
        if drone_type == "silence":
            return
        
        # Get file path
        filename = self.DRONES.get(drone_type)
        if not filename:
            print(f"[DRONE_AUDIO] Unknown drone type: {drone_type}")
            return
        
        filepath = self.assets_dir / filename
        
        # Check if file exists
        if not filepath.exists():
            print(f"[DRONE_AUDIO] File not found: {filepath}")
            print("[DRONE_AUDIO] Skipping (file will be created later)")
            return
        
        try:
            # Load and play
            self.current_sound = pygame.mixer.Sound(str(filepath))
            self.current_sound.set_volume(self.volume)
            self.current_sound.play(loops=-1)  # Infinite loop
            self.current_drone = drone_type
            
            print(f"[DRONE_AUDIO] Started: {drone_type} (volume: {self.volume})")
            
        except Exception as e:
            print(f"[DRONE_AUDIO] Error loading {drone_type}: {e}")
    
    def stop(self):
        """Stop current drone"""
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound = None
            self.current_drone = None
            print("[DRONE_AUDIO] Stopped")
    
    def set_volume(self, volume: float):
        """
        Set drone volume (0.0 to 1.0).
        
        Args:
            volume: Volume level
        """
        self.volume = max(0.0, min(1.0, volume))
        
        if self.current_sound:
            self.current_sound.set_volume(self.volume)
        
        print(f"[DRONE_AUDIO] Volume: {self.volume}")
    
    def modulate_volume(self, intensity: int):
        """
        Adjust volume based on horror intensity (1-10).
        
        Args:
            intensity: Horror intensity level
        """
        # Base volume: 0.2 at intensity 1, 0.5 at intensity 10
        volume = 0.2 + (intensity / 10) * 0.3
        self.set_volume(volume)
    
    def fade_to(self, drone_type: str, duration=3000):
        """
        Crossfade to a different drone.
        
        Args:
            drone_type: Target drone type
            duration: Fade duration in milliseconds
        """
        if not self.enabled:
            return
        
        # TODO: Implement smooth crossfade
        # For now, just switch
        print(f"[DRONE_AUDIO] Fading to: {drone_type}")
        self.stop()
        
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, lambda: self.start_drone(drone_type))
    
    def set_act_drone(self, act_num: int):
        """
        Set appropriate drone for Act.
        
        Args:
            act_num: Act number (1-4)
        """
        drone_map = {
            1: "fan",        # Act 1: Subtle mechanical hum
            2: "static",     # Act 2: TV static
            3: "whisper",    # Act 3: Creepy whispers
            4: "infrasound"  # Act 4: Deep infrasound
        }
        
        drone = drone_map.get(act_num, "fan")
        intensity_map = {1: 3, 2: 5, 3: 7, 4: 9}
        
        self.fade_to(drone)
        self.modulate_volume(intensity_map.get(act_num, 5))


# Singleton instance
_drone_instance = None

def get_drone_audio() -> DroneAudioLayer:
    """Get singleton DroneAudioLayer instance"""
    global _drone_instance
    if _drone_instance is None:
        _drone_instance = DroneAudioLayer()
    return _drone_instance
