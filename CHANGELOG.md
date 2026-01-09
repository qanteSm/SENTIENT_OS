# Değişiklik Günlüğü (Changelog)

Tüm önemli değişiklikler bu dosyada dokümante edilir.

Format [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) standardını takip eder.

## [4.1.0] - 2026-01-09

### Eklenenler
- 📚 **Kapsamlı dokümantasyon**
  - README.md: Detaylı proje açıklaması, kurulum ve kullanım rehberi
  - CONTRIBUTING.md: Katkıda bulunma rehberi ve kodlama standartları
  - ARCHITECTURE.md: Sistem mimarisi ve teknik dokümantasyon
  - CHANGELOG.md: Değişiklik günlüğü

- ⚙️ **Ayarlar Sistemi** (`core/settings_manager.py`)
  - Zorluk seviyeleri (Kolay, Normal, Zor, Extreme)
  - Ses kontrolü
  - Erişilebilirlik seçenekleri (strobe koruma, yüksek kontrast, yavaş mod)
  - Gizlilik ayarları (streamer modu, analitik)
  - Gelişmiş ayarlar (güvenli donanım, kaos seviyesi)
  - JSON tabanlı kalıcı depolama

- 🏆 **Başarı Sistemi** (`core/achievement_system.py`)
  - 20+ benzersiz başarı
  - 6 kategori: Hayatta kalma, Hikaye, Etkileşim, Direniş, İtaat, Keşif
  - Gizli başarılar
  - Puan sistemi
  - Otomatik ilerleme takibi

- 🖥️ **CLI Ayarlar Yöneticisi** (`settings_cli.py`)
  - İnteraktif menü sistemi
  - Tüm ayarları yönetme
  - Başarıları görüntüleme
  - Kolay kullanım için komut satırı arayüzü

### İyileştirmeler
- ✨ Kod organizasyonu ve modülerlik artırıldı
- 📝 Tüm temel bileşenler için detaylı dokümantasyon
- 🎯 Event bus sistemi dokümante edildi
- 🔧 Daha iyi hata yönetimi için altyapı hazırlandı

### Gelecek Planlar (v4.2.0)
- [ ] Multi-language support (İngilizce çeviriler)
- [ ] GUI settings manager (PyQt6)
- [ ] Performance monitoring dashboard
- [ ] Plugin system for custom effects
- [ ] Cloud sync for achievements
- [ ] Telemetry system (opsiyonel)

---

## [4.0.0] - 2026-01-08

### Eklenenler
- 🎭 Hikaye sistemi (4 perde)
- 🤖 Gemini AI entegrasyonu
- 🧠 Hafıza ve öğrenme sistemi
- 😡 Anger engine (öfke sistemi)
- 🎨 Görsel efektler ve overlay'ler
- 🔒 Güvenlik ve geri yükleme mekanizmaları
- ⚡ Event bus sistemi
- 🎮 Checkpoint ve crash recovery

### Değiştirilenler
- Konsol tabanlı yaklaşımdan PyQt6'ya geçiş
- Mock mode desteği (API olmadan test)
- Windows odaklı özellikler

---

## [3.x.x] - 2025

### Önceki Versiyonlar
- İlk konsept ve prototip geliştirme
- Temel AI etkileşimleri
- Basit horror efektleri

---

## Versiyon Numaralandırma

Bu proje [Semantic Versioning](https://semver.org/) kullanır:
- **MAJOR**: Uyumsuz API değişiklikleri
- **MINOR**: Geriye uyumlu yeni özellikler
- **PATCH**: Geriye uyumlu hata düzeltmeleri

## Değişiklik Kategorileri

- **Eklenenler** (Added): Yeni özellikler
- **Değiştirilenler** (Changed): Mevcut fonksiyonlarda değişiklikler
- **Kullanımdan Kaldırılanlar** (Deprecated): Yakında kaldırılacak özellikler
- **Kaldırılanlar** (Removed): Kaldırılan özellikler
- **Düzeltilenler** (Fixed): Hata düzeltmeleri
- **Güvenlik** (Security): Güvenlik güncellemeleri
