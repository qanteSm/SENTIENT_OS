"""
Safety Net - Güvenlik Ağı ve Kaçış Girişimi Tespiti

Kill Switch (CTRL+SHIFT+Q) ile acil çıkış.
YENİ: Alt+F4, Task Manager gibi kaçış girişimlerini tespit eder ve memory'ye kaydeder.
"""
import sys
import os
from PyQt6.QtWidgets import QApplication
from hardware.keyboard_ops import KeyboardOps
from hardware.mouse_ops import MouseOps
from visual.fake_ui import FakeUI
from config import Config

# Try to import keyboard for hotkey listening
try:
    if Config.IS_MOCK:
        raise ImportError("Mock Mode")
    import keyboard
except ImportError:
    keyboard = None


class SafetyNet:
    """
    Monitors for the Kill Switch (CTRL+SHIFT+Q).
    Also detects escape attempts (Alt+F4, Task Manager) and logs them.
    """
    
    # Memory referansı - dışarıdan ayarlanır
    memory = None
    
    def __init__(self):
        self.is_active = False
        self.escape_attempts = 0

    def start_monitoring(self):
        """Starts the listener for the kill switch and escape attempts."""
        if Config.IS_MOCK or not keyboard:
            print("[SAFETY_NET] Kill Switch Monitor Active (CTRL+SHIFT+Q) [MOCK]")
            return

        print("[SAFETY_NET] Kill Switch Monitor Active (CTRL+SHIFT+Q)")
        try:
            # Kill switch
            keyboard.add_hotkey('ctrl+shift+q', self.emergency_cleanup)
            
            # YENİ: Kaçış girişimi tespiti
            keyboard.add_hotkey('alt+f4', self._on_escape_attempt_altf4)
            keyboard.add_hotkey('ctrl+shift+esc', self._on_escape_attempt_taskman)
            keyboard.add_hotkey('ctrl+alt+delete', self._on_escape_attempt_taskman)
            
            self.is_active = True
        except Exception as e:
            print(f"[SAFETY_NET] Failed to register hotkey: {e}")
    
    def _on_escape_attempt_altf4(self):
        """Alt+F4 tespit edildi - kaydet ve tepki ver."""
        self.escape_attempts += 1
        print(f"[SAFETY_NET] ESCAPE ATTEMPT DETECTED: Alt+F4 (#{self.escape_attempts})")
        
        if SafetyNet.memory:
            SafetyNet.memory.record_behavior("escape_attempt", "Alt+F4")
            SafetyNet.memory.add_memorable_moment("Alt+F4 ile kaçmaya çalıştı")
        
        # İlk birkaç denemede blokla (gerçek kapatmayı engelleme)
        # Not: Bu sadece tepki için, gerçek Alt+F4'ü engelleyemeyiz
    
    def _on_escape_attempt_taskman(self):
        """Task Manager açma girişimi tespit edildi."""
        self.escape_attempts += 1
        print(f"[SAFETY_NET] ESCAPE ATTEMPT DETECTED: Task Manager (#{self.escape_attempts})")
        
        if SafetyNet.memory:
            SafetyNet.memory.record_behavior("escape_attempt", "Task Manager")
            SafetyNet.memory.add_memorable_moment("Task Manager açmaya çalıştı")
    
    @classmethod
    def set_memory(cls, memory):
        """Memory referansını ayarla."""
        cls.memory = memory

    def emergency_cleanup(self):
        """Restores system to normal state (unlock mouse, clear screen)."""
        print("\n!!! EMERGENCY KILL SWITCH TRIGGERED !!!")
        
        # Kaçışı kaydet
        if SafetyNet.memory:
            SafetyNet.memory.log_event("KILL_SWITCH_USED", {})
            SafetyNet.memory.shutdown()  # Son kayıt
        
        # 1. Unlock Hardware
        KeyboardOps.unlock_input()
        MouseOps.unfreeze_cursor()
        
        # 2. Close Visuals (If running)
        app = QApplication.instance()
        if app:
            app.quit()
        
        # 3. Kill Process
        print("System Exiting...")
        os._exit(0)
