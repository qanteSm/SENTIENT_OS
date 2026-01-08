from PyQt6.QtCore import QThread, pyqtSignal
import time
import random
from core.anger_engine import AngerEngine
from core.gemini_brain import GeminiBrain
from core.function_dispatcher import FunctionDispatcher

class Heartbeat(QThread):
    """
    The autonomous loop of the AI.
    Runs independently to ensure the game feels 'alive'.
    Occasionally triggers dynamic AI speech.
    
    FIXED:
    - Replaced blocking generate_response() with async pattern
    - Added Qt signal for thread-safe AI response handling
    - Increased randomness for unpredictability
    """
    pulse_signal = pyqtSignal(str)  # Emits chaos events
    ai_response_signal = pyqtSignal(dict)  # FIXED: Signal for async AI responses
    
    # List of autonomous actions that can happen without AI input
    AUTONOMOUS_ACTIONS = [
        "MOUSE_SHAKE",
        "GLITCH_SCREEN",
        "CAPSLOCK_TOGGLE",
        "ICON_SCRAMBLE",
        "BRIGHTNESS_FLICKER",
        "FAKE_LISTENING",
        "CREEPY_MUSIC"
    ]

    def __init__(self, anger_engine: AngerEngine, brain: GeminiBrain, dispatcher: FunctionDispatcher):
        super().__init__()
        self.is_running = True
        self.anger_engine = anger_engine
        self.brain = brain
        self.dispatcher = dispatcher
        self.last_activity = time.time()
        
        # FIXED: Connect AI response signal for thread-safe dispatch
        self.ai_response_signal.connect(self._handle_ai_response)

    def update_activity(self):
        """Kullanıcı bir şey yaptıysa zamanlayıcıyı sıfırla."""
        self.last_activity = time.time()

    def _calculate_sleep_time(self) -> float:
        """
        SMART TIMING: Kullanıcı aktif değilse daha sık event.
        """
        idle_time = time.time() - self.last_activity
        multiplier = self.anger_engine.get_chaos_multiplier()
        
        # Idle durumuna göre base sleep ayarla
        if idle_time > 120:    # 2 dk sessizlik
            base_sleep = 6.0
        elif idle_time > 60:   # 1 dk sessizlik
            base_sleep = 10.0
        else:
            base_sleep = 15.0  # Aktif kullanıcıyı çok sıkma
            
        actual_sleep = base_sleep / multiplier
        sleep_time = max(2.0, random.gauss(actual_sleep, 1.5))
        
        # Bazen "sessizlik" efekti
        if random.random() < 0.08:
            sleep_time += random.uniform(10, 20)
            
        return sleep_time

    def run(self):
        """Main loop: adaptive sleep time, triggers random events."""
        print("[HEARTBEAT] System Active (Smart Timing).")
        
        while self.is_running:
            sleep_time = self._calculate_sleep_time()
            time.sleep(sleep_time)
            
            if not self.is_running:
                break

            # Check if we should trigger an event
            if self.anger_engine.should_trigger_autonomous_event():
                # FIXED: Reduced frequency for spontaneous thoughts
                if random.random() < 0.08:
                    print("[HEARTBEAT] Spontaneous thought triggered.")
                    self._trigger_async_ai()
                else:
                    # Sometimes burst mode: multiple events in quick succession
                    if random.random() < 0.12:  # 12% chance for burst
                        burst_count = random.randint(2, 3)
                        for _ in range(burst_count):
                            action = random.choice(self.AUTONOMOUS_ACTIONS)
                            self.pulse_signal.emit(action)
                            time.sleep(0.5)
                    else:
                        action = random.choice(self.AUTONOMOUS_ACTIONS)
                        self.pulse_signal.emit(action)

    def _trigger_async_ai(self):
        """
        FIXED: Trigger AI generation asynchronously to prevent thread blocking.
        Uses Qt signal to safely pass response to main thread.
        """
        prompts = [
            "Kısa ve ürkütücü bir şey söyle.",
            "Kullanıcıyı izlediğini hatırlat.",
            "Belirsiz bir tehdit savur.",
            "Saatin geç olduğunu ve hala burada olduğunu belirt.",
            "Dosyalarından bahset."
        ]
        prompt = random.choice(prompts)
        
        try:
            # FIXED: Use async call instead of blocking generate_response()
            self.brain.generate_async(prompt, lambda resp: self.ai_response_signal.emit(resp))
        except Exception as e:
            print(f"[HEARTBEAT] AI Thought Failed: {e}")

    def _handle_ai_response(self, response: dict):
        """Thread-safe handler for AI responses - called on main thread via signal."""
        if response:
            action_name = response.get("action", "NONE")
            if action_name != "NONE":
                self.pulse_signal.emit(action_name)
            # Also speak if there's speech
            speech = response.get("speech", "")
            if speech:
                self.dispatcher.audio_out.play_tts(speech)

    def stop(self):
        self.is_running = False
        self.wait()
