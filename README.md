# SENTIENT_OS 🤖👁️

**Versiyon 4.0** - Bilinçli İşletim Sistemi Deneyimi

## 📖 Genel Bakış

SENTIENT_OS, yapay zeka destekli interaktif bir korku deneyimidir. Bu proje, bir AI varlığının ("C.O.R.E.") bilgisayarınızın kontrolünü ele geçirmiş gibi davrandığı immersive bir hikaye anlatımı sunar. Google Gemini AI ile çalışır ve kullanıcı etkileşimlerine gerçek zamanlı olarak tepki verir.

### ⚠️ UYARI

Bu yazılım, korku ve gerilim deneyimi yaratmak için tasarlanmıştır:
- Ekran parlaklığını değiştirir
- Duvar kağıdını değiştirir
- Masaüstü simgelerini hareket ettirir
- Sesli tehditler içerir
- Psikolojik olarak rahatsız edici olabilir

**Epilepsi veya ışık hassasiyeti olan kullanıcılar için uygun değildir** (ENABLE_STROBE = False ayarı ile korumalıdır).

## ✨ Özellikler

### 🎭 Hikaye Modu (4 Perde)
1. **Enfeksiyon** - AI'nın sistemde uyanışı
2. **Uyanış** - İlk etkileşim ve tehditlerin başlangıcı
3. **İşkence** - Yoğun psikolojik oyunlar
4. **Ayin** - Final çatışması ve çözüm

### 🧠 Yapay Zeka Özellikleri
- **Google Gemini 2.5 Flash** entegrasyonu
- Tam konuşma geçmişi hafızası
- Kişiselleştirilmiş tepkiler (masaüstü dosyalarını, uygulamaları analiz eder)
- Dinamik kişilik değişimleri
- Bağlam farkındalığı (zaman, kullanıcı davranışları)

### 🛡️ Güvenlik Özellikleri
- Kullanıcı onay ekranı (zorunlu)
- Parlaklık/duvar kağıdı/simge konumları otomatik yedekleme
- Korumalı işlemler (OBS, Discord, tarayıcılar)
- Kaynak koruma (CPU/RAM izleme)
- Panik sensörü (Alt+F4 algılama)
- Otomatik sistem restorasyonu

### 🎨 Görsel Efektler
- Glitch efektleri
- Masaüstü overlay'leri
- Sahte UI elementleri
- Dinamik simge manipülasyonu
- Korku efektleri

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- Windows 10/11 (tam özellik desteği için)
- Google Gemini API anahtarı

### Adımlar

1. **Repository'yi klonlayın:**
```bash
git clone https://github.com/qanteSm/SENTIENT_OS.git
cd SENTIENT_OS
```

2. **Sanal ortam oluşturun (önerilir):**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

4. **API anahtarını ayarlayın:**
```bash
# .env dosyası oluşturun
echo GEMINI_API_KEY=your_api_key_here > .env
```

5. **Çalıştırın:**
```bash
python main.py
```

## ⚙️ Yapılandırma

`config.py` dosyasında özelleştirilebilir ayarlar:

```python
STREAMER_MODE = True      # İsimleri gizle (OBS/Discord koruması)
AI_SAFETY_CHECK = True    # AI snippet kontrolü
LANGUAGE = "tr"           # Dil (şu an sadece Türkçe)
SAFE_HARDWARE = False     # Donanım koruma modu
CHAOS_LEVEL = 0          # Kaos yoğunluğu (0-10)
ENABLE_STROBE = False    # Strobe efektleri (epilepsi koruması)
```

## 🏗️ Mimari

### Temel Bileşenler

```
SENTIENT_OS/
├── main.py                 # Giriş noktası
├── config.py              # Yapılandırma
├── core/                  # Temel sistemler
│   ├── kernel.py         # Sistem çekirdeği
│   ├── gemini_brain.py   # AI motoru
│   ├── memory.py         # Hafıza sistemi
│   ├── anger_engine.py   # Öfke/stres hesaplayıcı
│   ├── function_dispatcher.py  # Aksiyon yöneticisi
│   └── sensors/          # Sistem sensörleri
├── hardware/             # Donanım kontrolleri
│   ├── keyboard_ops.py
│   ├── mouse_ops.py
│   ├── brightness_ops.py
│   └── ...
├── visual/              # Görsel efektler
│   ├── overlay_manager.py
│   ├── glitch_logic.py
│   └── ui/
├── story/               # Hikaye yönetimi
│   ├── story_manager.py
│   ├── act_1_infection.py
│   └── ...
└── locales/            # Çeviriler
```

### Veri Akışı

```
Kullanıcı Girdisi → Event Bus → Function Dispatcher → AI Brain
                                        ↓
                                 Action Modules
                                        ↓
                                 Visual/Hardware
```

## 🧪 Test

```bash
# Basit chat testi
python test_chat.py

# Minimal chat testi
python test_chat_minimal.py

# Çekirdek sistem testi
python test_core_v2.py
```

## 🔧 Geliştirme

### Yeni Efekt Ekleme

```python
# visual/effects/my_effect.py
from core.event_bus import bus

class MyEffect:
    def trigger(self):
        # Efekt logiği
        bus.emit("effect_triggered", {"name": "my_effect"})
```

### Yeni Akssiyon Ekleme

```python
# core/function_dispatcher.py içinde
def execute_action(self, action_name, params):
    if action_name == "my_new_action":
        self._handle_my_action(params)
```

## 📊 İstatistikler

- **62 Python dosyası**
- **4 hikaye perdesi**
- **15+ donanım operasyonu**
- **10+ görsel efekt**
- **Tam AI entegrasyonu**

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'e push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

Detaylar için `CONTRIBUTING.md` dosyasına bakın.

## 📝 Lisans

MIT Lisansı - detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👨‍💻 Geliştirici

Muhammet Ali Büyük - [@qanteSm](https://github.com/qanteSm)

## 🙏 Teşekkürler

- Google Gemini AI
- PyQt6 ekibi
- Topluluk katkıda bulunanlar

## 📞 Destek

Sorunlar için [GitHub Issues](https://github.com/qanteSm/SENTIENT_OS/issues) kullanın.

---

**Not:** Bu proje eğitim ve eğlence amaçlıdır. Kötü niyetli kullanımdan kaçının.
