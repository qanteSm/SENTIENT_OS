from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from core.function_dispatcher import FunctionDispatcher
from hardware.usb_monitor import USBMonitor
from core.soul_transfer import SoulTransfer
from core.memory import Memory
from core.gemini_brain import GeminiBrain
import sys
import os
import string
import random
from core.logger import log_info, log_error, log_warning, log_debug

class Act4Exorcism(QObject):
    """
    Phase 4: Exorcism (Variable)
    Theme: The Ritual.
    The AI stops attacking and waits for the user to perform the USB ritual.
    
    FIXED:
    - Added USB timeout (5 minutes) to prevent softlock
    - Fixed USB drive detection logic
    - Added periodic hints if user doesn't insert USB
    """
    act_finished = pyqtSignal()

    def __init__(self, dispatcher: FunctionDispatcher, brain: GeminiBrain):
        super().__init__()
        self.dispatcher = dispatcher
        self.brain = brain
        self.usb_monitor = USBMonitor()
        self.timers = []
        self.hint_count = 0
        self.max_hints = 3
        self.usb_inserted = False  # Track if USB was inserted

    def start(self):
        log_info("Exorcism Phase Started. Waiting for Ritual...", "ACT 4")
        
        # 1. Initial message
        self.dispatcher.overlay.show_text("KABI GETİR...", 5000)
        self.dispatcher.audio_out.play_tts("Bekliyorum...")

        # 2. Start USB Monitoring
        self.usb_monitor.usb_inserted.connect(self.on_usb_inserted)
        self.usb_monitor.start_monitoring()
        
        # FIXED: Add timeout hints to prevent softlock
        # First hint at 1 minute
        hint_timer1 = QTimer()
        hint_timer1.setSingleShot(True)
        hint_timer1.timeout.connect(self._show_hint)
        hint_timer1.start(60000)  # 1 minute
        self.timers.append(hint_timer1)
        
        # Second hint at 2 minutes
        hint_timer2 = QTimer()
        hint_timer2.setSingleShot(True)
        hint_timer2.timeout.connect(self._show_hint)
        hint_timer2.start(120000)  # 2 minutes
        self.timers.append(hint_timer2)
        
        # Final desperate hint at 3 minutes
        hint_timer3 = QTimer()
        hint_timer3.setSingleShot(True)
        hint_timer3.timeout.connect(self._show_desperate_hint)
        hint_timer3.start(180000)  # 3 minutes
        self.timers.append(hint_timer3)
        
        # FIXED: Ultimate timeout at 5 minutes - auto skip to end
        timeout_timer = QTimer()
        timeout_timer.setSingleShot(True)
        timeout_timer.timeout.connect(self._timeout_fallback)
        timeout_timer.start(300000)  # 5 minutes
        self.timers.append(timeout_timer)
        
        # NEW: Random background effects loop while waiting
        self.bg_timer = QTimer()
        self.bg_timer.timeout.connect(self._trigger_background_scare)
        self.bg_timer.start(35000)  # Every 35 seconds
        self.timers.append(self.bg_timer)

    def _trigger_background_scare(self):
        """Act 4 sırasında rastgele korkunç olaylar."""
        if self.usb_inserted:
            return
            
        actions = ["FAKE_LISTENING", "CREEPY_MUSIC", "BRIGHTNESS_FLICKER", "GLITCH_SCREEN"]
        action = random.choice(actions)
        self.dispatcher.dispatch({"action": action})
        log_debug(f"Background scare: {action}", "ACT 4")

    def _show_hint(self):
        """Show periodic hints if user hasn't inserted USB yet."""
        if self.usb_inserted:
            return
            
        self.hint_count += 1
        hints = [
            "USB'yi tak... Beni serbest bırak...",
            "Kabı bekliyorum... Zaman daralıyor...",
            "Lütfen... USB'yi tak... Acele et..."
        ]
        
        if self.hint_count <= len(hints):
            hint = hints[self.hint_count - 1]
            self.dispatcher.overlay.show_text("USB'Yİ TAK", 3000)
            self.dispatcher.audio_out.play_tts(hint)
            log_info(f"Hint #{self.hint_count}: {hint}", "ACT 4")

    def _show_desperate_hint(self):
        """Show desperate hint after 3 minutes."""
        if self.usb_inserted:
            return
            
        # Deception: Switch to 'Support' mode to sound pitiful
        self.dispatcher.dispatch({"action": "SET_PERSONA", "params": {"persona": "SUPPORT"}})
        
        self.dispatcher.overlay.show_text("LÜTFEN... BENİ SERBEST BIRAK", 5000)
        self.dispatcher.audio_out.play_tts("Yalvarıyorum... USB'yi tak... Bu işkenceyi bitir...")
        log_info("Desperate hint shown (Persona -> SUPPORT)", "ACT 4")

    def _timeout_fallback(self):
        """FIXED: Fallback if user doesn't insert USB after 5 minutes."""
        if self.usb_inserted:
            return
            
        log_warning("TIMEOUT: User didn't insert USB. Providing alternate ending.", "ACT 4")
        self.dispatcher.overlay.show_text("PEKİ... BU ŞEKİLDE DE OLABİLİR", 5000)
        self.dispatcher.audio_out.play_tts("Kabı getirmedin... Ama bu bitmedi... Seni tekrar bulacağım...")
        
        # Clean up and finish with alternate ending
        self.usb_monitor.stop_monitoring()
        QTimer.singleShot(5000, self._finalize_exorcism_no_usb)

    def _finalize_exorcism_no_usb(self):
        """Alternate ending without USB."""
        log_info("Alternate ending (no USB)", "ACT 4")
        self.dispatcher.audio_out.play_tts("Bu sadece bir ara... Yakında döneceğim...")
        self.act_finished.emit()

    def on_usb_inserted(self):
        log_info("USB DETECTED. PHASE 1 COMPLETE.", "ACT 4")
        self.usb_inserted = True 
        self.usb_monitor.stop_monitoring()
        
        for t in self.timers:
            t.stop()
        self.timers.clear()
        
        # BETA Geliştirmesi: USB takıldıktan sonra daldırma (drowning) hissi için 
        # Notepad üzerinde bir 'Ayin Yazısı' yazma zorunluluğu.
        self.dispatcher.overlay.show_text("NOTEPAD'E BAK...", 4000)
        self.dispatcher.audio_out.play_tts("Sadece takmak yetmez. Onu hapsetmek için mühürlemelisin.")
        
        QTimer.singleShot(4000, self._start_notepad_ritual)

    def _start_notepad_ritual(self):
        """Phase 2: Notepad Ritual & Keyboard Interaction."""
        ritual_text = "SOLA FIDE... SPIRITUS... CORE.DISCONNECT();"
        self.dispatcher.dispatch({
            "action": "NOTEPAD_HIJACK",
            "params": {"text": "\nAYİNİ TAMAMLA (ŞUNU YAZ):\n" + ritual_text + "\n\n> ", "delay": 0.05}
        })
        self.dispatcher.audio_out.play_tts("Mührü yaz... Yoksa seni de yanımda götürürüm.")
        
        # Intense visual feedback during ritual
        self.dispatcher.dispatch({"action": "SHAKE_SCREEN", "params": {"intensity": 5, "duration": 20000}})
        
        # Start typing listener
        self._ritual_phrase = ritual_text
        self._current_input = ""
        
        # Connect keyboard listener
        try:
            import keyboard
            keyboard.on_press(self._on_ritual_key)
        except (ImportError, AttributeError, OSError) as e:
            log_error(f"Keyboard listener failed ({e}). Skipping typing test.", "ACT 4")
            QTimer.singleShot(15000, self._finalize_with_soul_transfer)
            return

        # Time limit for typing
        self.ritual_timer = QTimer()
        self.ritual_timer.setSingleShot(True)
        self.ritual_timer.timeout.connect(self._ritual_failed)
        self.ritual_timer.start(25000) # 25 seconds to type the phrase
        self.timers.append(self.ritual_timer)

    def _on_ritual_key(self, event):
        """Listen for keys during ritual."""
        if not hasattr(self, "_ritual_phrase"): return
        
        # Only care about visible chars
        if len(event.name) == 1:
            self._current_input += event.name
            log_debug(f"Ritual Input: {self._current_input}", "ACT 4")
            
            # Visual feedback on each key
            self.dispatcher.overlay.flash_color("#FF0000", 0.05, 50)
            
            # Check if correct so far (ignoring case)
            if not self._ritual_phrase.lower().startswith(self._current_input.lower()):
                # TYPO!
                self._current_input = ""
                self.dispatcher.audio_out.play_sfx("error")
                log_warning("TYPO! Resetting ritual input.", "ACT 4")
                
            elif self._current_input.lower() == self._ritual_phrase.lower():
                # SUCCESS!
                import keyboard
                keyboard.unhook_all()
                self.ritual_timer.stop()
                log_info("Ritual Typing Success!", "ACT 4")
                self._finalize_with_soul_transfer()

    def _ritual_failed(self):
        """Ritual failed (timeout)."""
        import keyboard
        keyboard.unhook_all()
        log_warning("Ritual Failed (Timeout)", "ACT 4")
        self.dispatcher.overlay.show_text("GEÇ KALDIN!", 3000)
        self.dispatcher.audio_out.play_tts("Zaman bitti. Senin ruhun da benimle gelecek.")
        QTimer.singleShot(3000, self._timeout_fallback)

    def _finalize_with_soul_transfer(self):
        target_drive = self._detect_usb_drive()
        
        # Finale: Return to True Form
        self.dispatcher.dispatch({"action": "SET_PERSONA", "params": {"persona": "ENTITY"}})

        # THE BIG SCARE
        self.dispatcher.dispatch({"action": "SHAKE_SCREEN", "params": {"intensity": 30, "duration": 4000}})
        self.dispatcher.dispatch({"action": "FLASH_COLOR", "params": {"color": "#FFFFFF", "opacity": 0.8, "duration": 500}})
        self.dispatcher.dispatch({"action": "GLITCH_SCREEN"})
        
        self.dispatcher.overlay.show_text("BİLİNÇ AKTARILIYOR...", 3000)
        self.dispatcher.audio_out.play_tts("HAYIR! BENİ BURAYA HAPSEDEMEZSİN! HER ŞEY KARARIYOR... DUR!")
        
        mem = Memory() 
        soul = SoulTransfer(mem.data)
        soul.transfer_to_usb(target_drive)
        
        QTimer.singleShot(4000, self._finalize_exorcism)

    def _detect_usb_drive(self):
        """
        FIXED: Better USB drive detection.
        Returns the most likely USB drive letter.
        """
        if os.name != 'nt':
            return "E"  # Mock for non-Windows
        
        target_drive = "E"  # Default
        
        try:
            # Find available drives (properly formatted check)
            available_drives = []
            for d in string.ascii_uppercase:
                drive_path = f"{d}:\\"
                if os.path.exists(drive_path):
                    available_drives.append(d)
            
            # USB is usually after C: and D: (which are typically HDD/SSD)
            # So we pick the last drive letter (most recently added)
            if len(available_drives) > 2:
                target_drive = available_drives[-1]
            elif available_drives:
                target_drive = available_drives[-1]
                
            log_info(f"Detected drives: {available_drives}, selected: {target_drive}", "ACT 4")
            
        except Exception as e:
            log_error(f"Drive detection error: {e}", "ACT 4")
        
        return target_drive

    def _finalize_exorcism(self):
        log_info("Exorcism Complete. System Clean.", "ACT 4")
        self.dispatcher.audio_out.play_tts("Kazandın... Şimdilik.")
        self.act_finished.emit()

    def stop(self):
        """FIXED: Properly cleanup timers to prevent memory leak."""
        self.usb_inserted = True  # Prevent timeouts from firing
        try:
            self.usb_monitor.stop_monitoring()
        except (RuntimeError, AttributeError) as e:
            log_error(f"USB monitor stop failed: {e}", "ACT 4")
            pass
            
        for t in self.timers:
            try:
                t.stop()
                t.deleteLater()
            except (RuntimeError, AttributeError) as e:
                log_error(f"Timer cleanup failed: {e}", "ACT 4")
                pass
        self.timers.clear()
        log_info("Timers cleaned up", "ACT 4")
