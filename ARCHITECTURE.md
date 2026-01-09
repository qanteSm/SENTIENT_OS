# SENTIENT_OS Mimari Dokümantasyonu

## 📐 Sistem Mimarisi

### Genel Bakış

SENTIENT_OS, modüler ve olay-tabanlı (event-driven) bir mimari kullanır. Sistem, merkezi bir çekirdek (kernel) etrafında organize edilmiş bağımsız bileşenlerden oluşur.

```
┌─────────────────────────────────────────────────┐
│                  SentientKernel                  │
│         (Merkezi Koordinasyon Birimi)            │
└─────────────────────────────────────────────────┘
           │                │                │
           ▼                ▼                ▼
    ┌──────────┐     ┌──────────┐     ┌──────────┐
    │  Core    │     │ Hardware │     │  Visual  │
    │ Systems  │     │ Controls │     │ Effects  │
    └──────────┘     └──────────┘     └──────────┘
           │                │                │
           └────────────────┴────────────────┘
                          │
                   ┌──────▼───────┐
                   │  Event Bus   │
                   │ (Merkezi Hub)│
                   └──────────────┘
```

## 🧩 Ana Bileşenler

### 1. Kernel (Çekirdek)
**Dosya:** `core/kernel.py`

Sistemin kalbidir. Tüm bileşenleri başlatır ve yaşam döngüsünü yönetir.

**Sorumluluklar:**
- Uygulama başlatma (boot)
- Bileşen yaşam döngüsü yönetimi
- Onay ekranı koordinasyonu
- Kapanış ve temizlik işlemleri

**Önemli Metodlar:**
```python
def boot(self):
    """Sistemi başlatır, onay ekranını gösterir"""
    
def _complete_boot(self):
    """Onay sonrası tam başlatma"""
    
def shutdown(self):
    """Güvenli kapatma ve geri yükleme"""
```

### 2. Event Bus (Olay Yolu)
**Dosya:** `core/event_bus.py`

Bileşenler arası iletişim için merkezi mesajlaşma sistemi.

**Tasarım Deseni:** Observer Pattern

**Kullanım:**
```python
from core.event_bus import bus

# Dinleyici kaydetme
bus.on("user_message", self.handle_message)

# Olay yayınlama
bus.emit("ai_response", {"text": "Merhaba", "anger": 50})

# Dinleyici kaldırma
bus.off("user_message", self.handle_message)
```

**Olay Kategorileri:**
- `user_*` - Kullanıcı eylemleri
- `ai_*` - AI yanıtları ve durumları
- `system_*` - Sistem olayları
- `hardware_*` - Donanım değişiklikleri
- `visual_*` - Görsel efektler

### 3. AI Brain (Gemini Entegrasyonu)
**Dosya:** `core/gemini_brain.py`

Google Gemini API ile iletişim ve AI kişiliği yönetimi.

**Özellikler:**
- Asenkron API çağrıları
- Konuşma geçmişi yönetimi
- Bağlam toplama (ContextObserver)
- Mock mode (API olmadan test)
- Kişilik sistemleri (ENTITY, SUPPORT)

**Akış:**
```
Kullanıcı Mesajı
      ↓
Context Observer → Desktop analizi
      ↓
Prompt Oluşturma → Geçmiş + Bağlam + Persona
      ↓
Gemini API Çağrısı
      ↓
JSON Yanıt Parsing
      ↓
Action Dispatcher
```

**API Formatı:**
```json
{
  "speech": "Kullanıcıya söylenen metin",
  "mood": "aggressive|whispering|fake_friendly|glitching|child",
  "actions": [
    {
      "name": "action_name",
      "params": {"key": "value"}
    }
  ],
  "anger_change": 10
}
```

### 4. Function Dispatcher (Aksiyon Yöneticisi)
**Dosya:** `core/function_dispatcher.py`

AI'dan gelen aksiyonları uygun modüllere yönlendirir.

**Sorumluluklar:**
- Aksiyon validasyonu
- Güvenlik kontrolleri (SafetyNet)
- Hız sınırlama (rate limiting)
- Hata yakalama ve loglama

