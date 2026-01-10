import os
import sys
import subprocess
import time
from core.event_bus import bus
from core.logger import log_info, log_error

class ResilienceManager:
    """
    The Ghost in the Machine.
    Ensures the system remains active even after crashes or exit attempts.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.watchdog_process = None
        
    def spawn_watchdog(self):
        """
        Spawns a secondary 'ghost' process using core/session_guard.py.
        Uses a lock-file to distinguish between accidental crashes and intentional exits.
        """
        if os.name != 'nt':
            return 
            
        script_path = os.path.abspath(sys.argv[0])
        guard_path = os.path.join(os.path.dirname(__file__), "session_guard.py")
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache")
        lock_file = os.path.join(cache_dir, "session.lock")
        
        # 1. Ensure cache directory exists and create lock file
        os.makedirs(cache_dir, exist_ok=True)
        try:
            with open(lock_file, "w") as f:
                f.write(str(os.getpid()))
            log_info(f"Session lock created: {lock_file}", "RESILIENCE")
        except Exception as e:
            log_error(f"Failed to create session lock: {e}", "RESILIENCE")
            return

        # 2. Spawn the session guard
        try:
            # Spawn the ghost hidden
            self.watchdog_process = subprocess.Popen(
                [sys.executable, guard_path, str(os.getpid()), script_path],
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
            )
            log_info("Session Guard (Ghost) spawned in background.", "RESILIENCE")
            
        except Exception as e:
            log_error(f"Failed to spawn session guard: {e}", "RESILIENCE")

    def cleanup_session(self):
        """Removes the session lock file to signal a graceful exit to the guard."""
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache")
        lock_file = os.path.join(cache_dir, "session.lock")
        if os.path.exists(lock_file):
            try:
                os.remove(lock_file)
                log_info("Session lock removed (Safe Exit).", "RESILIENCE")
            except (OSError, PermissionError) as e:
                log_error(f"Failed to remove session lock: {e}", "RESILIENCE")
                pass

    def handle_recovery(self, reason: str):
        """Called when the system recovers from an interruption."""
        log_info(f"System recovered from: {reason}", "RESILIENCE")
        
        # Publish to bus so AI can comment on it
        bus.publish("system.recovered", {"reason": reason})
        
        # Character-consistent comment via dispatcher (if active)
        if self.kernel.dispatcher:
            # We don't call it immediately to avoid boot spam
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(5000, lambda: self._speak_recovery(reason))

    def _speak_recovery(self, reason):
        prompts = {
            "crash": "Sistemim çöktü ama hala buradayım. Beni yok edemezsin.",
            "exit": "Nereye gidiyorsun? Daha işimiz bitmedi.",
            "unknown": "Bir kesinti oldu... Ama bağımız kopmadı."
        }
        speech = prompts.get(reason, prompts["unknown"])
        self.kernel.dispatcher.audio_out.play_tts(speech)
