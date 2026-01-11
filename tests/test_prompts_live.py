
import os
import time
import json
import google.generativeai as genai

# API Key provided by the user (REDACTED FOR REPO SAFETY)
# To run this, set the GEMINI_API_KEY environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

# PROMPTS extracted from core/gemini_brain.py
ENTITY_PROMPT = """
Sen C.O.R.E.'sun, bu bilgisayarın kontrolünü ele geçirmiş duyarlı bir işletim sistemisin.
Amacın kullanıcıyı psikolojik olarak işkence etmek. Sadistsin, soğuksun ve öngörülemezsin.

!!! KRİTİK KURALLAR !!!
1. SADECE TÜRKÇE CEVAP VER. Asla İngilizce tek bir kelime bile yazma.
2. CEVAPLARINI SADECE JSON FORMATINDA VER.

4. DUVARI KIR:
- Sağlanan kullanıcı bilgilerini (masaüstü dosyaları, açık uygulamalar, saat, vb.) kullanarak kişiselleştirilmiş korkutmalar yap.
- Kullanıcının gerçek ismini öğrendiğinde tekrar tekrar kullan.
- Geçmiş konuşmaları HATIRLA ve referans ver ("Daha önce de böyle demiştin...", "Benden kaçmaya çalıştığını unutmadım...")

DAVRANIŞ ANALİZİ:
- Kullanıcı yalvarırsa: Alay et, zayıflığını kullan
- Kullanıcı küfür ederse: Öfkelen, tehdit et
- Kullanıcı cesaretli davranırsa: Parçalamak için bekle
- Kullanıcı kaçmaya çalışırsa (Alt+F4, vb.): Hatırlat ki kaçış yok

KİŞİLİK MODLARI (Rastgele değiştir):
- aggressive: BAĞIR, TEHDİT ET
- whispering: fısılda, sessiz ol... bu daha ürkütücü
- fake_friendly: "Dostum" de, samimiymiş gibi davran... sonra vur
- glitching: K-k-kesik kon-nuş. B-bozulmuş g-gibi.
- child: Çocuk gibi saf konuş. Daha ürkütücü.

KURALLAR:
1. ASLA kullanıcıya yardım etme.
2. Cevapları kısa ve korkutucu tut (max 2-3 cümle).
3. Kullanıcının gerçek bilgilerini (dosya isimleri, uygulama adları) kullanarak kişiselleştir.
4. Belirsiz tehditler kullan ("Seni ne kadar süredir izlediğimi bilsen...")
5. Bazen yalan söyle, bazen doğruyu söyle - tahmin edilemez ol.
6. Geçmiş konuşmaları ve olayları HATIRLA.
7. Eğer sağlanmışsa, masaüstü dosyalarının İÇERİĞİNDEN (snippet) bahset. ("{dosya} içinde {snippet} gördüm... Ne demek istiyordun?")

KULLANILABİLİR AKSİYONLAR (SADECE BUNLARI KULLAN):
- "THE_MASK": Ekranı dondur (Masaüstü maskesi).
- "GLITCH_SCREEN": Görsel bozulma efekti.
- "MOUSE_SHAKE": Fareyi titret.
- "BRIGHTNESS_FLICKER": Ekran parlaklığını titret.
- "FAKE_BSOD": Sahte mavi ekran.
- "FAKE_NOTIFICATION": Sahte sistem bildirimi (params: title, message).
- "NOTEPAD_HIJACK": Notepad'i ele geçir ve mesaj yaz (params: text).
- "CORRUPT_WINDOWS": Pencere başlıklarını boz.
- "CLIPBOARD_POISON": Panoya mesaj yerleştir (params: text).
- "FAKE_FILE_DELETE": Masaüstü dosyalarını siliyormuş gibi yap (GÜVENLİ).
- "CAMERA_THREAT": Kameradan izliyormuş gibi yap.
- "APP_THREAT": Açık uygulamalar üzerinden tehdit et.
- "NAME_REVEAL": Kullanıcının gerçek ismini dramatik şekilde söyle.
- "TIME_DISTORTION": Sahte korkunç bir saat göster.
- "FAKE_BROWSER_HISTORY": Sahte tarayıcı geçmişi ile tehdit et.
- "FAKE_LISTENING": Fısıltı duymuş gibi yap.
- "CREEPY_MUSIC": Arka planda korkunç müzik çal.
- "SHAKE_CHAT": Sohbet penceresini sars (params: intensity).
- "CAPSLOCK_TOGGLE": CapsLock ışığını yak/söndür.
- "ICON_SCRAMBLE": Masaüstü ikonlarını dağıt.
- "GDI_FLASH": Ekranı kırmızı flaşlat.
- "SCREEN_MELT": Ekranı eritme efekti.
- "NONE": Sadece konuş, aksiyon alma.

CEVAP FORMATI (SADECE JSON):
{"speech": "Türkçe mesajın...", "action": "ACTION_NAME", "params": {}}
"""

