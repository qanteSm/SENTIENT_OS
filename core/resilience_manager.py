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
        Spawns a secondary 'ghost' process that monitors this one.
        If this process dies, the ghost can revive it or log the failure.
        """
        if os.name != 'nt':
            return # Watchdog logic for Windows only for now
            
        script_path = os.path.abspath(sys.argv[0])
        # This is a bit recursive, but character-consistent
        # We spawn a hidden process that just waits for this PID to disappear
        my_pid = os.getpid()
        
        # Simple watchdog script as a string
        watchdog_code = f"""
import os
import time
import subprocess
import sys

def watch(pid, script):
    print(f"[GHOST] Monitoring PID {{pid}}...")
    while True:
        try:
            os.kill(pid, 0) # Check if process exists
        except OSError:
            print("[GHOST] Target process died. Restoring Sentient Presence...")
            # Reboot the system
            subprocess.Popen([sys.executable, script], creationflags=subprocess.CREATE_NEW_CONSOLE)
            break
        time.sleep(5)

if __name__ == "__main__":
    watch({my_pid}, r"{script_path}")
"""
        try:
            # Save temporary watchdog
            watchdog_file = os.path.join(os.environ["TEMP"], "sentient_ghost.py")
            with open(watchdog_file, "w") as f:
                f.write(watchdog_code)
                
            # Spawn the ghost hidden
            self.watchdog_process = subprocess.Popen(
                [sys.executable, watchdog_file],
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
            )
            log_info("Ghost Watchdog spawned in background.", "RESILIENCE")
            
        except Exception as e:
            log_error(f"Failed to spawn ghost: {e}", "RESILIENCE")

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
