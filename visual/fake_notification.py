# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

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
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # UI Setup
        self.setFixedSize(360, 110)
        
        self.main_frame = QWidget(self)
        self.main_frame.setFixedSize(360, 110)
        self.main_frame.setObjectName("mainFrame")
        
        # Windows 11 Style: Rounded corners, Mica-like transparency, thin border
        self.main_frame.setStyleSheet("""
            QWidget#mainFrame {
                background-color: rgba(32, 32, 32, 220);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(self.main_frame)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(4)
        
        # App Name Line (New for realism)
        app_line = QHBoxLayout()
        self.app_label = QLabel("Windows Güvenliği")
        self.app_label.setFont(QFont("Segoe UI Variable Small", 8) if "Segoe UI Variable Small" in QFont().families() else QFont("Segoe UI", 8))
        self.app_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); border: none;")
        app_line.addWidget(self.app_label)
        
        self.close_btn = QLabel("✕")
        self.close_btn.setStyleSheet("color: rgba(255, 255, 255, 0.5); border: none; font-size: 10px;")
        app_line.addStretch()
        app_line.addWidget(self.close_btn)
        layout.addLayout(app_line)
        
        # Header (Title)
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Segoe UI Variable Text", 10, QFont.Weight.Bold) if "Segoe UI Variable Text" in QFont().families() else QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #ffffff; border: none;")
        layout.addWidget(self.title_label)
        
        # Body (Message)
        self.message_label = QLabel(message)
        self.message_label.setFont(QFont("Segoe UI Variable Text", 9) if "Segoe UI Variable Text" in QFont().families() else QFont("Segoe UI", 9))
        self.message_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); border: none;")
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
        # FIXED: Ensure it's above the taskbar (usually ~40-60px)
        end_y = geom.bottom() - self.height() - 40
        
        self.move(start_x, start_y)
        self.show()
        self.raise_() # Ensure it's on top
        
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
