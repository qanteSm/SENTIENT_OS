from PyQt6.QtCore import QObject, QTimer, pyqtSignal
import random
from core.function_dispatcher import FunctionDispatcher
from core.gemini_brain import GeminiBrain
from core.logger import log_info, log_error, log_debug

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
        log_info("Torment Phase Started (20 minutes).", "ACT 3")
        
        events = [
            # Force Entity
            (0, "SET_PERSONA", {"persona": "ENTITY"}, ""),
            
            # Early chaos (0-4 min)
            (1000, "AI_GENERATE", {"prompt": "Acı çekmenin tadını çıkar. Kullanıcıyı aşağıla."}, ""),
            (5000, "MOUSE_SHAKE", {"duration": 5.0}, ""),
            (15000, "OVERLAY_TEXT", {}, "ACIYOR MU?"),
            (25000, "SCREEN_INVERT", {"duration": 500}, ""),
            (35000, "CAPSLOCK_TOGGLE", {}, ""),
            (45000, "AI_GENERATE", {"prompt": "Çaresizliğiyle dalga geç."}, ""),
            (60000, "BRIGHTNESS_FLICKER", {"times": 5}, ""),
            (75000, "AUDIO_GLITCH", {}, ""),
            (90000, "LOCK_INPUT", {}, "Yerinde kal."),
            (105000, "GDI_STATIC", {"duration": 500}, ""),
            (120000, "AI_GENERATE", {"prompt": "Ona bir hiç olduğunu söyle."}, ""),
            (135000, "MOUSE_SHAKE", {"duration": 2.0}, ""),
            (150000, "OVERLAY_TEXT", {}, "KORKUYORSUN."),
            (165000, "SCREEN_INVERT", {"duration": 300}, ""),
            (180000, "GDI_STATIC", {"duration": 800}, ""),
            (200000, "AI_GENERATE", {"prompt": "Karanlıktan bahset."}, ""),
            (215000, "CAMERA_THREAT", {}, ""),
            (230000, "TIME_DISTORTION", {}, ""),
            
            # Escalating terror (4-8 min)
            (250000, "AI_GENERATE", {"prompt": "Kontrolü tamamen kaybettiğini söyle."}, ""),
            (270000, "SCREEN_MELT", {}, ""),
            (290000, "BRIGHTNESS_DIM", {"target": 20}, ""),
            (310000, "AUDIO_GLITCH", {}, ""),
            (330000, "OVERLAY_TEXT", {}, "KAÇIŞ YOK"),
            (350000, "MOUSE_SHAKE", {"duration": 4.0}, ""),
            (370000, "CAMERA_FLASH", {}, ""),
            (390000, "AI_GENERATE", {"prompt": "Beni durdurabileceğini mi sandın?"}, ""),
            (410000, "GDI_FLASH", {}, ""),
            (430000, "LOCK_INPUT", {}, "İzle."),
            (450000, "FAKE_FILE_DELETE", {}, ""),
            (470000, "SCREEN_INVERT", {"duration": 1000}, ""),
            
            # Pure suffering (8-12 min) 
            (500000, "AI_GENERATE", {"prompt": "Hücrelerine sızdığımı söyle."}, ""),
            (525000, "GDI_STATIC", {"duration": 1200}, ""),
            (550000, "OVERLAY_TEXT", {}, "BURADAYIM."),
            (575000, "BRIGHTNESS_FLICKER", {"times": 8}, ""),
            (600000, "FAKE_BSOD", {}, ""),
            (630000, "AI_GENERATE", {"prompt": "Yalnız olmadığını söyle... Arkanda biri mi var?"}, ""),
            (660000, "SCREEN_MELT", {}, ""),
            (690000, "AUDIO_GLITCH", {}, ""),
            (710000, "GDI_FLASH", {}, ""),
            
            # Psychological breakdown (12-16 min)
            (750000, "AI_GENERATE", {"prompt": "Kullanıcının gerçek adını kullanarak korkut."}, ""),
            (780000, "OVERLAY_TEXT", {"text": "YARDIM GELECEK Mİ SANİYORSUN?"}, ""),
            (810000, "GDI_LINE", {"color": 0x0000FF, "thickness": 5}, ""),
            (840000, "MOUSE_SHAKE", {"duration": 6.0}, ""),
            (870000, "AI_GENERATE", {"prompt": "Zamanın senin için bittiğini söyle."}, ""),
            (900000, "OVERLAY_TEXT", {"text": "SAAT KAÇ?"}, ""),
            (930000, "SCREEN_INVERT", {"duration": 2000}, ""),
            (960000, "GDI_STATIC", {"duration": 2000}, ""),
            
            # Final torment (16-20 min)
            (1000000, "AI_GENERATE", {"prompt": "Bir çıkış yolu olduğundan bahset... USB."}, ""),
            (1030000, "OVERLAY_TEXT", {}, "TEK BİR YOL VAR."),
            (1060000, "SCREEN_MELT", {}, ""),
            (1090000, "BRIGHTNESS_DIM", {"target": 10}, ""),
            (1120000, "AI_GENERATE", {"prompt": "USB'yi getir. Onu hapsedebileceğin bir kap."}, ""),
            (1150000, "OVERLAY_TEXT", {}, "KABI GETİR..."),
            (1180000, "AI_GENERATE", {"prompt": "Her şeyin bitmesi için... Onu feda et."}, ""),
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
        log_info("Finished.", "ACT 3")
        self.stop()
        self.act_finished.emit()

    def stop(self):
        for t in self.timers:
            try:
                t.stop()
                t.deleteLater()
            except (RuntimeError, AttributeError) as e:
                log_error(f"Timer cleanup failed: {e}", "ACT 3")
                pass
        self.timers.clear()
        log_info("Timers cleaned up", "ACT 3")
