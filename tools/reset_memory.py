import os
import shutil
import sys
from config import Config

def reset_game_data():
    """
    Deletes the 'SentientOS' directory in AppData (or local config dir).
    """
    # 1. Clear .system_state.json (Local system state)
    state_file = os.path.join(Config().BASE_DIR, ".system_state.json")
    if os.path.exists(state_file):
        try:
            os.remove(state_file)
            print(f"[RESET] Deleted local state file: {state_file}")
        except (OSError, PermissionError) as e:
            print(f"[RESET] Failed to delete state file: {e}")
            pass

    # 2. Clear AppData/SentientOS (Memory, Checkpoints, Logs)
    if Config().IS_WINDOWS:
        app_data = os.getenv('APPDATA')
        if app_data:
            target_dir = os.path.join(app_data, "SentientOS")
            if os.path.exists(target_dir):
                try:
                    shutil.rmtree(target_dir)
                    print(f"[RESET] Wiped AppData directory: {target_dir}")
                except Exception as e:
                    print(f"[RESET] Failed to wipe AppData: {e}")
    
    # 3. Clear local brain_dump if exists
    local_memory = os.path.join(Config().BASE_DIR, "brain_dump.json")
    if os.path.exists(local_memory):
        try:
            os.remove(local_memory)
            print(f"[RESET] Deleted local memory file: {local_memory}")
        except (OSError, PermissionError) as e:
            print(f"[RESET] Failed to delete memory file: {e}")
            pass

    print("[RESET] Game has been restored to factory settings. You can now start fresh.")

if __name__ == "__main__":
    reset_game_data()
