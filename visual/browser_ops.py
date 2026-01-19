# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

from config import Config
import webbrowser

class BrowserOps:
    """
    Opens browsers to specific URLs safely (or scary ones).
    """
    def open_url(self, url: str):
        if Config().IS_MOCK:
            print(f"[MOCK] BROWSER OPENED: {url}")
            return
        
        try:
            webbrowser.open(url)
            print(f"[VISUAL] Browser opened to {url}")
        except Exception as e:
            print(f"[VISUAL] Failed to open browser: {e}")
