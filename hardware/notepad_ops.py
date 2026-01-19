# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Notepad Hijacking Operations
Autonomously opens and types into Notepad for psychological horror.
"""
from config import Config
import time

try:
    if Config().IS_MOCK:
        raise ImportError("Mock Mode")
    import subprocess
    import pywinauto
    from pywinauto import application
    HAS_PYWINAUTO = True
except ImportError:
    HAS_PYWINAUTO = False

class NotepadOps:
    """
    Operations to hijack Notepad and type messages autonomously.
    """
    
    @staticmethod
    def hijack_and_type(message: str, delay_per_char: float = 0.1):
        """
        Opens Notepad and types a message character by character.
        
        Args:
            message: The text to type
            delay_per_char: Delay between characters in seconds (for typing effect)
        """
        if Config().IS_MOCK or not HAS_PYWINAUTO:
            print(f"[MOCK] NOTEPAD HIJACK: {message}")
            return
        
        try:
            # Launch Notepad
            subprocess.Popen(['notepad.exe'])
            time.sleep(1.5)  # Wait for Notepad to open
            
            # Connect to Notepad window
            app = application.Application().connect(title_re=".*Notepad.*|.*Not Defteri.*")
            
            # Get the edit control and type
            # Notepad's edit control is usually the main window itself
            notepad_window = app.window(title_re=".*Notepad.*|.*Not Defteri.*")
            
            # Type with delays for horror effect
            notepad_window.type_keys(message, with_spaces=True, pause=delay_per_char)
            
            print(f"[NOTEPAD] Successfully hijacked and typed: {message[:20]}...")
            
        except Exception as e:
            print(f"[NOTEPAD] Hijack failed: {e}")
            # Fallback: just print
            
    @staticmethod
    def close_notepad_without_saving():
        """
        Forcefully closes Notepad without saving.
        """
        if Config().IS_MOCK or not HAS_PYWINAUTO:
            print("[MOCK] NOTEPAD CLOSED")
            return
            
        try:
            app = application.Application().connect(title_re=".*Notepad.*|.*Not Defteri.*")
            app.kill()
        except (Exception) as e:
            print(f"[NOTEPAD] Close failed: {e}")
            pass
