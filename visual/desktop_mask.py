"""
Desktop Mask - Ekran Dondurucu

Masaüstünün ekran görüntüsünü alır ve tam ekran overlay olarak gösterir.
FIXED:
- Kill switch (Ctrl+Shift+Q) maske açıkken de çalışır
- 10 kez ESC'ye basılırsa zorla kapat (panik modu)
- Auto timeout (default 15 saniye)
"""
from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from config import Config
import sys

try:
    if Config().IS_MOCK:
        raise ImportError("Mock Mode")
    import keyboard
    HAS_KEYBOARD = True
except ImportError:
    HAS_KEYBOARD = False
    keyboard = None


class DesktopMask(QWidget):
    """
    Takes a screenshot of the desktop and sets it as a full-screen overlay.
    
    FIXED:
    - Kill switch çalışır (Ctrl+Shift+Q)
    - Panik modu: 10 ESC = zorla kapat
    - Auto timeout
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self._timeout_timer = None
        self._escape_count = 0  # Panik modu için ESC sayacı
        self._escape_reset_timer = None

    def capture_and_mask(self, duration_ms: int = 15000):
        """
        Captures and masks the desktop.
        
        Args:
            duration_ms: Maskenin ne kadar kalacağı (default 15 saniye)
        """
        if Config().IS_MOCK and (sys.platform == 'linux' or not QApplication.instance()):
            print(f"[MOCK] DESKTOP CAPTURED AND MASKED (Linux Mock) - {duration_ms}ms")
            return

        screen = QApplication.primaryScreen()
        if not screen:
            print("[MASK] Error: No screen found.")
            return

        # 1. Capture Screenshot
        pixmap = screen.grabWindow(0)
        self.label.setPixmap(pixmap)
        
        # 2. Show Fullscreen
        target_idx = Config().get("TARGET_MONITOR_INDEX", 0)
        screens = QApplication.screens()
        if target_idx < len(screens):
            self.setGeometry(screens[target_idx].geometry())
            self.label.setGeometry(self.rect())
            self.showFullScreen()
            print(f"[MASK] Desktop Mask Active for {duration_ms}ms")
        
        # Reset escape counter
        self._escape_count = 0
        
        # Auto timeout - mask otomatik kapanır
        if self._timeout_timer:
            self._timeout_timer.stop()
        
        self._timeout_timer = QTimer()
        self._timeout_timer.setSingleShot(True)
        self._timeout_timer.timeout.connect(self.remove_mask)
        self._timeout_timer.start(duration_ms)
        
        # FIXED: Kill switch'i kaydet (maske açıkken de çalışsın)
        if HAS_KEYBOARD:
            try:
                keyboard.add_hotkey('ctrl+shift+q', self.remove_mask_emergency, suppress=True)
            except:
                pass

    def keyPressEvent(self, event):
        """
        FIXED: ESC 10 kez basılırsa zorla kapat (panik modu).
        Diğer tuşlar engellenir.
        """
        key = event.key()
        
        # ESC tuşu - panik modu
        if key == Qt.Key.Key_Escape:
            self._escape_count += 1
            print(f"[MASK] ESC pressed ({self._escape_count}/10)")
            
            # 10 ESC = panik modu
            if self._escape_count >= 10:
                print("[MASK] PANIC MODE - Force closing mask!")
                self.remove_mask()
                return
            
            # 3 saniye içinde basılmazsa sayaç sıfırla
            if self._escape_reset_timer:
                self._escape_reset_timer.stop()
            self._escape_reset_timer = QTimer()
            self._escape_reset_timer.setSingleShot(True)
            self._escape_reset_timer.timeout.connect(self._reset_escape_count)
            self._escape_reset_timer.start(3000)
        
        # Ctrl+Shift+Q - kill switch
        modifiers = event.modifiers()
        if (modifiers == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier) 
            and key == Qt.Key.Key_Q):
            print("[MASK] Kill switch detected - removing mask")
            self.remove_mask_emergency()
            return
        
        event.ignore()
    
    def _reset_escape_count(self):
        """Escape sayacını sıfırla."""
        self._escape_count = 0
    
    def remove_mask_emergency(self):
        """Acil durum - kill switch ile kapama."""
        print("[MASK] EMERGENCY REMOVAL via kill switch")
        self.remove_mask()

    def remove_mask(self):
        """Removes the mask overlay."""
        if Config().IS_MOCK and (sys.platform == 'linux' or not QApplication.instance()):
            print("[MOCK] MASK REMOVED")
            return
        
        if self._timeout_timer:
            self._timeout_timer.stop()
            self._timeout_timer = None
        
        if self._escape_reset_timer:
            self._escape_reset_timer.stop()
            self._escape_reset_timer = None
        
        self.close()
        print("[MASK] Desktop Mask Removed")
