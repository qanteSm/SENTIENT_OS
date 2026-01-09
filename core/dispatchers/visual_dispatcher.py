"""
Visual Dispatcher - Handles visual effects and screen modifications

Supported actions:
- OVERLAY_TEXT, FLASH_COLOR, SHAKE_SCREEN, SHAKE_CHAT
- SCREEN_INVERT, GDI_STATIC, GDI_LINE, GDI_FLASH
"""
from typing import List, Dict, Any
from core.dispatchers.base_dispatcher import BaseDispatcher
from core.logger import log_info


class VisualDispatcher(BaseDispatcher):
    """
    Handles all visual effects and screen modifications.
    
    Dependencies: OverlayManager, GDIEngine
    Actions: ~8 visual effects
    """
    
    def __init__(self):
        from visual.overlay_manager import OverlayManager
        from visual.gdi_engine import GDIEngine
        
        self.overlay = OverlayManager()
        self.gdi = GDIEngine()
    
    def get_supported_actions(self) -> List[str]:
        """Visual effect actions"""
        return [
            "OVERLAY_TEXT",
            "FLASH_COLOR",
            "SHAKE_SCREEN",
            "SHAKE_CHAT",
            "SCREEN_INVERT",
            "GDI_STATIC",
            "GDI_LINE",
            "GDI_FLASH",
        ]
    
    def dispatch(self, action: str, params: Dict[str, Any], speech: str = ""):
        """Execute visual action"""
        log_info(f"Visual action: {action}", "VISUAL_DISPATCHER")
        
        if action == "OVERLAY_TEXT":
            text = params.get("text", "...")
            duration = params.get("duration", 3000)
            self.overlay.show_text(text, duration)
        
        elif action == "FLASH_COLOR":
            color = params.get("color", "#FF0000")
            opacity = params.get("opacity", 0.4)
            duration = params.get("duration", 300)
            self.overlay.flash_color(color, opacity, duration)
        
        elif action == "SHAKE_SCREEN":
            intensity = params.get("intensity", 20)
            duration = params.get("duration", 1000)
            self.overlay.shake_screen(intensity, duration)
        
        elif action == "SHAKE_CHAT":
            # Will be handled by FunctionDispatcher (needs chat reference)
            pass
        
        elif action == "SCREEN_INVERT":
            duration = params.get("duration", 200)
            self.gdi.invert_screen(duration)
        
        elif action == "GDI_STATIC":
            duration = params.get("duration", 500)
            density = params.get("density", 0.01)
            self.gdi.draw_static_noise(duration_ms=duration, density=density)
        
        elif action == "GDI_LINE":
            color = params.get("color", 0x0000FF)
            thickness = params.get("thickness", 2)
            self.gdi.draw_horror_line(color=color, thickness=thickness)
        
        elif action == "GDI_FLASH":
            self.gdi.flash_red_glitch()
