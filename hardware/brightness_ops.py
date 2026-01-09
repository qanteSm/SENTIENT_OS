"""
Screen Brightness Manipulation
Flickers screen brightness for horror effect.

FIXED:
- Added persistent brightness restore file
- Recovery check on startup
- Better error handling
"""
from config import Config
import time
import random
import os
import json

try:
    if Config().IS_MOCK:
        raise ImportError("Mock Mode")
    import screen_brightness_control as sbc
    HAS_BRIGHTNESS = True
except ImportError:
    HAS_BRIGHTNESS = False

class BrightnessOps:
    """
    Controls screen brightness for psychological effects.
    """
    
    _original_brightness = None
    _original_brightness = None
    
    @staticmethod
    def save_brightness():
        """Saves current brightness for restoration - both in memory and on disk."""
        if Config().IS_MOCK or not HAS_BRIGHTNESS:
            BrightnessOps._original_brightness = 50
            return
        
        try:
            current = sbc.get_brightness()
            if isinstance(current, list):
                BrightnessOps._original_brightness = current[0]
            else:
                BrightnessOps._original_brightness = current
            print(f"[BRIGHTNESS] Saved: {BrightnessOps._original_brightness}%")
            
            # FIXED: Also save to file for crash recovery
            BrightnessOps._save_to_file(BrightnessOps._original_brightness)
            
        except Exception as e:
            print(f"[BRIGHTNESS] Save failed: {e}")
            BrightnessOps._original_brightness = 50

    @staticmethod
    def _save_to_file(brightness):
        """Saves brightness to persistent state via StateManager."""
        try:
            from core.state_manager import StateManager
            StateManager().update_state("brightness", brightness)
        except Exception as e:
            print(f"[BRIGHTNESS] State save failed: {e}")

    @staticmethod
    def _load_from_file():
        """Loads brightness from StateManager."""
        try:
            from core.state_manager import StateManager
            return StateManager().get_state("brightness")
        except Exception as e:
            print(f"[BRIGHTNESS] State load failed: {e}")
        return None

    @staticmethod
    def _cleanup_restore_file():
        """Removes the brightness entry from StateManager."""
        try:
            from core.state_manager import StateManager
            StateManager().remove_state("brightness")
        except:
            pass

    @staticmethod
    def check_and_restore_on_startup():
        """
        FIXED: Call this on game startup to restore brightness if crashed previously.
        Returns True if restoration was performed.
        """
        saved_brightness = BrightnessOps._load_from_file()
        if saved_brightness is not None:
            print(f"[BRIGHTNESS] Found crash recovery data: {saved_brightness}%")
            if not Config().IS_MOCK and HAS_BRIGHTNESS:
                try:
                    sbc.set_brightness(saved_brightness)
                    print(f"[BRIGHTNESS] Crash recovery: Restored to {saved_brightness}%")
                except Exception as e:
                    print(f"[BRIGHTNESS] Crash recovery failed: {e}")
            BrightnessOps._cleanup_restore_file()
            return True
        return False
    
    @staticmethod
    def restore_brightness():
        """Restores original brightness."""
        if BrightnessOps._original_brightness is None:
            # Try to load from file
            BrightnessOps._original_brightness = BrightnessOps._load_from_file()
            if BrightnessOps._original_brightness is None:
                return
        
        if Config().IS_MOCK or not HAS_BRIGHTNESS:
            print(f"[MOCK] BRIGHTNESS RESTORED TO {BrightnessOps._original_brightness}%")
            BrightnessOps._cleanup_restore_file()
            return
        
        try:
            sbc.set_brightness(BrightnessOps._original_brightness)
            print(f"[BRIGHTNESS] Restored to {BrightnessOps._original_brightness}%")
            BrightnessOps._cleanup_restore_file()
        except Exception as e:
            print(f"[BRIGHTNESS] Restore failed: {e}")
    
    @staticmethod
    def flicker(times: int = 3):
        """
        Rapidly flickers brightness between dark and bright.
        """
        if Config().IS_MOCK or not HAS_BRIGHTNESS:
            print(f"[MOCK] BRIGHTNESS FLICKERED {times} times")
            return
        
        try:
            # Save if not already saved
            if BrightnessOps._original_brightness is None:
                BrightnessOps.save_brightness()
            
            # Check photosensitivity safety
            is_strobe = Config.ENABLE_STROBE
            
            for _ in range(times):
                if is_strobe:
                    # TRUE STROBE: Hard 10% to 100%
                    sbc.set_brightness(10)
                    time.sleep(0.15)
                    sbc.set_brightness(100)
                    time.sleep(0.15)
                else:
                    # SAFE MODE: Soft pulsing instead (40% to 80%)
                    sbc.set_brightness(40)
                    time.sleep(0.5)
                    sbc.set_brightness(80)
                    time.sleep(0.5)
            
            # Return to original
            BrightnessOps.restore_brightness()
            
        except Exception as e:
            print(f"[BRIGHTNESS] Flicker failed: {e}")
    
    @staticmethod
    def gradual_dim(target: int = 10, steps: int = 10, auto_restore_ms: int = 10000):
        """
        Gradually dims the screen to create unease.
        FIXED: Runs in thread + auto-restore.
        """
        if Config().IS_MOCK or not HAS_BRIGHTNESS:
            print(f"[MOCK] BRIGHTNESS DIMMED TO {target}%")
            return
        
        try:
            if BrightnessOps._original_brightness is None:
                BrightnessOps.save_brightness()
            
            current = BrightnessOps._original_brightness
            step_size = (current - target) / steps
            
            import threading
            def dim_thread():
                for i in range(steps):
                    new_brightness = int(current - (step_size * (i + 1)))
                    sbc.set_brightness(new_brightness)
                    time.sleep(0.5)
            
            threading.Thread(target=dim_thread, daemon=True).start()
            
            # Auto-restore
            if auto_restore_ms > 0:
                from PyQt6.QtCore import QTimer
                QTimer.singleShot(auto_restore_ms, BrightnessOps.restore_brightness)
            
        except Exception as e:
            print(f"[BRIGHTNESS] Gradual dim failed: {e}")