**Desteklenen Aksiyonlar:**
```python
ACTIONS = {
    # Görsel
    "desktop_glitch": visual.glitch_logic,
    "show_fake_error": visual.fake_ui,
    "overlay_message": visual.overlay_manager,
    
    # Donanım
    "dim_screen": hardware.brightness_ops,
    "move_icons": visual.icon_ops,
    "change_wallpaper": hardware.wallpaper_ops,
    
    # Audio
    "play_sound": hardware.audio_out,
    "text_to_speech": hardware.audio_out,
    
    # Sistem
    "open_notepad": hardware.notepad_ops,
    "type_text": hardware.keyboard_ops,
}
```

### 5. Memory (Hafıza Sistemi)
**Dosya:** `core/memory.py`

Kalıcı veri saklama ve geçmiş yönetimi.

**Veri Yapısı:**
```python
{
    "user_name": "İsim",
    "conversations": [
        {
            "role": "user|ai",
            "text": "Mesaj",
            "timestamp": "ISO-8601",
            "anger_level": 50
        }
    ],
    "statistics": {
        "swear_count": 5,
        "alt_f4_attempts": 3,
        "obedience_count": 2
    },
    "learned_facts": {
        "desktop_files": [...],
        "favorite_app": "chrome"
    },
    "current_act": 2
}
```

**Depolama:** JSON dosyası (`brain_dump.json`)

### 6. Anger Engine (Öfke Motoru)
**Dosya:** `core/anger_engine.py`

Kullanıcı davranışlarına göre AI'nın stres seviyesini hesaplar.

**Formül:**
```
Anger = Base + Σ(Penalties) - Σ(Rewards)
Constraints: 0 ≤ Anger ≤ 100
```

**Öfke Etkisi:**
- 0-20: Normal davranış (1.0x chaos)
- 21-50: Sinirli (1.5x chaos)
- 51-80: Agresif (2.0x chaos)
- 81-100: Kontrolsüz (3.0x chaos)

### 7. Story Manager (Hikaye Yöneticisi)
**Dosya:** `story/story_manager.py`

4 perdelik hikaye akışını yönetir.

**Perde Yapısı:**
```python
class BaseAct:
    def start(self):
        """Perde başlangıcı"""
    
    def handle_user_input(self, text):
        """Kullanıcı girdisi işleme"""
    
    def check_completion(self):
        """Perde tamamlanma kontrolü"""
    
    def cleanup(self):
        """Perde sonu temizlik"""
```

**Geçiş Akışı:**
```
Act 1 (Enfeksiyon)
    ↓ [30 saniye + koşul]
Act 2 (Uyanış)
    ↓ [5 dakika + etkileşim]
Act 3 (İşkence)
    ↓ [10 dakika + kaos seviyesi]
Act 4 (Ayin - Final)
    ↓
Bitti → Geri Yükleme
```

## 🔒 Güvenlik Katmanları

### 1. Safety Net
**Dosya:** `core/safety_net.py`

**Kontroller:**
- Yasaklı aksiyonlar (fiziksel zarar)
- Korumalı işlem kontrolü (OBS, Discord)
- Strobe efekt koruması (epilepsi)
- Monitör hedefleme (OBS koruma)

### 2. Resource Guard
**Dosya:** `core/resource_guard.py`

**İzleme:**
- CPU kullanımı (>80% → uyarı)
- RAM kullanımı (>85% → uyarı)
- Disk kullanımı

### 3. Process Guard
**Dosya:** `core/process_guard.py`

Korumalı işlemleri izler ve sonlandırma girişimlerini engeller.

## 🎨 Görsel Sistem

### Overlay Manager
**Dosya:** `visual/overlay_manager.py`

PyQt6 ile şeffaf, tıklanamaz overlay'ler oluşturur.

**Katmanlar:**
```
Z-Index Sistemi:
9999: Kritik mesajlar
5000: Normal overlay'ler
1000: Arka plan efektleri
```

### Glitch Logic
**Dosya:** `visual/glitch_logic.py`

