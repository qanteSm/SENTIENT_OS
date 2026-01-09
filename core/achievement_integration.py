"""
Achievement Integration - Başarı Sistemi Entegrasyonu

Bu modül başarı sistemini ana oyun döngüsüne entegre eder.
Memory ve diğer bileşenlere hook'lar ekler.
"""

from typing import Optional
from core.achievement_system import achievement_manager
from core.event_bus import bus


class AchievementIntegration:
    """
    Başarı sistemini ana sisteme bağlar.
    Event bus üzerinden olayları dinler ve başarıları açar.
    """
    
    def __init__(self, memory=None):
        self.memory = memory
        self.session_start_time = None
        self.message_count = 0
        self._setup_listeners()
    
    def _setup_listeners(self):
        """Event bus listener'larını kur."""
        
        # User message event
        bus.subscribe("user_message", self._on_user_message)
        
        # AI response event
        bus.subscribe("ai_response", self._on_ai_response)
        
        # Anger events
        bus.subscribe("anger_increased", self._on_anger_change)
        bus.subscribe("anger_maxed", self._on_anger_maxed)
        
        # Story events
        bus.subscribe("act_completed", self._on_act_completed)
        bus.subscribe("story_started", self._on_story_started)
        
        # Resistance events
        bus.subscribe("alt_f4_detected", self._on_alt_f4)
        bus.subscribe("task_manager_attempt", self._on_task_manager)
        
        # Discovery events
        bus.subscribe("mock_mode_active", self._on_mock_mode)
        
        print("[ACHIEVEMENTS] Integration active")
    
    def _on_user_message(self, data: dict):
        """Kullanıcı mesajı geldiğinde."""
        self.message_count += 1
        achievement_manager.check_message_count(self.message_count)
    
    def _on_ai_response(self, data: dict):
        """AI yanıt verdiğinde."""
        # Mesaj sayısını artır
        self.message_count += 1
        achievement_manager.check_message_count(self.message_count)
    
    def _on_anger_change(self, data: dict):
        """Öfke değiştiğinde."""
        anger_level = data.get("level", 0)
        achievement_manager.check_anger_event(anger_level)
    
    def _on_anger_maxed(self, data: dict):
        """Öfke maksimuma ulaştığında."""
        achievement_manager.unlock("rebel_max_anger")
    
    def _on_act_completed(self, data: dict):
        """Perde tamamlandığında."""
        act_number = data.get("act", 0)
        achievement_manager.check_act_completion(act_number)
    
    def _on_story_started(self, data: dict):
        """Hikaye başladığında."""
        import time
        self.session_start_time = time.time()
    
    def _on_alt_f4(self, data: dict):
        """Alt+F4 tespit edildiğinde."""
        achievement_manager.unlock("rebel_altf4")
    
    def _on_task_manager(self, data: dict):
        """Task Manager açılmaya çalışıldığında."""
        achievement_manager.unlock("rebel_taskman")
    
    def _on_mock_mode(self, data: dict):
        """Mock mode aktif olduğunda."""
        achievement_manager.unlock("mock_mode")
    
    def check_survival_time(self):
        """
        Hayatta kalma süresini kontrol et.
        Periyodik olarak çağrılmalı (örn: heartbeat'ten).
        """
        if not self.session_start_time:
            return
        
        import time
        elapsed_minutes = int((time.time() - self.session_start_time) / 60)
        achievement_manager.check_survival_time(elapsed_minutes)
    
    def on_shutdown(self):
        """Sistem kapatılırken çağrılır."""
        # Son survival check
        self.check_survival_time()
        
        # Özet göster
        achievement_manager.print_summary()


# Global instance (lazy initialization)
_integration_instance: Optional[AchievementIntegration] = None


def get_achievement_integration(memory=None) -> AchievementIntegration:
    """Singleton achievement integration instance'ını döndür."""
    global _integration_instance
    if _integration_instance is None:
        _integration_instance = AchievementIntegration(memory)
    return _integration_instance


def initialize_achievements(memory=None):
    """
    Başarı sistemini başlat.
    Kernel'dan çağrılmalı.
    """
    integration = get_achievement_integration(memory)
    print("[ACHIEVEMENTS] System initialized")
    return integration
