from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from core.localization_manager import tr
from core.function_dispatcher import FunctionDispatcher
from core.gemini_brain import GeminiBrain
from core.logger import log_info, log_error, log_debug

class Act1Infection(QObject):
    # ... (class docstring kept as is) ...
    act_finished = pyqtSignal()
    ai_response_ready = pyqtSignal(dict)

    def __init__(self, dispatcher: FunctionDispatcher, brain: GeminiBrain):
        super().__init__()
        self.dispatcher = dispatcher
        self.brain = brain
        self.timers = []
        self.threads = []
        self.duration = 240 * 1000  # OPTIMIZED: 4 minutes (was 8) (Condensed experience)

        self.ai_response_ready.connect(self._handle_ai_response)

    def start(self):
        log_info("Infection Phase Started (4 minutes - Optimized)", "ACT 1")
        
        # OPTIMIZED EVENT TIMELINE - Compressed for Pacing
        events = [
            # Phase 0: Setup Persona (Immediate)
            (0, "SET_PERSONA", {"persona": "SUPPORT"}, ""),
            
            # Phase 1: Uncertainty (0-1min) - No more dead air
            (2000, "MOUSE_SHAKE", {"duration": 0.2}, ""), # Immediate subtle tell
            (5000, "OVERLAY_TEXT", {}, "..."),
            (12000, "CLIPBOARD_POISON", {"text": "Yardım mı lazım?"}, ""),
            (18000, "FAKE_NOTIFICATION", {}, '{"title":"' + tr("notifications.title_info") + '", "message":"' + tr("system.background_update") + '"}'),
            (25000, "AI_GENERATE", {}, f"prompt:{tr('system.scanning_prompt')}"),
            (35000, "OVERLAY_TEXT", {}, tr("system.scanning")),
            (42000, "BRIGHTNESS_FLICKER", {"times": 1}, ""),
            (50000, "MOUSE_SHAKE", {"duration": 0.5}, ""),
            
            # Phase 2: First Contact (1-2min) - Early Chat
            (60000, "OVERLAY_TEXT", {}, tr("act1.i_see_you")),
            (65000, "CAPSLOCK_TOGGLE", {}, ""),
            (70000, "CLIPBOARD_POISON", {"text": tr("clipboard.hello")}, ""),
            (75000, "OVERLAY_TEXT", {}, tr("act1.communication")),
            (80000, "ENABLE_CHAT", {}, tr("act1.chat_invite")),
            (85000, "FAKE_NOTIFICATION", {}, '{"title":"' + tr("notifications.title_info") + '", "message":"' + tr("system.connection_detected") + '"}'),
            
            # Interactive Phase starts early
            (95000, "AI_GENERATE", {}, "prompt:Kullanıcının açık uygulamalarını gördüğünü söyle"),
            (105000, "MOUSE_SHAKE", {"duration": 0.8}, ""),
            (115000, "OVERLAY_TEXT", {}, tr("act1.watching")),
            (125000, "CLIPBOARD_POISON", {"text": tr("clipboard.cant_stop_me")}, ""),
             # Threat Escalation
            (135000, "FAKE_NOTIFICATION", {}, '{"title":"' + tr("notifications.title_defender") + '", "message":"' + tr("notifications.msg_threat_detected") + '"}'),
            (140000, "SET_PERSONA", {"persona": "ENTITY"}, ""),
            
            # Phase 3: Mask Drops (2-3min) - Aggressive
            (150000, "AI_GENERATE", {}, f"prompt:{tr('act1.mask_drop_prompt')}"),
            (160000, "OVERLAY_TEXT", {}, tr("act1.mask_drops")),
            (170000, "NOTEPAD_HIJACK", {"text": tr("act1.you_are_mine"), "delay": 0.15}, ""),
            (180000, "BRIGHTNESS_FLICKER", {"times": 3}, ""),
            (185000, "CORRUPT_WINDOWS", {}, ""),
            (190000, "FAKE_NOTIFICATION", {}, '{"title":"' + tr("notifications.title_error") + '", "message":"' + tr("notifications.msg_files_changed") + '"}'),
            (200000, "MOUSE_SHAKE", {"duration": 2.0}, ""),
            
            # Phase 4: Chaos Finale (3-4min)
            (210000, "OVERLAY_TEXT", {}, tr("act1.fear_begins")),
            (220000, "AI_GENERATE", {}, "prompt:Dosyalarının ne kadar lezzetli olduğundan bahset"),
            (225000, "FAKE_BSOD", {}, ""),
            (230000, "GLITCH_SCREEN", {}, ""),
            (235000, "OVERLAY_TEXT", {}, tr("act1.act2_start")),
            (238000, "MOUSE_SHAKE", {"duration": 2.5}, ""),
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
        from PyQt6.QtCore import QObject, QTimer, pyqtSignal
        import random
        import json
        
        # Action specific preprocessing
        if action == "AI_GENERATE":
            prompt = data.replace("prompt:", "") if data.startswith("prompt:") else "Ürkütücü bir şey söyle"
            # Using generate_async properly
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
                except (json.JSONDecodeError, ValueError) as e:
                    log_error(f"JSON parse failed: {e}", "ACT 1")
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
        log_info("Finished.", "ACT 1")
        self.stop()  # Clean up timers before finishing
        self.act_finished.emit()

    def stop(self):
        """FIXED: Properly cleanup timers to prevent memory leak."""
        for t in self.timers:
            try:
                t.stop()
                t.deleteLater()  # Qt nesnesini sil
            except (RuntimeError, AttributeError) as e:
                log_error(f"Timer cleanup failed: {e}", "ACT 1")
                pass
        self.timers.clear()
        self.threads.clear()
        log_info("Timers cleaned up", "ACT 1")
