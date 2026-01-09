"""
Horror Dispatcher - Handles horror-specific effects and scares

Supported actions:
- THE_MASK, SCREEN_TEAR, PIXEL_MELT, SCREEN_MELT
- FAKE_BSOD, FAKE_UPDATE
- FAKE_FILE_DELETE, CAMERA_THREAT, NAME_REVEAL, TIME_DISTORTION
- FAKE_BROWSER_HISTORY, FAKE_LISTENING, CREEPY_MUSIC, WHISPER
- DIGITAL_GLITCH_SURGE
"""
from typing import List, Dict, Any
from core.dispatchers.base_dispatcher import BaseDispatcher
from core.logger import log_info


class HorrorDispatcher(BaseDispatcher):
    """
    Handles horror-specific effects and psychological scares.
    
    Dependencies: DesktopMask, FakeUI, ScreenTear, PixelMelt, HorrorEffects
    Actions: ~15 horror effects
    """
    
    def __init__(self):
        from visual.desktop_mask import DesktopMask
        from visual.fake_ui import FakeUI
        from visual.effects.screen_tear import ScreenTear
        from visual.effects.pixel_melt import PixelMelt
        from visual.effects.screen_melter import trigger_melt
        from visual.horror_effects import get_horror_effects
        
        self.mask = DesktopMask()
        self.fake_ui = FakeUI()
        self.screen_tear = ScreenTear
        self.pixel_melt = PixelMelt
        self.trigger_melt = trigger_melt
        self.get_horror = get_horror_effects
    
    def get_supported_actions(self) -> List[str]:
        """Horror effect actions"""
        return [
            "THE_MASK",
            "GLITCH_SCREEN",
            "SCREEN_TEAR",
            "PIXEL_MELT",
            "SCREEN_MELT",
            "FAKE_BSOD",
            "FAKE_UPDATE",
            "FAKE_FILE_DELETE",
            "CAMERA_THREAT",
            "APP_THREAT",
            "NAME_REVEAL",
            "TIME_DISTORTION",
            "FAKE_BROWSER_HISTORY",
            "FAKE_LISTENING",
            "CREEPY_MUSIC",
            "WHISPER",
            "DIGITAL_GLITCH_SURGE",
        ]
    
    def dispatch(self, action: str, params: Dict[str, Any], speech: str = ""):
        """Execute horror action"""
        log_info(f"Horror action: {action}", "HORROR_DISPATCHER")
        
        if action == "THE_MASK":
            self.mask.capture_and_mask()
        
        elif action == "GLITCH_SCREEN":
            # This might be handled by visual dispatcher - using overlay
            pass
        
        elif action == "SCREEN_TEAR":
            intensity = params.get("intensity", 15)
            duration = params.get("duration", 500)
            self.screen_tear.tear_screen(intensity, duration)
        
        elif action == "PIXEL_MELT":
            self.pixel_melt.trigger_random()
        
        elif action == "SCREEN_MELT":
            self.trigger_melt()
        
        elif action == "FAKE_BSOD":
            self.fake_ui.show_bsod()
        
        elif action == "FAKE_UPDATE":
            percent = params.get("percent", 0)
            self.fake_ui.show_fake_update(percent)
        
        elif action == "FAKE_FILE_DELETE":
            horror = self.get_horror(None)  # Will need dispatcher ref
            horror.fake_file_deletion()
        
        elif action == "CAMERA_THREAT":
            # Handled by camera ops
            pass
        
        elif action == "APP_THREAT":
            horror = self.get_horror(None)
            horror.app_specific_threat()
        
        elif action == "NAME_REVEAL":
            horror = self.get_horror(None)
            horror.dramatic_name_reveal()
        
        elif action == "TIME_DISTORTION":
            horror = self.get_horror(None)
            horror.time_distortion_effect()
        
        elif action == "FAKE_BROWSER_HISTORY":
            horror = self.get_horror(None)
            horror.fake_browser_history_threat()
        
        elif action == "FAKE_LISTENING":
            horror = self.get_horror(None)
            horror.fake_listening_feedback()
        
        elif action == "CREEPY_MUSIC":
            horror = self.get_horror(None)
            horror.creepy_lullaby()
        
        elif action == "WHISPER":
            horror = self.get_horror(None)
            horror.mechanical_whispers()
        
        elif action == "DIGITAL_GLITCH_SURGE":
            horror = self.get_horror(None)
            horror.digital_glitch_surge()
