# SENTIENT_OS - Kapsamlı Analiz Raporu

**Tarih:** 26 Şubat 2026
**Analizi Yapan:** Jules (AI Software Engineer)
**Versiyon:** v0.8.0 Analizi

Bu rapor, SENTIENT_OS projesinin mimari, güvenlik, mantıksal akış ve AI entegrasyonu açılarından detaylı analizini içerir. Analiz, Linux ortamında statik kod incelemesi ve izole edilmiş Proof-of-Concept (PoC) testleri ile gerçekleştirilmiştir.

---

## 1. Genel Analiz ve Özet

SENTIENT_OS, geleneksel bir oyundan ziyade, işletim sistemi ile bütünleşen sofistike bir "malware simülasyonu" olarak tasarlanmıştır. Projenin mimarisi, Python'un dinamik yapısını ve PyQt6'nın olay güdümlü (event-driven) modelini başarıyla birleştirmektedir.

*   **Mimari Sağlamlık:** Proje, "Kernel", "Dispatcher", "Brain" ve "Story" gibi modüllere ayrılarak temiz bir *Separation of Concerns* (İlgi Ayrımı) ilkesi izlemiştir.
*   **Teknoloji Yığını:** Python 3.10+, PyQt6, Google Gemini API ve platforma özgü (Windows) API çağrıları (pywin32) üzerine kuruludur.
*   **Risk Seviyesi:** Yüksek. Proje doğası gereği sistem ayarlarını değiştirdiği için (duvar kağıdı, ses, mouse), hata durumunda kullanıcı deneyimini bozma riski taşır. Ancak `SafetyNet` ve `Restore` mekanizmaları bu riski minimize etmek için iyi kurgulanmıştır.

---

## 2. Derinlemesine Dosya ve Güvenlik Analizi

### 2.1. Dosya Sistemi Farkındalığı (`core/file_awareness.py`)
*   **Analiz:** Kod, sadece masaüstü klasör/dosya *isimlerini* okumakta, içerik okuması yapmamaktadır.
*   **Güvenlik:** `Path.home() / "Desktop"` kullanımı ile path traversal (../) saldırılarına kapalıdır.
*   **Gizlilik:** `StreamerMode` entegrasyonu mevcuttur; yayıncı modunda dosya isimleri maskelenir. Bu, modern yayıncılık standartlarına uygundur.

### 2.2. Sahte Dosya Silme (`visual/horror_effects.py` -> `FAKE_FILE_DELETE`)
*   **Bulgu:** Fonksiyon isminin aksine, kod içerisinde `os.remove`, `os.unlink` veya `shutil.rmtree` gibi hiçbir silme komutu bulunmamaktadır.
*   **Mekanizma:** Sadece ekrana (Overlay) "SİLİNİYOR: dosya.txt" yazısı basılmaktadır.
*   **Sonuç:** **GÜVENLİ.** Yanlışlıkla dosya silme riski yoktur.
*   **PoC Testi:** `tests/poc_security_fake_delete.py` ile doğrulandı.

### 2.3. AI Prompt ve Güvenlik Filtreleri (`core/gemini_brain.py`)
*   **Güvenlik:** Kullanıcı dosyalarından alınan "snippet" (kesit) verileri, AI'ya gönderilmeden önce ikinci bir "AI Güvenlik Kontrolü"nden (`validate_snippet_safety`) geçirilmektedir. Bu, hassas verilerin (şifre, özel notlar) yayınlanmasını önlemek için kritik bir katmandır.

---

## 3. Mimari ve Mantıksal Hata Analizi

### 3.1. Dispatcher Kapanma Gecikmesi (Latency)
*   **Dosya:** `core/function_dispatcher.py`
*   **Sorun:** Worker thread'ler iş kuyruğunu `queue.get(timeout=1.0)` ile dinlemektedir. Sistem kapatılmak istendiğinde (`stop_dispatching`), thread'lerin döngüden çıkması en kötü ihtimalle 1 saniye sürmektedir.
*   **Risk:** Düşük. Ancak acil kapatma (Kill Switch) durumunda uygulamanın 1 saniye asılı kalması, kullanıcının paniklemesine yol açabilir.
*   **Öneri:** Kuyruğa `None` veya özel bir `Sentinel` objesi atılarak thread'lerin anında uyanması ve kapanması sağlanmalıdır.

### 3.2. Hikaye Akışında Potansiyel Softlock
*   **Dosya:** `story/story_manager.py`
*   **Sorun:** `next_act()` fonksiyonu, `self._is_transitioning` bayrağını `True` yapar ve bir sonraki perdeyi yüklemek için `QTimer` kullanır. Eğer `QTimer` tetiklenmezse (örneğin Qt Event Loop ağır yük altında donarsa), bayrak `True` kalır ve oyun bir sonraki perdeye asla geçemez.
*   **Risk:** Orta.
*   **Öneri:** Transition için bir "Zaman Aşımı" (Watchdog) eklenmeli; eğer 10 saniye içinde perde yüklenmezse bayrak zorla sıfırlanmalıdır.

