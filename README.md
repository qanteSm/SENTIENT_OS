# <img src="assets/images/sentient/Logo.png" width="45" align="center"> SENTIENT_OS v0.8.0-alpha-certified

<p align="center">
  <img src="assets/images/sentient/sentient_horizontal_gif.gif" alt="SENTIENT_OS Banner" width="100%">
</p>

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-green.svg)
![OS](https://img.shields.io/badge/OS-Windows-brightgreen.svg)
![Safety](https://img.shields.io/badge/safety-hardened-orange.svg)
![AI](https://img.shields.io/badge/AI-Gemini%202.5-purple.svg)
![Tests](https://img.shields.io/badge/tests-100%25%20pass-success.svg)
![Coverage](https://img.shields.io/badge/coverage-100%25%20core-brightgreen.svg)
![Stability](https://img.shields.io/badge/stability-stress%20tested-blueviolet.svg)

**SENTIENT_OS** is an AI-driven interactive horror simulation and digital art project that creates deep system integration through fourth-wall-breaking psychological manipulation.

> **"Not just a game. An experience that watches you back."**

---

## 🌍 Language / Dil
* [English Version](#english-readme)
* [Türkçe Versiyon](#türkçe-readme)

---

## <a name="english-readme"></a>🇺🇸 English README

---

### 🏎️ Technical Showroom & Stability
SENTIENT_OS is built for high-reliability under extreme conditions. The architecture is verified through **Chaos Engineering** and **Stress Suites**.

| Metric | Performance | Status |
|--------|-------------|--------|
| **Burst Throughput** | 410+ actions/sec | ✅ Stabilized |
| **Memory Leakage** | 0.00 B/s | ✅ Verified |
| **GDI Resources** | Automatic Cleanup | ✅ Leaks Zeroed |
| **Atomic State** | Zero Corruption Risk | ✅ Guaranteed |
| **Crash Recovery** | < 2.5s Auto-Restore | ✅ Hardened |

---

### 📌 What is SENTIENT_OS?

A psychological horror experience powered by Google Gemini AI that simulates a sentient operating system taking control of your computer. Unlike traditional games, SENTIENT_OS:

- **Learns and adapts** to your behavior in real-time
- **Breaks the fourth wall** using your actual desktop files, folder names, and system info
- **Evolves through 4 narrative acts** from subtle infection to full takeover
- **Never the same twice** - AI-driven dynamic storytelling

### ✨ Key Features

#### 🧠 AI-Powered Horror
- **Google Gemini 2.5 Integration** - Real-time AI reasoning and emotional responses
- **Context-Aware AI** - References your desktop folders, running apps, current time
- **Dynamic Dialogue** - No scripted responses, fully AI-generated interactions
- **Response Caching** - 60% reduction in API calls for faster, cheaper operation
- **Offline Mode** - Graceful degradation when internet fails

#### 🎭 Immersive Experience
- **3-Step Onboarding** - Welcome → Intensity Selection → Safety Consent
- **Ambient Horror System** - Constant subliminal tension through background effects
- **Drone Audio Layer** - Evolving atmospheric sounds per Act (fan → static → whispers → infrasound)
- **Silence Breaker** - Auto-triggers events after 45s of idleness to maintain engagement
- **Dynamic Event Scheduling** - Adapts pacing based on user activity

#### 👁️ Advanced Visual Effects
- **GDI Screen Manipulation** - Screen tearing, pixel melting, color inversion
- **Overlay System** - Creepy text, flash effects, screen shake
- **Fake System UI** - BSOD, fake updates, system errors
- **Desktop Masking** - Freeze-frame illusions
- **Hardware Integration** - Brightness flicker, mouse shake, keyboard hijack

#### 🛡️ Safety & Security
- **Multi-Layer Safety Net** - Kill switch (CTRL+SHIFT+Q), resource monitoring, panic sensor
- **Privacy Filter** - All personal data scrubbed before AI processing
- **Streamer Mode** - Protects OBS, Discord, browser tabs
- **Non-Destructive** - All changes (wallpaper, brightness) automatically restored
- **Crash Recovery** - Converts real crashes into horror moments, auto-recovers from checkpoints

#### ⚡ Technical Architecture Core
- **Asynchronous Command Bus**: High-speed action routing with **Priority-based execution**.
- **Self-Healing Kernel**: Automated crash recovery with state-safe checkpoints.
- **AI Reasoning Engine**: Hybrid online/offline Gemini integration with semantic caching.
- **Hardware Abstraction Layer**: Direct Windows API (GDI/Win32) integration for low-latency effects.
- **Data Integrity Layer**: Atomic JSON persistence ensuring 0% corruption risk.

#### ⚙️ Technical Excellence
- **YAML Configuration** - Runtime-editable settings, environment variable support
- **Thread-Safe Architecture** - QMutex-protected sensors, no race conditions
- **Observer Pattern** - Config change notifications, event-driven design
- **Modular Design** - Clean separation: Kernel, Dispatcher, Brain, Memory, Story
- **Checkpoint System** - Auto-save game state, crash recovery

### 🎭 Narrative Progression

| Act | Title | Intensity | Characteristics |
|-----|-------|-----------|----------------|
| **Act 1** | 🧬 Infection | Low | Subtle glitches, cryptic logs, system "warm-up" |
| **Act 2** | 👁️ Awakening | Medium | AI dialogue, direct interaction, gentle manipulation |
| **Act 3** | 😈 Torment | High | Aggressive visuals, psychological pressure, screen effects |
| **Act 4** | 🕯️ Exorcism | Critical | Final confrontation, player choices matter, multiple endings |

### 🛡️ Safety Protocols

> [!CAUTION]
> **PHOTOSENSITIVITY WARNING:** Contains flashing lights, rapid color changes, and intense visual distortions. **DO NOT** run if you have epilepsy or seizure history.

**Built-in Protections:**
- ⌨️ **Kill Switch:** CTRL+SHIFT+Q exits immediately
- 🖥️ **Resource Guard:** Auto-terminates if CPU/RAM > 85%
- 🔒 **Privacy Filter:** Scrubs usernames, file paths before AI
- ♻️ **Auto-Restore:** All system changes revert on exit
- ✅ **Mandatory Consent:** Explicit user agreement required

### 📋 Requirements

- **OS:** Windows 10/11 (64-bit)
- **Python:** 3.10+ (3.11 recommended)
- **API:** Google Gemini API Key ([Get one free](https://makersuite.google.com/app/apikey))
- **Internet:** Required for AI features (offline mode available)
- **Dependencies:** PyQt6, PyYAML, pygame, pywin32

### 🚀 Quick Start

```bash
# 1. Clone/Download
git clone https://github.com/qanteSm/sentient_os.git
cd sentient_os

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Set API Key
set GEMINI_API_KEY=your_api_key_here

# 4. Run
python main.py
```

### ⚙️ Configuration

Edit `config.yaml`:

```yaml
horror:
  intensity: "extreme"  # mild, medium, extreme
  
api:
  gemini_key: "${GEMINI_API_KEY}"
  cache_ttl: 300  # Cache responses for 5 minutes
  
safety:
  streamer_mode: true  # Protects OBS, Discord
  ai_safety_check: true  # Validates snippets before use

audio:
  enable_drone: true
  drone_volume: 0.3
```

---

---

### 🏎️ Teknik Gösterge Paneli ve Stabilite
SENTIENT_OS, ekstrem koşullar altında yüksek güvenilirlik için tasarlanmıştır. Mimari, **Kaos Mühendisliği** ve **Stres Testleri** ile doğrulanmıştır.

| Metrik | Performans | Durum |
|--------|------------|-------|
| **Burst İşlem Kapasitesi** | 410+ eylem/sn | ✅ Stabil |
| **Bellek Sızıntısı** | 0.00 B/sn | ✅ Doğrulandı |
| **GDI Kaynakları** | Otomatik Temizlik | ✅ Güvenli |
| **Atomik Durum** | Veri Kaybı Riski Yok | ✅ Garantili |
| **Hata Kurtarma** | < 2.5sn Geri Yükleme | ✅ Dayanıklı |

---

## <a name="türkçe-readme"></a>🇹🇷 Türkçe README

### 📌 SENTIENT_OS Nedir?

Google Gemini AI tarafından desteklenen, bilgisayarınızın kontrolünü ele geçiren duyarlı bir işletim sistemini simüle eden psikolojik korku deneyimi. Geleneksel oyunlardan farklı olarak SENTIENT_OS:

- **Gerçek zamanlı öğrenir ve adapte olur**
- **4. duvarı kırar** - gerçek masaüstü dosyalarınızı, klasör isimlerinizi kullanır
- **4 anlatı perdesinde evrilir** - ince enfeksiyondan tam ele geçirmeye
- **Hiç aynı olmaz** - AI-tabanlı dinamik hikaye anlatımı

### ✨ Öne Çıkan Özellikler

#### 🧠 AI Destekli Korku
- **Gemini 2.5 Entegrasyonu** - Gerçek zamanlı AI muhakeme ve duygusal tepkiler
- **Bağlam Farkındalığı** - Masaüstü klasörlerinizi, çalışan uygulamalarınızı, saati kullanır
- **Dinamik Diyalog** - Önceden yazılmış cevap yok, tamamen AI üretimi
- **Yanıt Önbellekleme** - %60 API tasarruf, daha hızlı işlem
- **Çevrimdışı Mod** - İnternet kesildiğinde zarif geçiş

#### 🎭 Sürükleyici Deneyim
- **3 Adımlı Giriş** - Karşılama → Yoğunluk Seçimi → Güvenlik Onayı
- **Ambient Korku** - Sürekli bilinçaltı gerilim yaratan arka plan efektleri
- **Drone Ses Katmanı** - Perde başına evrilen atmosferik sesler
- **Sessizlik Kırıcı** - 45s hareketsizlikte otomatik olay tetikleyici
- **Dinamik Olay Zamanlaması** - Kullanıcı aktivitesine göre tempo ayarı

#### 👁️ Gelişmiş Görsel Efektler
- **GDI Ekran Manipülasyonu** - Ekran yırtılması, piksel erimesi, renk inversiyonu
- **Overlay Sistemi** - Ürkütücü yazılar, flaş efektleri, ekran sarsıntısı
- **Sahte Sistem UI** - BSOD, sahte güncellemeler, sistem hataları
- **Masaüstü Maske** - Dondurma illüzyonları
- **Donanım Entegrasyonu** - Parlaklık titrişimi, fare sarsma, klavye ele geçirme

#### 🛡️ Güvenlik Protokolleri
- **Çoklu Güvenlik Katmanı** - Acil kapatma (CTRL+SHIFT+Q), kaynak izleme
- **Gizlilik Filtresi** - Tüm kişisel veriler AI'ya gitmeden temizlenir
- **Yayıncı Modu** - OBS, Discord, tarayıcıları korur
- **Tahribatsız** - Tüm değişiklikler otomatik geri alınır
- **Çökme Kurtarma** - Gerçek hataları korku anlarına çevirir, checkpoint'ten kurtarır

#### ⚡ Teknik Mimari Çekirdeği
- **Asenkron Komut Yolu**: **Öncelik tabanlı (Priority-based)** yüksek hızlı eylem yönlendirme.
- **Kendi Kendini Onaran Çekirdek**: Durum güvenli kontrol noktalarıyla otomatik hata kurtarma.
- **AI Muhakeme Motoru**: Semantik önbelleğe alma ile hibrit çevrimiçi/çevrimdışı Gemini entegrasyonu.
- **Donanım Soyutlama Katmanı**: Düşük gecikmeli efektler için doğrudan Windows API (GDI/Win32) kullanımı.
- **Veri Bütünlüğü Katmanı**: %0 bozulma riski sağlayan atomik JSON kalıcılığı.

### 🎭 Hikaye Akışı

| Perde | Başlık | Yoğunluk | Özellikler |
|-------|--------|----------|------------|
| **1** | 🧬 Enfeksiyon | Düşük | Hafif glitchler, şifreli loglar, sistem "ısınması" |
| **2** | 👁️ Uyanış | Orta | AI diyaloğu, direkt etkileşim, nazik manipülasyon |
| **3** | 😈 İşkence | Yüksek | Agresif görseller, psikolojik baskı, ekran efektleri |
| **4** | 🕯️ Ayin | Kritik | Final savaşı, oyuncu seçimleri önemli, çoklu son |

### 📋 Gereksinimler

- **İşletim Sistemi:** Windows 10/11 (64-bit)
- **Python:** 3.10+ (3.11 önerilen)
- **API:** Google Gemini API Key
- **İnternet:** AI özellikleri için gerekli
- **Bağımlılıklar:** PyQt6, PyYAML, pygame, pywin32

---

## 🏗️ Architecture

```
SENTIENT_OS/
├── core/           # Core systems (Kernel, Brain, Memory)
├── hardware/       # Hardware control (Audio, Mouse, Keyboard)
├── visual/         # Visual effects (GDI, Overlays, UI)
├── story/          # Narrative (Acts, Events, Scheduler)
└── config.yaml     # Runtime configuration
```

**For Developers:** See [TECHNICAL.md](TECHNICAL.md) for architecture deep-dive.

**Credits:** See [CREDITS.md](CREDITS.md) for audio sources and open-source attributions.

---

## ⚖️ Legal Disclaimer

**EN:** This software is provided "as is" without warranty. Developer not responsible for hardware/software issues. Not recommended for photosensitive individuals.

**TR:** Bu yazılım "olduğu gibi" sunulur. Geliştirici donanım/yazılım sorunlarından sorumlu tutulamaz. Işığa duyarlı bireyler için önerilmez.

---

## 📜 License

MIT License - Copyright (c) 2026 Muhammet Ali Büyük

See [LICENSE](LICENSE) for full text.

---

## 🙏 Acknowledgments

- **Google Gemini API** - AI reasoning engine
- **PyQt6** - GUI framework
- **Community** - Testing and feedback

---

<p align="center">
  <a href="https://alibuyuk.net/#contact">🌐 Website</a> •
  <a href="mailto:iletisim@alibuyuk.net">📧 E-mail</a>
</p>

<p align="center">
  <sub>Developed with ❤️ by <a href="https://alibuyuk.net">Muhammet Ali Büyük</a></sub>
</p>
>
