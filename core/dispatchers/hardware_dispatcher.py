# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Hardware Dispatcher - Handles hardware control (mouse, keyboard, audio, camera)

Supported actions:
- MOUSE_SHAKE, GHOST_TYPE, KEYBOARD_BLOCK
- TTS_SPEAK, PLAY_SFX, AUDIO_GLITCH
- CAMERA_FLASH, BRIGHTNESS_FLICKER, BRIGHTNESS_DIM
"""
from typing import List, Dict, Any
from core.dispatchers.base_dispatcher import BaseDispatcher
from core.logger import log_info


class HardwareDispatcher(BaseDispatcher):
    """
    Handles all hardware control operations.
    
    Dependencies: MouseOps, KeyboardOps, AudioOut, CameraOps, BrightnessOps
    Actions: ~12 hardware operations
    """
    
    def __init__(self, process_guard=None):
        from hardware.mouse_ops import MouseOps
        from hardware.keyboard_ops import KeyboardOps
        from hardware.audio_out import AudioOut
        from hardware.camera_ops import CameraOps
        from hardware.brightness_ops import BrightnessOps
        
        self.mouse = MouseOps
        self.keyboard = KeyboardOps
        self.audio = AudioOut()
        self.camera = CameraOps()
        self.brightness = BrightnessOps
        self.process_guard = process_guard
    
    def get_supported_actions(self) -> List[str]:
        """Hardware control actions"""
        return [
            "MOUSE_SHAKE",
            "LOCK_INPUT",
            "UNLOCK_INPUT",
            "GHOST_TYPE",
            "PLAY_SFX",
            "AUDIO_GLITCH",
            "CAMERA_FLASH",
            "BRIGHTNESS_FLICKER",
            "BRIGHTNESS_DIM",
            "CAPSLOCK_TOGGLE",
            "PLAY_SOUND",
            "TTS_SPEAK",
        ]
    
    def dispatch(self, action: str, params: Dict[str, Any], speech: str = ""):
        """Execute hardware action"""
        log_info(f"Hardware action: {action}", "HARDWARE_DISPATCHER")
        
        if action == "MOUSE_SHAKE":
            self.mouse.shake_cursor()
        
        elif action == "LOCK_INPUT":
            self.keyboard.lock_input()
        
        elif action == "UNLOCK_INPUT":
            self.keyboard.unlock_input()
        
        elif action == "GHOST_TYPE":
            text = params.get("text", "Geri dönüşün yok.")
            self.keyboard.ghost_type(text, self.process_guard)
        
        elif action == "PLAY_SFX":
            sound = params.get("sound_name", "glitch")
            self.audio.play_sfx(sound)
        
        elif action == "AUDIO_GLITCH":
            self.audio.play_sfx("static_noise")
        
        elif action == "CAMERA_FLASH":
            self.camera.camera_flash_scare()
        
        elif action == "BRIGHTNESS_FLICKER":
            times = params.get("times", 3)
            self.brightness.flicker(times)
        
        elif action == "BRIGHTNESS_DIM":
            target = params.get("target", 10)
            self.brightness.gradual_dim(target)
        
        elif action == "CAPSLOCK_TOGGLE":
            self.keyboard.toggle_caps_lock()
            
        elif action == "PLAY_SOUND":
            # Map PLAY_SOUND to play_sfx
            sound = params.get("sound") or params.get("sound_name") or "glitch"
            self.audio.play_sfx(sound)
            
        elif action == "TTS_SPEAK":
            speech = params.get("speech") or params.get("text")
            if speech:
                self.audio.play_tts(speech)
