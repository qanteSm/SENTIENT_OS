from config import Config
from PyQt6.QtCore import QTimer
import random
import time

# Windows Imports
try:
    if Config().IS_MOCK:
        raise ImportError("Mock Mode")
    import pyttsx3
    HAS_PYTTSX3 = True
except ImportError:
    HAS_PYTTSX3 = False
    pyttsx3 = None

try:
    if Config().IS_MOCK:
        raise ImportError("Mock Mode")
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    HAS_PYCAW = True
except ImportError:
    HAS_PYCAW = False
    AudioUtilities = None
    IAudioEndpointVolume = None

from hardware.audio_manager import AudioManager

class AudioOut:
    """
    Handles TTS (Text-to-Speech), System Audio Volume, and SFX/Ambience via AudioManager.
    
    FIXED:
    - Singleton pattern
    - Türkçe TTS desteği eklendi (pyttsx3 ile)
    - TTS rate limiting
    """
    
    _instance = None
    _initialized = False
    
    # Rate limiting için class-level değişkenler
    _last_tts_time = 0
    _min_tts_interval = 5.0  # Minimum 5 saniye aralık
    _is_speaking = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioOut, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if AudioOut._initialized:
            return
            
        self.engine = None
        self.audio_manager = AudioManager()

        if HAS_PYTTSX3:
            try:
                self.engine = pyttsx3.init()
                # Ses tonu ve hızı ayarla
                self.engine.setProperty('rate', 150)
                self.engine.setProperty('volume', 0.9)
                
                # Türkçe ses seç
                voices = self.engine.getProperty('voices')
                turkish_voice = None
                for voice in voices:
                    voice_id_lower = voice.id.lower()
                    voice_name_lower = voice.name.lower() if voice.name else ""
                    if 'turkish' in voice_id_lower or 'tr-tr' in voice_id_lower or 'tr_tr' in voice_id_lower or 'tolga' in voice_name_lower:
                        turkish_voice = voice
                        break
                
                if turkish_voice:
                    self.engine.setProperty('voice', turkish_voice.id)
                    print(f"[AUDIO] Türkçe ses bulundu: {turkish_voice.name}")
                else:
                    # Türkçe ses yoksa, mevcut sesleri listele ve erkek ses bul
                    print("[AUDIO] UYARI: Türkçe ses bulunamadı! Mevcut sesler:")
                    male_voice = None
                    for voice in voices:
                        print(f"  - {voice.id}: {voice.name}")
                        # Erkek ses bulmaya çalış
                        if 'male' in voice.name.lower() or 'david' in voice.name.lower() or 'mark' in voice.name.lower():
                            male_voice = voice
                    
                    if male_voice:
                        self.engine.setProperty('voice', male_voice.id)
                        print(f"[AUDIO] Erkek ses seçildi: {male_voice.name}")
                
                # Hız ve ses ayarları
                self.engine.setProperty('rate', 150)  # Biraz yavaş
                self.engine.setProperty('volume', 0.9)
                
                print("[AUDIO] pyttsx3 TTS Engine başlatıldı")
                
            except Exception as e:
                print(f"[AUDIO] pyttsx3 Init Failed: {e}")
                self.engine = None

    def play_tts(self, text: str, force: bool = False):
        """
        Speaks the text using pyttsx3.
        FIXED: Non-blocking - arka planda thread'de çalışır, UI donmaz.
        
        Args:
            text: Konuşulacak metin
            force: True ise rate limiting'i atla
        """
        if not text or text.strip() == "":
            return
            
        if Config().IS_MOCK or not self.engine:
            print(f"[MOCK] TTS: {text}")
            return
        
        # Rate limiting - çok sık konuşmayı engelle
        current_time = time.time()
        time_since_last = current_time - AudioOut._last_tts_time
        
        if not force and time_since_last < AudioOut._min_tts_interval:
            print(f"[AUDIO] TTS atlandı (son konuşmadan {time_since_last:.1f}sn geçti)")
            return
        
        # Zaten konuşuyorsa atla
        if AudioOut._is_speaking:
            print("[AUDIO] TTS atlandı (zaten konuşuyor)")
            return
        
        # Çok uzun metinleri kısalt
        if len(text) > 150:
            text = text[:150] + "..."
        
        # FIXED: Thread'de çalıştır - UI donmaz
        import threading
        
        def speak_in_thread():
            try:
                AudioOut._is_speaking = True
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"[AUDIO] TTS Error: {e}")
            finally:
                AudioOut._is_speaking = False
        
        AudioOut._last_tts_time = current_time
        thread = threading.Thread(target=speak_in_thread, daemon=True)
        thread.start()
        print(f"[AUDIO] TTS started (async): {text[:30]}...")

    def play_tts_async(self, text: str):
        """Asenkron TTS - artık play_tts zaten async."""
        self.play_tts(text)

    def set_system_volume(self, level: float):
        """
        Sets system master volume (0.0 to 1.0).
        """
        if Config().IS_MOCK or not HAS_PYCAW:
            print(f"[MOCK] SYSTEM VOLUME SET: {level * 100}%")
            return

        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Scalar volume is 0.0 to 1.0
            volume.SetMasterVolumeLevelScalar(level, None)
        except Exception as e:
            print(f"[AUDIO] Volume Control Error: {e}")

    def max_volume_jumpscare(self):
        """Sets volume to 100% immediately."""
        self.set_system_volume(1.0)

    def play_sound_3d(self, sound_file: str, direction: str):
        """
        Placeholder for 3D sound logic.
        """
        if Config().IS_MOCK:
            print(f"[MOCK] PLAY 3D SOUND: {sound_file} from {direction}")
            return
        pass

    # --- AudioManager Proxies ---
    def start_ambience(self):
        if self.audio_manager:
            self.audio_manager.start_ambience()

    def stop_ambience(self):
        if self.audio_manager:
            self.audio_manager.stop_ambience()

    def play_sfx(self, name: str):
        if self.audio_manager:
            self.audio_manager.play_sfx(name)
    
    def play_typing_custom(self):
        if self.audio_manager:
            self.audio_manager.play_typing_sound()
    
    @staticmethod
    def set_min_tts_interval(seconds: float):
        """TTS'ler arası minimum bekleme süresini ayarla."""
        AudioOut._min_tts_interval = max(1.0, seconds)
