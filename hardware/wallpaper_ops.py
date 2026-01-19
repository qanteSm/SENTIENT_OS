# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import ctypes
import os
import shutil
from config import Config
from core.logger import log_info, log_error

class WallpaperOps:
    """
    Manages system wallpaper changes and restoration.
    """
    _original_wallpaper = None

    @classmethod
    def save_current_wallpaper(cls):
        """Saves path to current wallpaper for restoration."""
        if cls._original_wallpaper: return
        
        try:
            path_buf = ctypes.create_unicode_buffer(512)
            # SPI_GETDESKWALLPAPER = 0x0073
            ctypes.windll.user32.SystemParametersInfoW(0x0073, 512, path_buf, 0)
            cls._original_wallpaper = path_buf.value
            log_info(f"Original wallpaper saved: {cls._original_wallpaper}", "WALLPAPER")
        except Exception as e:
            log_error(f"Failed to save wallpaper: {e}", "WALLPAPER")

    @classmethod
    def set_wallpaper(cls, image_path: str):
        """Sets the system wallpaper to the given image."""
        if not os.path.exists(image_path):
            log_error(f"Wallpaper file not found: {image_path}", "WALLPAPER")
            return

        try:
            # SPI_SETDESKWALLPAPER = 0x0014
            # SPIF_UPDATEINIFILE = 0x01
            # SPIF_SENDWININICHANGE = 0x02
            ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, image_path, 0x01 | 0x02)
            log_info(f"Wallpaper changed to {image_path}", "WALLPAPER")
        except Exception as e:
            log_error(f"Failed to set wallpaper: {e}", "WALLPAPER")

    @classmethod
    def restore_wallpaper(cls):
        """Restores the original wallpaper."""
        if cls._original_wallpaper and os.path.exists(cls._original_wallpaper):
            cls.set_wallpaper(cls._original_wallpaper)
            log_info("Original wallpaper restored.", "WALLPAPER")
        else:
            log_warning("No original wallpaper to restore.", "WALLPAPER")

    @classmethod
    def set_creepy_wallpaper(cls, variant="glitch"):
        """Sets a pre-defined creepy wallpaper if available."""
        # For now, let's assume we have some assets or we generate one
        # Placeholder logic
        log_info(f"Attempting to set creepy wallpaper: {variant}", "WALLPAPER")
        # In actual implementation, we might use generate_image to create a creepy one
        pass
