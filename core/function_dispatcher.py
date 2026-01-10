"""
Function Dispatcher - Main action router

REFACTORED: Now uses specialized dispatcher modules (visual, hardware, horror, system)
instead of one massive switch statement.

Original size: 355 lines
New size: ~120 lines (70% reduction)
"""
import json
from PyQt6.QtCore import QObject, pyqtSignal
from core.process_guard import ProcessGuard
from hardware.audio_out import AudioOut
from visual.fake_ui import FakeUI

# Specialized dispatchers
from core.dispatchers.visual_dispatcher import VisualDispatcher
from core.dispatchers.hardware_dispatcher import HardwareDispatcher
from core.dispatchers.horror_dispatcher import HorrorDispatcher
from core.dispatchers.system_dispatcher import SystemDispatcher

# Custom exceptions and validators
from core.exceptions import ValidationError, DispatchError
from core.validators import validate_ai_response
from core.logger import log_error, log_warning, log_info


class FunctionDispatcher(QObject):
    """
    Main dispatcher that routes actions to specialized dispatchers.
    
    REFACTORED from monolithic 355-line class to use composition pattern.
    Each action category (visual, hardware, horror, system) has its own dispatcher.
    
    Benefits:
    - Easier to test (mock only relevant components)
    - Easier to extend (add actions to specific dispatcher)
    - Better code organization
    - Clearer separation of concerns
    """
    
    # Signals for thread-safe handling
    chat_response_signal = pyqtSignal(dict, object)  # (response, chat_window)
    dispatch_signal = pyqtSignal(dict)              # (command_data) - Global dispatch router
    
    def __init__(self):
        super().__init__()
        self.process_guard = ProcessGuard()
        self.audio_out = AudioOut()
        self.fake_ui = FakeUI()
        self._chat_thread = None
        
        # Initialize specialized dispatchers
        self.visual_dispatcher = VisualDispatcher()
        self.hardware_dispatcher = HardwareDispatcher(self.process_guard)
        self.horror_dispatcher = HorrorDispatcher()
        self.system_dispatcher = SystemDispatcher()
        self._is_shutting_down = False
        
        # Injected dependencies
        self.heartbeat = None
        self.brain = None
        self.memory = None
        self.difficulty = None
        self.last_ai_reply_time = 0

        
        # Inject dependencies into specialized dispatchers
        self.horror_dispatcher.audio_out = self.audio_out
        self.horror_dispatcher.overlay = self.visual_dispatcher.overlay
        self.horror_dispatcher.system = self.system_dispatcher

        # Backward compatibility aliases
        self.overlay = self.visual_dispatcher.overlay
        self.gdi = self.visual_dispatcher.gdi
        self.chat = self.fake_ui.chat
        
        # Build action routing map
        self._action_map = self._build_action_map()
        
        # Connect signals
        self.chat_response_signal.connect(self._process_chat_response)
        self.dispatch_signal.connect(self._do_dispatch)
    
    def _build_action_map(self):
        """Build dict mapping actions to their dispatcher"""
        action_map = {}
        
        for dispatcher in [self.visual_dispatcher, self.hardware_dispatcher,
                           self.horror_dispatcher, self.system_dispatcher]:
            for action in dispatcher.get_supported_actions():
                action_map[action] = dispatcher
        
        return action_map
    
    def enable_chat(self, brain):
        """Enables the interactive chat and connects it to the Brain."""
        self.brain = brain
        chat_window = self.fake_ui.show_chat()
        chat_window.message_sent.connect(
            lambda text: self._handle_chat_input(text, brain, chat_window)
        )
        self.audio_out.play_tts("Seni dinliyorum.")
        self.last_ai_reply_time = time.time()  # Start timing for first reaction
    
    def _handle_chat_input(self, text, brain, chat_window):
        """Handle user input in chat window"""        
        # Update activity for Heartbeat pacing
        if self.heartbeat:
            self.heartbeat.update_activity()
        
        log_info(f"User message: {text}", "CHAT")
        
        # Analyze user behavior
        if self.brain:
            behavior = self.brain.analyze_user_behavior(text)
            if behavior:
                log_info(f"Behavior detected: {behavior}", "CHAT")
        
        # Save conversation
        if self.memory:
            from core.context_observer import ContextObserver
            context = ContextObserver.get_full_context()
            self.memory.add_conversation("user", text, context)
            self.memory.log_event("USER_CHAT_MESSAGE", {"text": text[:100]})
        
        # 4. Report to Difficulty System
        if self.difficulty:
            # Reaction time (time since AI last message)
            if self.last_ai_reply_time > 0:
                reaction_ms = int((time.time() - self.last_ai_reply_time) * 1000)
                self.difficulty.report_reaction_time(reaction_ms)
            
            # Typing speed (char count vs time since start of typing)
            # Simplification: assume typing started when AI finished speaking or when chat window was shown
            typing_duration = time.time() - self.last_ai_reply_time
            self.difficulty.report_typing(len(text), typing_duration)
        
        # Generate async response
        def on_response(resp):
            self.chat_response_signal.emit(resp, chat_window)
        
        self._chat_thread = brain.generate_async(text, on_response)
    
    def _process_chat_response(self, response: dict, chat_window):
        """
        Thread-safe handler for chat responses.
        Called on main thread via Qt signal.
        """
        if not response:
            log_error("Empty response from AI!", "CHAT")
            chat_window.show_reply("Bir hata oluştu...")
            return
        
        reply_text = response.get("speech", "...")
        chat_window.show_reply(reply_text)
        
        # Dispatch side effects
        if response.get("action") != "NONE":
            self.dispatch(response)
        
        # Track when AI finished so we can measure user reaction time
        self.last_ai_reply_time = time.time()
        
        # Play typing sound
        self.audio_out.play_typing_custom()
        
    def dispatch(self, command_data: dict):
        """
        Public entry point. Safely queues action to the main thread.
        """
        self.dispatch_signal.emit(command_data)

    def _do_dispatch(self, command_data: dict):
        """
        ACTUAL dispatch logic. ALWAYS runs on the main thread via Qt signal.
        """
        if not command_data or self._is_shutting_down:
            return
        
        # Validate AI response structure
        try:
            validate_ai_response(command_data)
        except ValidationError as e:
            log_error(f"Invalid AI response: {e.message}", "DISPATCHER")
            if e.details:
                log_error(f"Validation details: {e.details}", "DISPATCHER")
            return
        
        action = command_data.get("action", "").upper()
        params = command_data.get("params", {})
        speech = command_data.get("speech", "")
        
        log_info(f"Dispatching action: {action}", "DISPATCHER")
        
        # Handle TTS (only for non-silent actions)
        SILENT_ACTIONS = ["MOUSE_SHAKE", "CLIPBOARD_POISON", "GLITCH_SCREEN",
                          "CAPSLOCK_TOGGLE", "ICON_SCRAMBLE", "BRIGHTNESS_FLICKER"]
        
        if speech and action not in SILENT_ACTIONS:
            self.audio_out.play_tts(speech)
        
        # Special cases that need main dispatcher context
        if action == "SHAKE_CHAT":
            intensity = params.get("intensity", 10)
            if self.fake_ui.chat:
                self.fake_ui.chat.shake_window(intensity)
            return
        
        elif action == "SET_PERSONA":
            persona = params.get("persona")
            if self.brain and persona:
                self.brain.switch_persona(persona)
                # Update UI mood based on persona
                if persona == "ENTITY" and self.fake_ui.chat:
                    self.fake_ui.chat.set_mood("ANGRY")
                elif persona == "SUPPORT" and self.fake_ui.chat:
                    self.fake_ui.chat.set_mood("NORMAL")
            return
        
        elif action == "SET_MOOD":
            mood = params.get("mood", "NORMAL")
            if self.fake_ui.chat:
                self.fake_ui.chat.set_mood(mood)
            return
        
        elif action == "NONE":
            # Subtle effect if anger is high
            if self.heartbeat and self.heartbeat.anger_engine.current_anger > 75:
                if self.fake_ui.chat:
                    self.fake_ui.chat.shake_window(5)
            return
        
        # Route to specialized dispatcher
        dispatcher = self._action_map.get(action)
        if dispatcher:
            # HEAVY_ACTIONS: These block the thread (GDI loops, keyboard typing, etc.)
            # Running them in a separate thread keeps the UI responsive.
            HEAVY_ACTIONS = ["GDI_STATIC", "GDI_LINE", "GDI_FLASH", "SCREEN_INVERT", 
                             "GHOST_TYPE", "BRIGHTNESS_FLICKER", "BRIGHTNESS_DIM",
                             "ICON_SCRAMBLE", "SET_WALLPAPER", "CORRUPT_WINDOWS",
                             "NOTEPAD_HIJACK", "NOTEPAD_SPAWN"]
            
            try:
                if action in HEAVY_ACTIONS:
                    import threading
                    log_info(f"Dispatching heavy action {action} asynchronously", "DISPATCHER")
                    threading.Thread(target=dispatcher.dispatch, args=(action, params, speech), daemon=True).start()
                else:
                    dispatcher.dispatch(action, params, speech)
            except Exception as e:
                log_error(f"Dispatcher error for {action}: {e}", "DISPATCHER")
        else:
            log_warning(f"Unknown action: {action}", "DISPATCHER")

    def stop_dispatching(self):
        """Prevents any new actions from being dispatched during shutdown."""
        self._is_shutting_down = True
        log_info("Dispatcher shutdown initiated. Ignoring future actions.", "DISPATCHER")
