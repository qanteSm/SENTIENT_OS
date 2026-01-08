"""
Window Title Corruption Operations
Corrupts window titles for psychological horror.
"""
from config import Config
import random

try:
    if Config.IS_MOCK:
        raise ImportError("Mock Mode")
    import win32gui
    import win32con
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

class WindowOps:
    """
    Operations to manipulate window titles and properties.
    """
    
    # Original titles backup for restoration
    _original_titles = {}
    
    @staticmethod
    def corrupt_all_windows():
        """
        Corrupts the titles of all visible windows except our own.
        """
        if Config.IS_MOCK or not HAS_WIN32:
            print("[MOCK] WINDOW TITLES CORRUPTED")
            return
        
        corruptions = [
            "█ HATALI BELLEK ███",
            "▓▒ SİSTEM HATASI ▒▓",
            "⚠ YETKISIZ ERIŞIM ⚠",
            "*** BOZUK VERI ***",
            "░▒▓ HATA 0x000000 ▓▒░",
            "C.O.R.E. KONTROLÜNDE",
            "█ █ █ HATA █ █ █",
        ]
        
        def callback(hwnd, extra):
            try:
                if win32gui.IsWindowVisible(hwnd):
                    current_title = win32gui.GetWindowText(hwnd)
                    
                    # Skip if no title or if it's our app
                    if not current_title or "SENTIENT" in current_title or "C.O.R.E" in current_title:
                        return
                    
                    # Backup original if not already saved
                    if hwnd not in WindowOps._original_titles:
                        WindowOps._original_titles[hwnd] = current_title
                    
                    # Set corrupted title
                    new_title = random.choice(corruptions)
                    win32gui.SetWindowText(hwnd, new_title)
            except:
                pass
        
        try:
            win32gui.EnumWindows(callback, None)
            print(f"[WINDOWS] Corrupted {len(WindowOps._original_titles)} window titles")
            
            # YENİ: StateManager'a kaydet
            from core.state_manager import StateManager
            StateManager().update_state("windows_corrupted", True)
            
        except Exception as e:
            print(f"[WINDOWS] Corruption failed: {e}")
    
    @staticmethod
    def restore_all_windows():
        """
        Restores all corrupted window titles to originals.
        """
        if Config.IS_MOCK or not HAS_WIN32:
            print("[MOCK] WINDOW TITLES RESTORED")
            return
        
        for hwnd, original_title in WindowOps._original_titles.items():
            try:
                if win32gui.IsWindow(hwnd):
                    win32gui.SetWindowText(hwnd, original_title)
            except:
                pass
        
        WindowOps._original_titles.clear()
        
        # YENİ: StateManager'dan temizle
        from core.state_manager import StateManager
        StateManager().remove_state("windows_corrupted")
        
        print("[WINDOWS] All titles restored")
    
    @staticmethod
    def flash_window(hwnd_or_title: str, times: int = 5):
        """
        Makes a window flash in the taskbar.
        """
        if Config.IS_MOCK or not HAS_WIN32:
            print(f"[MOCK] FLASHING WINDOW: {hwnd_or_title}")
            return
        
        # Implementation would use FlashWindowEx
        pass
