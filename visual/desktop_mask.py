# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

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
from core.logger import log_info, log_error, log_warning
import threading

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
        self._escape_count = 0  # Panic mode for ESC counter
        self._escape_reset_timer = None
        self.max_duration = 5000  # 5 seconds max safety
        self.esc_threshold = 3    # 3 ESC = close

    def capture_and_mask(self, duration_ms: int = 15000):
        """
        Captures and masks the desktop.
        
        Args:
            duration_ms: Maskenin ne kadar kalacağı (default 15 saniye)
        """
        if Config().IS_MOCK and (sys.platform == 'linux' or not QApplication.instance()):
            log_info(f"DESKTOP CAPTURED AND MASKED (Mock) - {duration_ms}ms", "MASK")
            return

        screen = QApplication.primaryScreen()
        if not screen:
            log_error("No screen found.", "MASK")
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
            
            # Duration limit for safety
            safe_duration = min(duration_ms, self.max_duration)
            
            self.showFullScreen()
            log_info(f"Desktop Mask Active for {safe_duration}ms", "MASK")
            
            # Emergency safety timeout (Qt level)
            QTimer.singleShot(safe_duration + 1000, self._emergency_close)
        
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
            except (AttributeError, OSError, Exception) as e:
                log_error(f"Kill switch registration failed: {e}", "MASK")
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
            log_info(f"ESC pressed ({self._escape_count}/{self.esc_threshold})", "MASK")
            
            # 3 ESC = panik modu
            if self._escape_count >= self.esc_threshold:
                log_warning("PANIC MODE - Force closing mask!", "MASK")
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
        """Reset escape counter."""
        self._escape_count = 0
        
    def _emergency_close(self):
        """Emergency safety closure if mask hangs."""
        if self.isVisible():
            log_warning("Emergency safety timeout reached, forcing mask close", "MASK")
            self.remove_mask()
    
    def remove_mask_emergency(self):
        """Acil durum - kill switch ile kapama ve tam sistem kapatma."""
        log_warning("EMERGENCY REMOVAL via kill switch", "MASK")
        self.remove_mask()
        
        # Trigger full system shutdown
        from core.event_bus import bus
        bus.publish("system.shutdown", {"reason": "kill_switch_mask"})

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
        log_info("Desktop Mask Removed", "MASK")
