# Sıkça Sorulan Sorular (FAQ)

## Genel Sorular

### SENTIENT_OS nedir?
SENTIENT_OS, yapay zeka destekli interaktif bir korku deneyimidir. Google Gemini AI kullanarak kullanıcıyla etkileşime giren, "bilgisayarın kontrolünü ele geçirmiş" bir AI varlığı simüle eder.

### Güvenli mi?
Evet, SENTIENT_OS güvenlik odaklı tasarlanmıştır:
- Tüm sistem değişiklikleri otomatik olarak yedeklenir
- Korumalı işlemler (OBS, Discord) zarar görmez
- Kapanırken her şey geri yüklenir
- Epilepsi koruması varsayılan olarak aktiftir

### Gerçekten korkutucu mu?
Psikolojik olarak rahatsız edici olabilir. Özellikle:
- Kişiselleştirilmiş tehditler
- Masaüstü manipülasyonu
- Sesli uyarılar
- Belirsizlik ve tahmin edilemezlik

### Hangi platformlarda çalışır?
- **Windows 10/11**: Tam özellik desteği
- **Linux/Mac**: Mock mode (sınırlı özellikler, test için)

## Teknik Sorular

### API anahtarı gerekli mi?
- **Hayır**: Mock mode ile AI olmadan çalışabilir
- **Evet (önerilir)**: Tam deneyim için Google Gemini API anahtarı gerekli
- Ücretsiz API: https://makersuite.google.com/app/apikey

### Mock mode nedir?
API olmadan çalışan test modu. AI yerine önceden yazılmış yanıtlar kullanır. Özellikler sınırlıdır.

### Bağımlılıkları nasıl yüklerim?
```bash
pip install -r requirements.txt
```

veya

```bash
python quickstart.py  # Otomatik kurulum
```

### Python versiyonu ne olmalı?
Python 3.8 veya üzeri gerekli. Python 3.10+ önerilir.

## Kullanım Soruları

### Programı nasıl başlatırım?
```bash
python main.py
```

İlk kez kullanıyorsanız:
```bash
python quickstart.py  # Otomatik kurulum ve başlatma
```

### Zorluk seviyesini nasıl değiştiririm?
```bash
python settings_cli.py
```

Menüden "2. Zorluk Seviyesi Değiştir" seçin.

### Başarıları nasıl görürüm?
```bash
python settings_cli.py
```

Menüden "7. Başarıları Görüntüle" seçin.

### Programı nasıl kapatırım?
- Normal kapatma: Hikayeyi tamamlayın
- Zorla kapatma: `Ctrl+C` (terminal) veya Task Manager
- Her durumda ayarlar geri yüklenir

### Strobe efektlerini nasıl devre dışı bırakırım?
**Önemli**: Varsayılan olarak KAPATILMIŞTIR.

Manuel kontrol:
1. `python settings_cli.py`
2. "4. Erişilebilirlik Ayarları"
3. "1. Strobe Efektlerini Devre Dışı Bırak"

veya `config.py` içinde:
```python
ENABLE_STROBE = False  # Zaten varsayılan
```

### Streamer mode nedir?
İsimleri, dosya adlarını ve hassas bilgileri gizler. OBS/Discord kullanıcıları için:
- Ekran paylaşımında gerçek isminiz görünmez
- Masaüstü dosyaları anonimleştirilir
- Korumalı işlemler zarar görmez

## Hata Giderme

### "ModuleNotFoundError: No module named 'PyQt6'"
Bağımlılıklar yüklenmemiş:
```bash
pip install -r requirements.txt
```

### "No API Key found. Reverting to Mock Mode."
Gemini API anahtarı bulunamadı. İki seçenek:
1. `.env` dosyası oluşturun:
   ```
   GEMINI_API_KEY=your_key_here
   ```
2. Mock mode ile devam edin (sınırlı)

### Parlaklık/duvar kağıdı geri yüklenmiyor
Crash nedeniyle geri yükleme başarısız olabilir. Manuel düzeltme:
- Parlaklık: Windows ayarlarından düzeltin
- Duvar kağıdı: `cache/wallpaper_backup.jpg` varsa manuel ayarlayın
- Simgeler: Sağ tık → "Refresh" veya F5

### Program çökmeye devam ediyor
1. Sistem durumunu kontrol edin:
   ```bash
   python diagnostic.py
   ```

2. Güvenli moda geçin (`config.py`):
   ```python
   SAFE_HARDWARE = True
   CHAOS_LEVEL = 0
   ```

3. Temiz başlatma:
   ```bash
   python tools/reset_memory.py  # Hafızayı sıfırla
   python main.py
   ```

### "Permission denied" hatası
1. Yönetici olarak çalıştırın (Windows):
   - PowerShell'i yönetici olarak açın
   - `python main.py`

2. İzinleri kontrol edin:
   ```bash
   python diagnostic.py
   ```

### CPU/RAM kullanımı çok yüksek
Resource guard devreye girmelidir. Manuel düşürme:

`config.py` içinde:
```python
CHAOS_LEVEL = 0  # Daha az efekt
```

veya `settings_cli.py` ile zorluk seviyesini düşürün.

## Özelleştirme

### Dil nasıl değiştirilir?
Şu an sadece Türkçe destekleniyor. İngilizce v4.2'de gelecek.

### Yeni efektler nasıl eklenir?
Plugin sistemi v4.2'de gelecek. Şimdilik:
1. `visual/effects/` klasörüne yeni efekt ekleyin
2. `core/function_dispatcher.py` içinde aksiyonu kaydedin

### Kendi hikayemi yazabilir miyim?
Evet! `story/` klasöründe yeni Act oluşturun:
```python
# story/act_5_custom.py
from story.base_act import BaseAct

class Act5Custom(BaseAct):
    # Implement your story
    pass
```

## Topluluk

### Nasıl katkıda bulunabilirim?
[CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bakın.

### Hata bildirimi nasıl yaparım?
GitHub Issues kullanın:
https://github.com/qanteSm/SENTIENT_OS/issues

### Özellik önerebilir miyim?
Elbette! Issues'da "enhancement" etiketi ile açın.

## Gelişmiş

### Başarıları manuel nasıl açarım?
Test/debug için:
```python
from core.achievement_system import achievement_manager
achievement_manager.unlock("achievement_id")
```

### Hafıza dosyasını nerede bulabilirim?
- Windows: `%APPDATA%\SentientOS\brain_dump.json`
- Linux/Mac: `./brain_dump.json`

### Ayarları nasıl sıfırlarım?
```bash
python settings_cli.py
```
Menüden "8. Ayarları Sıfırla"

veya manuel olarak:
```bash
rm user_settings.json achievements.json brain_dump.json
```

### Kod yapısını nasıl anlayabilirim?
[ARCHITECTURE.md](ARCHITECTURE.md) dosyasını okuyun.

## Yasal

### Lisans nedir?
MIT License - ticari kullanım dahil özgürce kullanılabilir.

### Kötü niyetli kullanım?
Bu proje eğitim ve eğlence amaçlıdır. Kötü niyetli kullanımdan kaçının:
- Başkalarını korkutmak için izinsiz kullanmayın
- Zararlı yazılım gibi dağıtmayın
- Etik ve yasal kurallara uyun

---

**Sorunuz cevaplanmadı mı?**

GitHub Discussions veya Issues kullanın:
https://github.com/qanteSm/SENTIENT_OS
