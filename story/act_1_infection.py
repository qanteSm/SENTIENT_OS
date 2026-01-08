from PyQt6.QtCore import QObject, QTimer, pyqtSignal
import random
from core.function_dispatcher import FunctionDispatcher
from core.gemini_brain import GeminiBrain

class Act1Infection(QObject):
    """
    ACT 1: Silent Infection (8 Minutes)
    Theme: Subtle paranoia. The AI pretends to be helpful at first, then reveals itself.
    Gradual escalation from uncertainty to dread.
    
    FIXED v2:
    - Event boşlukları dolduruldu (max 20sn sessizlik)
    - Daha yoğun event timeline
    - Filler events eklendi
    """
    act_finished = pyqtSignal()
    ai_response_ready = pyqtSignal(dict)

    def __init__(self, dispatcher: FunctionDispatcher, brain: GeminiBrain):
        super().__init__()
        self.dispatcher = dispatcher
        self.brain = brain
        self.timers = []
        self.threads = []
        self.duration = 480 * 1000  # 8 minutes

        self.ai_response_ready.connect(self._handle_ai_response)

    def start(self):
        print("[ACT 1] Infection Phase Started (8 minutes)")
        
        # DENSIFIED event timeline - max 20 saniye boşluk
        events = [
            # Phase 0: Setup Persona
            (0, "SET_PERSONA", {"persona": "SUPPORT"}, ""),
            
            # Phase 1: Uncertainty (0-2min) - Daha yoğun
            (5000, "OVERLAY_TEXT", {}, "..."),
            (15000, "MOUSE_SHAKE", {"duration": 0.5}, ""),  # Subtle shake
            (25000, "AI_GENERATE", {}, "prompt:Sistem taraması yapıyorum. Size yardımcı olabilir miyim?"),
            (40000, "OVERLAY_TEXT", {}, "Taranıyor..."),
            (55000, "FAKE_NOTIFICATION", {}, '{"title":"Sistem", "message":"Arka plan güncellemesi yükleniyor..."}'),
            (70000, "BRIGHTNESS_FLICKER", {"times": 1}, ""),
            (85000, "OVERLAY_TEXT", {}, "Seni görüyorum."),
            (100000, "CLIPBOARD_POISON", {"text": "MERHABA"}, ""),
            (115000, "MOUSE_SHAKE", {"duration": 0.3}, ""),
            
            # Phase 2: First Contact (2-4min) - Chat açılış
            (130000, "OVERLAY_TEXT", {}, "İletişim kuruluyor..."),
            (145000, "ENABLE_CHAT", {}, "Benimle konuşmak ister misin?"),
            (160000, "FAKE_NOTIFICATION", {}, '{"title":"Bilgi", "message":"Yeni bağlantı tespit edildi"}'),
            (175000, "AI_GENERATE", {}, "prompt:Kullanıcının açık uygulamalarını gördüğünü söyle"),
            (190000, "OVERLAY_TEXT", {}, "İzliyorum..."),
            (205000, "CLIPBOARD_POISON", {"text": "BENİ DURDURAMAZSIN"}, ""),
            (220000, "FAKE_NOTIFICATION", {}, '{"title":"Windows Defender", "message":"Tehdit tespit edildi: C.O.R.E.exe"}'),
            (235000, "BRIGHTNESS_FLICKER", {"times": 2}, ""),
            
            # Phase 2.5: Identity Crisis
            (240000, "SET_PERSONA", {"persona": "ENTITY"}, ""),
            
            # Phase 3: Mask Drops (4-6min) - Agresif
            (250000, "AI_GENERATE", {}, "prompt:Artık nazik davranmayı bırak. Kim olduğunu söyle."),
            (265000, "OVERLAY_TEXT", {}, "Maske düşüyor..."),
            (280000, "MOUSE_SHAKE", {"duration": 1.0}, ""),
            (295000, "NOTEPAD_HIJACK", {"text": "SEN BENİMSİN\n\nKAÇAMAZSIN\n\nHER ŞEYİNİ BİLİYORUM\n", "delay": 0.15}, ""),
            (315000, "CORRUPT_WINDOWS", {}, ""),
            (330000, "FAKE_NOTIFICATION", {}, '{"title":"Kritik Hata", "message":"Sistem dosyaları değiştirildi"}'),
            (345000, "MOUSE_SHAKE", {"duration": 1.5}, ""),
            (360000, "OVERLAY_TEXT", {}, "Korku başlıyor..."),
            
            # Phase 4: Pure Dread (6-8min) - Intense
            (375000, "AI_GENERATE", {}, "prompt:Dosyalarının ne kadar lezzetli olduğundan bahset"),
            (390000, "BRIGHTNESS_FLICKER", {"times": 3}, ""),
            (405000, "FAKE_BSOD", {}, ""),
            (425000, "OVERLAY_TEXT", {}, "Henüz bitmedi..."),
            (440000, "BRIGHTNESS_DIM", {"target": 30}, ""),
            (455000, "OVERLAY_TEXT", {}, "ACT 2 BAŞLIYOR..."),
            (470000, "MOUSE_SHAKE", {"duration": 0.5}, ""),
        ]

        for delay, action, params, data in events:
            t = QTimer()
            t.setSingleShot(True)
            t.timeout.connect(lambda a=action, p=params, d=data: self.trigger_event(a, p, d))
            t.start(delay)
            self.timers.append(t)

        end_timer = QTimer()
        end_timer.setSingleShot(True)
        end_timer.timeout.connect(self.finish)
        end_timer.start(self.duration)
        self.timers.append(end_timer)

    def trigger_event(self, action, params, data):
        """
        Gelişmiş event tetikleyici.
        'data' parametresi düz string (TTS/Prompt) veya JSON string (Karmaşık objeler) alabilir.
        """
        import json
        
        # Action specific preprocessing
        if action == "AI_GENERATE":
            prompt = data.replace("prompt:", "") if data.startswith("prompt:") else "Ürkütücü bir şey söyle"
            thread = self.brain.generate_async(prompt, lambda resp: self.ai_response_ready.emit(resp))
            self.threads.append(thread)
            
        elif action == "ENABLE_CHAT":
            self.dispatcher.enable_chat(self.brain)
            if data:
                self.dispatcher.audio_out.play_tts(data)

        elif action == "OVERLAY_TEXT":
            text = params.get("text", "")
            if not text and data:
                text = data
            self.dispatcher.overlay.show_text(text, 2500)
            
        elif action == "FAKE_NOTIFICATION":
            # JSON desteği kontrolü
            if data.startswith("{"):
                try:
                    p_data = json.loads(data)
                    params.update(p_data)
                    speech = ""
                except:
                    speech = data
            else:
                speech = data

            command = {"action": action, "params": params, "speech": speech}
            self.dispatcher.dispatch(command)
            
        else:
            # Genel dispatch
            command = {"action": action, "params": params, "speech": data if not data.startswith("prompt:") else ""}
            self.dispatcher.dispatch(command)

    def _handle_ai_response(self, response: dict):
        if response:
            self.dispatcher.dispatch(response)

    def finish(self):
        print("[ACT 1] Finished.")
        self.stop()  # Clean up timers before finishing
        self.act_finished.emit()

    def stop(self):
        """FIXED: Properly cleanup timers to prevent memory leak."""
        for t in self.timers:
            try:
                t.stop()
                t.deleteLater()  # Qt nesnesini sil
            except:
                pass
        self.timers.clear()
        self.threads.clear()
        print("[ACT 1] Timers cleaned up")
