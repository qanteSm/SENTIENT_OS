# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import random
from core.event_bus import EventBus
from core.logger import log_info

class GlitchLogic:
    """
    Connects system events to autonomous visual glitches.
    Makes the system feel 'alive' and reactive.
    """
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self._setup_subscriptions()
        log_info("Glitch Logic Layer Online.", "VISUAL")

    def _setup_subscriptions(self):
        """Subscribe to events that should trigger glitches."""
        EventBus().subscribe("ui.window_changed", self._on_window_changed)
        EventBus().subscribe("ui.user_activity", self._on_user_activity)
        EventBus().subscribe("anger.escalated", self._on_anger_escalated)

    def _on_window_changed(self, data):
        """Trigger a glitch based on Window Class (Language Independent)."""
        from hardware.window_ops import WindowOps
        
        # Get detailed info
        info = WindowOps.get_active_window_info()
        proc = info.get('process', '').lower()
        cls = info.get('class', '')
        title = info.get('title', '').lower()
        
        # 1. Aggressive Reaction (Anti-Escape)
        # Task Manager, Process Hacker, MMC (Services)
        if proc in ["taskmgr.exe", "processhacker.exe", "mmc.exe"] or cls == "TaskManagerWindow":
            self.dispatcher.dispatch({"action": "SCREEN_MELT"})
            log_info(f"Aggressive glitch triggered by escape attempt: {proc}", "GLITCH")
            
        # 2. Helpful/Creepy Reaction (Anti-Help) - Contextual
        # Installers / Uninstallers often use #32770 or msiexec
        elif proc == "msiexec.exe" or ("uninstall" in title) or ("kaldır" in title):
            self.dispatcher.dispatch({"action": "GDI_LINE"})
            self.dispatcher.dispatch({"action": "SCREEN_INVERT", "params": {"duration": 200}})
            log_info(f"Glitch triggered by modification attempt: {proc}", "GLITCH")

        # 3. Subtle Warning (Browsers)
        elif proc in ["chrome.exe", "msedge.exe", "firefox.exe", "opera.exe"]:
            if random.random() < 0.2: # 20% chance
                self.dispatcher.dispatch({"action": "GDI_FLASH"})

    def _on_user_activity(self, data):
        """Trigger a flicker if the user is moving mouse too fast/hesitantly."""
        # Simple probability based reaction
        if random.random() < 0.05: # Rare subtle flicker
            self.dispatcher.dispatch({"action": "BRIGHTNESS_FLICKER", "params": {"times": 1}})

    def _on_anger_escalated(self, data):
        """Trigger more aggressive visuals when AI gets angrier."""
        level = data.get("level", 0)
        if level > 80:
            if random.random() < 0.3:
                self.dispatcher.dispatch({"action": "SCREEN_INVERT", "params": {"duration": 150}})
