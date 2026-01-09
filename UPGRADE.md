# Upgrade Guide - Yükseltme Rehberi

## v4.0 → v4.1 Yükseltme

### Yeni Özellikler

#### 1. Settings System (Ayarlar Sistemi)
Artık kullanıcı ayarları `user_settings.json` dosyasında saklanıyor.

**İlk Çalıştırma:**
```bash
python settings_cli.py
```

**Programatik Kullanım:**
```python
from core.settings_manager import settings

# Ayar okuma
difficulty = settings.get("difficulty")
volume = settings.get("audio_volume")

# Ayar değiştirme
settings.set("difficulty", "hard")
settings.set("audio_volume", 0.8)

# Config'e uygulama (kernel başlangıcında)
settings.apply_to_config()
```

#### 2. Achievement System (Başarı Sistemi)
Kullanıcı ilerlemesi ve başarılar artık takip ediliyor.

**Başarıları Görüntüleme:**
```bash
python settings_cli.py
# Menüden "7. Başarıları Görüntüle" seçin
```

**Kod İçinde Kullanım:**
```python
from core.achievement_system import achievement_manager

# Başarı açma
achievement_manager.unlock("survivor_10")

# İlerleme kontrolü
achievement_manager.check_survival_time(30)  # 30 dakika
achievement_manager.check_message_count(50)  # 50 mesaj
achievement_manager.check_act_completion(2)  # Act 2 tamamlandı

# Özet
achievement_manager.print_summary()
```

**Otomatik Entegrasyon:**
Kernel'a achievement entegrasyonunu eklemek için:
```python
# core/kernel.py içinde
from core.achievement_integration import initialize_achievements

def _complete_boot(self):
    # ... mevcut kod ...
    
    # Achievement sistemi başlat
    self.achievement_integration = initialize_achievements(self.memory)
```

#### 3. Diagnostic Tool (Tanılama Aracı)
Sistem durumunu kontrol etmek için:
```bash
python diagnostic.py
```

### Yeni Dosyalar
Aşağıdaki dosyalar eklendi:
- `README.md` - Proje dokümantasyonu
- `CONTRIBUTING.md` - Katkı rehberi
- `ARCHITECTURE.md` - Mimari dokümantasyon
- `CHANGELOG.md` - Değişiklik günlüğü
- `core/settings_manager.py` - Ayarlar sistemi
- `core/achievement_system.py` - Başarı sistemi
- `core/achievement_integration.py` - Başarı entegrasyonu
- `settings_cli.py` - CLI ayarlar aracı
- `diagnostic.py` - Tanılama aracı
- `.pre-commit-config.yaml` - Pre-commit hooks

### Breaking Changes (Kırılma Değişiklikleri)
**YOK** - Bu sürüm tamamen geriye uyumludur.

### Önerilen Değişiklikler

#### Kernel Entegrasyonu
`core/kernel.py` dosyasını güncelleyin:

```python
# Başta import ekleyin
from core.achievement_integration import initialize_achievements

# _complete_boot metodunda
def _complete_boot(self):
    # Mevcut koddan sonra
    self.achievement_integration = initialize_achievements(self.memory)
    
    # Mock mode bildirimi
    if Config.IS_MOCK:
        from core.event_bus import bus
        bus.publish("mock_mode_active", {})

# shutdown metodunda
def shutdown(self):
    # Kapanmadan önce
    if hasattr(self, 'achievement_integration'):
        self.achievement_integration.on_shutdown()
    
    # Mevcut shutdown kodu...
```

#### Story Manager Entegrasyonu
`story/story_manager.py` dosyasını güncelleyin:

```python
# Act tamamlanınca
def _on_act_complete(self, act_number):
    from core.event_bus import bus
    bus.publish("act_completed", {"act": act_number})
    # Mevcut kod...

# Hikaye başlangıcında
def start_story(self):
    from core.event_bus import bus
    bus.publish("story_started", {})
    # Mevcut kod...
```

#### Anger Engine Entegrasyonu
`core/anger_engine.py` dosyasını güncelleyin:

```python
def calculate_anger(self, user_action_type: str) -> int:
    # Mevcut kod...
    
    # Öfke değişimini bildir
    from core.event_bus import bus
    bus.publish("anger_increased", {"level": self.current_anger})
    
    if self.current_anger >= 100:
        bus.publish("anger_maxed", {})
    
    return self.current_anger
```

### Yeni Bağımlılıklar
**YOK** - Yeni harici bağımlılık eklenmedi.

### Migration Checklist

- [ ] Yeni dosyaları pull/merge et
- [ ] `python diagnostic.py` çalıştır - sistem sağlığını kontrol et
- [ ] `python settings_cli.py` çalıştır - ayarları yapılandır
- [ ] (Opsiyonel) Kernel'a achievement entegrasyonu ekle
- [ ] (Opsiyonel) Story manager'a event emission ekle
- [ ] (Opsiyonel) Anger engine'e event emission ekle
- [ ] `python main.py` ile test et
- [ ] Pre-commit hooks kurmak istiyorsan:
  ```bash
  pip install pre-commit
  pre-commit install
  ```

### Sorun Giderme

**Soru:** Settings dosyası nerede?
**Cevap:** `user_settings.json` proje kök dizininde oluşturulur.

**Soru:** Achievements çalışmıyor?
**Cevap:** Event bus entegrasyonu gerekiyor. Yukarıdaki kernel entegrasyonunu ekleyin.

**Soru:** Eski ayarlarım ne olacak?
**Cevap:** Eski `config.py` ayarları korunur. Yeni settings sistemi ilave seçenekler sunar.

**Soru:** Diagnostic tool hata veriyor?
**Cevap:** Gerekli dizinlerin oluşturulduğundan emin olun:
```bash
mkdir -p logs cache locales
```

### Sonraki Adımlar (v4.2.0)
- GUI settings manager (PyQt6)
- Multi-language support (English translations)
- Performance monitoring
- Plugin system
- Cloud sync

---

**Destek:** Sorun yaşarsanız [GitHub Issues](https://github.com/qanteSm/SENTIENT_OS/issues) açın.
