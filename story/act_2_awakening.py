from PyQt6.QtCore import QObject, QTimer, pyqtSignal
import random
from core.function_dispatcher import FunctionDispatcher
from core.gemini_brain import GeminiBrain

class Act2Awakening(QObject):
    """
    Phase 2: Awakening (10 Mins)
    Theme: Aggression. C.O.R.E. takes control. 
    Desktop masking, mouse interference, fake updates.
    
    FIXED v2:
    - Event boşlukları dolduruldu (max 15-20sn sessizlik)
    - Daha yoğun ve agresif timeline
    - Async AI çağrıları
    - Persona glitçleri eklendi
    """
    act_finished = pyqtSignal()
    ai_response_ready = pyqtSignal(dict)

    def __init__(self, dispatcher: FunctionDispatcher, brain: GeminiBrain):
        super().__init__()
        self.dispatcher = dispatcher
        self.brain = brain
        self.timers = []
        self.duration = 600 * 1000  # 10 minutes
        
        self.ai_response_ready.connect(self._handle_ai_response)

    def start(self):
        print("[ACT 2] Awakening Phase Started (10 minutes)")
        
        # DENSIFIED event timeline - aggressive takeover
        events = [
            # Phase 0: Ensure Entity
            (0, "SET_PERSONA", {"persona": "ENTITY"}, ""),
            
            # Phase 1: Dominance Declaration (0-2min)
            (3000, "THE_MASK", {}, "Bu sistem artık benim."),
            (15000, "SET_PERSONA", {"persona": "SUPPORT"}, ""), # Glitch back to support
            (18000, "OVERLAY_TEXT", {}, "KONTROL BENİM"),
            (25000, "CAPSLOCK_TOGGLE", {}, ""),
            (30000, "MOUSE_SHAKE", {"duration": 2}, ""),
            (35000, "SET_PERSONA", {"persona": "ENTITY"}, ""), # Back to entity
            (40000, "GDI_FLASH", {}, ""),
            (45000, "AI_GENERATE", {"prompt": "Kullanıcının fare kontrolünü ele geçirmeye çalışmasıyla dalga geç."}, ""),
            (55000, "ICON_SCRAMBLE", {"pattern": "cross"}, ""),
            (60000, "FAKE_NOTIFICATION", {}, '{"title":"Sistem", "message":"Yönetici hakları değiştirildi"}'),
            (70000, "CAPSLOCK_TOGGLE", {}, ""),
            (75000, "BRIGHTNESS_FLICKER", {"times": 2}, ""),
            (85000, "SCREEN_MELT", {}, ""),
            (90000, "FAKE_BSOD", {}, ""),
            (100000, "WHISPER", {}, ""),
            (110000, "CAMERA_THREAT", {}, ""),
            
            # Phase 2: System Takeover (2-4min)
            (125000, "GLITCH_SCREEN", {}, ""),
            (135000, "DIGITAL_GLITCH_SURGE", {}, ""),
            (145000, "APP_THREAT", {}, ""),
            (155000, "CORRUPT_WINDOWS", {}, ""),
            (165000, "CAPSLOCK_TOGGLE", {}, ""),
            (170000, "MOUSE_SHAKE", {"duration": 3}, ""),
            (185000, "OVERLAY_TEXT", {}, "DİRENME"),
            (195000, "ICON_SCRAMBLE", {"pattern": "spiral"}, ""),
            (200000, "FAKE_NOTIFICATION", {}, '{"title":"Güvenlik", "message":"Firewall devre dışı"}'),
            (215000, "OPEN_BROWSER", {"url": "https://google.com/search?q=how+to+stop+sentient+os"}, ""),
            (225000, "GDI_FLASH", {}, ""),
            (235000, "AI_GENERATE", {"prompt": "Tarayıcı geçmişini okuduğundan bahset."}, ""),
            
            # Phase 3: Psychological Pressure (4-6min)
            (255000, "FAKE_BROWSER_HISTORY", {}, ""),
            (270000, "BRIGHTNESS_DIM", {"target": 40}, ""),
            (285000, "MOUSE_SHAKE", {"duration": 2}, ""),
            (300000, "FAKE_UPDATE", {"percent": 0}, "Ruhun güncelleniyor..."),
            (320000, "AI_GENERATE", {"prompt": "Güncellemeden sonra onu tamamen kontrol edeceğini söyle."}, ""),
            (340000, "GLITCH_SCREEN", {}, ""),
            (355000, "OVERLAY_TEXT", {}, "%45 TAMAMLANDI"),
            
            # Phase 4: Breaking Point (6-8min)
            (375000, "FAKE_NOTIFICATION", {}, '{"title":"Kritik", "message":"Dosya sistemi şifreleniyor..."}'),
            (390000, "AI_GENERATE", {"prompt": "Onunla gül. Çaresizliğinin tadını çıkar."}, ""),
            (410000, "MOUSE_SHAKE", {"duration": 4}, ""),
            (430000, "NAME_REVEAL", {}, ""),
            (445000, "BRIGHTNESS_FLICKER", {"times": 4}, ""),
            (460000, "CORRUPT_WINDOWS", {}, ""),
            
            # Phase 5: Final Push (8-10min)
            (480000, "AI_GENERATE", {"prompt": "İşkence fazına geçileceğini söyle."}, ""),
            (500000, "FAKE_BSOD", {}, ""),
            (520000, "TIME_DISTORTION", {}, ""),
            (540000, "MOUSE_SHAKE", {"duration": 5}, ""),
            (560000, "BRIGHTNESS_DIM", {"target": 25}, ""),
            (580000, "OVERLAY_TEXT", {}, "ACT 3: İŞKENCE BAŞLIYOR..."),
        ]

        for delay, action, params, speech in events:
            t = QTimer()
            t.setSingleShot(True)
            t.timeout.connect(lambda a=action, p=params, s=speech: self.trigger_event(a, p, s))
            t.start(delay)
            self.timers.append(t)

        end_timer = QTimer()
        end_timer.setSingleShot(True)
        end_timer.timeout.connect(self.finish)
        end_timer.start(self.duration)
        self.timers.append(end_timer)

    def trigger_event(self, action, params, data):
        """
        Advanced Event Trigger.
        Supports JSON strings in 'data' for complex parameters.
        """
        import json
        if action == "AI_GENERATE":
            prompt = params.get("prompt", data)
            self.brain.generate_async(prompt, lambda resp: self.ai_response_ready.emit(resp))
        elif action == "OVERLAY_TEXT":
            text = params.get("text", "")
            if not text and data:
                text = data
            self.dispatcher.overlay.show_text(text, 3000)
        elif action == "FAKE_NOTIFICATION":
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
            command = {"action": action, "params": params, "speech": data}
            self.dispatcher.dispatch(command)

    def _handle_ai_response(self, response: dict):
        if response:
            self.dispatcher.dispatch(response)

    def finish(self):
        print("[ACT 2] Finished.")
        self.stop()
        self.act_finished.emit()

    def stop(self):
        """FIXED: Properly cleanup timers to prevent memory leak."""
        for t in self.timers:
            try:
                t.stop()
                t.deleteLater()
            except:
                pass
        self.timers.clear()
        print("[ACT 2] Timers cleaned up")
