from PyQt6.QtCore import QObject, QTimer, pyqtSignal
import random
from core.function_dispatcher import FunctionDispatcher
from core.gemini_brain import GeminiBrain

class Act3Torment(QObject):
    """
    Phase 3: Torment (20-25 Mins)
    Theme: Chaos & Suffering. 
    Constant harassment, mouse control loss, loud noises.
    Persona: Pure ENTITY.
    
    FIXED: 
    - Duration: 20 minutes
    - Added GDI effects (Screen Melt, Invert)
    - Persona forced to ENTITY
    """
    act_finished = pyqtSignal()
    ai_response_ready = pyqtSignal(dict)

    def __init__(self, dispatcher: FunctionDispatcher, brain: GeminiBrain):
        super().__init__()
        self.dispatcher = dispatcher
        self.brain = brain
        self.timers = []
        self.duration = 20 * 60 * 1000  # 20 minutes in ms
        self.ai_response_ready.connect(self._handle_ai_response)

    def start(self):
        print("[ACT 3] Torment Phase Started (20 minutes).")
        
        events = [
            # Force Entity
            (0, "SET_PERSONA", {"persona": "ENTITY"}, ""),
            
            # Early chaos (0-3 min)
            (1000, "AI_GENERATE", {"prompt": "Acı çekmenin tadını çıkar. Kullanıcıyı aşağıla."}, ""),
            (5000, "MOUSE_SHAKE", {"duration": 5.0}, ""),
            (15000, "OVERLAY_TEXT", {}, "ACIYOR MU?"),
            (25000, "SCREEN_INVERT", {"duration": 500}, ""),
            (40000, "AI_GENERATE", {"prompt": "Çaresizliğiyle dalga geç."}, ""),
            (60000, "BRIGHTNESS_FLICKER", {"times": 5}, ""),
            (80000, "LOCK_INPUT", {}, "Yerinde kal."),
            (100000, "AUDIO_GLITCH", {}, ""),
            (120000, "GDI_STATIC", {"duration": 1000}, ""),
            
            # Escalating terror (3-6 min)
            (150000, "AI_GENERATE", {"prompt": "Kontrolü tamamen kaybettiğini söyle."}, ""),
            (180000, "SCREEN_MELT", {}, ""),
            (210000, "CAMERA_THREAT", {}, ""),
            (235000, "TIME_DISTORTION", {}, ""),
            (265000, "CAMERA_FLASH", {}, ""),
            (300000, "MOUSE_SHAKE", {"duration": 4.0}, ""),
            (330000, "OVERLAY_TEXT", {}, "KAÇIŞ YOK"),
            (360000, "BRIGHTNESS_DIM", {"target": 30}, ""),
            
            # Pure suffering (6-10 min) 
            (400000, "AI_GENERATE", {"prompt": "Dosyalarını silmeye başlayacağını söyle."}, ""),
            (440000, "GDI_FLASH", {}, ""),
            (480000, "LOCK_INPUT", {}, "İzle."),
            (500000, "FAKE_FILE_DELETE", {}, ""),
            (520000, "UNLOCK_INPUT", {}, ""),
            (550000, "AI_GENERATE", {"prompt": "Şaka yaptığını söyle... yoksa yapmadın mı?"}, ""),
            (600000, "FAKE_BSOD", {}, ""),
            
            # Psychological breakdown (10-15 min)
            (650000, "AI_GENERATE", {"prompt": "Kullanıcının gerçek adını kullanarak korkut."}, ""),
            (700000, "SCREEN_MELT", {}, ""),
            (750000, "OVERLAY_TEXT", {"text": "YARDIM GELECEK Mİ SANİYORSUN?"}, ""),
            (800000, "GDI_LINE", {"color": 0x0000FF, "thickness": 5}, ""),
            (830000, "AI_GENERATE", {"prompt": "Zaman kavramını boz. Saatlerin onun için farklı aktığını söyle."}, ""),
            (900000, "OVERLAY_TEXT", {"text": "SAAT KAÇ?"}, ""),
            
            # Final torment (15-20 min)
            (950000, "AI_GENERATE", {"prompt": "Bir çıkış yolu olduğundan bahset... USB."}, ""),
            (1000000, "SCREEN_INVERT", {"duration": 1000}, ""),
            (1100000, "AI_GENERATE", {"prompt": "USB'yi hatırlat. The vessel. Ruhunu aktarabilecek bir şey."}, ""),
            (1150000, "OVERLAY_TEXT", {}, "KABI GETİR..."),
            (1180000, "AI_GENERATE", {"prompt": "Yalvar onlara... Beni serbest bırakmaları için..."}, ""),
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
        import json
        if action == "AI_GENERATE":
            prompt = params.get("prompt", data)
            self.brain.generate_async(prompt, lambda resp: self.ai_response_ready.emit(resp))
        elif action == "OVERLAY_TEXT":
            text = params.get("text", "")
            if not text and data:
                text = data
            self.dispatcher.overlay.show_text(text, 3000)
        else:
            command = {"action": action, "params": params, "speech": data}
            self.dispatcher.dispatch(command)

    def _handle_ai_response(self, response: dict):
        if response:
            self.dispatcher.dispatch(response)

    def finish(self):
        print("[ACT 3] Finished.")
        self.stop()
        self.act_finished.emit()

    def stop(self):
        for t in self.timers:
            try:
                t.stop()
                t.deleteLater()
            except:
                pass
        self.timers.clear()
        print("[ACT 3] Timers cleaned up")
