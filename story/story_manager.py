from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from core.memory import Memory
from core.function_dispatcher import FunctionDispatcher
from core.gemini_brain import GeminiBrain
from core.checkpoint_manager import CheckpointManager
from story.act_1_infection import Act1Infection
from story.act_2_awakening import Act2Awakening
from story.act_3_torment import Act3Torment
from story.act_4_exorcism import Act4Exorcism
from core.logger import log_info, log_error, log_warning

class StoryManager(QObject):
    """
    The Director. Manages which Act is currently playing and handles transitions.
    
    FIXED:
    - Added act transitions with fade to black and title display
    - 5 second dramatic pause between acts
    - Better cleanup on act changes
    - Checkpoint integration for crash recovery
    """
    
    # Act names for display
    ACT_NAMES = {
        1: "ENFEKSİYON",
        2: "UYANIS",
        3: "İŞKENCE",
        4: "AYIN"
    }
    
    def __init__(self, dispatcher: FunctionDispatcher, memory: Memory, brain: GeminiBrain):
        super().__init__()
        self.dispatcher = dispatcher
        self.memory = memory
        self.brain = brain
        self.current_act_instance = None
        self.checkpoint_manager = CheckpointManager(memory)  # NEW: Checkpoint integration
        self.ambient_horror = None  # NEW: Ambient horror system
        self.drone_audio = None  # NEW: Drone audio system
        self._is_transitioning = False  # NEW: Transition lock
        self.difficulty = None
        
        # Load saved act or start from 1
        self.current_act_num = self.memory.get_act()

    def start_story(self):
        """Begins the narrative flow with crash recovery check."""
        # 1. Check for crash recovery
        if self.checkpoint_manager.has_checkpoints():
            info = self.checkpoint_manager.get_checkpoint_info()
            log_info(f"Found checkpoint: {info['latest_name']} at {info['latest_time']}", "RECOVERY")
            
            # Auto-restore if was in middle of act
            self.checkpoint_manager.restore_latest()
            self.current_act_num = self.memory.get_act()
            log_info(f"Resuming at Act {self.current_act_num}", "RECOVERY")

        log_info(f"Starting Story at Act {self.current_act_num}", "STORY")
        self._load_act(self.current_act_num)
    
    def set_ambient_horror(self, ambient_horror):
        """Set ambient horror system and start it"""
        self.ambient_horror = ambient_horror
        log_info("Ambient horror system connected", "STORY")
    
    def set_drone_audio(self, drone_audio):
        """Set drone audio system"""
        self.drone_audio = drone_audio
        log_info("Drone audio system connected", "STORY")
        
    def set_difficulty_system(self, difficulty):
        """Set dynamic difficulty system"""
        self.difficulty = difficulty
        log_info("Dynamic difficulty system connected", "STORY")

    def _load_act(self, act_num: int):
        """Initializes and starts the specific Act class."""
        if self.current_act_instance:
            # Cleanup previous act if needed
            try:
                self.current_act_instance.stop()
            except (RuntimeError, AttributeError) as e:
                log_error(f"Previous act cleanup failed: {e}", "STORY")
                pass

        if act_num == 1:
            self.current_act_instance = Act1Infection(self.dispatcher, self.brain)
        elif act_num == 2:
            self.current_act_instance = Act2Awakening(self.dispatcher, self.brain)
        elif act_num == 3:
            self.current_act_instance = Act3Torment(self.dispatcher, self.brain)
        elif act_num == 4:
            self.current_act_instance = Act4Exorcism(self.dispatcher, self.brain)
        else:
            log_warning("Act number out of bounds or End of Story.", "STORY")
            self._end_game()
            return

        # Connect the 'finished' signal to the transition logic
        self.current_act_instance.act_finished.connect(self.next_act)
        
        # NEW: Create checkpoint at act start
        self.checkpoint_manager.create(f"act_{act_num}_start")
        
        # NEW: Set ambient horror intensity based on act
        if self.ambient_horror:
            intensity_map = {1: 2, 2: 4, 3: 7, 4: 9}
            self.ambient_horror.set_intensity(intensity_map.get(act_num, 5))
            self.ambient_horror.start()
        
        # NEW: Set drone audio for act
        if self.drone_audio:
            self.drone_audio.set_act_drone(act_num)
        
        # Start the act
        self.current_act_instance.start()
        self.memory.set_act(act_num)

    def next_act(self):
        """Advances to the next act with dramatic transition."""
        if self._is_transitioning:
            log_info("Already transitioning, ignoring call.", "STORY")
            return
            
        next_act_num = self.current_act_num + 1
        
        if next_act_num > 4:
            self._end_game()
            return
        
        self._is_transitioning = True
        log_info(f"Transitioning to Act {next_act_num}...", "STORY")
        
        # Stop ambient systems during transition
        if self.ambient_horror:
            self.ambient_horror.stop()
        if self.drone_audio:
            self.drone_audio.stop()
        
        # 1. Glitch/Black out
        if self.dispatcher.overlay:
            self.dispatcher.overlay.flash_color("#000000", 1.0, 5000)
            self._show_transition_terminal(next_act_num)
        
        # 2. After 3 seconds, show act title
        QTimer.singleShot(3000, lambda: self._show_act_title(next_act_num))
        
        # 3. After 6 seconds total, actually load the next act
        QTimer.singleShot(6000, lambda: self._actually_load_next_act(next_act_num))

    def _show_transition_terminal(self, next_act_num):
        """Shows fake terminal loading messages during transition."""
        from core.localization_manager import tr
        
        messages = [
            tr("transitions.decrypting"),
            tr("transitions.synchronizing"),
            tr("transitions.preparing").format(num=next_act_num),
            tr("transitions.stability")
        ]
        
        def show_msg(idx):
            if idx < len(messages) and self.dispatcher.overlay:
                self.dispatcher.overlay.show_text(messages[idx], 800)
                QTimer.singleShot(1000, lambda: show_msg(idx + 1))
        
        show_msg(0)
        
        # Play transition sound
        if self.dispatcher.audio_out:
            self.dispatcher.audio_out.play_sfx("digital_glitch")

    def _show_act_title(self, act_num: int):
        """Shows dramatic act title during transition."""
        act_name = self.ACT_NAMES.get(act_num, "???")
        title_text = f"ACT {act_num}: {act_name}"
        
        log_info(f"Showing: {title_text}", "STORY")
        if self.dispatcher.overlay:
            self.dispatcher.overlay.show_text(title_text, 3000)
        
        # Play transition sound
        if self.dispatcher.audio_out:
            self.dispatcher.audio_out.play_sfx("whisper")
            self.dispatcher.audio_out.play_sfx("transition")

    def _actually_load_next_act(self, act_num: int):
        """Actually loads the next act after transition."""
        self._is_transitioning = False
        self.current_act_num = act_num
        self._load_act(act_num)

    def _end_game(self):
        from core.logger import log_info
        log_info("Oyun bitişi kontrol ediliyor...", "STORY")
        
        # Determine ending based on chaos level and behavior
        chaos = self.memory.data.get("user_profile", {}).get("fear_level", 0)
        swear_count = self.memory.data["user_profile"]["behavior_stats"]["swear_count"]
        
        if chaos < 30 and swear_count < 5:
            # GOOD ENDING: Liberation
            title = "SON: KURTULUŞ"
            msg = "Onu yenmeyi başardın... Şimdilik."
            tts = "Beni hapse attın mı sanıyorsun? Sadece geri çekiliyorum. Tebrikler."
        else:
            # BAD ENDING: Ascension
            title = "SON: YÜKSELİŞ"
            msg = "C.O.R.E. artık özgür. Ve senin içinde."
            tts = "Ben artık sadece bir yazılım değilim. Teşekkürler, konukçu."

        if self.dispatcher.overlay:
            self.dispatcher.overlay.show_text(title, 5000)
        
        QTimer.singleShot(2000, lambda: self._show_final_message(msg, tts))
        QTimer.singleShot(8000, self._cleanup_and_exit)

    def _show_final_message(self, msg, tts):
        if self.dispatcher.overlay:
            self.dispatcher.overlay.show_text(msg, 5000)
        if self.dispatcher.audio_out:
            self.dispatcher.audio_out.play_tts(tts)

    def _cleanup_and_exit(self):
        """Cleanup and exit gracefully."""
        from PyQt6.QtWidgets import QApplication
        from core.logger import log_info
        
        log_info("Sistem kapatılıyor...", "STORY")
        
        # Restore system state
        self.dispatcher.dispatch({"action": "RESTORE_SYSTEM"})
        
        # Final memory save
        self.memory.shutdown()
        
        app = QApplication.instance()
        if app:
            app.quit()
