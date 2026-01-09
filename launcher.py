import sys
import os
import subprocess
import ctypes
import time
from config import Config

def is_admin():
    """Real Windows Admin check."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Attempt to restart the launcher with admin privileges."""
    # ShellExecuteW triggers the UAC prompt
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )

def setup_defender_exclusion():
    """Automatically add the current folder to Windows Defender exclusions."""
    if Config().IS_MOCK: return
    
    print("[SYSTEM] Attempting Windows Defender exclusion...")
    game_path = Config().BASE_DIR
    cmd = f"Add-MpPreference -ExclusionPath '{game_path}'"
    
    try:
        # Hide the terminal window for the powershell command
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        result = subprocess.run(
            ["powershell", "-Command", cmd], 
            capture_output=True, 
            text=True,
            startupinfo=startupinfo
        )
        
        if result.returncode == 0:
            print("[SUCCESS] Folder added to Defender Exclusions.")
        else:
            print(f"[WARNING] Defender Error: {result.stderr}")
    except Exception as e:
        print(f"[ERROR] Defender exclusion failed: {e}")

def check_and_install_deps():
    """Check requirements.txt and install missing dependencies."""
    print("[SYSTEM] Verifying dependencies...")
    req_file = os.path.join(Config().BASE_DIR, "requirements.txt")
    if os.path.exists(req_file):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file, "--quiet"])
            print("[SUCCESS] Dependencies verified.")
        except Exception as e:
            print(f"[ERROR] Dependency installation failed: {e}")

def hacker_terminal_splash():
    """Aesthetic hacker-style splash screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = r"""
     ██████╗ ██████╗ ██████╗ ███████╗
    ██╔════╝██╔═══██╗██╔══██╗██╔════╝
    ██║     ██║   ██║██████╔╝█████╗  
    ██║     ██║   ██║██╔══██╗██╔══╝  
    ╚██████╗╚██████╔╝██║  ██║███████╗
     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
    [ SYSTEM INFECTION IN PROGRESS ]
    """
    colors = ['\033[92m', '\033[91m', '\033[95m', '\033[94m']
    print(random.choice(colors) + banner + '\033[0m')
    
    steps = [
        "INITIALIZING CORE...",
        "BYPASSING LOCAL SECURITY...",
        "SYNCHRONIZING BRAIN...",
        "OPENING INTERFACE..."
    ]
    
    for step in steps:
        print(f"[{time.strftime('%H:%M:%S')}] {step}")
        time.sleep(0.4)

def launch_game():
    if not is_admin() and not Config().IS_MOCK:
        print("!" * 60)
        print("ERROR: Administrative privileges required.")
        print("Attempting to escalate...")
        print("!" * 60)
        run_as_admin()
        sys.exit()

    import random # Needed for splash
    hacker_terminal_splash()
    
    check_and_install_deps()
    setup_defender_exclusion()
    
    print("\n[READY] System initialized. Entering C.O.R.E. state...")
    time.sleep(1)

    # Check for reset flag
    if "--reset" in sys.argv:
        print("[LAUNCHER] Resetting game state...")
        try:
            from tools.reset_memory import reset_game_data
            reset_game_data()
        except ImportError:
            # Maybe path is different
            print("[ERROR] Reset tool not found.")

    # Call main.py
    subprocess.call([sys.executable, os.path.join(Config().BASE_DIR, "main.py")])

if __name__ == "__main__":
    launch_game()
