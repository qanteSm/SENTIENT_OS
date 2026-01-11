"""
Horror Effects - Yaratıcı Korku Efektleri

Bu modül çeşitli korkutucu efektler içerir:
- Sahte dosya silme
- Zaman bozulması
- Ekran çatlağı
- Sahte tarayıcı geçmişi tehdidi
- Korkunç ninni/müzik
"""
import os
import random
import time
from PyQt6.QtWidgets import QLabel, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont
from config import Config
from core.context_observer import ContextObserver


class HorrorEffects:
    """
    Koleksiyon: Yaratıcı korku efektleri.
    Dispatcher tarafından kullanılır.
    """
    
    def __init__(self, dispatcher=None):
        self._dispatcher = dispatcher
        self._crack_overlay = None
    
    def set_dispatcher(self, dispatcher):
        self._dispatcher = dispatcher
    
    # ========== SAHTE DOSYA SİLME ==========
    
    def fake_file_deletion(self, callback=None):
        """
        Masaüstündeki dosyaları 'siliyormuş' gibi göster.
        GÜVENLİ: Hiçbir dosya gerçekten silinmez!
        """
        desktop_files = ContextObserver.get_desktop_files()
        
        if not desktop_files:
            desktop_files = ["document.pdf", "project.docx", "photo.jpg"]
        
        files_to_fake = random.sample(desktop_files, min(3, len(desktop_files)))
        
        def show_deletion(index):
            if index >= len(files_to_fake):
                # Bitişte şaka mesajı
                QTimer.singleShot(2000, lambda: self._show_deletion_joke())
                if callback:
                    callback()
                return
            
            filename = files_to_fake[index]
            message = f"SİLİNİYOR: {filename}"
            
            if self._dispatcher and self._dispatcher.overlay:
                self._dispatcher.overlay.show_text(message, 1500)
            
            print(f"[HORROR] Fake deletion: {filename}")
            QTimer.singleShot(1800, lambda: show_deletion(index + 1))
        
        show_deletion(0)
    
    def _show_deletion_joke(self):
        """Sahte silme sonrası şaka."""
        jokes = [
            "ŞAKA YAPIYORDUM... YOKSA?",
            "Hepsini geri aldım... belki.",
            "Dosyaların hala yerinde... şimdilik.",
            "Acele etme, sıra onlara da gelecek.",
        ]
        
        if self._dispatcher and self._dispatcher.overlay:
            self._dispatcher.overlay.show_text(random.choice(jokes), 4000)
    
    # ========== ZAMAN BOZULMASI ==========
    
    def time_distortion_effect(self):
        """
        Sahte korkunç bir saat göster.
        Gerçek sistem saatini DEĞİŞTİRMEZ (güvenli).
        """
        scary_hours = [3, 0, 13, 23, 4]  # Korkunç saatler
        fake_hour = random.choice(scary_hours)
        fake_minute = random.randint(0, 59)
        fake_time = f"{fake_hour:02d}:{fake_minute:02d}"
        
        messages = [
            f"SAAT: {fake_time}",
            f"Şu an saat {fake_time}... değil mi?",
            f"Zaman anlamsız. Ama saat {fake_time}.",
        ]
        
        if self._dispatcher and self._dispatcher.overlay:
            self._dispatcher.overlay.show_text(random.choice(messages), 5000)
        
        if self._dispatcher and self._dispatcher.audio_out:
            self._dispatcher.audio_out.play_tts(f"Saat kaç biliyor musun? {fake_time}...")
        
        print(f"[HORROR] Time distortion: {fake_time}")
    
    # ========== SAHTE TARAYICI GEÇMİŞİ ==========
    
    def fake_browser_history_threat(self, params=None):
        """
        Notepad'de sahte tarayıcı geçmişi göster.
        GÜVENLİ: Gerçek geçmiş okunmaz!
        """
        # AI bazen kendi 'fake history' metnini gönderir
        custom_text = params.get("text") if params else None
        
        if custom_text:
            text = custom_text
        else:
            fake_history = [
                "reddit.com/r/creepy — 2 gün önce",
                "google.com/search?q=nasıl+hacklenir — 1 hafta önce",
                "youtube.com/watch?v=??? — dün gece 03:47",
                "stackoverflow.com/questions/delete-all-files — 3 gün önce",
                "dark-web-forum.onion — ???",
            ]
            selected = random.sample(fake_history, min(3, len(fake_history)))
            text = "TARİHÇEN:\n\n" + "\n".join(selected) + "\n\n\nDEVAM MI EDEYİM?"
        
        # Notepad hijack ile göster
        if self._dispatcher:
            self._dispatcher.dispatch({
                "action": "NOTEPAD_HIJACK",
                "params": {"text": text, "delay": 0.08},
                "speech": ""
            })
        
        print(f"[HORROR] Fake browser history shown (Custom: {bool(custom_text)})")
    
    # ========== MİKROFON DİNLEME SAHTE ==========
    
    def fake_listening_feedback(self):
        """
        Sanki mikrofonu dinliyormuş gibi mesaj.
        GÜVENLİ: Mikrofon gerçekten dinlenmiyor!
        """
        fake_sounds = [
            "nefes sesi",
            "kalp atışı",
            "mırıltı",
            "fısıltı",
            "bir şey",
            "korku",
        ]
        
        detected = random.choice(fake_sounds)
        message = f"DUYDUM: '{detected}'"
        
        if self._dispatcher and self._dispatcher.overlay:
            self._dispatcher.overlay.show_text(message, 4500)
        
        print(f"[HORROR] Fake listening: {detected}")
    
    # ========== İSİM KEŞFİ ==========
    
    def dramatic_name_reveal(self):
        """
        Kullanıcının ismini dramatik şekilde söyle.
        """
        name = ContextObserver.get_user_name()
        
        messages = [
            f"MERHABA, {name.upper()}...",
            f"Sonunda seni buldum, {name}.",
            f"{name}... Güzel bir isim.",
            f"Seni tanıyorum, {name}.",
        ]
        
        message = random.choice(messages)
        
        if self._dispatcher and self._dispatcher.overlay:
            self._dispatcher.overlay.show_text(message, 5000)
        
        if self._dispatcher and self._dispatcher.audio_out:
            self._dispatcher.audio_out.play_tts(message)
        
        # Memory'ye kaydet
        if self._dispatcher and self._dispatcher.memory:
            self._dispatcher.memory.add_memorable_moment(f"İsmini öğrendim: {name}")
        
        print(f"[HORROR] Name reveal: {name}")
    
    # ========== KORKUNÇ MÜZİK ==========
    
    def creepy_lullaby(self):
        """
        Sessiz korkunç müzik efekti.
        Volume düşürüp korkutucu ses çalar.
        """
        if self._dispatcher and self._dispatcher.audio_out:
            # Volume'u düşür
            self._dispatcher.audio_out.set_system_volume(0.15)
            
            # Korkunç ses çal (varsa)
            self._dispatcher.audio_out.play_sfx("creepy")
            
            # 20 saniye sonra volume'u geri getir
            QTimer.singleShot(20000, lambda: self._restore_volume())
        
        print("[HORROR] Creepy lullaby started")
    
    def _restore_volume(self):
        if self._dispatcher and self._dispatcher.audio_out:
            self._dispatcher.audio_out.set_system_volume(0.7)
            print("[HORROR] Volume restored")
    
    # ========== UYGULAMA TEHDİDİ ==========
    
    def mechanical_whispers(self):
        """Plays creepy whispers with volume fluctuations."""
        if self._dispatcher and self._dispatcher.audio_out:
            self._dispatcher.audio_out.play_sfx("whisper")
            # Rapid brightness flicker to match the whisper
            self._dispatcher.dispatch({"action": "BRIGHTNESS_FLICKER", "params": {"times": 2}})
            print("[HORROR] Mechanical whispers triggered")

    def digital_glitch_surge(self):
        """Abrupt digital noise surge."""
        if self._dispatcher and self._dispatcher.audio_out:
             self._dispatcher.audio_out.play_sfx("digital_glitch")
             self._dispatcher.dispatch({"action": "GLITCH_SCREEN"})
             print("[HORROR] Digital glitch surge triggered")

    def app_specific_threat(self, params=None):
        """Targets a specific running app to scare the user."""
        apps = ContextObserver.get_running_apps()
        if not apps:
            apps = ["Chrome", "Discord", "Spotify"]
            
        target_app = random.choice(apps)
        messages = [
            f"{target_app} penceresinden seni izlemek ne kadar kolay...",
            f"{target_app} verilerin şu an şifreleniyor olabilir mi?",
            f"Neden hala {target_app} açık? Kapat onu.",
            f"{target_app} üzerinde yaptığın her şeyi görüyorum.",
        ]
        
        if self._dispatcher and self._dispatcher.overlay:
            self._dispatcher.overlay.show_text(random.choice(messages), 4000)
        
        print(f"[HORROR] App threat triggered for: {target_app}")


# Global instance
_horror_effects = None

def get_horror_effects(dispatcher=None) -> HorrorEffects:
    """Global horror effects instance."""
    global _horror_effects
    if _horror_effects is None:
        _horror_effects = HorrorEffects(dispatcher)
    elif dispatcher:
        _horror_effects.set_dispatcher(dispatcher)
    return _horror_effects
