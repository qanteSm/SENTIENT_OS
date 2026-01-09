"""
Settings Manager - Yapılandırma Yönetimi

Bu modül kullanıcı tercihlerini kaydetmek ve yüklemek için kullanılır.
Config.py'den statik ayarları okur, ancak runtime'da değişebilir tercihleri yönetir.
"""

import json
import os
import copy
from typing import Dict, Any, Optional
from config import Config


class SettingsManager:
    """
    Kullanıcı tercihlerini yönetir ve kaydeder.
    
    Ayarlar:
    - Zorluk seviyesi
    - Ses şiddeti
    - Efekt yoğunluğu
    - Dil tercihi
    - Erişilebilirlik seçenekleri
    """
    
    SETTINGS_FILE = "user_settings.json"
    
    DEFAULT_SETTINGS = {
        "difficulty": "normal",  # easy, normal, hard, extreme
        "audio_volume": 0.7,  # 0.0 - 1.0
        "effect_intensity": 1.0,  # 0.5 - 2.0
        "language": "tr",  # tr, en
        "accessibility": {
            "disable_strobe": True,  # Epilepsi koruması
            "high_contrast": False,  # Yüksek kontrast mod
            "slow_motion": False,  # Yavaş mod (daha fazla reaksiyon süresi)
            "subtitles": True,  # Sesli konuşmalar için altyazı
        },
        "privacy": {
            "streamer_mode": True,  # İsimleri ve hassas bilgileri gizle
            "analytics": False,  # Anonim kullanım istatistikleri
        },
        "advanced": {
            "safe_hardware": False,  # Donanım koruma modu
            "chaos_level": 0,  # 0-10, yüksek = daha kaotik
            "mock_mode": Config.IS_MOCK,  # Test modu
        }
    }
    
    def __init__(self):
        self.settings_path = os.path.join(Config.BASE_DIR, self.SETTINGS_FILE)
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Kaydedilmiş ayarları yükler veya varsayılanları kullanır."""
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    # Merge with defaults to handle new settings
                    merged = self._deep_merge(self.DEFAULT_SETTINGS.copy(), saved_settings)
                    print(f"[SETTINGS] Loaded from {self.settings_path}")
                    return merged
            except Exception as e:
                print(f"[SETTINGS] Error loading settings: {e}. Using defaults.")
                return copy.deepcopy(self.DEFAULT_SETTINGS)
        else:
            print("[SETTINGS] No saved settings found. Using defaults.")
            return copy.deepcopy(self.DEFAULT_SETTINGS)
    
    def save_settings(self) -> bool:
        """Mevcut ayarları diske kaydeder."""
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            print(f"[SETTINGS] Saved to {self.settings_path}")
            return True
        except Exception as e:
            print(f"[SETTINGS] Error saving settings: {e}")
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Ayar değerini getirir. Noktalı yol kullanılabilir.
        
        Örnek:
            get("difficulty") -> "normal"
            get("accessibility.disable_strobe") -> True
        """
        keys = key_path.split('.')
        value = self.settings
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any) -> bool:
        """
        Ayar değerini değiştirir. Noktalı yol kullanılabilir.
        
        Örnek:
            set("difficulty", "hard")
            set("accessibility.disable_strobe", False)
        """
        keys = key_path.split('.')
        current = self.settings
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set the value
        current[keys[-1]] = value
        return self.save_settings()
    
    def reset_to_defaults(self) -> bool:
        """Tüm ayarları varsayılanlara döndürür."""
        self.settings = copy.deepcopy(self.DEFAULT_SETTINGS)
        return self.save_settings()
    
    def get_difficulty_multiplier(self) -> float:
        """
        Zorluk seviyesine göre efekt çarpanı döndürür.
        
        Returns:
            0.5 (easy) - 2.0 (extreme)
        """
        difficulty_map = {
            "easy": 0.5,
            "normal": 1.0,
            "hard": 1.5,
            "extreme": 2.0
        }
        return difficulty_map.get(self.get("difficulty", "normal"), 1.0)
    
    def apply_to_config(self):
        """Bazı ayarları Config modülüne uygular (runtime değişiklik)."""
        Config.ENABLE_STROBE = not self.get("accessibility.disable_strobe", True)
        Config.STREAMER_MODE = self.get("privacy.streamer_mode", True)
        Config.SAFE_HARDWARE = self.get("advanced.safe_hardware", False)
        Config.CHAOS_LEVEL = self.get("advanced.chaos_level", 0)
        Config.LANGUAGE = self.get("language", "tr")
        
        print("[SETTINGS] Applied to Config:")
        print(f"  - Strobe effects: {Config.ENABLE_STROBE}")
        print(f"  - Streamer mode: {Config.STREAMER_MODE}")
        print(f"  - Safe hardware: {Config.SAFE_HARDWARE}")
        print(f"  - Chaos level: {Config.CHAOS_LEVEL}")
        print(f"  - Language: {Config.LANGUAGE}")
    
    @staticmethod
    def _deep_merge(base: Dict, updates: Dict) -> Dict:
        """İki dictionary'yi derin birleştirme (yeni anahtarları ekle)."""
        result = base.copy()
        for key, value in updates.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = SettingsManager._deep_merge(result[key], value)
            else:
                result[key] = value
        return result


# Global instance
settings = SettingsManager()


# Convenience functions
def get_setting(key: str, default: Any = None) -> Any:
    """Kısa yol: ayar getir"""
    return settings.get(key, default)


def set_setting(key: str, value: Any) -> bool:
    """Kısa yol: ayar değiştir"""
    return settings.set(key, value)
