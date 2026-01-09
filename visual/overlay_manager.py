from PyQt6.QtWidgets import QWidget, QLabel, QApplication, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt6.QtGui import QFont, QColor, QPalette, QCursor
import random
from config import Config

class OverlayManager(QWidget):
    """
    Manages transparent overlay windows for scare effects.
    
    FIXED:
    - Multi-screen iyileştirmesi: Mouse cursor'un olduğu ekranda gösterir
    - Daha iyi animasyon kontrolü
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        # Position on the target monitor
        self.update_geometry()

        # Label for text
        self.label = QLabel(self)
        self.label.setFont(QFont("Segoe UI", 48, QFont.Weight.Bold))
        self.label.setStyleSheet("color: #ff0000; text-shadow: 2px 2px 4px #000000;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.hide()
        
        # Animations
        self.opacity_effect = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(self.opacity_effect)
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        
        # Track if currently showing
        self._is_showing = False
        self._original_pos = self.pos()
        
        # Color Flash Layer (Full screen)
        self.flash_layer = QWidget(self)
        self.flash_layer.hide()
        self.flash_layer.setAutoFillBackground(True)

    def update_geometry(self):
        """
        FIXED: Updates geometry based on where the mouse cursor is.
        Falls back to target monitor if cursor detection fails.
        """
        screens = QApplication.screens()
        if not screens:
            return
            
        # Try to find screen where cursor is
        try:
            cursor_pos = QCursor.pos()
            for screen in screens:
                if screen.geometry().contains(cursor_pos):
                    self.setGeometry(screen.geometry())
                    return
        except:
            pass
        
        # Fallback to target monitor
        target_idx = Config().get("TARGET_MONITOR_INDEX", 0)
        if target_idx < len(screens):
            self.setGeometry(screens[target_idx].geometry())
        else:
            self.setGeometry(screens[0].geometry())

    def show_text(self, text: str, duration=3000):
        """Displays text that fades in and out."""
        if Config().IS_MOCK and not QApplication.instance():
            print(f"[MOCK] OVERLAY TEXT: {text}")
            return

        # Don't overlap with previous text
        if self._is_showing:
            self.clear_overlays()

        # Update geometry to current cursor screen
        self.update_geometry()

        self.label.setText(text)
        self.label.adjustSize()
        
        # Position - center with slight random offset
        center_x = (self.width() - self.label.width()) // 2
        center_y = (self.height() - self.label.height()) // 2
        
        offset_x = random.randint(-100, 100)
        offset_y = random.randint(-50, 50)
        
        x = max(0, min(center_x + offset_x, self.width() - self.label.width()))
        y = max(0, min(center_y + offset_y, self.height() - self.label.height()))
        
        self.label.move(x, y)
        
        self.label.show()
        self.show()
        self._is_showing = True

        # Fade In
        self.anim.stop()
        self.anim.setDirection(QPropertyAnimation.Direction.Forward)
        self.anim.setDuration(500)  # Faster fade in
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()

        # Schedule Fade Out
        QTimer.singleShot(duration, self._fade_out)

    def _fade_out(self):
        if not self._is_showing:
            return
            
        self.anim.stop()
        self.anim.setDirection(QPropertyAnimation.Direction.Backward)
        self.anim.setDuration(500)
        self.anim.start()
        
        # Hide after animation
        QTimer.singleShot(600, self._hide_label)

    def _hide_label(self):
        self.label.hide()
        self._is_showing = False

    def clear_overlays(self):
        self.label.hide()
        self.flash_layer.hide()
        self._is_showing = False

    def shake_screen(self, intensity=20, duration=1000):
        """Rapidly moves the overlay window to simulate screen shaking."""
        if not self.isVisible():
            self.show()
            
        original_geometry = self.geometry()
        
        def do_shake(count):
            if count <= 0:
                self.setGeometry(original_geometry)
                return
                
            dx = random.randint(-intensity, intensity)
            dy = random.randint(-intensity, intensity)
            self.move(original_geometry.x() + dx, original_geometry.y() + dy)
            QTimer.singleShot(30, lambda: do_shake(count - 1))
            
        do_shake(duration // 30)

    def flash_color(self, color_hex="#FF0000", opacity=0.3, duration=200):
        """Flashes a full-screen color for extreme impact."""
        self.update_geometry()
        self.flash_layer.setGeometry(self.rect())
        
        palette = self.flash_layer.palette()
        color = QColor(color_hex)
        color.setAlphaF(opacity)
        palette.setColor(QPalette.ColorRole.Window, color)
        self.flash_layer.setPalette(palette)
        
        self.flash_layer.show()
        self.show()
        
        QTimer.singleShot(duration, self.flash_layer.hide)
