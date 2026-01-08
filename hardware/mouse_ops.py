from config import Config
import time
import random
import threading

try:
    if Config.IS_MOCK:
        raise ImportError("Mock Mode")
    import mouse
except ImportError:
    mouse = None

class MouseOps:
    """
    Handles cursor locking, shaking, and gravity effects.
    """
    _shaking = False
    _frozen = False

    @staticmethod
    def freeze_cursor():
        """Locks mouse to center of screen."""
        if Config.IS_MOCK or not mouse:
            print("[MOCK] CURSOR FROZEN")
            return

        MouseOps._frozen = True
        
        def _freeze_loop():
            while MouseOps._frozen:
                mouse.move(960, 540, absolute=True, duration=0)
                time.sleep(0.01)
        
        t = threading.Thread(target=_freeze_loop, daemon=True)
        t.start()

    @staticmethod
    def unfreeze_cursor():
        MouseOps._frozen = False
        print("[HARDWARE] Cursor Unfrozen")

    @staticmethod
    def _is_safe_to_interact():
        """
        Checks if the currently active window is 'safe' for interference.
        Blocks interaction on Explorer, Task Manager, and system dialogs/installers.
        Language-independent (uses Class and Process names).
        """
        from hardware.window_ops import WindowOps
        info = WindowOps.get_active_window_info()
        
        # 1. Block by Process Name (Critical)
        blocked_processes = [
            "explorer.exe", "taskmgr.exe", "mmc.exe", 
            "msiexec.exe", "regedit.exe", "cmd.exe", "powershell.exe"
        ]
        if info['process'] in blocked_processes:
            # print(f"[INPUT_GUARD] Suppressed interaction on {info['process']}")
            return False
            
        # 2. Block by Window Class (Universal)
        # CabinetWClass = Explorer
        # #32770 = Common dialogs (Properties, Format, Delete confirmations)
        # TaskManagerWindow = Task Manager
        blocked_classes = ["CabinetWClass", "#32770", "TaskManagerWindow", "ConsoleWindowClass"]
        if info['class'] in blocked_classes:
            # print(f"[INPUT_GUARD] Suppressed interaction on Class: {info['class']}")
            return False
            
        return True

    @staticmethod
    def shake_cursor(duration=1.0):
        """Jitters the mouse for a duration. SUPPRESSED on system windows."""
        if Config.IS_MOCK or not mouse:
            print(f"[MOCK] CURSOR SHAKE ({duration}s)")
            return

        if not MouseOps._is_safe_to_interact():
            print("[INPUT_GUARD] Aborting shake: Current window is system-critical.")
            return

        MouseOps._shaking = True
        
        def _shake_loop():
            start_time = time.time()
            while time.time() - start_time < duration:
                if not MouseOps._is_safe_to_interact():
                    break # Stop if user switches to a system window
                
                x_offset = random.randint(-8, 8)
                y_offset = random.randint(-8, 8)
                try:
                    mouse.move(x_offset, y_offset, absolute=False, duration=0)
                except:
                    pass
                time.sleep(0.04)
            MouseOps._shaking = False
            
        t = threading.Thread(target=_shake_loop, daemon=True)
        t.start()

    @staticmethod
    def click_randomly():
        """Performs a random click, ONLY if it's safe."""
        if Config.IS_MOCK or not mouse:
            return
            
        if MouseOps._is_safe_to_interact():
            # print("[HARDWARE] Clicking...")
            mouse.click('left')
        else:
            print("[INPUT_GUARD] Click suppressed on system window.")
 bitumen
 bitumen
 bitumen
