import sys
import random
from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QPixmap, QPainter, QColor
from config import Config

class ScreenMelter(QWidget):
    """
    Captures the current screen and creates a 'melting' effect
    by shifting columns of pixels downwards at different speeds.
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                           Qt.WindowType.WindowStaysOnTopHint | 
                           Qt.WindowType.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Get primary screen
        self.screen = QApplication.primaryScreen()
        self.screenshot = self.screen.grabWindow(0)
        self.setGeometry(self.screen.geometry())
        
        self.width_px = self.width()
        self.height_px = self.height()
        
        # Melt parameters
        self.column_width = 8
        self.num_columns = self.width_px // self.column_width + 1
        self.offsets = [0] * self.num_columns
        self.speeds = [random.uniform(5, 15) for _ in range(self.num_columns)]
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_melt)
        self.timer.start(30)
        
        # Life timer
        self.life_timer = QTimer(self)
        self.life_timer.singleShot(5000, self.close) # 5 seconds of melting
        
        self.showFullScreen()

    def update_melt(self):
        for i in range(self.num_columns):
            self.offsets[i] += self.speeds[i]
            # Accelerate a bit
            self.speeds[i] += 0.5
            
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # Draw the background (slightly dim)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 10))
        
        for i in range(self.num_columns):
            x = i * self.column_width
            offset = int(self.offsets[i])
            
            # Source rect from screenshot
            src_rect = QRect(x, 0, self.column_width, self.height_px)
            # Target rect on current widget
            target_rect = QRect(x, offset, self.column_width, self.height_px)
            
            painter.drawPixmap(target_rect, self.screenshot, src_rect)

    def keyPressEvent(self, event):
        # Allow emergency escape (for dev)
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def closeEvent(self, event):
        """Clean up resources and refresh screen."""
        self.timer.stop()
        self.screenshot = None # Release pixmap
        
        # Trigger screen refresh to clear any lingering pixels
        from visual.gdi_engine import GDIEngine
        GDIEngine.force_refresh_screen()
        
        super().closeEvent(event)

_current_melter = None

def trigger_melt():
    """Helper to start the melt from the main thread with overlap prevention."""
    global _current_melter
    
    # Check if a melter is already active to prevent system lockup
    if _current_melter is not None:
        print("[SCREEN_MELTER] Already active, skipping duplicate trigger.")
        return
        
    if Config().IS_MOCK:
        print("[MOCK] Screen Melting triggered.")
        return
        
    print("[SCREEN_MELTER] Capturing screen for melt effect...")
    _current_melter = ScreenMelter()
    
    # Ensure it cleans up its own pointer when closed or destroyed
    _current_melter.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    _current_melter.destroyed.connect(_on_melter_destroyed)
    _current_melter.show()

def _on_melter_destroyed():
    global _current_melter
    _current_melter = None
    print("[SCREEN_MELTER] Memory cleared.")
