# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Pixel Melt Effect - Simulates screen melting.

Creates the illusion of pixels "dripping" downward.
Uses GDI pixel manipulation for realistic melting effect.
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


class PixelMelt:
    """
    Creates screen melting effect.
    
    Gradually shifts pixels downward in a region to simulate
    melting/dripping visual corruption.
    """
    
    @staticmethod
    def melt_region(x=None, y=None, width=300, height=200, speed=5):
        """
        Melt a screen region.
        
        Args:
            x, y: Top-left corner (None = random)
            width, height: Region size
            speed: Melt speed (higher = faster drip)
        """
        if not HAS_WIN32:
            print("[PIXEL_MELT] Win32 not available, effect skipped")
            return
        
        from config import Config
        if Config().get("SAFE_HARDWARE", False):
            print("[PIXEL_MELT] Safe mode enabled, effect skipped")
            return
        
        try:
            # Get screen dimensions
            screen_width = windll.user32.GetSystemMetrics(0)
            screen_height = windll.user32.GetSystemMetrics(1)
            
            # Random position if not specified
            if x is None:
                x = random.randint(0, screen_width - width)
            if y is None:
                y = random.randint(0, screen_height // 2)  # Top half only
            
            print(f"[PIXEL_MELT] Melting region at ({x}, {y})")
            
            # Get device context
            hdc = windll.user32.GetDC(0)
            screen_dc = win32ui.CreateDCFromHandle(hdc)
            mem_dc = screen_dc.CreateCompatibleDC()
            
            # Create bitmap for region
            bitmap = win32ui.CreateBitmap()
            bitmap.CreateCompatibleBitmap(screen_dc, width, height)
            mem_dc.SelectObject(bitmap)
            
            # Copy region
            mem_dc.BitBlt((0, 0), (width, height),
                         screen_dc, (x, y), win32con.SRCCOPY)
            
            # Apply melting effect
            max_drip = 100  # Maximum drip distance
            drip_columns = []
            
            # Initialize random drip for each column
            for col in range(0, width, 2):  # Every 2 pixels for performance
                drip_columns.append(random.randint(0, max_drip))
            
            # Apply drip effect
            for col_idx, col in enumerate(range(0, width, 2)):
                drip_amount = drip_columns[col_idx]
                
                if drip_amount > 0:
                    # Shift pixels down
                    for offset in range(0, drip_amount, speed):
                        if y + height + offset < screen_height:
                            screen_dc.BitBlt(
                                (x + col, y + offset),
                                (2, height),
                                mem_dc,
                                (col, 0),
                                win32con.SRCCOPY
                            )
            
            # Cleanup
            mem_dc.DeleteDC()
            screen_dc.DeleteDC()
            windll.user32.ReleaseDC(0, hdc)
            
            # Auto-restore after 1 second
            QTimer.singleShot(1000, lambda: windll.user32.InvalidateRect(0, None, True))
            
        except Exception as e:
            print(f"[PIXEL_MELT] Error: {e}")
    
    @staticmethod
    def trigger_random():
        """Trigger with random parameters"""
        width = random.randint(200, 400)
        height = random.randint(150, 300)
        speed = random.randint(3, 8)
        PixelMelt.melt_region(width=width, height=height, speed=speed)
