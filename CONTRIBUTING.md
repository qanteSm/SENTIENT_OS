# Katkıda Bulunma Rehberi

SENTIENT_OS'e katkıda bulunmak istediğiniz için teşekkürler! 🎉

## 🌟 Katkı Türleri

### 1. Hata Raporlama
- GitHub Issues kullanın
- Sorunu açık ve detaylı tanımlayın
- Yeniden üretme adımlarını ekleyin
- Sistem bilgilerinizi paylaşın (OS, Python versiyonu)

### 2. Özellik Önerileri
- Önce Issues'da tartışın
- Kullanım senaryosu açıklayın
- Mümkünse mockup/tasarım ekleyin

### 3. Kod Katkıları
- Pull Request açın
- Kodlama standartlarını takip edin
- Test ekleyin
- Dokümantasyon güncelleyin

## 🔧 Geliştirme Ortamı Kurulumu

1. **Repository'yi fork edin ve klonlayın:**
```bash
git clone https://github.com/YOUR_USERNAME/SENTIENT_OS.git
cd SENTIENT_OS
```

2. **Sanal ortam oluşturun:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Geliştirme branch'i oluşturun:**
```bash
git checkout -b feature/my-feature
```

## 📝 Kodlama Standartları

### Python Stil Rehberi
- **PEP 8** standartlarını takip edin
- Maksimum satır uzunluğu: 100 karakter
- Fonksiyonlar için docstring kullanın
- Değişken isimleri açıklayıcı olsun

### Örnek Kod Stili

```python
def calculate_anger_level(user_action: str, context: dict) -> int:
    """
    Kullanıcı aksiyonuna göre öfke seviyesi hesaplar.
    
    Args:
        user_action: Kullanıcı aksiyonunun türü
        context: Bağlamsal bilgiler
    
    Returns:
        0-100 arası öfke seviyesi
    """
    anger = 0
    
    if user_action == "swear":
        anger += 15
    elif user_action == "escape_attempt":
        anger += 25
    
    return min(100, anger)
```

### Dosya Organizasyonu
```
core/           # Temel sistem bileşenleri
├── kernel.py   # Sistem çekirdeği (SentientKernel sınıfı)
├── memory.py   # Hafıza yönetimi
└── ...

hardware/       # Donanım operasyonları
├── keyboard_ops.py
├── mouse_ops.py
└── ...

visual/         # Görsel efektler ve UI
├── effects/    # Görsel efekt modülleri
├── ui/         # PyQt6 UI bileşenleri
└── ...

story/          # Hikaye ve senaryo yönetimi
└── ...
```

## 🧪 Test Yazma

### Test Yapısı
```python
# test_my_feature.py
import unittest
from core.my_module import MyClass

class TestMyFeature(unittest.TestCase):
    def setUp(self):
        """Her test öncesi çalışır."""
        self.instance = MyClass()
    
    def test_basic_functionality(self):
        """Temel fonksiyonalite testi."""
        result = self.instance.do_something()
        self.assertEqual(result, expected_value)
    
    def test_edge_case(self):
        """Kenar durum testi."""
        with self.assertRaises(ValueError):
            self.instance.do_something_invalid()
```

### Test Çalıştırma
```bash
# Tek bir test dosyası
python test_my_feature.py

# Tüm testler
python -m unittest discover
```

## 🎯 Commit Mesaj Formatı

Anlamlı ve açıklayıcı commit mesajları yazın:

```
[TÜR] Kısa açıklama (50 karakter max)

Detaylı açıklama (isteğe bağlı)
- Neden bu değişiklik gerekli
- Nasıl çalışıyor
- Yan etkileri

Fixes #123
```

### Commit Türleri:
- `[FEAT]` - Yeni özellik
- `[FIX]` - Hata düzeltme
- `[DOCS]` - Dokümantasyon
- `[STYLE]` - Kod formatı
- `[REFACTOR]` - Kod yeniden yapılandırma
- `[TEST]` - Test ekleme/düzeltme
- `[PERF]` - Performans iyileştirme

