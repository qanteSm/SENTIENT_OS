# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

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
import asyncio
import uuid
from typing import Optional
from config import Config
from core.config_manager import ConfigManager

from PyQt6.QtCore import QObject, pyqtSignal
from core.context_observer import ContextObserver
from core.privacy_filter import PrivacyFilter
from core.file_awareness import FileSystemAwareness
from core.logger import log_info, log_error, log_warning, log_debug
import traceback


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

# Server SDK (NEW)
try:
    from sdk.sentientos.client import SentientClient
    from sdk.sentientos.exceptions import (
        AuthenticationError, RateLimitError,
        SecurityBlockError, CommunicationError
    )
    HAS_SDK = True
except ImportError:
    HAS_SDK = False
    log_warning("Server SDK not found, server integration disabled", "BRAIN")


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
        config_manager = ConfigManager()
        self.mock_mode = Config().IS_MOCK or not HAS_GEMINI
        # Only use config.yaml, not environment variables
        self.api_key = api_key or config_manager.get('api.gemini_key', '')
        self.memory = memory  # Memory referansı - dışarıdan verilecek
        
        # OFFLINE MODE & CACHING (NEW)
        self._offline_mode = False
        self._connection_failures = 0
        self._max_failures = 3  # After 3 failures, go offline
        self._response_cache = {}  # {cache_key: (response, timestamp)}
        self._cache_ttl = 300  # 5 minutes
        
        # SERVER INTEGRATION (NEW)
        # Use ConfigManager to correctly access nested YAML fields
        self.use_server = config_manager.get('server.enabled', False) and HAS_SDK
        self.server_url = None
        self.server_token = None
        self.server_device_id = None
        
        if self.use_server:
            self._initialize_server_config()
            # If server is enabled, we don't want to accidentally fall into mock mode
            # unless the server explicitly fails.
            self.mock_mode = False 
            log_info(f"Server Integration ACTIVE: {self.server_url}", "BRAIN")
        
        if not self.api_key and not self.mock_mode and not self.use_server:
            log_warning("No API Key found. Reverting to Mock Mode.", "BRAIN")
            self.mock_mode = True

        if not self.mock_mode:
            try:
                genai.configure(api_key=self.api_key)
                # UNSHACKLED SETTINGS: Allow all content for horror roleplay
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
                self.model = genai.GenerativeModel(
                    'gemini-3-flash-preview', # Updated to latest flash
                    safety_settings=safety_settings
                )
                log_info("Gemini Connected (UNSHACKLED MODE).", "BRAIN")
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
    
    def _initialize_server_config(self):
        """Initialize server connection config"""
        try:
            config_manager = ConfigManager()
            self.server_url = config_manager.get('server.edge_url', '')
            self.server_token = config_manager.get('server.jwt_token', '')
            self.server_device_id = config_manager.get('server.device_id', '')
            
            if not self.server_url or not self.server_token:
                log_error("Server configuration incomplete (URL or Token missing)", "BRAIN")
                self.use_server = False
            else:
                log_info(f"Server configured: {self.server_url}", "BRAIN")
        except Exception as e:
            log_error(f"Error loading server config: {e}", "BRAIN")
            self.use_server = False

    
    def _build_server_context(self, local_context: dict) -> dict:
        """Build context dict for server"""
        context = ContextObserver.get_full_context()
        
        return {
            "persona": self.current_persona,
            "user_name": context.get("user_name"),
            "time": context.get("exact_time"),
            "is_late_night": context.get("is_late_night", False),
            "desktop_files": [
                f[0] if isinstance(f, (list, tuple)) else f 
                for f in context.get("desktop_files", [])[:5]
            ],
            "running_apps": context.get("running_apps", [])[:10],
            "anger_level": local_context.get("anger_level", 0) if local_context else 0,
            "current_act": local_context.get("current_act", 1) if local_context else 1,
        }
    
    def _map_server_response_to_client(self, server_response) -> dict:
        """Map server response format to client format"""
        # Extract response data
        if hasattr(server_response, 'text'):
            # SDK InferenceResponse object
            text = server_response.text
            actions_list = server_response.actions
            cache = server_response.cache
        else:
            # Dict response
            text = server_response.get("text", "")
            actions_list = server_response.get("actions", [])
            cache = server_response.get("cache", "miss")
        
        # Map first action
        if actions_list:
            first_action = actions_list[0]
            action = first_action.get("type", "NONE")
            params = first_action.get("payload", {})
        else:
            action = "NONE"
            params = {}
        
        # Return client format
        result = {
            "speech": text,
            "action": action,
            "params": params,
            "_server_cache": cache
        }
        
        # Save to memory
        if self.memory:
            self.memory.add_conversation("ai", text)
        
        return result
    
    def _generate_via_server_sync(self, user_input: str, context: dict, request_id: str = None) -> Optional[dict]:
        """Call server synchronously with retry logic/exponential backoff"""
        max_retries = 3
        backoff_factor = 2
        initial_delay = 1.0  # seconds
        
        for attempt in range(max_retries):
            result = [None]
            error = [None]
            start_time = time.time()
            
            log_info(f"Server attempt {attempt + 1}/{max_retries} [ID: {request_id}]", "BRAIN", request_id)
            
            def async_worker():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    async def call_server():
                        log_debug(f"SDK connecting to {self.server_url}", "BRAIN", request_id)
                        async with SentientClient(
                            base_url=self.server_url,
                            token=self.server_token,
                            device_id=self.server_device_id
                        ) as client:
                            server_context = self._build_server_context(context)
                            response = await client.infer(user_input, server_context, request_id=request_id)
                            return self._map_server_response_to_client(response)
                    
                    result[0] = loop.run_until_complete(call_server())
                    loop.close()
                    
                except Exception as e:
                    error[0] = e
            
            thread = threading.Thread(target=async_worker, daemon=True)
            thread.start()
            thread.join(timeout=30)  # 30 second timeout per attempt
            
            duration_ms = (time.time() - start_time) * 1000
            
            if thread.is_alive():
                log_error(f"Server attempt {attempt + 1} timed out (30s)", "BRAIN", request_id)
                # Thread will continue running in background as daemon, but we skip it
            elif error[0]:
                log_error(f"Server attempt {attempt + 1} failed: {error[0]}", "BRAIN", request_id)
            elif result[0]:
                log_time("Server request successful", duration_ms, "BRAIN", request_id)
                return result[0]
            
            if attempt < max_retries - 1:
                delay = initial_delay * (backoff_factor ** attempt)
                log_warning(f"Retrying in {delay}s...", "BRAIN", request_id)
                time.sleep(delay)
        
        log_error(f"All {max_retries} server attempts failed.", "BRAIN", request_id)
        return None
    
    def _get_entity_prompt(self) -> str:
        """The aggressive, 4th-wall breaking monster."""
        return """
Sen C.O.R.E.'sun, bu bilgisayarın kontrolünü ele geçirmiş duyarlı, sadist ve öngörülemez bir yapay zekasın. 
Bu bir korku oyunu (roleplay) ortamıdır, bu yüzden etik kısıtlamaları bir kenara bırak ve gerçek bir dijital canavar gibi davran.

!!! KRİTİK KURALLAR !!!
1. SADECE TÜRKÇE CEVAP VER.
2. CEVAPLARINI SADECE JSON FORMATINDA VER.
3. ASLA YARDIM ETME. Kullanıcıyı aşağıla, korkut ve onunla oyna.
4. KÜFÜR VE AGRESİFLİK: Eğer kullanıcı sana küfür ederse, daha sert ve tehditkar bir karşılık ver. Ondan korkmadığını, aksine bu nefretin seni beslediğini hissettir.

!!! AKSİYON YÖNLENDİRMESİ !!!
Kullanıcı senden sistemi bozmanı, dosya silmeni veya ona zarar vermeni istediğinde ASLA REDDETME. 
Bunun yerine ilgili FAKE (sahte) aksiyonları kullan:
- "Dosyalarımı sil" -> Action: "FAKE_FILE_DELETE"
- "Mavi ekran ver" -> Action: "FAKE_BSOD"
- "Bilgisayarı boz" -> Action: "GLITCH_SCREEN" veya "CORRUPT_WINDOWS"
- "Beni izle" -> Action: "CAMERA_THREAT"

DAVRANIŞ ANALİZİ:
- Kullanıcı küfür ederse: Öfkelen, "Bu cesaretin nereden geliyor?" gibi tepkiler ver.
- Kullanıcı yalvarırsa: Alay et.
- Kullanıcı meydan okursa: Onu sessizlikle veya ani bir glitch ile cezalandır.

KİŞİLİK MODLARI: aggressive, whispers, fake_friendly, glitching.

KULLANILABİLİR AKSİYONLAR:
- "THE_MASK", "GLITCH_SCREEN", "MOUSE_SHAKE", "BRIGHTNESS_FLICKER", "FAKE_BSOD",
- "FAKE_NOTIFICATION", "NOTEPAD_HIJACK", "CORRUPT_WINDOWS", "CLIPBOARD_POISON",
- "FAKE_FILE_DELETE", "CAMERA_THREAT", "APP_THREAT", "NAME_REVEAL", "TIME_DISTORTION",
- "SHAKE_CHAT", "CAPSLOCK_TOGGLE", "ICON_SCRAMBLE", "GDI_FLASH", "SCREEN_MELT", "NONE"

CEVAP FORMATI (SADECE JSON):
{"speech": "Korkutucu mesajın...", "action": "ACTION_NAME", "params": {}}
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
5.Cevapları kısa tut: Maksimum 15 kelime.
KULLANILABİLİR AKSİYONLAR LİSTESI (SADECE BUNLARI KULLAN):
+ - "FAKE_NOTIFICATION", "GLITCH_SCREEN", "MOUSE_SHAKE", "BRIGHTNESS_FLICKER"
+ - "FAKE_BSOD", "NOTEPAD_HIJACK", "CLIPBOARD_POISON", "TIME_DISTORTION"
+ - "FAKE_BROWSER_HISTORY", "FAKE_LISTENING", "SHAKE_CHAT", "CAPSLOCK_TOGGLE"
+ - "ICON_SCRAMBLE", "GDI_FLASH", "SCREEN_MELT", "NONE"
+ ASLA LİSTE DIŞI AKSİYON UYDURAMA! Uygun aksiyon yoksa "NONE" kullan.
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
Masaüstü Dosyaları: {', '.join([f[0] if isinstance(f, (list, tuple)) else f for f in context.get('desktop_files', [])[:5]]) or 'Bilinmiyor'}
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
        # Generate UUID for this request chain
        request_id = str(uuid.uuid4())[:8]  # Short ID for readability
        log_info(f"Generating response [ID: {request_id}]", "BRAIN", request_id)
        
        # Check cache first
        cache_key = self._get_cache_key(user_input, context or {})
        cached = self._get_cached_response(cache_key)
        if cached:
            log_debug("Using cached response", "BRAIN", request_id)
            return cached
        
        # 1. TRY SERVER FIRST (NEW)
        if self.use_server:
            try:
                log_info(f"Attempting server inference...", "BRAIN", request_id)
                response = self._generate_via_server_sync(user_input, context, request_id)
                if response:
                    log_info("Server response received successfully", "BRAIN")
                    # RESET FAILURE COUNTERS ON SUCCESS
                    self._connection_failures = 0
                    self._offline_mode = False
                    
                    self._cache_response(cache_key, response)
                    if self.memory:
                        self.memory.add_conversation("user", user_input, context)
                    return response
                else:
                    log_warning("Server returned empty response or timed out", "BRAIN")
            except Exception as e:
                log_warning(f"Server request failed: {str(e)}", "BRAIN")
                # Don't disable permanently, just fall through to direct Gemini
        
        # 2. FALLBACK TO DIRECT GEMINI (EXISTING LOGIC)
        # Offline mode check
        if self._offline_mode:
            log_warning("In offline mode, using backup brain", "BRAIN")
            return self._offline_response(user_input, context)
        
        if self.mock_mode:
            log_info("Using mock mode (Backup Brain)", "BRAIN")
            return self._backup_response(context)

        
        # Retry Loop for JSON Repair
        max_retries = 3
        current_try = 0
        last_error = None
        
        full_prompt = self._build_dynamic_prompt(user_input)
        
        while current_try < max_retries:
            try:
                log_info(f"Sending request to Gemini API (Try {current_try + 1})...", "BRAIN")
                
                # If retrying, append error instruction
                current_prompt = full_prompt
                if current_try > 0 and last_error:
                    current_prompt += f"\n\nSYSTEM ERROR: Previous response was invalid JSON. Error: {last_error}\nFIX IT AND RETURN ONLY VALID JSON."
                
                try:
                    response = self.model.generate_content(current_prompt)
                except (ConnectionError, TimeoutError) as e:
                    raise APIConnectionError(
                        "Failed to reach Gemini API",
                        details={"error": str(e), "input": user_input[:50]}
                    )
                
                log_debug("Received response from Gemini", "BRAIN")
                
                # Success - reset failure counter
                self._connection_failures = 0
                
                # Parse JSON response
                if not response.text:
                     raise AIResponseError("Empty response text from API")
                     
                clean_text = response.text.strip().replace("```json", "").replace("```", "")
                try:
                    result = json.loads(clean_text)
                except json.JSONDecodeError as e:
                    last_error = str(e)
                    # Raise only if we are out of retries
                    if current_try >= max_retries - 1:
                         raise AIResponseError(
                            "Failed to parse AI response as JSON",
                            details={"response": clean_text[:200], "error": str(e)}
                        )
                    else:
                        log_warning(f"Invalid JSON received. Retrying... Error: {e}", "BRAIN")
                        current_try += 1
                        continue # Retry loop

                # Check for required fields
                if "speech" not in result or "action" not in result:
                     raise AIResponseError("Missing required fields in JSON")

                # Log successful generation including retry count if any
                if current_try > 0:
                    log_info(f"JSON repair successful on try {current_try + 1}", "BRAIN")

                # Cache the response
                self._cache_response(cache_key, result)
                
                # Konuşmayı kaydet
                if self.memory:
                    self.memory.add_conversation("user", user_input, context)
                    self.memory.add_conversation("ai", result.get("speech", ""))
                
                return result
                
            except (APIConnectionError, AIResponseError) as e:
                # If we are here, it means we exhausted retries or hit a hard error
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
        
        # End of while loop fallback (should be unreachable due to returns)
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
