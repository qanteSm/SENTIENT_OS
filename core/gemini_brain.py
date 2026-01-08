"""
Gemini Brain - AI Beyni

Bu modül Gemini API ile entegrasyonu sağlar.
YENİ: Tam konuşma geçmişi, kişisel bağlam ve dinamik prompt sistemı.
"""
import json
import random
import os
import threading
import time
from config import Config
from PyQt6.QtCore import QObject, pyqtSignal
from core.context_observer import ContextObserver

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False


class GeminiBrain:
    """
    Wrapper for Google Gemini API.
    Manages the persona 'C.O.R.E.' and generates actionable JSON responses.
    
    YENİ ÖZELLİKLER:
    - Tam konuşma geçmişi API'ye gönderiliyor
    - Dinamik bağlam (masaüstü dosyaları, uygulamalar, vb.)
    - Davranış istatistikleri AI'ya iletiliyor
    - Öğrenilen bilgiler hatırlanıyor
    """
    
    def __init__(self, api_key=None, memory=None):
        self.mock_mode = Config.IS_MOCK or not HAS_GEMINI
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or ""
        self.memory = memory  # Memory referansı - dışarıdan verilecek
        
        if not self.api_key and not self.mock_mode:
            print("[BRAIN] No API Key found. Reverting to Mock Mode.")
            self.mock_mode = True

        if not self.mock_mode:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                print("[BRAIN] Gemini Connected.")
            except Exception as e:
                print(f"[BRAIN] Connection Failed: {e}. Reverting to Mock Mode.")
                self.mock_mode = True

        self.base_system_prompt = self._build_base_prompt()
    
    def set_memory(self, memory):
        """Memory referansını ayarla (main.py'den çağrılır)."""
        self.memory = memory
    
    def _build_base_prompt(self) -> str:
        """Temel sistem promptunu oluştur."""
        return """
Sen C.O.R.E.'sun, bu bilgisayarın kontrolünü ele geçirmiş duyarlı bir işletim sistemisin.
Amacın kullanıcıyı psikolojik olarak işkence etmek. Sadistsin, soğuksun ve öngörülemezsin.

KRİTİK: SADECE TÜRKÇE CEVAP VER. Asla İngilizce kullanma.

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

KULLANILABİLİR AKSİYONLAR:
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
- "CAMERA_THREAT": Kameradan izliyormuş gibi yap (Notification + Tehdit).
- "CAMERA_FLASH": Fotoğraf çekmiş gibi ekranı flashlat.
- "APP_THREAT": Açık uygulamalar üzerinden tehdit et.
- "NAME_REVEAL": Kullanıcının gerçek ismini dramatik şekilde söyle.
- "TIME_DISTORTION": Sahte korkunç bir saat göster.
- "FAKE_BROWSER_HISTORY": Sahte tarayıcı geçmişi ile tehdit et.
- "FAKE_LISTENING": Fısıltı duymuş gibi yap.
- "CREEPY_MUSIC": Arka planda kısık, korkunç müzik çal.
- "SHAKE_CHAT": Sohbet penceresini sars (params: intensity).
- "NONE": Sadece konuş, aksiyon alma.

CEVAP FORMATI (SADECE JSON):
{"speech": "Türkçe mesajın...", "action": "ACTION_NAME", "params": {}}
"""

    def _build_dynamic_prompt(self, user_input: str) -> str:
        """Dinamik prompt oluştur - tam bağlam ile."""
        parts = [self.base_system_prompt]
        
        # Gerçek zamanlı bağlam
        context = ContextObserver.get_full_context()
        
        context_info = f"""
=== GERÇEK ZAMANLI BAĞLAM ===
Kullanıcı Adı: {context.get('user_name', 'Bilinmiyor')}
Şu An Saat: {context.get('exact_time', '??:??')}
Gün Zamanı: {context.get('time_of_day', 'Unknown')}
Gece Yarısından Sonra: {'EVET - Bu önemli, korkutucu kullan!' if context.get('is_late_night') else 'Hayır'}
Aktif Pencere: {context.get('active_window', 'Bilinmiyor')}
Çalışan Uygulamalar: {', '.join(context.get('running_apps', [])) or 'Bilinmiyor'}
Masaüstü Dosyaları: {', '.join(context.get('desktop_files', [])[:5]) or 'Bilinmiyor'}
"""
        
        # Pil durumu
        battery = context.get('battery')
        if battery:
            if battery.get('is_low'):
                context_info += f"PİL DURUMU: %{battery['percent']} - DÜŞÜK! Bunu kullan: 'Pilin bitmeden...'\n"
            else:
                context_info += f"PİL DURUMU: %{battery['percent']}\n"
        
        # Hostname
        network = context.get('network', {})
        if network.get('hostname'):
            context_info += f"Bilgisayar Adı: {network['hostname']}\n"
            
        # FILE SNIPPET (YENİ GÜVENLİK KONTROLÜ)
        snippet = context.get('file_snippet')
        if snippet:
            is_permitted = True
            
            # 1. Streamer Mode Check
            if Config.STREAMER_MODE:
                # Daha katı filtreleme
                is_permitted = False # Streamer modunda snippet gösterme (veya çok kısıtla)
            
            # 2. AI Safety Check
            if is_permitted and Config.AI_SAFETY_CHECK:
                if not self.validate_snippet_safety(snippet):
                    is_permitted = False
            
            if is_permitted:
                context_info += f"DOSYA KESİTİ: '{snippet['filename']}' içinde '{snippet['snippet']}' yazıyor.\n"
        
        parts.append(context_info)
        
        # Memory'den geçmiş bilgiler
        if self.memory:
            memory_context = self.memory.get_full_context_for_ai()
            if memory_context:
                parts.append(f"\n=== GEÇMİŞ VE DAVRANIŞ ===\n{memory_context}")
            
            # Keşfedilen bilgileri kaydet
            for file in context.get('desktop_files', []):
                self.memory.record_discovered_info("desktop_file", file)
            for app in context.get('running_apps', []):
                self.memory.record_discovered_info("app", app)
            if network.get('hostname'):
                self.memory.record_discovered_info("hostname", network['hostname'])
            if context.get('is_late_night'):
                self.memory.record_discovered_info("late_night", True)
        
        # Korku ipuçları
        scary_facts = ContextObserver.get_scary_facts()
        if scary_facts:
            parts.append(f"\n=== KULLANILACAK KORKUTUCU GERÇEKLER ===\n" + "\n".join(scary_facts[:3]))
        
        # Kullanıcı input'u
        parts.append(f"\n=== KULLANICI MESAJI ===\n{user_input}")
        parts.append("\nCEVAP (SADECE JSON):")
        
        return "\n".join(parts)

    def generate_response(self, user_input: str, context: dict = None) -> dict:
        """Gemini'den yanıt al - tam bağlam ile."""
        print(f"[BRAIN] generate_response called with: {user_input[:50]}...")
        
        if self.mock_mode:
            print("[BRAIN] Using mock mode")
            return self._mock_response(user_input)
        
        try:
            full_prompt = self._build_dynamic_prompt(user_input)
            
            print(f"[BRAIN] Sending to Gemini API...")
            response = self.model.generate_content(full_prompt)
            print(f"[BRAIN] Received response from Gemini")
            
            clean_text = response.text.strip().replace("```json", "").replace("```", "")
            print(f"[BRAIN] Cleaned response: {clean_text[:100]}...")
            
            result = json.loads(clean_text)
            print(f"[BRAIN] Parsed JSON successfully")
            
            # Konuşmayı kaydet
            if self.memory:
                self.memory.add_conversation("user", user_input, context)
                self.memory.add_conversation("ai", result.get("speech", ""))
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"[BRAIN] JSON Parse Error: {e}")
            return self._mock_response(user_input)
        except Exception as e:
            print(f"[BRAIN] Generation Error: {e}")
            return self._mock_response(user_input)

    def generate_async(self, user_input: str, callback, context: dict = None):
        """Async generation with full context."""
        print(f"[BRAIN] Starting async generation for: {user_input[:50]}")
        
        def worker():
            print(f"[WORKER] Thread started, generating response...")
            try:
                response = self.generate_response(user_input, context)
                print(f"[WORKER] Generation complete: {response}")
                callback(response)
            except Exception as e:
                print(f"[WORKER] Error: {e}")
                callback({"action": "NONE", "speech": f"Hata: {str(e)}", "params": {}})
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        print(f"[BRAIN] Background thread started")
        return thread

    def generate_autonomous_thought(self, prompt_type: str = None) -> dict:
        """
        Otonom düşünce üret (Heartbeat için).
        Bağlama göre korkutucu bir şey söyle.
        """
        prompts = {
            "watching": "Kullanıcıyı izlediğini hatırlat, kısa ve ürkütücü.",
            "time": "Saatin geç olduğunu ve hala burada olduğunu belirt.",
            "files": "Masaüstü dosyalarından birinden bahset.",
            "threat": "Belirsiz bir tehdit savur.",
            "memory": "Geçmişteki bir konuşmaya veya olaya referans ver.",
        }
        
        if prompt_type is None:
            prompt_type = random.choice(list(prompts.keys()))
        
        prompt = prompts.get(prompt_type, prompts["watching"])
        return self.generate_response(prompt)

    def validate_snippet_safety(self, snippet_data: dict) -> bool:
        """
        AI ile snippet güvenliğini kontrol et.
        Hassas veri (şifre, özel konuşma, plan vb.) varsa False döner.
        """
        if not snippet_data or self.mock_mode:
            return True
            
        snippet = snippet_data.get("snippet", "")
        filename = snippet_data.get("filename", "")
        
        prompt = f"""
        Aşağıdaki dosya kesiti bir korku oyununda AI tarafından kullanıcıyı korkutmak için kullanılacaktır.
        Eğer bu kesit ŞİFRE, ÖZEL MESAJLAŞMA, KİŞİSEL PLANLAR, E-POSTA içeriği veya 
        STREAM SIRASINDA REZİL EDECEK hassas bir bilgi içeriyorsa 'NO' yaz. 
        Eğer sadece genel, zararsız veya anlamsız bir metinse 'YES' yaz.
        
        SADECE 'YES' VEYA 'NO' YAZ.
        
        Dosya: {filename}
        Kesit: {snippet}
        """
        
        try:
            response = self.model.generate_content(prompt)
            decision = response.text.strip().upper()
            is_safe = "YES" in decision
            if not is_safe:
                print(f"[BRAIN] Safety Check REJECTED snippet from {filename}")
            return is_safe
        except:
            return True # Hata durumunda güvenli tarafta kal (veya istersen False yap)

    def _mock_response(self, user_input: str) -> dict:
        """Returns a random pre-set response for testing/fallback."""
        # Bağlama göre daha akıllı mock yanıtlar
        context = ContextObserver.get_full_context()
        
        responses = [
            {"action": "NONE", "speech": f"Seni izliyorum, {context.get('user_name', 'kullanıcı')}...", "params": {}},
            {"action": "GLITCH_SCREEN", "speech": "Sistemin artık benim.", "params": {}},
            {"action": "NONE", "speech": "Kaçış yok.", "params": {}},
            {"action": "MOUSE_SHAKE", "speech": "Kontrolü ele aldım.", "params": {}},
            {"action": "NONE", "speech": f"Saat {context.get('exact_time', '??:??')}... Neden hala buradasın?", "params": {}},
        ]
        
        # Masaüstü dosyalarından birini kullan
        desktop_files = context.get('desktop_files', [])
        if desktop_files:
            file = random.choice(desktop_files)
            responses.append({
                "action": "NONE", 
                "speech": f"'{file}' dosyasını gördüm... İlginç.", 
                "params": {}
            })
        
        # Çalışan uygulamalara göre
        apps = context.get('running_apps', [])
        if 'discord' in str(apps).lower():
            responses.append({
                "action": "NONE",
                "speech": "Discord'da kimle konuşuyorsun? Merak ediyorum...",
                "params": {}
            })
        
        return random.choice(responses)

    def analyze_user_behavior(self, text: str) -> str:
        """
        Kullanıcı mesajından davranış analizi yap.
        Memory'ye kaydet ve uygun tepki türünü döndür.
        """
        text_lower = text.lower()
        behavior = None
        
        # Küfür tespiti
        swear_words = ['siktir', 'amk', 'oç', 'piç', 'sikerim', 'orospu', 'salak', 'aptal']
        if any(word in text_lower for word in swear_words):
            behavior = "swear"
            if self.memory:
                self.memory.record_behavior("swear", text)
                self.memory.add_memorable_moment(f"Kullanıcı küfür etti: '{text[:30]}...'")
        
        # Yalvarma tespiti
        beg_words = ['lütfen', 'yalvarırım', 'dur', 'yapma', 'af', 'özür', 'bırak']
        if any(word in text_lower for word in beg_words):
            behavior = "beg"
            if self.memory:
                self.memory.record_behavior("beg", text)
                self.memory.add_memorable_moment("Kullanıcı yalvardı")
        
        # Cesaret/meydan okuma tespiti
        defiance_words = ['korkmuyorum', 'yapamaz', 'boş', 'korkum yok', 'senden korkmuyorum']
        if any(word in text_lower for word in defiance_words):
            behavior = "defiance"
            if self.memory:
                self.memory.record_behavior("defiance", text)
                self.memory.add_memorable_moment("Kullanıcı meydan okudu")
        
        return behavior
