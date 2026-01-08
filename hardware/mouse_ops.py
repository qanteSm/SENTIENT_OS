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
    def shake_cursor(duration=1.0):
        """Jitters the mouse for a duration."""
        if Config.IS_MOCK or not mouse:
            print(f"[MOCK] CURSOR SHAKE ({duration}s)")
            return

        MouseOps._shaking = True
        
        def _shake_loop():
            start_time = time.time()
            while time.time() - start_time < duration:
                x_offset = random.randint(-5, 5)
                y_offset = random.randint(-5, 5)
                try:
                    mouse.move(x_offset, y_offset, absolute=False, duration=0)
                except:
                    pass
                time.sleep(0.02)
            MouseOps._shaking = False
            
        t = threading.Thread(target=_shake_loop, daemon=True)
        t.start()
