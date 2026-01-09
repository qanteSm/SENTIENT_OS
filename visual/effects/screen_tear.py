"""
Screen Tear Effect - Advanced GDI manipulation.

Creates glitch effect by shifting screen regions horizontally.
Uses Windows BitBlt for hardware-accelerated screen manipulation.
"""

import random
from PyQt6.QtCore import QTimer

try:
    import win32gui
    import win32ui
    import win32con
    from ctypes import windll
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False


class ScreenTear:
    """
    Creates screen tearing effect using GDI BitBlt.
    
    SAFETY:
    - Non-destructive (temporary visual only)
    - Auto-restores after effect completes
    - Respects SAFE_HARDWARE config
    """
    
    @staticmethod
    def tear_screen(intensity=10, duration=500):
        """
        Apply screen tear effect.
        
        Args:
            intensity: Pixel offset for tear (1-50)
            duration: Effect duration in milliseconds
        """
        if not HAS_WIN32:
            print("[SCREEN_TEAR] Win32 not available, effect skipped")
            return
        
        from config import Config
        if Config().get("SAFE_HARDWARE", False):
            print("[SCREEN_TEAR] Safe mode enabled, effect skipped")
            return
        
        print(f"[SCREEN_TEAR] Applying tear effect (intensity: {intensity})")
        
        try:
            # Get screen dimensions
            screen_width = windll.user32.GetSystemMetrics(0)
            screen_height = windll.user32.GetSystemMetrics(1)
            
            # Get device context
            hdc = windll.user32.GetDC(0)
            screen_dc = win32ui.CreateDCFromHandle(hdc)
            mem_dc = screen_dc.CreateCompatibleDC()
            
            # Create bitmap
            bitmap = win32ui.CreateBitmap()
            bitmap.CreateCompatibleBitmap(screen_dc, screen_width, screen_height)
            mem_dc.SelectObject(bitmap)
            
            # Copy screen to memory
            mem_dc.BitBlt((0, 0), (screen_width, screen_height),
                         screen_dc, (0, 0), win32con.SRCCOPY)
            
            # Apply tear effect - shift random horizontal slices
            num_tears = random.randint(3, 8)
            for _ in range(num_tears):
                y_pos = random.randint(0, screen_height - 100)
                slice_height = random.randint(20, 80)
                offset = random.randint(-intensity, intensity)
                
                # Copy slice with offset
                screen_dc.BitBlt(
                    (offset, y_pos),
                    (screen_width - abs(offset), slice_height),
                    mem_dc,
                    (0 if offset > 0 else abs(offset), y_pos),
                    win32con.SRCCOPY
                )
            
            # Cleanup
            mem_dc.DeleteDC()
            screen_dc.DeleteDC()
            windll.user32.ReleaseDC(0, hdc)
            
            # Auto-restore after duration
            QTimer.singleShot(duration, lambda: windll.user32.InvalidateRect(0, None, True))
            
        except Exception as e:
            print(f"[SCREEN_TEAR] Error: {e}")
    
    @staticmethod
    def trigger_random():
        """Trigger with random parameters"""
        intensity = random.randint(5, 25)
        duration = random.randint(300, 800)
        ScreenTear.tear_screen(intensity, duration)
