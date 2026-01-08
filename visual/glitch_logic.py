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

    def _on_window_changed(self, event_type, data):
        """Trigger a glitch when the user tries to 'switch' context or seek help."""
        title = data.get("title", "").lower()
        
        # 1. Aggressive Reaction (Anti-Escape)
        if any(term in title for term in ["task manager", "görev yöneticisi", "process hacker"]):
            self.dispatcher.dispatch({"action": "SCREEN_MELT"})
            log_info(f"Aggressive glitch triggered by escape attempt: {title}", "GLITCH")
            
        # 2. Helpful/Creepy Reaction (Anti-Help)
        elif any(term in title for term in ["delete", "remove", "silme", "nasıl silinir", "uninstaller"]):
            self.dispatcher.dispatch({"action": "GDI_LINE"})
            self.dispatcher.dispatch({"action": "SCREEN_INVERT", "params": {"duration": 200}})
            log_info(f"Glitch triggered by help-seeking behavior: {title}", "GLITCH")

        # 3. Subtle Warning (Normal switching)
        elif any(term in title for term in ["browser", "chrome", "edge", "settings", "ayarlar"]):
            if random.random() < 0.2: # 20% chance
                self.dispatcher.dispatch({"action": "GDI_FLASH"})
                log_info(f"Subtle glitch triggered by window change: {title}", "GLITCH")

    def _on_user_activity(self, event_type, data):
        """Trigger a flicker if the user is moving mouse too fast/hesitantly."""
        # Simple probability based reaction
        if random.random() < 0.05: # Rare subtle flicker
            self.dispatcher.dispatch({"action": "BRIGHTNESS_FLICKER", "params": {"times": 1}})

    def _on_anger_escalated(self, event_type, data):
        """Trigger more aggressive visuals when AI gets angrier."""
        level = data.get("level", 0)
        if level > 80:
            if random.random() < 0.3:
                self.dispatcher.dispatch({"action": "SCREEN_INVERT", "params": {"duration": 150}})
