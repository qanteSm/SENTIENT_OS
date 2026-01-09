import os
import random
from config import Config

try:
    if Config().IS_MOCK:
        raise ImportError("Mock Mode")
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False

class AudioManager:
    """
    Manages centralized audio using Pygame.
    Handles background ambience, UI sound effects, and glitches.
    """
    def __init__(self):
        self.mock_mode = Config().IS_MOCK or not HAS_PYGAME
        
        if not self.mock_mode:
            try:
                pygame.mixer.init()
                pygame.mixer.set_num_channels(8) # Allow multiple overlapping sounds
                print("[AUDIO] Pygame Mixer Initialized.")
            except Exception as e:
                print(f"[AUDIO] Pygame Init Failed: {e}")
                self.mock_mode = True

        # Preload assets path (Placeholder paths for now)
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sounds")
        
        # We will create channels
        self.ambience_channel = None
        
    def play_sfx(self, sound_name: str):
        """
        Plays a short sound effect.
        Args:
            sound_name: 'type', 'glitch', 'error', 'startup'
        """
        if self.mock_mode:
            # print(f"[MOCK AUDIO] SFX: {sound_name}") 
            # Commented out to reduce console spam
            return

        # TODO: In a real scenario, we would load actual .wav files here.
        # For now, we will generate synthetic beeps if no file exists or just pass.
        # since we don't have assets yet, we can't actually play anything.
        # We will just print for now until assets are added.
        print(f"[AUDIO] Playing SFX: {sound_name}")
        
    def start_ambience(self):
        """Starts the low-frequency dread hum."""
        if self.mock_mode:
            print("[MOCK AUDIO] Starting Ambience Loop")
            return
            
        print("[AUDIO] Starting Ambience Loop (Placeholder)")
        # In real impl:
        # sound = pygame.mixer.Sound(os.path.join(self.assets_dir, "hum.wav"))
        # self.ambience_channel = sound.play(loops=-1)

    def stop_ambience(self):
        if self.mock_mode: return
        if self.ambience_channel:
            self.ambience_channel.stop()

    def play_typing_sound(self):
        """Plays a random click key sound."""
        self.play_sfx("type_key")
