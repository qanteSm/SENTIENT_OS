# SENTIENT_OS 🤖👁️

**Versiyon 4.1** - Bilinçli İşletim Sistemi Deneyimi

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey.svg)]()

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

### 🏆 Yeni! (v4.1)
- **Başarı Sistemi** - 20+ başarı ile ilerleme takibi
- **Ayarlar Yöneticisi** - Zorluk, ses, erişilebilirlik ayarları
- **Tanılama Aracı** - Sistem sağlık kontrolü
- **Hızlı Başlangıç** - Otomatik kurulum scripti

## 🚀 Kurulum

### Hızlı Kurulum (Önerilir - Yeni Kullanıcılar)

```bash
git clone https://github.com/qanteSm/SENTIENT_OS.git
cd SENTIENT_OS
python quickstart.py
```

Bu script tüm kurulum adımlarını otomatik yapar ve programı başlatır.

### Manuel Kurulum

### Gereksinimler
- Python 3.8+
- Windows 10/11 (tam özellik desteği için)
- Google Gemini API anahtarı (opsiyonel)

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

4. **API anahtarını ayarlayın (opsiyonel):**
```bash
# .env dosyası oluşturun
echo GEMINI_API_KEY=your_api_key_here > .env
```

5. **Sistem durumunu kontrol edin:**
```bash
python diagnostic.py
```

6. **Çalıştırın:**
```bash
python main.py
```

## 🛠️ Araçlar ve Komutlar

```bash
# Ana program
python main.py              # SENTIENT_OS'i başlat

# Yardımcı araçlar
python quickstart.py        # Hızlı kurulum ve başlatma
python diagnostic.py        # Sistem sağlığı kontrolü
python settings_cli.py      # Ayarları yönet
python test_chat.py         # Chat sistemini test et

# Geliştirici araçları
python tools/reset_memory.py    # Hafızayı sıfırla
python verify_enhancements.py   # Geliştirmeleri doğrula
```

## ⚙️ Yapılandırma

### CLI Ayarlar Yöneticisi (Önerilir)

```bash
python settings_cli.py
```

İnteraktif menüden tüm ayarları yönetebilirsiniz:
- Zorluk seviyesi (Kolay/Normal/Zor/Extreme)
- Ses şiddeti
- Erişilebilirlik seçenekleri
- Gizlilik ayarları
- Gelişmiş ayarlar

### Manuel Yapılandırma

`config.py` dosyasında özelleştirilebilir ayarlar:

```python
STREAMER_MODE = True      # İsimleri gizle (OBS/Discord koruması)
AI_SAFETY_CHECK = True    # AI snippet kontrolü
LANGUAGE = "tr"           # Dil (şu an sadece Türkçe)
SAFE_HARDWARE = False     # Donanım koruma modu
CHAOS_LEVEL = 0          # Kaos yoğunluğu (0-10)
ENABLE_STROBE = False    # Strobe efektleri (epilepsi koruması)
```

## 🏆 Başarı Sistemi

SENTIENT_OS'de ilerlemenizi takip eden 20+ başarı bulunur:

**Kategoriler:**
- 🎮 Hayatta Kalma (10dk, 30dk, 1 saat)
- 📖 Hikaye (Perdeleri tamamlama)
- 💬 Etkileşim (Mesaj sayısı)
- ⚡ Direniş (AI'ya karşı koyma)
- 🤝 İtaat (AI'nın isteklerini yerine getirme)
- 🔍 Keşif (Gizli özellikleri bulma)

**Başarıları görüntüle:**
```bash
python settings_cli.py  # Menüden "7. Başarıları Görüntüle"
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

- **70+ Python dosyası**
- **4 hikaye perdesi**
- **15+ donanım operasyonu**
- **10+ görsel efekt**
- **20+ başarı**
- **Tam AI entegrasyonu**

## 📚 Dokümantasyon

- **[README.md](README.md)** - Genel bakış ve kurulum
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Katkıda bulunma rehberi
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Teknik mimari
- **[CHANGELOG.md](CHANGELOG.md)** - Versiyon geçmişi
- **[UPGRADE.md](UPGRADE.md)** - Yükseltme rehberi
- **[FAQ.md](FAQ.md)** - Sıkça sorulan sorular
- **[docs/PLUGIN_SYSTEM.md](docs/PLUGIN_SYSTEM.md)** - Plugin sistemi tasarımı

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'e push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

**Önerilen:**
- Pre-commit hooks kurun: `pip install pre-commit && pre-commit install`
- [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını okuyun

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
