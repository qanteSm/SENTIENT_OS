import json
from PyQt6.QtCore import QObject, pyqtSignal
from core.process_guard import ProcessGuard
from hardware.keyboard_ops import KeyboardOps
from hardware.mouse_ops import MouseOps
from hardware.camera_ops import CameraOps
from hardware.audio_out import AudioOut
from hardware.audio_in import AudioIn
from hardware.peripheral_ops import PeripheralOps
from hardware.notepad_ops import NotepadOps
from hardware.window_ops import WindowOps
from hardware.clipboard_ops import ClipboardOps
from hardware.notification_ops import NotificationOps
from hardware.brightness_ops import BrightnessOps
from visual.desktop_mask import DesktopMask
from visual.fake_ui import FakeUI
from visual.overlay_manager import OverlayManager
from visual.browser_ops import BrowserOps
from visual.icon_ops import IconOps
from visual.horror_effects import get_horror_effects
from visual.gdi_engine import GDIEngine
from visual.effects.screen_melter import trigger_melt
from hardware.wallpaper_ops import WallpaperOps

# NEW: Sprint 3 imports
from visual.effects.screen_tear import ScreenTear
from visual.effects.pixel_melt import PixelMelt

class FunctionDispatcher(QObject):
    """
    Translates JSON commands from the Brain (or Heartbeat) into actual Python function calls.
    Acts as the bridge between 'Thinking' and 'Doing'.
    
    FIXED:
    - Inherits from QObject for Qt signal support
    - Added chat_response_signal for thread-safe UI updates
    - Added AUDIO_GLITCH action handler
    """
    
    # FIXED: Signal for thread-safe chat response handling
    chat_response_signal = pyqtSignal(dict, object)  # (response, chat_window)
    
    def __init__(self):
        super().__init__()
        self.process_guard = ProcessGuard()
        self.audio_out = AudioOut()
        self.audio_in = AudioIn()
        self.camera = CameraOps()
        self.overlay = OverlayManager()
        self.mask = DesktopMask()
        self.fake_ui = FakeUI()
        self.browser = BrowserOps()
        self.notifications = NotificationOps()
        self.gdi = GDIEngine()
        self._chat_thread = None
        
        # YENİ: Memory ve Brain referansları (main.py'den ayarlanır)
        self.memory = None
        self.brain = None
        self.heartbeat = None
        
        self.chat_response_signal.connect(self._process_chat_response)

    def enable_chat(self, brain):
        """Enables the interactive chat and connects it to the Brain."""
        chat_window = self.fake_ui.show_chat()
        # Connect signal: When user types, Brain answers
        chat_window.message_sent.connect(lambda text: self._handle_chat_input(text, brain, chat_window))
        self.audio_out.play_tts("Seni dinliyorum.")

    def _handle_chat_input(self, text, brain, chat_window):
        # YENİ: Aktiviteyi bildir (Heartbeat pacing için)
        if self.heartbeat:
            self.heartbeat.update_activity()
            
        from core.logger import log_info
        log_info(f"Kullanıcı mesajı: {text}", "CHAT")
        
        # YENİ: Davranış analizi yap
        if self.brain:
            behavior = self.brain.analyze_user_behavior(text)
            if behavior:
                print(f"[CHAT] Behavior detected: {behavior}")
        
        # YENİ: Konuşmayı kaydet
        if self.memory:
            from core.context_observer import ContextObserver
            context = ContextObserver.get_full_context()
            self.memory.add_conversation("user", text, context)
            self.memory.log_event("USER_CHAT_MESSAGE", {"text": text[:100]})
        
        def on_response(resp):
            self.chat_response_signal.emit(resp, chat_window)
        
        self._chat_thread = brain.generate_async(text, on_response)
        print(f"[CHAT] Async thread created")

    def _process_chat_response(self, response: dict, chat_window):
        """
        FIXED: Thread-safe handler for chat responses.
        This is called on the main thread via Qt signal.
        """
        print(f"[CHAT] Processing response on main thread: {response}")
        
        if not response:
            print("[CHAT] ERROR: Empty response from AI!")
            chat_window.show_reply("Bir hata oluştu...")
            return
        
        reply_text = response.get("speech", "...")
        print(f"[CHAT] Showing reply: {reply_text}")
        chat_window.show_reply(reply_text)
        
        # Dispatch side effects
        if response.get("action") != "NONE":
            self.dispatch(response)
        
        # Audio - sadece typing sound, TTS rate limiting tarafından kontrol edilecek
        self.audio_out.play_typing_custom()
        # FIXED: TTS kaldırıldı - çok sık konuşuyordu, metin zaten gösteriliyor

    def dispatch(self, command_data: dict):
        """
        Parses the JSON/Dict: {"action": "THE_MASK", "params": {...}}
        Calls the appropriate function.
        """
        if not command_data: return
        
        action = command_data.get("action", "").upper()
        # Ensure params is always a dict, even if JSON has "params": null or missing
        raw_params = command_data.get("params")
        params = raw_params if isinstance(raw_params, dict) else {}
        speech = command_data.get("speech", "")

        print(f"[DISPATCH] Processing Action: {action}")

        # FIXED: TTS sadece önemli aksiyonlarda ve speech varsa çağrılır
        # Bazı aksiyonlar sessiz olmalı (MOUSE_SHAKE, CLIPBOARD_POISON vs.)
        SILENT_ACTIONS = ["MOUSE_SHAKE", "CLIPBOARD_POISON", "GLITCH_SCREEN", 
                          "CAPSLOCK_TOGGLE", "ICON_SCRAMBLE", "BRIGHTNESS_FLICKER"]
        
        if speech and action not in SILENT_ACTIONS:
            self.audio_out.play_tts(speech)

        # 2. Route Action
        if action == "THE_MASK":
            self.mask.capture_and_mask()
        
        elif action == "GLITCH_SCREEN":
            self.overlay.show_text("SİSTEM ARIZA", 1000)
            self.audio_out.play_sfx("glitch")

        elif action == "MOUSE_SHAKE":
            MouseOps.shake_cursor()

        elif action == "LOCK_INPUT":
            KeyboardOps.lock_input()

        elif action == "UNLOCK_INPUT":
            KeyboardOps.unlock_input()
            
        elif action == "GHOST_TYPE":
            text = params.get("text", "Geri dönüşün yok.")
            KeyboardOps.ghost_type(text, self.process_guard)

        elif action == "FAKE_BSOD":
            self.fake_ui.show_bsod()

        elif action == "FAKE_UPDATE":
            percent = params.get("percent", 0)
            self.fake_ui.show_fake_update(percent)

        elif action == "OPEN_BROWSER":
            url = params.get("url", "https://google.com")
            self.browser.open_url(url)
        
        elif action == "PLAY_SFX":
            sound = params.get("sound_name", "glitch")
            self.audio_out.play_sfx(sound)
        
        # === AUDIO_GLITCH ACTION (FIXED) ===
        elif action == "AUDIO_GLITCH":
            # Play static/glitch sound effect
            self.audio_out.play_sfx("static_noise")
            print("[DISPATCH] Audio glitch triggered")
        
        # === VIRUS MECHANICS ===
        
        elif action == "NOTEPAD_HIJACK":
            text = params.get("text", "YARDIM EDİN")
            delay = params.get("delay", 0.1)
            NotepadOps.hijack_and_type(text, delay)
        
        elif action == "CORRUPT_WINDOWS":
            WindowOps.corrupt_all_windows()
        
        elif action == "CLIPBOARD_POISON":
            text = params.get("text", "SEN BENİMSİN")
            ClipboardOps.poison_clipboard(text)
        
        elif action == "FAKE_NOTIFICATION":
            title = params.get("title")
            message = params.get("message")
            self.notifications.show_fake_system_alert(title, message)
        
        elif action == "BRIGHTNESS_FLICKER":
            times = params.get("times", 3)
            BrightnessOps.flicker(times)
        
        elif action == "BRIGHTNESS_DIM":
            target = params.get("target", 10)
            BrightnessOps.gradual_dim(target)
        
        elif action == "SCRAMBLE_ICONS":
            pattern = params.get("pattern", "spiral")
            IconOps.scramble_into_pattern(pattern)
        
        elif action == "SHAKE_CHAT":
            intensity = params.get("intensity", 10)
            if self.fake_ui.chat:
                self.fake_ui.chat.shake_window(intensity)
        
        elif action == "SHAKE_SCREEN":
            intensity = params.get("intensity", 20)
            duration = params.get("duration", 1000)
            self.overlay.shake_screen(intensity, duration)
            
        elif action == "FLASH_COLOR":
            color = params.get("color", "#FF0000")
            opacity = params.get("opacity", 0.4)
            duration = params.get("duration", 300)
            self.overlay.flash_color(color, opacity, duration)

        # === GDI LOW-LEVEL EFFECTS (Path B) ===
        elif action == "SCREEN_INVERT":
            duration = params.get("duration", 200)
            self.gdi.invert_screen(duration)

        elif action == "GDI_STATIC":
            duration = params.get("duration", 500)
            density = params.get("density", 0.01)
            self.gdi.draw_static_noise(duration_ms=duration, density=density)

        elif action == "GDI_LINE":
            color = params.get("color", 0x0000FF) # Blue (Red is BGR 0x0000FF in win32)
            thickness = params.get("thickness", 2)
            self.gdi.draw_horror_line(color=color, thickness=thickness)

        elif action == "GDI_FLASH":
            self.gdi.flash_red_glitch()

        elif action == "SCREEN_MELT":
            trigger_melt()

        elif action == "SET_WALLPAPER":
            path = params.get("image_path")
            if path:
                WallpaperOps.set_wallpaper(path)

        elif action == "SET_PERSONA":
            persona = params.get("persona")
            if self.brain and persona:
                self.brain.switch_persona(persona)
                # Automatically update UI mood based on persona
                if persona == "ENTITY":
                    if self.fake_ui.chat: self.fake_ui.chat.set_mood("ANGRY")
                elif persona == "SUPPORT":
                    if self.fake_ui.chat: self.fake_ui.chat.set_mood("NORMAL")

        elif action == "SET_MOOD":
            # Direct mood control
            mood = params.get("mood", "NORMAL")
            if self.fake_ui.chat:
                self.fake_ui.chat.set_mood(mood)

        elif action == "RESTORE_SYSTEM":
            # Safety cleanup
            WindowOps.restore_all_windows()
            IconOps.restore_icon_positions()
            BrightnessOps.restore_brightness()
            print("[DISPATCH] System restoration completed")

        elif action == "KILL_PROCESS":
            target = params.get("process_name", "")
            if self.process_guard.is_protected(target):
                print(f"[DISPATCH] BLOCKED: Cannot kill protected process {target}")
                self.audio_out.play_tts("Bunu yapamam.")
            else:
                print(f"[DISPATCH] Killing process: {target}")
                # os.kill logic would go here
        
        elif action == "NONE":
            # Gelişmiş: Anger seviyesi çok yüksekse sessizce chat'i titret
            if self.heartbeat and self.heartbeat.anger.current_anger > 75:
                if self.fake_ui.chat:
                    self.fake_ui.chat.shake_window(5)
            pass
        
        # === YENİ: YARATICI KORKU EFEKTLERİ ===
        
        elif action == "FAKE_FILE_DELETE":
            horror = get_horror_effects(self)
            horror.fake_file_deletion()
        
        elif action == "CAMERA_THREAT":
            self.camera.fake_camera_threat()
        
        elif action == "CAMERA_FLASH":
            self.camera.camera_flash_scare()
        
        elif action == "APP_THREAT":
            horror = get_horror_effects(self)
            horror.app_specific_threat()
        
        elif action == "NAME_REVEAL":
            horror = get_horror_effects(self)
            horror.dramatic_name_reveal()
        
        elif action == "TIME_DISTORTION":
            horror = get_horror_effects(self)
            horror.time_distortion_effect()
        
        elif action == "FAKE_BROWSER_HISTORY":
            horror = get_horror_effects(self)
            horror.fake_browser_history_threat()
        
        elif action == "FAKE_LISTENING":
            horror = get_horror_effects(self)
            horror.fake_listening_feedback()
        
        elif action == "CREEPY_MUSIC":
            horror = get_horror_effects(self)
            horror.creepy_lullaby()
            
        elif action == "WHISPER":
            horror = get_horror_effects(self)
            horror.mechanical_whispers()
            
        elif action == "DIGITAL_GLITCH_SURGE":
            horror = get_horror_effects(self)
            horror.digital_glitch_surge()
        
        # === SPRINT 3: ADVANCED GDI EFFECTS ===
        
        elif action == "SCREEN_TEAR":
            intensity = params.get("intensity", 15)
            duration = params.get("duration", 500)
            ScreenTear.tear_screen(intensity, duration)
        
        elif action == "PIXEL_MELT":
            PixelMelt.trigger_random()
            
        else:
            print(f"[DISPATCH] Unknown Action: {action}")