Ekran glitch efektleri:
- CRT bozulma
- Renk kaydırma
- Piksel gürültüsü
- Tarama çizgileri

### Effects System
**Klasör:** `visual/effects/`

Modüler efekt sistemi:
```python
# visual/effects/base_effect.py
class BaseEffect:
    def trigger(self, intensity=1.0):
        """Efekti tetikle"""
        
    def stop(self):
        """Efekti durdur"""
```

## 🔌 Hardware Kontrolleri

### Moduler Yapı
Her hardware operasyonu bağımsız modül:

```python
class HardwareOps:
    @staticmethod
    def safe_operation():
        """Güvenli operasyon"""
        try:
            if Config.IS_MOCK:
                return mock_operation()
            return real_operation()
        except Exception as e:
            log_error(f"Operation failed: {e}")
            return fallback()
```

### Yedekleme Sistemi
Tüm değiştirilebilir öğeler yedeklenir:
- Parlaklık → `_saved_brightness`
- Duvar kağıdı → `cache/wallpaper_backup.jpg`
- Simge pozisyonları → `cache/icon_positions.json`

## 🧪 Test Stratejisi

### Test Seviyeleri

1. **Unit Tests:** Bileşen testi
2. **Integration Tests:** Bileşen etkileşimi
3. **System Tests:** Tam sistem akışı
4. **Mock Tests:** API olmadan test

### Test Dosyaları
```
test_chat.py          # Chat UI testi
test_chat_minimal.py  # Minimal chat
test_core_v2.py       # Çekirdek sistem
```

## 📊 Performans Optimizasyonları

### 1. Asenkron İşlemler
- AI API çağrıları → Thread pool
- Dosya okuma → Async IO
- Event handling → Non-blocking

### 2. Önbellekleme
```python
# Örnek: Desktop analizi cache
last_analysis = None
last_analysis_time = 0

def get_desktop_files():
    if time.time() - last_analysis_time < 60:
        return last_analysis
    # Yeni analiz...
```

### 3. Lazy Loading
Modüller sadece kullanıldığında yüklenir:
```python
def get_glitch_effect():
    if not hasattr(self, '_glitch'):
        from visual.glitch_logic import GlitchLogic
        self._glitch = GlitchLogic()
    return self._glitch
```

## 🔄 Veri Akışı Diyagramları

### Kullanıcı Mesajı Akışı
```
[User Types Message]
        ↓
[FakeChat captures]
        ↓
[emit: user_message]
        ↓
[StoryManager receives]
        ↓
[Context gathered]
        ↓
[GeminiBrain.generate_async]
        ↓
[Gemini API call]
        ↓
[JSON response]
        ↓
[FunctionDispatcher.execute]
        ↓
[Hardware/Visual Actions]
        ↓
[FakeChat displays response]
```

### Sistem Boot Akışı
```
[main.py starts]
        ↓
[SentientKernel.boot()]
        ↓
[Qt Application init]
        ↓
[Show ConsentScreen]
        ↓
[User accepts] ──→ [User declines]
        ↓                    ↓
[_complete_boot()]      [System exit]
        ↓
[Initialize all components]
        ↓
[Load saved state]
        ↓
[Start sensors & heartbeat]
        ↓
[Begin story]
        ↓
[Main event loop]
```

## 🚀 Gelecek İyileştirmeler

### Planlanan Özellikler
1. **Plugin System:** Üçüncü parti efektler
2. **Cloud Sync:** Çoklu cihaz desteği
3. **Telemetry:** Kullanıcı deneyimi analizi
4. **VR Support:** Sanal gerçeklik entegrasyonu
5. **Multiplayer:** Çoklu kullanıcı oturumları

### Teknik Borç
- [ ] Type hints tüm fonksiyonlara
- [ ] Unit test coverage %80+
- [ ] Async/await kullanımı artırılmalı
- [ ] Kod tekrarı azaltılmalı
- [ ] Error handling iyileştirilmeli

---

**Son Güncelleme:** 2026-01-09  
**Versiyon:** 4.0
