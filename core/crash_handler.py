"""
Crash Handler - Converts real crashes into horror moments.

Installs a global exception hook that catches unhandled exceptions,
saves game state, shows a fake crash screen, and auto-recovers.

FEATURES:
- Global sys.excepthook override
- Emergency state saving
- Horror-themed crash screen
- Automatic recovery from checkpoint
- Detailed error logging
"""

import sys
import traceback
import time
from pathlib import Path
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication


class CrashHandler:
    """
    Global exception handler that turns crashes into horror.
    
    CRITICAL SAFETY:
    - Always saves state before recovery
    - Logs all errors for debugging
    - Provides manual recovery option
    """
    
    _recovery_in_progress = False
    
    @staticmethod
    def install():
        """Install the global exception hook"""
        sys.excepthook = CrashHandler._handle_exception
        print("[CRASH] Global crash handler installed")
    
    @staticmethod
    def _handle_exception(exc_type, exc_value, exc_traceback):
        """
        Global exception handler.
        Called automatically when an unhandled exception occurs.
        """
        # Prevent recursive crash handling
        if CrashHandler._recovery_in_progress:
            print("[CRASH] Recovery already in progress, aborting")
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        CrashHandler._recovery_in_progress = True
        
        # Format error message
        error_msg = ''.join(traceback.format_exception(
            exc_type, exc_value, exc_traceback
        ))
        
        print(f"\n{'='*60}")
        print("[CRASH] UNHANDLED EXCEPTION CAUGHT")
        print(f"{'='*60}")
        print(error_msg)
        print(f"{'='*60}\n")
        
        # Log to file
        CrashHandler._log_error(error_msg)
        
        # Save emergency checkpoint
        try:
            CrashHandler._emergency_save()
        except Exception as save_error:
            print(f"[CRASH] Failed to save state: {save_error}")
        
        # Show fake crash screen (horror moment)
        try:
            CrashHandler._show_fake_crash(error_msg)
        except Exception as ui_error:
            print(f"[CRASH] Failed to show crash UI: {ui_error}")
        
        # Schedule auto-recovery
        if QApplication.instance():
            QTimer.singleShot(3000, CrashHandler._auto_recover)
        else:
            # No Qt app, just exit
            print("[CRASH] No Qt application, exiting...")
            sys.exit(1)
    
    @staticmethod
    def _log_error(error_msg: str):
        """Log error to crash.log"""
        try:
            from core.logger import log_error
            log_error(f"CRASH:\n{error_msg}", "CRASH_HANDLER")
        except:
            # Fallback to simple file logging
            try:
                crash_log = Path("logs/crash.log")
                crash_log.parent.mkdir(exist_ok=True)
                
                with open(crash_log, 'a', encoding='utf-8') as f:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"\n{'='*60}\n")
                    f.write(f"CRASH at {timestamp}\n")
                    f.write(f"{'='*60}\n")
                    f.write(error_msg)
                    f.write(f"\n{'='*60}\n\n")
            except Exception as e:
                print(f"[CRASH] Cannot log error: {e}")
    
    @staticmethod
    def _emergency_save():
        """Save game state to emergency checkpoint"""
        try:
            from core.state_manager import StateManager
            state = StateManager()
            state.emergency_save("CRASH_RECOVERY")
            print("[CRASH] Emergency checkpoint saved")
        except Exception as e:
            print(f"[CRASH] Emergency save failed: {e}")
    
    @staticmethod
    def _show_fake_crash(error_msg: str):
        """
        Display horror-themed crash screen.
        Thread-safe UI invocation.
        """
        def _trigger_ui():
            try:
                from visual.fake_ui import FakeUI
                fake_ui = FakeUI()
                
                crash_messages = [
                    "CORE.SYS FATAL ERROR\n\nMemory corruption at 0x{addr}\nSystem integrity compromised...\n\nRestoring...",
                    "CRITICAL FAILURE\n\nUnauthorized process detected\nC.O.R.E. containment breach\n\nInitiating...",
                    "KERNEL PANIC\n\nStack overflow in consciousness.dll\nEntity state: UNSTABLE",
                ]
                
                import random
                message = random.choice(crash_messages).format(
                    addr=hex(random.randint(0x10000000, 0x7FFFFFFF))
                )
                
                fake_ui.show_system_failure(
                    title="⚠️ SYSTEM FATAL ERROR",
                    message=message,
                    glitch=True
                )
                print("[CRASH] Fake crash screen displayed via Main Thread")
            except Exception as e:
                print(f"[CRASH] UI Thread Error: {e}")

        # Use QTimer.singleShot(0) to ensure the UI call is queued on the main thread
        app = QApplication.instance()
        if app:
            # If we are NOT in the main thread (like win10toast thread), 
            # singleShot safely queues the lambda to the main event loop.
            QTimer.singleShot(0, _trigger_ui)
        else:
            print("[CRASH] No QApplication instance, cannot show UI")
    
    @staticmethod
    def _auto_recover():
        """
        Attempt automatic recovery from checkpoint.
        """
        print("[CRASH] Attempting auto-recovery...")
        
        try:
            from core.kernel import SentientKernel
            from core.state_manager import StateManager
            
            # Try to load emergency checkpoint
            state = StateManager()
            if state.has_emergency_checkpoint():
                print("[CRASH] Emergency checkpoint found, restoring...")
                state.restore_from("CRASH_RECOVERY")
            
            # Restart kernel in recovery mode
            kernel = SentientKernel()
            if hasattr(kernel, 'recovery_boot'):
                kernel.recovery_boot()
            else:
                # Fallback: normal boot
                print("[CRASH] recovery_boot() not available, attempting normal boot")
                # Don't call boot() again - would cause infinite loop
                # Instead, just clean up and exit
                print("[CRASH] Recovery not possible, exiting gracefully")
                if QApplication.instance():
                    QApplication.instance().quit()
        
        except Exception as recovery_error:
            print(f"[CRASH] Recovery failed: {recovery_error}")
            print("[CRASH] Exiting application...")
            
            if QApplication.instance():
                QApplication.instance().quit()
            
            sys.exit(1)
    
    @staticmethod
    def test_crash():
        """
        Test function to intentionally crash the application.
        Used for testing crash recovery.
        """
        print("[CRASH] Triggering test crash in 2 seconds...")
        time.sleep(2)
        raise RuntimeError("TEST CRASH - This is intentional for testing crash recovery")


# Convenience function for manual installation
def install_crash_handler():
    """Install the global crash handler"""
    CrashHandler.install()
