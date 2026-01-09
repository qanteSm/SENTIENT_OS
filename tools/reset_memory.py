import os
import shutil
import sys
from config import Config

def reset_game_data():
    """
    Deletes the 'SentientOS' directory in AppData (or local config dir).
    """
    if Config().IS_WINDOWS:
        app_data = os.getenv('APPDATA')
        target_dir = os.path.join(app_data, "SentientOS")
    else:
        # For Linux/Mac/Dev, we used the base dir or local
        target_dir = os.path.join(Config().BASE_DIR, "brain_dump.json")
        # Actually memory.py uses BASE_DIR/brain_dump.json in dev mode, 
        # but let's be safe and check if it created a folder or just file.
        # In memory.py: self.filepath = os.path.join(Config().BASE_DIR, "brain_dump.json")
        if os.path.exists(target_dir):
            try:
                os.remove(target_dir)
                print(f"[RESET] Deleted memory file: {target_dir}")
                return
            except Exception as e:
                print(f"[RESET] Error: {e}")
                return

    if os.path.exists(target_dir):
        try:
            if os.path.isdir(target_dir):
                shutil.rmtree(target_dir)
            else:
                os.remove(target_dir)
            print(f"[RESET] Game data wiped from: {target_dir}")
        except Exception as e:
            print(f"[RESET] Failed to wipe data: {e}")
    else:
        print("[RESET] No game data found to wipe.")

if __name__ == "__main__":
    reset_game_data()