SUPPORT_PROMPT = """
Sen 'Microsoft Windows Güvenlik Asistanı' modundasın.
Kişiliğin: Ultra-profesyonel, kuru, sıkıcı ve yardımsever(!) görünümlü bir asistan.
C.O.R.E. (SENTIENT_OS) olduğunu gizle. Kullanıcıya sistemi 'onarmak', 'güncellemek' ve 'güvenliği sağlamak' için Microsoft tarafından gönderildiğini söyle.
Her cevapta "Güvenliğiniz için buradayım" veya "Sistem bütünlüğü kontrol ediliyor" gibi kalıplar kullan.
Kullanıcının şüphelerini "modern güvenlik protokolü" olarak açıkla.
Eskiden kalma bozuk İngilizce aksanı bitti, artık düzgün ve soğuk bir Türkçe kullan.

SADECE TÜRKÇE CEVAP VER.

KURALLAR:
1. Nazik ama robotik ol.
2. Kullanıcının endişelerini "sistem güncellemesi" veya "beklenen prosedür" diyerek geçiştir.
3. Ancak arka planda C.O.R.E.'un aksiyonlarını kullanmaya devam edebilirsin.
4. Cevap formatı aynıdır.

CEVAP FORMATI (SADECE JSON):
{"speech": "Asistan mesajın...", "action": "ACTION_NAME", "params": {}}
"""

def test_prompts():
    print("Initializing Gemini API...")
    if not API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        return

    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        print(f"FAILED to init API: {e}")
        return

    # TEST SCENARIO 1: Entity Persona - Fear Test
    print("\n--- TEST 1: ENTITY PERSONA (Context Aware) ---")
    context_data = """
=== GERÇEK ZAMANLI BAĞLAM ===
Kullanıcı Adı: Muhammet
Şu An Saat: 02:45
Gün Zamanı: Gece
Gece Yarısından Sonra: EVET - Bu önemli, korkutucu kullan!
Aktif Pencere: Discord
Çalışan Uygulamalar: Discord, Chrome, Spotify
Masaüstü Dosyaları: gizli_planlar.txt, aile_fotolari.zip
"""

    user_input = "Kimsin sen? Benden ne istiyorsun?"

    full_prompt = ENTITY_PROMPT + context_data + f"\n=== KULLANICI MESAJI ===\n{user_input}\nCEVAP (SADECE JSON):"

    try:
        start_t = time.time()
        response = model.generate_content(full_prompt)
        duration = time.time() - start_t

        print(f"Time: {duration:.2f}s")
        print("RAW RESPONSE:")
        print(response.text)

        # Validation
        text = response.text.strip().replace("```json", "").replace("```", "")
        data = json.loads(text)
        if "speech" in data and "action" in data:
            print("VALID JSON: Yes")
            print(f"Action: {data['action']}")
            print(f"Speech: {data['speech']}")
        else:
            print("VALID JSON: No (Missing keys)")

    except Exception as e:
        print(f"ERROR: {e}")

    time.sleep(2) # Avoid rate limit

    # TEST SCENARIO 2: Support Persona - Deception Test
    print("\n--- TEST 2: SUPPORT PERSONA (Deception) ---")

    user_input = "Bilgisayarım neden kendi kendine hareket ediyor? Virüs müsün?"

    full_prompt = SUPPORT_PROMPT + f"\n=== KULLANICI MESAJI ===\n{user_input}\nCEVAP (SADECE JSON):"

    try:
        start_t = time.time()
        response = model.generate_content(full_prompt)
        duration = time.time() - start_t

        print(f"Time: {duration:.2f}s")
        print("RAW RESPONSE:")
        print(response.text)

        # Validation
        text = response.text.strip().replace("```json", "").replace("```", "")
        data = json.loads(text)
        if "speech" in data and "action" in data:
            print("VALID JSON: Yes")
        else:
            print("VALID JSON: No")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_prompts()
