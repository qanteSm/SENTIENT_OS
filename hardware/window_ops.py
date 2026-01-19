# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Window Title Corruption Operations
Corrupts window titles for psychological horror.
"""
from config import Config
import random

try:
    if Config().IS_MOCK:
        raise ImportError("Mock Mode")
    import win32gui
    import win32con
    import win32process
    import win32api
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
    def get_active_window_info():
        """
        Returns info about the current foreground window.
        Returns: { 'title': str, 'class': str, 'process': str, 'hwnd': int }
        """
        if not HAS_WIN32:
            return {'title': 'Mock', 'class': 'MockClass', 'process': 'mock.exe', 'hwnd': 0}
        
        try:
            hwnd = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            
            # Get Process Name
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
            # win32process.GetModuleFileNameEx returns the full path
            full_path = win32process.GetModuleFileNameEx(handle, 0)
            process_name = full_path.split('\\')[-1].lower()
            win32api.CloseHandle(handle)
            
            return {
                'title': title,
                'class': class_name,
                'process': process_name,
                'hwnd': hwnd
            }
        except Exception as e:
            # print(f"[WINDOW_OPS] Error getting info: {e}")
            return {'title': 'Unknown', 'class': 'Unknown', 'process': 'unknown.exe', 'hwnd': 0}
    
    @staticmethod
    def corrupt_all_windows():
        """
        Corrupts the titles of all visible windows except our own.
        """
        if Config().IS_MOCK or not HAS_WIN32:
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
            except (Exception) as e:
                # Skip windows that can't be modified
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
        if Config().IS_MOCK or not HAS_WIN32:
            print("[MOCK] WINDOW TITLES RESTORED")
            return
        
        for hwnd, original_title in WindowOps._original_titles.items():
            try:
                if win32gui.IsWindow(hwnd):
                    win32gui.SetWindowText(hwnd, original_title)
            except (Exception) as e:
                print(f"[WINDOWS] Failed to restore window {hwnd}: {e}")
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
        if Config().IS_MOCK or not HAS_WIN32:
            print(f"[MOCK] FLASHING WINDOW: {hwnd_or_title}")
            return
        
        # Implementation would use FlashWindowEx
        pass
    @staticmethod
    def shift_active_window(dx: int = 10, dy: int = 10):
        """Slightly shifts the foreground window."""
        if Config().IS_MOCK or not HAS_WIN32:
            print(f"[MOCK] SHIFTING ACTIVE WINDOW by {dx}, {dy}")
            return
        
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                rect = win32gui.GetWindowRect(hwnd)
                # left, top, right, bottom
                width = rect[2] - rect[0]
                height = rect[3] - rect[1]
                
                win32gui.MoveWindow(hwnd, rect[0] + dx, rect[1] + dy, width, height, True)
        except Exception:
            pass

    @staticmethod
    def shake_active_window(intensity: int = 10, duration_ms: int = 500):
        """Vibrates the active window."""
        if Config().IS_MOCK or not HAS_WIN32:
            print(f"[MOCK] SHAKING WINDOW (intensity={intensity}, duration={duration_ms}ms)")
            return
            
        import threading
        import time
        
        def run_shake():
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd: return
            
            rect = win32gui.GetWindowRect(hwnd)
            orig_x, orig_y = rect[0], rect[1]
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            
            end_time = time.time() + (duration_ms / 1000.0)
            while time.time() < end_time:
                off_x = random.randint(-intensity, intensity)
                off_y = random.randint(-intensity, intensity)
                win32gui.MoveWindow(hwnd, orig_x + off_x, orig_y + off_y, width, height, True)
                time.sleep(0.02)
            
            # Restore
            win32gui.MoveWindow(hwnd, orig_x, orig_y, width, height, True)
            
        threading.Thread(target=run_shake, daemon=True).start()
