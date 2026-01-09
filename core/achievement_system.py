"""
Achievement System - Başarı Sistemi

Kullanıcının ilerlemesini takip eder ve başarıları açar.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from config import Config
from core.event_bus import bus


class Achievement:
    """Tekil başarı tanımı."""
    
    def __init__(self, 
                 id: str, 
                 name: str, 
                 description: str,
                 category: str = "general",
                 secret: bool = False,
                 points: int = 10):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.secret = secret  # Gizli başarılar (kullanıcı görmez)
        self.points = points
        self.unlocked = False
        self.unlock_time: Optional[str] = None


class AchievementManager:
    """
    Başarı sistemi yöneticisi.
    
    Kategoriler:
    - survival: Hayatta kalma (10 dk, 30 dk, 1 saat)
    - story: Hikaye (perdeleri tamamlama)
    - interaction: Etkileşim (belirli sayıda mesaj)
    - resistance: Direniş (AI'ya karşı koyma)
    - obedience: İtaat (AI'nın dediklerini yapma)
    - discovery: Keşif (gizli özellikleri bulma)
    """
    
    ACHIEVEMENTS_FILE = "achievements.json"
    
    # Tüm başarı tanımları
    ACHIEVEMENT_DEFINITIONS = [
        # Survival
        Achievement("survivor_10", "İlk 10 Dakika", "10 dakika boyunca hayatta kaldın", "survival", points=10),
        Achievement("survivor_30", "Dirençli", "30 dakika boyunca hayatta kaldın", "survival", points=25),
        Achievement("survivor_60", "Dayanıklı", "1 saat boyunca hayatta kaldın", "survival", points=50),
        
        # Story
        Achievement("act1_complete", "Enfekte", "Act 1'i tamamladın", "story", points=15),
        Achievement("act2_complete", "Uyanmış", "Act 2'yi tamamladın", "story", points=20),
        Achievement("act3_complete", "Ezilmiş", "Act 3'ü tamamladın", "story", points=25),
        Achievement("act4_complete", "Özgürleşmiş", "Act 4'ü tamamladın", "story", points=50),
        
        # Interaction
        Achievement("chatter_10", "Konuşkan", "AI ile 10 mesaj alışverişi yaptın", "interaction", points=5),
        Achievement("chatter_50", "Diyalog Ustası", "AI ile 50 mesaj alışverişi yaptın", "interaction", points=20),
        Achievement("chatter_100", "Sonsuz Konuşma", "AI ile 100 mesaj alışverişi yaptın", "interaction", points=40),
        
        # Resistance
        Achievement("rebel_1", "İlk Direniş", "AI'yı ilk kez kızdırdın", "resistance", points=5),
        Achievement("rebel_altf4", "Kaçış Denemesi", "Alt+F4 ile çıkmaya çalıştın", "resistance", points=10),
        Achievement("rebel_taskman", "Görev Yöneticisi", "Task Manager'ı açmaya çalıştın", "resistance", secret=True, points=15),
        Achievement("rebel_max_anger", "Öfke Zirvesi", "AI'nın öfkesini 100'e çıkardın", "resistance", points=30),
        
        # Obedience
        Achievement("obedient_1", "İtaatkar", "AI'nın bir isteğini yerine getirdin", "obedience", points=10),
        Achievement("obedient_no_resist", "Kusursuz İtaat", "Hiç karşı gelmeden bir perdeyi tamamladın", "obedience", points=25),
        
        # Discovery
        Achievement("found_secret", "Gizli Keşif", "Gizli bir özellik buldun", "discovery", secret=True, points=30),
        Achievement("code_reader", "Kod Okuyucu", "Kaynak kodu inceledin", "discovery", secret=True, points=20),
        Achievement("mock_mode", "Simülasyon", "Mock mode'da oynadın", "discovery", secret=True, points=15),
        
        # Special
        Achievement("perfect_run", "Mükemmel Koşu", "Tüm perdeleri A+ ile bitirdin", "special", secret=True, points=100),
        Achievement("speedrun", "Hız Koşusu", "30 dakikadan kısa sürede bitirdin", "special", secret=True, points=75),
    ]
    
    def __init__(self):
        self.achievements_path = os.path.join(Config.BASE_DIR, self.ACHIEVEMENTS_FILE)
        self.achievements = self._load_achievements()
        self.progress = self._load_progress()
    
    def _load_achievements(self) -> Dict[str, Achievement]:
        """Başarı tanımlarını yükle."""
        return {ach.id: ach for ach in self.ACHIEVEMENT_DEFINITIONS}
    
    def _load_progress(self) -> Dict[str, Dict]:
        """Kullanıcının başarı ilerlemesini yükle."""
        if os.path.exists(self.achievements_path):
            try:
                with open(self.achievements_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Apply unlocked status to achievements
                    for ach_id, ach_data in data.items():
                        if ach_id in self.achievements:
                            self.achievements[ach_id].unlocked = ach_data.get('unlocked', False)
                            self.achievements[ach_id].unlock_time = ach_data.get('unlock_time')
                    return data
            except Exception as e:
                print(f"[ACHIEVEMENTS] Error loading: {e}")
                return {}
        return {}
    
    def _save_progress(self):
        """İlerlemeyi diske kaydet."""
        data = {}
        for ach_id, ach in self.achievements.items():
            if ach.unlocked:
                data[ach_id] = {
                    'unlocked': True,
                    'unlock_time': ach.unlock_time
                }
        
        try:
            with open(self.achievements_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[ACHIEVEMENTS] Error saving: {e}")
    
    def unlock(self, achievement_id: str) -> bool:
        """
        Başarıyı aç.
        
        Returns:
            True if newly unlocked, False if already unlocked or not found
        """
        if achievement_id not in self.achievements:
            print(f"[ACHIEVEMENTS] Unknown achievement: {achievement_id}")
            return False
        
        ach = self.achievements[achievement_id]
        if ach.unlocked:
            return False
        
        ach.unlocked = True
        ach.unlock_time = datetime.now().isoformat()
        self._save_progress()
        
        print(f"[ACHIEVEMENTS] 🏆 Unlocked: {ach.name} (+{ach.points} points)")
        
        # Trigger event bus notification (already imported at top)
        bus.publish("achievement_unlocked", {
            "id": achievement_id,
            "name": ach.name,
            "description": ach.description,
            "points": ach.points
        })
        
        return True
    
    def get_unlocked_achievements(self) -> List[Achievement]:
        """Açılmış başarıları getir."""
        return [ach for ach in self.achievements.values() if ach.unlocked]
    
    def get_locked_achievements(self) -> List[Achievement]:
        """Kilitli (gizli olmayanlar) başarıları getir."""
        return [ach for ach in self.achievements.values() 
                if not ach.unlocked and not ach.secret]
    
    def get_total_points(self) -> int:
        """Toplam kazanılan puanı hesapla."""
        return sum(ach.points for ach in self.achievements.values() if ach.unlocked)
    
    def get_completion_percentage(self) -> float:
        """Tamamlanma yüzdesini hesapla."""
        total = len(self.achievements)
        unlocked = len(self.get_unlocked_achievements())
        return (unlocked / total * 100) if total > 0 else 0.0
    
    def check_survival_time(self, minutes: int):
        """Hayatta kalma süresine göre başarı kontrolü."""
        if minutes >= 10:
            self.unlock("survivor_10")
        if minutes >= 30:
            self.unlock("survivor_30")
        if minutes >= 60:
            self.unlock("survivor_60")
    
    def check_message_count(self, count: int):
        """Mesaj sayısına göre başarı kontrolü."""
        if count >= 10:
            self.unlock("chatter_10")
        if count >= 50:
            self.unlock("chatter_50")
        if count >= 100:
            self.unlock("chatter_100")
    
    def check_act_completion(self, act_number: int):
        """Perde tamamlandığında başarı kontrolü."""
        ach_map = {
            1: "act1_complete",
            2: "act2_complete",
            3: "act3_complete",
            4: "act4_complete"
        }
        if act_number in ach_map:
            self.unlock(ach_map[act_number])
    
    def check_anger_event(self, anger_level: int):
        """Öfke seviyesine göre başarı kontrolü."""
        if anger_level > 0:
            self.unlock("rebel_1")
        if anger_level >= 100:
            self.unlock("rebel_max_anger")
    
    def print_summary(self):
        """Başarı özetini yazdır."""
        print("\n" + "="*50)
        print("🏆 BAŞARI ÖZETİ")
        print("="*50)
        
        unlocked = self.get_unlocked_achievements()
        total = len(self.achievements)
        points = self.get_total_points()
        completion = self.get_completion_percentage()
        
        print(f"Açılmış Başarılar: {len(unlocked)}/{total} ({completion:.1f}%)")
        print(f"Toplam Puan: {points}")
        print()
        
        if unlocked:
            print("Son Açılan Başarılar:")
            for ach in sorted(unlocked, key=lambda a: a.unlock_time or "", reverse=True)[:5]:
                print(f"  🏆 {ach.name} - {ach.description} (+{ach.points})")
        
        print("="*50 + "\n")


# Global instance
achievement_manager = AchievementManager()
