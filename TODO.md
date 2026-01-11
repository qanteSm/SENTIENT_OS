# 📝 SENTIENT_OS - Future Roadmap & TODO

> **Not:** Mevcut özellikler (CapsLock Morse, Notepad Yazma, Fake Toast) listeden çıkarılmıştır. Sadece yeni eklemeler ve geliştirmeler kalmıştır.

## 🐛 Bug Fixes & Improvements (Raporlanan Hatalar)
Kullanıcı geri bildirimlerine dayalı düzeltme ve iyileştirmeler.

### Act 1 & Pacing
- [ ] **Pacing Optimization (Hızlandırma)**
    - [ ] `Act 1` başlangıcındaki "boşluk" hissi giderilmeli. 0-2 dakika arası çok durgun geçiyor.
    - [ ] Efekt ve olay sıklığı artırılmalı, timeline sıkıştırılmalı (8 dk -> daha kısa veya daha yoğun).
    - [ ] Kullanıcı etkileşim noktaları (iletişim, chat) daha erken gelmeli.

### System & Hardware
- [ ] **Notification System Overhaul**
    - [ ] "Windows notification gelmiyor" şikayeti: `notification_ops.py` ve `fake_notification.py` yenilenmeli.
    - [ ] Bildirim stili Windows 10/11 native görünümüne birebir benzetilmeli (Glass effect, animasyonlar).
    - [ ] Bildirimlerin her zaman en üstte (Always On Top) ve görünür olduğundan emin olunmalı.
- [ ] **TTS Stability (Ses Sorunu)**
    - [ ] "Bir kere konuşup susuyor" hatası giderilmeli.
    - [ ] `pyttsx3` motorunun thread yönetimi düzeltilmeli (COM initialization hataları).
    - [ ] Sürekli ve stabil konuşma için tek bir motor instance'ı veya sağlam bir kuyruk yapısı.

### Visual & Immersion
- [ ] **Subtitle Duration Fix**
    - [ ] "Nefes sesi (breath) alt yazısı çok kısa kalıyor" sorunu.
    - [ ] Alt yazı süresi ses/efekt süresine eşitlenmeli veya minimum okunabilir süre (2-3sn) tanımlanmalı.

### AI & Gemini Integration
- [ ] **Unshackled AI (Gemini Safety)**
    - [ ] "Dosyamı sil dediğimde yapmıyor, küfür edince tepki vermiyor" sorunu.
    - [ ] Gemini API Safety Settings `BLOCK_NONE` olarak ayarlanmalı.
    - [ ] Prompt mühendisliği ile AI'nın "Sanal Zarar Verme" (Roleplay) yeteneği açılmalı.
    - [ ] "Mavi ekran ver", "Sil" gibi komutları reddetmek yerine ilgili `FAKE_` aksiyonlara (fake delete, fake bsod) yönlendirmeli.

---

## 🔮 Phase 5: Physical Integration (Hardware)
Donanım dünyasına sızarak oyuncuyu "gerçeklikte" etkileme.

- [ ] **Gelişmiş LED Kontrolü (Num & Scroll Lock)**
    - [ ] Mevcut CapsLock özelliğine ek olarak NumLock ve ScrollLock ışıklarını da ritmik kullanma.
- [ ] **RGB Klavye Entegrasyonu (Yeni)**
    - [ ] Razer Chroma, Corsair iCUE veya Logitech G SDK'larını araştırma.
    - [ ] Tüm klavyeyi aniden kırmızıya (tehlike) veya tamamen siyaha (körlük) çevirme.
- [ ] **CD-ROM / Optik Sürücü (Retro Korku)**
    - [ ] Eğer donanım mevcutsa, CD tepsisini aniden açıp kapatma ("Eject" komutu).

## 📸 Phase 6: Personal Horror (Kamera ve Kişiselleştirme)
Dördüncü duvarı tamamen yıkmak için oyuncunun kendisine odaklanma.

- [ ] **Kamera Erişimi ve "Gözcü" Modu**
    - [ ] `OpenCV` (`cv2`) kütüphanesi ile web kamerasına sessizce erişme.
    - [ ] Oyuncunun fotoğrafını çekip arka planda işleme.
- [ ] **Korku Filtresi ve Wallpaper**
    - [ ] Çekilen fotoğrafa "glitch", "noise", "invert" veya "distortion" efektleri uygulama.
    - [ ] Bu korkunç hali anlık olarak masaüstü arka planı yapma (`WallpaperOps` güncellemesi).
    - [ ] *Güvenlik Notu:* Fotoğraf asla internete yüklenmemeli, oyun kapanınca silinmeli.
