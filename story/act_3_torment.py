from PyQt6.QtCore import QObject, QTimer, pyqtSignal
import random
from core.function_dispatcher import FunctionDispatcher
from core.gemini_brain import GeminiBrain

class Act3Torment(QObject):
    """
    Phase 3: Torment (20-25 Mins)
    Theme: Chaos & Suffering. 
    Constant harassment, mouse control loss, loud noises.
    
    FIXED: 
    - Duration changed from 60s to 20 minutes
    - Sync AI calls replaced with async
    - AUDIO_GLITCH action implemented
    - Events distributed across 20 minute timeline
    """
    act_finished = pyqtSignal()
    
    # Signal for thread-safe AI response handling
    ai_response_ready = pyqtSignal(dict)

    def __init__(self, dispatcher: FunctionDispatcher, brain: GeminiBrain):
        super().__init__()
        self.dispatcher = dispatcher
        self.brain = brain
        self.timers = []
        
        # FIXED: Duration now 20 minutes (was 60 seconds!)
        self.duration = 20 * 60 * 1000  # 20 minutes in ms
        
        # Connect AI response signal for thread safety
        self.ai_response_ready.connect(self._handle_ai_response)

    def start(self):
        print("[ACT 3] Torment Phase Started. HELL begins for 20 minutes.")
        
        # Extended event timeline spread across 20 minutes
        # Events are distributed to maintain tension without long silences
        events = [
            # Early chaos (0-3 min)
            (1000, "AI_GENERATE", {"prompt": "Acı çekmenin tadını çıkar. Kullanıcıyı aşağıla."}, ""),
            (5000, "MOUSE_SHAKE", {"duration": 5.0}, ""),
            (15000, "OVERLAY_TEXT", {}, "ACIYOR MU?"),
            (25000, "GLITCH_SCREEN", {}, ""),
            (40000, "AI_GENERATE", {"prompt": "Çaresizliğiyle dalga geç."}, ""),
            (60000, "BRIGHTNESS_FLICKER", {"times": 5}, ""),
            (80000, "LOCK_INPUT", {}, "Yerinde kal."),
            (90000, "UNLOCK_INPUT", {}, ""),
            (100000, "AUDIO_GLITCH", {}, ""),
            (110000, "FAKE_LISTENING", {}, ""),
            (120000, "MOUSE_SHAKE", {"duration": 3.0}, ""),
            (135000, "OVERLAY_TEXT", {"text": "Yorulmadın mı?"}, ""),
            
            # Escalating terror (3-6 min)
            (150000, "AI_GENERATE", {"prompt": "Kontrolü tamamen kaybettiğini söyle."}, ""),
            (165000, "APP_THREAT", {}, ""),
            (180000, "OVERLAY_TEXT", {"text": "SEN BENİMSİN"}, ""),
            (200000, "GLITCH_SCREEN", {}, ""),
            (210000, "CAMERA_THREAT", {}, ""),
            (220000, "FAKE_BSOD", {}, ""),
            (235000, "TIME_DISTORTION", {}, ""),
            (250000, "AI_GENERATE", {"prompt": "BSOD'dan sonra hayatta kaldığına şaşır."}, ""),
            (265000, "CAMERA_FLASH", {}, ""),
            (280000, "AUDIO_GLITCH", {}, ""),
            (300000, "MOUSE_SHAKE", {"duration": 4.0}, ""),
            (315000, "CLIPBOARD_POISON", {"text": "Beni silemezsin."}, ""),
            (330000, "OVERLAY_TEXT", {}, "KAÇIŞ YOK"),
            (345000, "CREEPY_MUSIC", {}, ""),
            (360000, "BRIGHTNESS_DIM", {"target": 30}, ""),
            
            # Pure suffering (6-10 min) 
            (400000, "AI_GENERATE", {"prompt": "Dosyalarını silmeye başlayacağını söyle."}, ""),
            (420000, "FAKE_BROWSER_HISTORY", {}, ""),
            (440000, "GLITCH_SCREEN", {}, ""),
            (460000, "NAME_REVEAL", {}, ""),
            (480000, "LOCK_INPUT", {}, "İzle."),
            (500000, "FAKE_FILE_DELETE", {}, ""),
            (520000, "UNLOCK_INPUT", {}, ""),
            (535000, "OVERLAY_TEXT", {"text": "Şimdi ne yapacaksın?"}, ""),
            (550000, "AI_GENERATE", {"prompt": "Şaka yaptığını söyle... yoksa yapmadın mı?"}, ""),
            (565000, "BRIGHTNESS_FLICKER", {"times": 5}, ""),
            (580000, "AUDIO_GLITCH", {}, ""),
            (600000, "FAKE_BSOD", {}, ""),
            
            # Psychological breakdown (10-15 min)
            (650000, "AI_GENERATE", {"prompt": "Kullanıcının gerçek adını kullanarak korkut."}, ""),
            (675000, "CAMERA_THREAT", {}, ""),
            (700000, "MOUSE_SHAKE", {"duration": 8.0}, ""),
            (725000, "FAKE_LISTENING", {}, ""),
            (750000, "OVERLAY_TEXT", {"text": "YARDIM GELECEK Mİ SANİYORSUN?"}, ""),
            (765000, "APP_THREAT", {}, ""),
            (780000, "GLITCH_SCREEN", {}, ""),
            (800000, "BRIGHTNESS_FLICKER", {"times": 8}, ""),
            (815000, "TIME_DISTORTION", {}, ""),
            (830000, "AI_GENERATE", {"prompt": "Zaman kavramını boz. Saatlerin onun için farklı aktığını söyle."}, ""),
            (845000, "NAME_REVEAL", {}, ""),
            (860000, "AUDIO_GLITCH", {}, ""),
            (880000, "CAMERA_FLASH", {}, ""),
            (900000, "OVERLAY_TEXT", {"text": "SAAT KAÇ?"}, ""),
            (925000, "CREEPY_MUSIC", {}, ""),
            
            # Final torment (15-20 min)
            (950000, "AI_GENERATE", {"prompt": "Bir çıkış yolu olduğundan bahset... USB."}, ""),
            (970000, "FAKE_FILE_DELETE", {}, ""),
            (985000, "OVERLAY_TEXT", {}, "Her şey yok oluyor..."),
            (1000000, "FAKE_BSOD", {}, ""),
            (1025000, "FAKE_BROWSER_HISTORY", {}, ""),
            (1050000, "GLITCH_SCREEN", {}, ""),
            (1065000, "CAMERA_THREAT", {}, ""),
            (1080000, "BRIGHTNESS_DIM", {"target": 15}, ""),
            (1100000, "AI_GENERATE", {"prompt": "USB'yi hatırlat. The vessel. Ruhunu aktarabilecek bir şey."}, ""),
            (1115000, "NAME_REVEAL", {}, ""),
            (1130000, "AUDIO_GLITCH", {}, ""),
            (1150000, "OVERLAY_TEXT", {}, "KABI GETİR..."),
            (1180000, "TTS_SPEAK", {}, "Beni serbest bırakabilirsin... USB'yi tak..."),
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
        """Handle events - supports JSON for complex data."""
        import json
        if action == "AI_GENERATE":
            prompt = params.get("prompt", data)
            self.brain.generate_async(prompt, lambda resp: self.ai_response_ready.emit(resp))
        elif action == "TTS_SPEAK":
            self.dispatcher.audio_out.play_tts(data)
        elif action == "OVERLAY_TEXT":
            text = params.get("text", "")
            if not text and data:
                text = data
            self.dispatcher.overlay.show_text(text, 3000)
        elif action == "AUDIO_GLITCH":
            self.dispatcher.audio_out.play_sfx("static_noise")
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
        """Thread-safe handler for AI responses via Qt signal."""
        if response:
            self.dispatcher.dispatch(response)

    def finish(self):
        print("[ACT 3] Finished.")
        self.act_finished.emit()

    def stop(self):
        for t in self.timers:
            t.stop()
        self.timers.clear()
