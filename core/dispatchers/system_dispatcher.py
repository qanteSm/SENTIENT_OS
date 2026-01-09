"""
System Dispatcher - Handles system operations and state management

Supported actions:
- SET_WALLPAPER, CLIPBOARD_POISON, FAKE_NOTIFICATION
- NOTEPAD_HIJACK, WINDOW_MANIPULATE, CORRUPT_WINDOWS
- SCRAMBLE_ICONS, ICON_SCRAMBLE
- SET_PERSONA, SET_MOOD
- RESTORE_SYSTEM, OPEN_BROWSER
"""
from typing import List, Dict, Any
from core.dispatchers.base_dispatcher import BaseDispatcher
from core.logger import log_info


class SystemDispatcher(BaseDispatcher):
    """
    Handles system operations, config changes, and cleanup.
    
    Dependencies: WallpaperOps, ClipboardOps, NotificationOps, 
                  NotepadOps, WindowOps, IconOps, BrowserOps
    Actions: ~11 system operations
    """
    
    def __init__(self):
        from hardware.wallpaper_ops import WallpaperOps
        from hardware.clipboard_ops import ClipboardOps
        from hardware.notification_ops import NotificationOps
        from hardware.notepad_ops import NotepadOps
        from hardware.window_ops import WindowOps
        from visual.icon_ops import IconOps
        from visual.browser_ops import BrowserOps
        
        self.wallpaper = WallpaperOps
        self.clipboard = ClipboardOps
        self.notifications = NotificationOps()
        self.notepad = NotepadOps
        self.window = WindowOps
        self.icons = IconOps
        self.browser = BrowserOps()
    
    def get_supported_actions(self) -> List[str]:
        """System operation actions"""
        return [
            "SET_WALLPAPER",
            "CLIPBOARD_POISON",
            "FAKE_NOTIFICATION",
            "NOTEPAD_HIJACK",
            "CORRUPT_WINDOWS",
            "SCRAMBLE_ICONS",
            "SET_PERSONA",
            "SET_MOOD",
            "RESTORE_SYSTEM",
            "OPEN_BROWSER",
        ]
    
    def dispatch(self, action: str, params: Dict[str, Any], speech: str = ""):
        """Execute system action"""
        log_info(f"System action: {action}", "SYSTEM_DISPATCHER")
        
        if action == "SET_WALLPAPER":
            path = params.get("image_path")
            if path:
                self.wallpaper.set_wallpaper(path)
        
        elif action == "CLIPBOARD_POISON":
            text = params.get("text", "SEN BENİMSİN")
            self.clipboard.poison_clipboard(text)
        
        elif action == "FAKE_NOTIFICATION":
            title = params.get("title")
            message = params.get("message")
            self.notifications.show_fake_system_alert(title, message)
        
        elif action == "NOTEPAD_HIJACK":
            text = params.get("text", "YARDIM EDİN")
            delay = params.get("delay", 0.1)
            self.notepad.hijack_and_type(text, delay)
        
        elif action == "CORRUPT_WINDOWS":
            self.window.corrupt_all_windows()
        
        elif action == "SCRAMBLE_ICONS":
            pattern = params.get("pattern", "spiral")
            self.icons.scramble_into_pattern(pattern)
        
        elif action == "SET_PERSONA":
            # Handled by main dispatcher (needs brain reference)
            pass
        
        elif action == "SET_MOOD":
            # Handled by main dispatcher (needs fake_ui reference)
            pass
        
        elif action == "RESTORE_SYSTEM":
            # Safety cleanup
            self.window.restore_all_windows()
            self.icons.restore_icon_positions()
            # BrightnessOps.restore_brightness() would need import
            log_info("System restoration completed", "SYSTEM_DISPATCHER")
        
        elif action == "OPEN_BROWSER":
            url = params.get("url", "https://google.com")
            self.browser.open_url(url)
