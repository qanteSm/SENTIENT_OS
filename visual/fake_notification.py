from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint, QRect, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon, QPainter, QBrush
import random

class FakeNotification(QWidget):
    """
    Native PyQt-based Windows 10/11 style notification.
    Safe replacement for win10toast.
    """
    def __init__(self, title, message, duration=5000):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.NoFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # UI Setup
        self.setFixedSize(360, 100)
        
        self.main_frame = QWidget(self)
        self.main_frame.setFixedSize(360, 100)
        self.main_frame.setObjectName("mainFrame")
        self.main_frame.setStyleSheet("""
            QWidget#mainFrame {
                background-color: rgba(30, 30, 30, 240);
                border: 1px solid #444;
                border-radius: 4px;
            }
        """)
        
        layout = QVBoxLayout(self.main_frame)
        
        # Header (Title)
        header_layout = QHBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #fff; border: none;")
        header_layout.addWidget(self.title_label)
        
        self.close_btn = QLabel("✕")
        self.close_btn.setStyleSheet("color: #888; border: none;")
        header_layout.addStretch()
        header_layout.addWidget(self.close_btn)
        
        layout.addLayout(header_layout)
        
        # Body (Message)
        self.message_label = QLabel(message)
        self.message_label.setFont(QFont("Segoe UI", 9))
        self.message_label.setStyleSheet("color: #ccc; border: none;")
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)
        
        # Animation
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(400)
        
        # Timer for auto-close
        self.duration = duration
        
    def show_toast(self):
        """Animates into view from bottom-right."""
        screens = QApplication.screens()
        screen = QApplication.primaryScreen()
        cursor_pos = QApplication.activeWindow()
        if cursor_pos:
            screen = cursor_pos.screen()
        
        geom = screen.availableGeometry()
        
        # Start position (Off screen)
        start_x = geom.right() - self.width() - 10
        start_y = geom.bottom()
        
        # End position (Inside screen)
        end_y = geom.bottom() - self.height() - 10
        
        self.move(start_x, start_y)
        self.show()
        
        self.anim.setStartValue(QPoint(start_x, start_y))
        self.anim.setEndValue(QPoint(start_x, end_y))
        self.anim.start()
        
        QTimer.singleShot(self.duration, self.close_toast)
        
    def close_toast(self):
        """Animates out and closes."""
        geom = QApplication.primaryScreen().availableGeometry()
        self.anim.setDirection(QPropertyAnimation.Direction.Backward)
        self.anim.start()
        QTimer.singleShot(400, self.close)
