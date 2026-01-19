# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

from config import Config
try:
    if Config().IS_MOCK:
        raise ImportError("Mock Mode")
    import keyboard
    import win32gui
except ImportError:
    keyboard = None
    win32gui = None

import time
from core.process_guard import ProcessGuard

class KeyboardOps:
    """
    Handles keyboard locking, LED manipulation, and typing.
    """
    @staticmethod
    def lock_input():
        if keyboard:
            try:
                # Block all keys
                for i in range(150):
                    keyboard.block_key(i)
                print("[HARDWARE] Keyboard Locked.")
            except Exception as e:
                print(f"[HARDWARE] Lock Error: {e}")
        else:
            print("[MOCK] KEYBOARD LOCKED")

    @staticmethod
    def unlock_input():
        if keyboard:
            try:
                keyboard.unhook_all()
                print("[HARDWARE] Keyboard Unlocked.")
            except Exception as e:
                print(f"[HARDWARE] Unlock Error: {e}")
        else:
            print("[MOCK] KEYBOARD UNLOCKED")

    @staticmethod
    def ghost_type(text: str, process_guard: ProcessGuard = None):
        """
        Types text into the active window.
        SAFE: Checks if active window is protected (OBS, Discord, etc.) before typing.
        """
        if Config().IS_MOCK or not keyboard or not win32gui:
            print(f"[MOCK] GHOST TYPE: {text}")
            return

        try:
            # 1. Get Detailed Window Info
            from hardware.window_ops import WindowOps
            info = WindowOps.get_active_window_info()
            proc = info.get('process', '').lower()
            
            # 2. Check Safety (Protected Processes)
            if process_guard:
                # Add Streamer apps to protected list
                protected_procs = [
                    "obs64.exe", "obs32.exe", "streamlabs.exe", 
                    "discord.exe", "vlc.exe", "mpc-hc.exe"
                ]
                protected_keywords = ["bank", "login", "password", "private", "özel", "şifre"]
                
                if proc in protected_procs:
                    print(f"[SAFETY] Ghost Type Blocked on Protected App: {proc}")
                    return
                
                title_lower = info.get('title', '').lower()
                for keyword in protected_keywords:
                    if keyword in title_lower:
                        print(f"[SAFETY] Ghost Type Blocked on Protected Window: {info.get('title')}")
                        return

            # 3. Type
            keyboard.write(text, delay=0.1)
        except Exception as e:
            print(f"[HARDWARE] Typing Error: {e}")

    @staticmethod
    def toggle_caps_lock():
        """Toggles the CapsLock state."""
        if keyboard:
            try:
                keyboard.send('caps lock')
                print("[HARDWARE] CapsLock Toggled.")
            except Exception as e:
                print(f"[HARDWARE] CapsLock Toggle Error: {e}")
        else:
            print("[MOCK] CAPSLOCK TOGGLED")

    @staticmethod
    def capslock_morse(message: str):
        """Blinks CapsLock LED. (Requires permission/drivers sometimes)"""
        if Config().IS_MOCK:
            print(f"[MOCK] CAPSLOCK MORSE: {message}")
            return
        
        # Toggle CapsLock
        if keyboard:
            for char in message:
                keyboard.send('caps lock')
                time.sleep(0.2)
                keyboard.send('caps lock')
                time.sleep(0.2)
