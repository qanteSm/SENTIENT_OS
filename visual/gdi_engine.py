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
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

class GDIEngine:
    """
    Low-level GDI drawing engine for direct screen manipulation.
    Bypasses the window manager to draw 'glitches' directly on the monitor.
    """
    
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
    def draw_static_noise(cls, area: Tuple[int, int, int, int] = None, density=0.01, duration_ms=500):
        """
        Optimized: Draws random black/white blocks (static) directly on the screen.
        Uses PatBlt instead of SetPixel for high performance.
        """
        if not HAS_WIN32:
            print("[GDI_MOCK] Drawing static noise...")
            return

        dc = cls.get_screen_dc()
        screen_w = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_h = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        
        x, y, w, h = area or (0, 0, screen_w, screen_h)
        
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
        w = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        h = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        
        # PATINVERT uses the destination bits and PATTERN
        # DSTINVERT simply inverts the destination bits
        try:
            # PATINVERT uses the destination bits and PATTERN
            # DSTINVERT simply inverts the destination bits
            
            # SAFE MODE: If strobe is disabled, make the inversion longer and less 'flickery'
            duration = duration_ms if Config.ENABLE_STROBE else (duration_ms * 3)
            
            win32gui.BitBlt(dc, 0, 0, w, h, dc, 0, 0, win32con.DSTINVERT)
            time.sleep(duration / 1000.0)
            win32gui.BitBlt(dc, 0, 0, w, h, dc, 0, 0, win32con.DSTINVERT) # Revert
        finally:
            cls.release_dc(dc)

    @classmethod
    def draw_horror_line(cls, color=0x0000FF, thickness=2):
        """Draws a random 'cut' line across the screen."""
        if not HAS_WIN32: return
        
        dc = cls.get_screen_dc()
        w = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        h = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        
        try:
            pen = win32gui.CreatePen(win32con.PS_SOLID, thickness, color)
            old_pen = win32gui.SelectObject(dc, pen)
            
            x1, y1 = random.randint(0, w), random.randint(0, h)
            x2, y2 = random.randint(0, w), random.randint(0, h)
            
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
        w = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        h = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        
        try:
            # SAFE MODE: Red flashing is a major seizure trigger. Suppress if not enabled.
            if not Config.ENABLE_STROBE:
                print("[GDI] Red flash suppressed for photosensitivity.")
                return

            brush = win32gui.CreateSolidBrush(win32api.RGB(255, 0, 0))
            old_brush = win32gui.SelectObject(dc, brush)
            
            # Use PATINVERT for a ghostly flicker effect instead of solid fill
            win32gui.PatBlt(dc, 0, 0, w, h, win32con.PATINVERT)
            time.sleep(0.05)
            win32gui.PatBlt(dc, 0, 0, w, h, win32con.PATINVERT)
            
            win32gui.SelectObject(dc, old_brush)
            win32gui.DeleteObject(brush)
        finally:
            cls.release_dc(dc)
