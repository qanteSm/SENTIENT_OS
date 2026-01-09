import winreg
import ctypes
import os

class VoiceFixer:
    """
    Automatically detects OneCore voices (like Tolga) and enables them for SAPI5/pyttsx3
    by copying registry keys. Requires Admin privileges to write to HKLM.
    """
    
    ONECORE_PATH = r"SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
    SAPI5_PATH = r"SOFTWARE\Microsoft\Speech\Voices\Tokens"

    @staticmethod
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    @classmethod
    def fix_tr_voice(cls):
        """Finds Tolga in OneCore and copies to SAPI5 if missing."""
        if not cls.is_admin():
            print("[VOICE_FIXER] Not running as admin. Skipping automated registry fix.")
            return False

        try:
            # 1. Find Tolga in OneCore
            tolga_key_name = "MSTTS_V110_trTR_Tolga"
            source_path = f"{cls.ONECORE_PATH}\\{tolga_key_name}"
            target_path = f"{cls.SAPI5_PATH}\\{tolga_key_name}"

            # Check if he's already in SAPI5
            try:
                winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, target_path)
                print("[VOICE_FIXER] Tolga is already enabled in SAPI5.")
                return True
            except OSError:
                pass # Not found, proceed with fix

            # Check if he exists in OneCore
            try:
                winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, source_path)
            except OSError:
                print("[VOICE_FIXER] Tolga not found in OneCore. Voice pack might not be installed.")
                return False

            print(f"[VOICE_FIXER] Found Tolga in OneCore. Enabling for SAPI5...")
            success = cls._copy_reg_key(winreg.HKEY_LOCAL_MACHINE, source_path, winreg.HKEY_LOCAL_MACHINE, target_path)
            
            if success:
                print("[VOICE_FIXER] SUCCESS: Tolga is now visible to the system protocols.")
                return True
            else:
                print("[VOICE_FIXER] FAILED to copy registry keys.")
                return False

        except Exception as e:
            print(f"[VOICE_FIXER] Unexpected Error: {e}")
            return False

    @classmethod
    def _copy_reg_key(cls, root_src, path_src, root_dst, path_dst):
        try:
            with winreg.OpenKey(root_src, path_src) as s_key:
                d_key = winreg.CreateKey(root_dst, path_dst)
                
                # Copy values
                i = 0
                while True:
                    try:
                        n, v, t = winreg.EnumValue(s_key, i)
                        winreg.SetValueEx(d_key, n, 0, t, v)
                        i += 1
                    except OSError:
                        break
                
                # Copy subkeys recursively
                i = 0
                while True:
                    try:
                        sub = winreg.EnumKey(s_key, i)
                        cls._copy_reg_key(s_key, sub, d_key, sub)
                        i += 1
                    except OSError:
                        break
                
                winreg.CloseKey(d_key)
                return True
        except Exception as e:
            print(f"[VOICE_FIXER] Subkey Copy Error: {e}")
            return False

if __name__ == "__main__":
    # Test run
    VoiceFixer.fix_tr_voice()