- [ ] **Ses Kaydı ve Yankı**
    - [ ] Oyuncunun mikrofonundan kısa sesler kaydedip, bozuk bir frekansla ona geri dinletme.

## ✍️ Phase 7: Enhanced Interaction (UI/UX)
Mevcut özellikleri daha zeki hale getirme.

- [ ] **Notepad AI Sohbeti (Gelişmiş)**
    - [ ] *Mevcut:* Düz yazı yazılıyor.
    - [ ] *Hedef:* AI'nın yazdığını "beğenmeyip silmesi" (backspace simülasyonu) ve düzeltmesi.
    - [ ] Kullanıcı bir şey yazdığında cevap vermesi (Read & Reply).
- [ ] **Kanlı ve Dinamik Yazı Efektleri**
    - [ ] Mevcut sade overlay yazılarının üzerine şeffaf PNG katmanları veya GDI çizimleri ile "kan damlama" efekti.
    - [ ] Yazıların titremesi, büyümesi/küçülmesi (nefes alma efekti).
- [ ] **Sahte Bildirim Senaryoları**
    - [ ] *Mevcut:* Toast mesajı gösterilebiliyor.
    - [ ] *Hedef:* "Düşük Pil (%1)", "Kritik Sistem Hatası", "Virüs Tespit Edildi" gibi inandırıcı presetler.

## 🎮 Phase 8: Gameplay & Interactive Story (Oynanış Devrimi)
Hikaye akışını "boş"luktan kurtarıp, aktif oynanışa ve sonuçlara bağlama.

- [ ] **Mouse Cursor Parkour (Cursor Avatar)**
    - [ ] **Konsept:** Oyuncunun karakteri doğrudan **Fare İmleci**'dir.
    - [ ] **Amaç:** Ekranda açılan pencereler, hata mesajları ve "glitch" alanları birer platform/engeldir. İmleci bu engellere çarptırmadan hedefe (örn: "Kurtar" butonu veya yeşil bir klasör) ulaştırmak.
    - [ ] **Zorluk:** Pencereler hareket eder, küçülür/büyür. İmleç "ağırlaşabilir" (input lag simülasyonu) veya titreyebilir.
    - [ ] **Meta-Korku:** Kaybedince imleç "ölür" (yok olur) ve sistem kilitlenmiş gibi davranır.
- [ ] **Virus Avcısı (Mini-Game)**
    - [ ] Masaüstünde rastgele hızla beliren "zararlı" pencereleri veya bozuk ikonları süre bitmeden tıklayıp kapatma.
    - [ ] *Sonuç:* Başarısız olunursa sistem daha fazla bozulur (Glitch artar).
- [ ] **Cezalandırıcı Döngü (Roguelike Elements)**
    - [ ] Mini oyunlarda kaybedince "Game Over" yerine **Act Başına Dönüş**.
    - [ ] "Seni uyardım..." diyerek AI'nın zorluk seviyesini artırması.

## 🧠 Phase 9: Psychological Warfare (Sinsi Özellikler)

- [ ] **İşitsel İllüzyonlar (Audio Deception)**
    - [ ] Arka planda çok düşük sesle (Discord, Slack, Whatsapp) bildirim sesi çalmak.
    - [ ] Binaural ses efektleri (Sağ/Sol kulak ayrımı).
- [ ] **Panoya Sızma (Clipboard Poisoning)**
    - [ ] Kopyalanan metni yapıştırırken değiştirmek (Örn: "YARDIM ET").
- [ ] **İkon Ritüelleri (Gelişmiş)**
    - [ ] *Mevcut:* Spiral/Rastgele dağıtım var.
    - [ ] *Hedef:* İkonları "HAÇ", "DAİRE" veya "ÖL" yazısı şeklinde dizmek.
- [ ] **İkinci Ekran Tacizi**
    - [ ] Çift monitör varsa, kullanılmayan ekranda anlık silüetler göstermek.
- [ ] **Sahte Tarayıcı Geçmişi**
    - [ ] Tarayıcıda korku temalı sahte sekmeler açmak.

## 🔒 Güvenlik & Etik
- [ ] **Duygu Analizi (Sentiment Analysis)**
    - [ ] Mikrofondan gelen ses tonunu analiz etme.
- [ ] **Gizli ARG Öğeleri**
    - [ ] Dosya sistemine şifreli ipuçları gizleme.