### Örnekler:
```bash
[FEAT] Yeni panik sensörü eklendi

Kullanıcı Alt+F4'e bastığında AI öfkeleniyor.
- PanicSensor sınıfı oluşturuldu
- Event bus entegrasyonu yapıldı
- AngerEngine ile bağlandı

[FIX] Parlaklık geri yükleme hatası düzeltildi

Windows 11'de bazı monitörlerde parlaklık geri 
yüklenemiyor hatası düzeltildi. WMI fallback eklendi.

Fixes #42
```

## 🔍 Pull Request Süreci

1. **Fork ve Branch:**
   - Repository'yi fork edin
   - Yeni branch oluşturun

2. **Değişiklikler:**
   - Küçük, odaklı değişiklikler yapın
   - Her commit mantıklı bir birim olmalı

3. **Test:**
   - Mevcut testlerin geçtiğinden emin olun
   - Yeni özellikler için test ekleyin

4. **Dokümantasyon:**
   - README.md'yi güncelleyin (gerekirse)
   - Kod içi dokümantasyon ekleyin
   - CHANGELOG.md'yi güncelleyin

5. **Pull Request Açın:**
   - Açıklayıcı başlık
   - Ne değişti ve neden
   - İlgili issue'lara referans

### PR Şablonu:
```markdown
## Değişiklik Türü
- [ ] Hata düzeltme
- [ ] Yeni özellik
- [ ] Kod iyileştirme
- [ ] Dokümantasyon

## Açıklama
Bu PR şunları yapar:
- ...
- ...

## Test
Nasıl test edildi:
- ...

## Ekran Görüntüsü
(Görsel değişiklikler varsa)

## Checklist
- [ ] Kod PEP 8'e uygun
- [ ] Testler eklendi ve geçiyor
- [ ] Dokümantasyon güncellendi
- [ ] Commit mesajları açık ve anlamlı
```

## 🛡️ Güvenlik

Güvenlik açığı bulursanız:
1. **Public issue AÇMAYIN**
2. Doğrudan proje sahibine ulaşın
3. Detayları ve yeniden üretme adımlarını gönderin

## 🌍 Yerelleştirme (i18n)

Yeni dil eklemek için:

1. `locales/` klasöründe yeni JSON dosyası:
```json
// locales/en.json
{
  "boot": {
    "starting": "System starting...",
    "loading": "Loading components..."
  },
  "threats": {
    "warning": "I see you..."
  }
}
```

2. `config.py` içinde dil ekleyin:
```python
SUPPORTED_LANGUAGES = ["tr", "en", "de"]
```

## 📚 Ek Kaynaklar

- [Python PEP 8 Style Guide](https://pep8.org/)
- [PyQt6 Documentation](https://doc.qt.io/qtforpython/)
- [Google Gemini API Docs](https://ai.google.dev/docs)

## 💬 İletişim

- **GitHub Issues:** Sorular ve tartışmalar için
- **Pull Requests:** Kod incelemeleri için
- **Discussions:** Genel konular için

## ⚖️ Davranış Kuralları

### Yapılması Gerekenler:
✅ Saygılı ve profesyonel olun
✅ Yapıcı geri bildirim verin
✅ Farklı görüşlere açık olun
✅ Topluluk odaklı düşünün

### Yapılmaması Gerekenler:
❌ Saldırgan dil kullanmayın
❌ Spam yapmayın
❌ Başkalarının çalışmalarını çalmayın
❌ Kötü niyetli kod eklemeyin

## 🎓 İlk Katkı Yapacaklar İçin

İlk kez açık kaynak projesine katkıda mı bulunuyorsunuz?
- `good-first-issue` etiketli issue'lara bakın
- Dokümantasyon iyileştirmeleri yapın
- Yazım hatalarını düzeltin
- Küçük bug fix'ler yapın

**Her katkı değerlidir!** 🌟

---

Tekrar teşekkürler! Katkılarınız SENTIENT_OS'i daha iyi yapar. 🚀
