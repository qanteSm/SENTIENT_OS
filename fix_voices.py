import winreg
import sys

def copy_key(source_root, source_path, target_root, target_path):
    try:
        with winreg.OpenKey(source_root, source_path) as source_key:
            # Create target key
            target_key = winreg.CreateKey(target_root, target_path)
            
            # Copy values
            i = 0
            while True:
                try:
                    name, value, type = winreg.EnumValue(source_key, i)
                    winreg.SetValueEx(target_key, name, 0, type, value)
                    i += 1
                except OSError:
                    break
            
            # Copy subkeys recursively
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(source_key, i)
                    copy_key(source_key, subkey_name, target_key, subkey_name)
                    i += 1
                except OSError:
                    break
            
            winreg.CloseKey(target_key)
            return True
    except Exception as e:
        print(f"Error copying {source_path}: {e}")
        return False

# Source: HKLM OneCore
# Target: HKCU Speech (Local User) - pyttsx3 looks here too
source_root = winreg.HKEY_LOCAL_MACHINE
source_base = r"SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens\MSTTS_V110_trTR_Tolga"
target_root = winreg.HKEY_CURRENT_USER
target_base = r"SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_trTR_Tolga"

print(f"Attempting to enable Tolga voice for pyttsx3...")
if copy_key(source_root, source_base, target_root, target_base):
    print("SUCCESS: Tolga voice data copied to local user registry.")
else:
    print("FAILURE: Could not copy Tolga voice data.")
