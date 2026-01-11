import random
import time
from typing import Tuple
from config import Config

try:
    if Config().IS_MOCK:
        raise ImportError("Mock Mode")
    import win32gui
    import win32api
    import win32con
    from ctypes import windll
    HAS_WIN32 = True
    HAS_WINDLL = True
except ImportError:
    HAS_WIN32 = False
    HAS_WINDLL = False
    windll = None

class GDIEngine:
    """
    Low-level GDI drawing engine for direct screen manipulation.
    Bypasses the window manager to draw 'glitches' directly on the monitor.
    """
    HAS_WIN32 = HAS_WIN32
    
    @staticmethod
    def get_screen_dc():
        """Returns the Device Context for the entire screen."""
        if not HAS_WIN32: return None
        return win32gui.GetDC(0)

    @staticmethod
    def release_dc(dc):
        """Releases the screen Device Context."""
        if not HAS_WIN32: return
        win32gui.ReleaseDC(0, dc)

    @classmethod
    def get_virtual_screen_rect(cls):
        """Returns (x, y, w, h) for the entire virtual screen (all monitors)."""
        if not HAS_WIN32: return (0, 0, 1920, 1080)
        
        # Virtual Screen Metrics
        SM_XVIRTUALSCREEN = 76
        SM_YVIRTUALSCREEN = 77
        SM_CXVIRTUALSCREEN = 78
        SM_CYVIRTUALSCREEN = 79
        
        x = win32api.GetSystemMetrics(SM_XVIRTUALSCREEN)
        y = win32api.GetSystemMetrics(SM_YVIRTUALSCREEN)
        w = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
        h = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)
        return (x, y, w, h)

    @classmethod
    def draw_static_noise(cls, area: Tuple[int, int, int, int] = None, density=0.01, duration_ms=500):
        """
        Optimized: Draws random black/white blocks (static) directly on the screen.
        Uses PatBlt instead of SetPixel for high performance.
        """
        if not HAS_WIN32:
            print("[GDI_MOCK] Drawing static noise...")
            return

        dc = cls.get_screen_dc()
        vx, vy, vw, vh = cls.get_virtual_screen_rect()
        
        # Default to full virtual screen if no area specified
        x, y, w, h = area or (vx, vy, vw, vh)
        
        end_time = time.time() + (duration_ms / 1000.0)
        
        try:
            # Create brushes once
            black_brush = win32gui.CreateSolidBrush(0)
            white_brush = win32gui.CreateSolidBrush(0xFFFFFF)
            
            while time.time() < end_time:
                # Draw noise in chunks
                for _ in range(20): # 20 blocks per iteration
                    bx = random.randint(x, x + w - 10)
                    by = random.randint(y, y + h - 10)
                    bw = random.randint(2, 20)
                    bh = random.randint(2, 20)
                    brush = random.choice([black_brush, white_brush])
                    
                    old_brush = win32gui.SelectObject(dc, brush)
                    win32gui.PatBlt(dc, bx, by, bw, bh, win32con.PATCOPY)
                    win32gui.SelectObject(dc, old_brush)
                
                time.sleep(0.01)
                
            win32gui.DeleteObject(black_brush)
            win32gui.DeleteObject(white_brush)
        finally:
            cls.release_dc(dc)

    @classmethod
    def invert_screen(cls, duration_ms=200):
        """Inverts the colors of the entire screen temporarily."""
        if not HAS_WIN32:
            print("[GDI_MOCK] Inverting screen colors...")
            return

        dc = cls.get_screen_dc()
        x, y, w, h = cls.get_virtual_screen_rect()
        
        # PATINVERT uses the destination bits and PATTERN
        # DSTINVERT simply inverts the destination bits
        try:
            # SAFE MODE: If strobe is disabled, make the inversion longer and less 'flickery'
            duration = duration_ms if Config().get("ENABLE_STROBE", False) else (duration_ms * 3)
            
            win32gui.BitBlt(dc, x, y, w, h, dc, 0, 0, win32con.DSTINVERT)
            time.sleep(duration / 1000.0)
            win32gui.BitBlt(dc, x, y, w, h, dc, 0, 0, win32con.DSTINVERT) # Revert
        finally:
            cls.release_dc(dc)

    @classmethod
    def draw_horror_line(cls, color=0x0000FF, thickness=2):
        """Draws a random 'cut' line across the screen."""
        if not HAS_WIN32: return
        
        dc = cls.get_screen_dc()
        vx, vy, vw, vh = cls.get_virtual_screen_rect()
        
        try:
            pen = win32gui.CreatePen(win32con.PS_SOLID, thickness, color)
            old_pen = win32gui.SelectObject(dc, pen)
            
            x1, y1 = random.randint(vx, vx + vw), random.randint(vy, vy + vh)
            x2, y2 = random.randint(vx, vx + vw), random.randint(vy, vy + vh)
            
            win32gui.MoveToEx(dc, x1, y1)
            win32gui.LineTo(dc, x2, y2)
            
            win32gui.SelectObject(dc, old_pen)
            win32gui.DeleteObject(pen)
        finally:
            cls.release_dc(dc)

    @classmethod
    def flash_red_glitch(cls):
        """Full screen red flash using PatBlt."""
        if not HAS_WIN32: return
        
        dc = cls.get_screen_dc()
        x, y, w, h = cls.get_virtual_screen_rect()
        
        try:
            # SAFE MODE: Red flashing is a major seizure trigger. Suppress if not enabled.
            if not Config().get("ENABLE_STROBE", False):
                print("[GDI] Red flash suppressed for photosensitivity.")
                return

            brush = win32gui.CreateSolidBrush(win32api.RGB(255, 0, 0))
            old_brush = win32gui.SelectObject(dc, brush)
            
            # Use PATINVERT for a ghostly flicker effect instead of solid fill
            win32gui.PatBlt(dc, x, y, w, h, win32con.PATINVERT)
            time.sleep(0.05)
            win32gui.PatBlt(dc, x, y, w, h, win32con.PATINVERT)
            
            win32gui.SelectObject(dc, old_brush)
            win32gui.DeleteObject(brush)
        finally:
            cls.release_dc(dc)

    @staticmethod
    def force_refresh_screen():
        """Forces the entire screen to redraw, clearing any GDI leftovers."""
        if not HAS_WINDLL: 
            return
        try:
            # InvalidateRect(0, None, True) triggers a full screen redraw
            windll.user32.InvalidateRect(0, None, True)
            print("[GDI] Screen refresh forced.")
        except Exception as e:
            print(f"[GDI] Refresh error: {e}")
