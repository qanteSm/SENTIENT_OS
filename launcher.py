import sys
import os
import subprocess
import ctypes
import time
import random   
from config import Config
from hardware.voice_fixer import VoiceFixer

def validate_environment():
    """Validate required environment variables before launch."""
    if not os.getenv("GEMINI_API_KEY"):
        print("\n" + "!" * 60)
        print(" ERROR: GEMINI_API_KEY environment variable not set!")
        print(" Please set it before running:")
        print('   set GEMINI_API_KEY=your_key_here  (Windows Command Prompt)')
        print('   $env:GEMINI_API_KEY="your_key_here" (PowerShell)')
        print("!" * 60 + "\n")
        sys.exit(1)

def is_admin():
    """Real Windows Admin check."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except (AttributeError, OSError) as e:
        print(f"[LAUNCHER] Admin check failed: {e}")
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
    validate_environment()
    
    # Check for DEV_MODE in config
    config = Config()
    dev_mode = config.get("DEV_MODE", False)
    
    if dev_mode:
        print("\n" + "=" * 60)
        print(" ⚡ DEVELOPER MODE ACTIVE - Skipping admin/intro checks")
        print(" Edit config.yaml to disable")
        print("=" * 60 + "\n")
    
    # Skip admin check in dev mode
    if not dev_mode and not is_admin() and not config.IS_MOCK:
        print("!" * 60)
        print("ERROR: Administrative privileges required.")
        print("Attempting to escalate...")
        print("!" * 60)
        run_as_admin()
        sys.exit()

    # Skip intro in dev mode
    if not dev_mode:
        hacker_terminal_splash()
    else:
        print("[DEV] Skipping intro animation...")
    
    # Skip dependency/defender checks in dev mode
    if not dev_mode:
        check_and_install_deps()
        setup_defender_exclusion()
        # Automatically fix Turkish voice if admin
        VoiceFixer.fix_tr_voice()
    else:
        print("[DEV] Skipping dependency checks...")
    
    print("\n[READY] System initialized. Entering C.O.R.E. state...")
    if not dev_mode:
        time.sleep(1)

    # Check for reset flag
    if "--reset" in sys.argv:
        print("[LAUNCHER] Resetting game state...")
        try:
            from tools.reset_memory import reset_game_data
            reset_game_data()
        except ImportError:
            print("[ERROR] Reset tool not found.")

    # Call main.py
    subprocess.call([sys.executable, os.path.join(config.BASE_DIR, "main.py")])

if __name__ == "__main__":
    launch_game()
