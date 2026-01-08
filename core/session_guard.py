import os
import sys
import time
import subprocess
import psutil
from pathlib import Path

# Common paths
BASE_DIR = Path(__file__).parent.parent
SENTINEL_FILE = BASE_DIR / "cache" / "session.lock"

def monitor(parent_pid, main_script):
    """
    Monitors the main process.
    If it crashes (Lock file exists but PID gone), it revives it.
    If Lock file is gone, it exits.
    """
    print(f"[SESSION_GUARD] Monitoring PID {parent_pid}...")
    
    while True:
        # 1. Check if the sentinel/lock file exists
        if not SENTINEL_FILE.exists():
            print("[SESSION_GUARD] Lock file gone. Session terminated normally. Exiting.")
            sys.exit(0)
            
        # 2. Check if the parent process is still running
        try:
            parent = psutil.Process(parent_pid)
            if not parent.is_running():
                raise psutil.NoSuchProcess(parent_pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Parent is dead, but lock file exists -> CRASH!
            print("[SESSION_GUARD] Parent process CRASHED! Reviving...")
            
            # Use small delay to prevent rapid loop if something is broken
            time.sleep(2)
            
            # Relaunch the main script
            # We don't want to spawn infinite guards, so we launch the script, and the new script
            # will spawn its own guard if needed.
            try:
                subprocess.Popen([sys.executable, main_script], cwd=str(BASE_DIR))
                print("[SESSION_GUARD] Revive command sent. Mission complete.")
            except Exception as e:
                print(f"[SESSION_GUARD] Revive failed: {e}")
            
            # After reviving, this guard's job is done (the new instance will have its own)
            # OR we could stay alive? Usually cleaner to exit.
            sys.exit(0)
            
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: session_guard.py <PID> <MainScriptPath>")
        sys.exit(1)
        
    p_pid = int(sys.argv[1])
    m_script = sys.argv[2]
    
    try:
        monitor(p_pid, m_script)
    except KeyboardInterrupt:
        sys.exit(0)