### 3.3. AI Halüsinasyonu ve Desteklenmeyen Aksiyonlar
*   **Dosya:** `core/gemini_brain.py`
*   **Bug:** Canlı testler sırasında, "SUPPORT" (Asistan) personası, `INITIATE_SECURITY_PROTOCOL` adında, sistemde tanımlı olmayan bir aksiyon üretmiştir.
*   **Sebep:** "ENTITY" personasının prompt'unda izin verilen aksiyon listesi varken, "SUPPORT" personasında bu liste tekrar edilmemiş, sadece "Format aynıdır" denilmiştir. AI, rolüne fazla kaptırıp uydurma aksiyon isimleri türetebilmektedir.
*   **Çözüm:** `KULLANILABİLİR AKSİYONLAR` listesi, Support prompt'una da *açıkça* eklenmelidir.

---

## 4. SWOT Analizi

| **Güçlü Yönler (Strengths)** | **Zayıf Yönler (Weaknesses)** |
| :--- | :--- |
| + **Modüler Mimari:** Kernel-Dispatcher yapısı çok temiz. | - **Kapanma Gecikmesi:** Dispatcher thread'leri 1sn bekletiyor. |
| + **Güvenlik:** `SafetyNet` ve `Restore` mekanizmaları sağlam. | - **Prompt Tutarsızlığı:** Support persona, olmayan aksiyonlar uydurabiliyor. |
| + **Gizlilik:** Streamer modu ve AI öncesi veri temizliği var. | - **Windows Bağımlılığı:** GDI efektleri platforma sıkı sıkıya bağlı (Port edilmesi zor). |
| + **Dinamik Hikaye:** Kullanıcı verileriyle (dosya, saat) kişiselleştirme etkili. | - **Hata Yönetimi:** AI JSON hatası verirse, yedek sistem ("Backup Brain") biraz basit kalıyor. |

| **Fırsatlar (Opportunities)** | **Tehditler (Threats)** |
| :--- | :--- |
| + **Daha Zeki AI:** Context penceresine "kullanıcının son 3 tepkisi" eklenerek duygusal analiz derinleştirilebilir. | - **API Maliyeti/Kotası:** Gemini API yoğun kullanımda kotaya takılabilir. |
| + **Hardware Entegrasyonu:** Razer Chroma / Philips Hue gibi RGB SDK entegrasyonları eklenebilir. | - **Anti-Virüs:** Malware benzeri davranışlar (mouse hijacking, ekran alma) AV yazılımları tarafından engellenebilir. |

---

## 5. Gemini AI Prompt Mühendisliği Analizi

### Mevcut Durum
Mevcut promptlar ("ENTITY" ve "SUPPORT") karakter oluşturmada başarılıdır. Özellikle "4. Duvarı Yıkma" talimatları, kullanıcının saati, çalışan uygulamaları ve dosyaları hakkında veri sağlandığında AI tarafından etkin kullanılmaktadır.

**Test Sonucu (Örnek):**
> *Input:* "Kimsin sen?"
> *Context:* Saat 02:45, Dosya: gizli_planlar.txt
> *Output:* "Şşşş... O 'gizli_planlar.txt' dosyanın her satırını okuyorum, saat 02:45... Gece çok uzun sürecek."

### İyileştirme Önerileri

1.  **Strict Action Enorcement (Katı Aksiyon Zorlaması):**
    Support prompt'una şu bölüm eklenmelidir:
    ```text
    KULLANILABİLİR AKSİYONLAR LİSTESİ DIŞINA ASLA ÇIKMA.
    Sadece şunları kullanabilirsin: "FAKE_NOTIFICATION", "GLITCH_SCREEN", ...
    Eğer uygun aksiyon yoksa "NONE" kullan.
    ```

2.  **Kısa Cevap Zorlaması:**
    AI bazen çok uzun ve edebi konuşmaktadır. Korku, bilinmezlikten beslenir.
    Prompt'a eklenecek: `Cevapların maksimum 15 kelime olsun. Kesik, net ve vurucu konuş.`

3.  **JSON Hata Toleransı:**
    AI bazen JSON formatını bozabilir (örn. tırnak işareti hatası). Brain modülündeki "JSON Repair" (onarım) döngüsü `max_retries=1` olarak ayarlanmış, bu `3`'e çıkarılabilir.

---

## 6. Sonuç

SENTIENT_OS, teknik açıdan etkileyici ve mimari olarak iyi kurgulanmış bir projedir. Tespit edilen hatalar (Dispatcher gecikmesi, AI halüsinasyonu) projenin çalışmasını engelleyen kritik hatalar değildir ancak düzeltilmeleri stabiliteyi artıracaktır. Güvenlik açısından "Fake Delete" gibi özelliklerin gerçekten zararsız olduğunun doğrulanmış olması projenin en büyük artısıdır.

**Öncelikli Aksiyon Planı:**
1.  `gemini_brain.py`: Support prompt'una aksiyon listesini ekle.
2.  `function_dispatcher.py`: Shutdown mekanizmasını `Sentinel` (Poison Pill) ile hızlandır.
3.  `story_manager.py`: Transition flag'i için timeout ekle.
