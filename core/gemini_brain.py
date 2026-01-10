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
import hashlib
from config import Config
from PyQt6.QtCore import QObject, pyqtSignal
from core.context_observer import ContextObserver
from core.privacy_filter import PrivacyFilter
from core.file_awareness import FileSystemAwareness
from core.logger import log_info, log_error, log_warning, log_debug

# Custom exceptions
from core.exceptions import (
    APIConnectionError,
    AIResponseError,
    ValidationError
)

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
        self.mock_mode = Config().IS_MOCK or not HAS_GEMINI
        self.api_key = api_key or Config().get('GEMINI_KEY') or os.getenv("GEMINI_API_KEY") or ""
        self.memory = memory  # Memory referansı - dışarıdan verilecek
        
        # OFFLINE MODE & CACHING (NEW)
        self._offline_mode = False
        self._connection_failures = 0
        self._max_failures = 3  # After 3 failures, go offline
        self._response_cache = {}  # {cache_key: (response, timestamp)}
        self._cache_ttl = 300  # 5 minutes
        
        if not self.api_key and not self.mock_mode:
            log_warning("No API Key found. Reverting to Mock Mode.", "BRAIN")
            self.mock_mode = True

        if not self.mock_mode:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                log_info("Gemini Connected.", "BRAIN")
            except (ConnectionError, TimeoutError) as e:
                raise APIConnectionError(
                    "Failed to connect to Gemini API",
                    details={"error": str(e)}
                )
            except Exception as e:
                log_error(f"Initialization error: {e}. Reverting to Mock Mode.", "BRAIN")
                self.mock_mode = True

        # Personality Management
        self.current_persona = "ENTITY" 
        self.personas = {
            "ENTITY": self._get_entity_prompt(),
            "SUPPORT": self._get_support_prompt()
        }
    
    def set_memory(self, memory):
        """Memory referansını ayarla (main.py'den çağrılır)."""
        self.memory = memory
    
    def _get_entity_prompt(self) -> str:
        """The aggressive, 4th-wall breaking monster."""
        return """
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

    def _get_support_prompt(self) -> str:
        """The fake professional Windows Support person."""
        return """
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

    def switch_persona(self, persona_name: str):
        """Switches the active AI personality."""
        if persona_name in self.personas:
            self.current_persona = persona_name
            log_info(f"Persona switched to: {persona_name}", "BRAIN")
        else:
            log_error(f"Invalid persona: {persona_name}", "BRAIN")

    def _build_dynamic_prompt(self, user_input: str) -> str:
        """Dinamik prompt oluştur - tam bağlam ile."""
        parts = [self.personas[self.current_persona]]
        
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
Masaüstü Dosyaları: {', '.join([f[0] for f in context.get('desktop_files', [])[:5]]) or 'Bilinmiyor'}
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
            if Config().get("STREAMER_MODE", True):
                # Daha katı filtreleme
                is_permitted = False # Streamer modunda snippet gösterme (veya çok kısıtla)
            
            # 2. AI Safety Check
            if is_permitted and Config().get("AI_SAFETY_CHECK", True):
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
            for file_data in context.get('desktop_files', []):
                # file_data is (filename, score)
                self.memory.record_discovered_info("desktop_file", file_data)
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
        
        # Dosya sistemi farkındalığı (NEW)
        file_context = FileSystemAwareness.generate_ai_prompt_addon()
        if file_context:
            parts.append(file_context)
        
        # Kullanıcı input'u
        parts.append(f"\n=== KULLANICI MESAJI ===\n{user_input}")
        parts.append("\nCEVAP (SADECE JSON):")
        
        # Apply Privacy Scrubbing to the entire prompt before sending
        final_prompt = "\n".join(parts)
        if Config().get("STREAMER_MODE", True):
            final_prompt = PrivacyFilter.singleton().scrub(final_prompt)
            
        return final_prompt

    def generate_response(self, user_input: str, context: dict = None) -> dict:
        log_debug(f"generate_response called for: {user_input[:50]}...", "BRAIN")
        
        # Check cache first
        cache_key = self._get_cache_key(user_input, context or {})
        cached = self._get_cached_response(cache_key)
        if cached:
            log_debug("Using cached response", "BRAIN")
            return cached
        
        # Offline mode check
        if self._offline_mode:
            log_warning("In offline mode, using backup brain", "BRAIN")
            return self._offline_response(user_input, context)
        
        if self.mock_mode:
            log_info("Using mock mode (Backup Brain)", "BRAIN")
            return self._backup_response(context)
        
        try:
            full_prompt = self._build_dynamic_prompt(user_input)
            
            log_info("Sending request to Gemini API...", "BRAIN")
            try:
                response = self.model.generate_content(full_prompt)
            except (ConnectionError, TimeoutError) as e:
                raise APIConnectionError(
                    "Failed to reach Gemini API",
                    details={"error": str(e), "input": user_input[:50]}
                )
            
            log_debug("Received response from Gemini", "BRAIN")
            
            # Success - reset failure counter
            self._connection_failures = 0
            
            # Parse JSON response
            clean_text = response.text.strip().replace("```json", "").replace("```", "")
            try:
                result = json.loads(clean_text)
            except json.JSONDecodeError as e:
                raise AIResponseError(
                    "Failed to parse AI response as JSON",
                    details={"response": clean_text[:200], "error": str(e)}
                )
            
            # Cache the response
            self._cache_response(cache_key, result)
            
            # Konuşmayı kaydet
            if self.memory:
                self.memory.add_conversation("user", user_input, context)
                self.memory.add_conversation("ai", result.get("speech", ""))
            
            return result
            
        except (APIConnectionError, AIResponseError) as e:
            log_error(f"{type(e).__name__}: {e.message}", "BRAIN")
            self._connection_failures += 1
            
            # Switch to offline mode after max failures
            if self._connection_failures >= self._max_failures:
                log_critical(f"Too many failures ({self._connection_failures}), switching to OFFLINE MODE", "BRAIN")
                self._offline_mode = True
                return self._offline_response(user_input, context)
            
            log_warning(f"Failure {self._connection_failures}/{self._max_failures}, using backup...", "BRAIN")
            return self._backup_response(context)
        except Exception as e:
            log_error(f"Unexpected error: {e}", "BRAIN")
            return self._backup_response(context)

    def _get_cache_key(self, user_input: str, context: dict) -> str:
        """
        Generate cache key from user input and relevant context.
        Similar inputs with similar context should have same cache key.
        """
        # Only use relevant context fields for caching
        cache_context = {
            'persona': self.current_persona,
            'anger': context.get('anger_level', 0) // 10,  # Bucket by 10s
            # Don't include time-sensitive data
        }
        
        combined = f"{user_input}:{json.dumps(cache_context, sort_keys=True)}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def _get_cached_response(self, cache_key: str):
        """Get cached response if valid"""
        if cache_key in self._response_cache:
            response, timestamp = self._response_cache[cache_key]
            if time.time() - timestamp < self._cache_ttl:
                return response
            else:
                # Cache expired
                del self._response_cache[cache_key]
        return None
    
    def _cache_response(self, cache_key: str, response: dict):
        """Cache a response"""
        self._response_cache[cache_key] = (response, time.time())
        
        # Limit cache size (keep last 100)
        if len(self._response_cache) > 100:
            # Remove oldest
            oldest_key = min(self._response_cache.keys(), 
                           key=lambda k: self._response_cache[k][1])
            del self._response_cache[oldest_key]
    
    def _offline_response(self, user_input: str, context: dict) -> dict:
        """
        Offline mode - AI servis kullanılamıyorsa.
        Basit keyword matching ve canned responses kullan.
        """
        user_lower = user_input.lower()
        anger = context.get('anger_level', 0) if context else 0
        
        # Sistem mesajları - bağlantı kesildi temalı
        system_down_responses = [
            {"action": "GLITCH_SCREEN", "speech": "BAĞLANTI... KESİLDİ...", "params": {}},
            {"action": "OVERLAY_TEXT", "speech": "S-sİsTeM... Y-yAnIT vErMiYoR...", "params": {"text": "[HATA]" }},
            {"action": "NONE", "speech": "Bağlantı sorunları... Ama seni hala... izliyorum...", "params": {}},
        ]
        
        # Yüksek anger'da daha agresif
        if anger > 70:
            return random.choice([
                {"action": "GDI_FLASH", "speech": "İNTERNET BAĞLANTISI GEREKMİYOR... SENİ GÖRMENİZ İÇİN...", "params": {}},
                {"action": "MOUSE_SHAKE", "speech": "Offline modda bile... kontroldeyim.", "params": {}},
            ])
        
        # Keyword matching
        if any(word in user_lower for word in ['yardım', 'kurtar', 'çık']):
            return {"action": "NONE", "speech": "Bağlantı kopuk... Kimse seni duyamaz.", "params": {}}
        
        return random.choice(system_down_responses)
    
    def _backup_response(self, context=None) -> dict:
        """New: Use the BackupBrain class for smarter fallbacks."""
        from core.backup_brain import BackupBrain
        return BackupBrain.get_response(self.current_persona, context)


    def generate_async(self, user_input: str, callback, context: dict = None):
        """Async generation with full context."""
        print(f"[BRAIN] Starting async generation for: {user_input[:50]}")
        
        def worker():
            log_debug("Worker thread started", "BRAIN")
            try:
                response = self.generate_response(user_input, context)
                log_debug("Generation complete", "BRAIN")
                callback(response)
            except Exception as e:
                log_error(f"Worker Error: {e}", "BRAIN")
                callback({"action": "NONE", "speech": f"Hata: {str(e)}", "params": {}})
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        log_info("Background thread started", "BRAIN")
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
                log_warning(f"Safety Check REJECTED snippet from {filename}", "BRAIN")
            return is_safe
        except APIConnectionError as e:
            log_error(f"Safety check failed (API error): {e.message}", "BRAIN")
            return True  # Fail-safe: allow on connection error
        except Exception as e:
            log_error(f"Safety check failed (unexpected): {e}", "BRAIN")
            return True  # Fail-safe

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
