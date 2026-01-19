# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import sys
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QApplication, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPalette, QBrush
from config import Config
from core.localization_manager import tr
from core.logger import log_info, log_error, log_warning

class ConsentScreen(QWidget):
    """
    Mandatory Ethical/Legal Consent Screen (The Contract).
    Ensures the user explicitly approves system-level effects.
    """
    consent_granted = pyqtSignal()
    consent_denied = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                           Qt.WindowType.WindowStaysOnTopHint |
                           Qt.WindowType.Tool)
        
        # Dark, semi-transparent background
        p = self.palette()
        p.setColor(QPalette.ColorRole.Window, QColor(10, 10, 15, 245))
        self.setPalette(p)
        self.setAutoFillBackground(True)
        
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(100, 80, 100, 80)
        layout.setSpacing(30)
        
        # Header (Creepy but professional)
        header = QLabel(tr("onboarding.consent_title"))
        header.setFont(QFont("Consolas", 28, QFont.Weight.Bold))
        header.setStyleSheet("color: #ff3333; letter-spacing: 5px; text-shadow: 0 0 10px #ff3333;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Separator Line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #444; border: 1px solid #444;")
        layout.addWidget(line)
        
        # Terms Text
        terms_text = tr("onboarding.consent_warning")
        
        terms = QLabel(terms_text)
        terms.setFont(QFont("Consolas", 16))
        # Red/Grey for warning
        terms.setStyleSheet("color: #ffaaaa; line-height: 1.8;") 
        terms.setWordWrap(True)
        terms.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(terms)
        
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(50)
        
        self.accept_btn = QPushButton(tr("onboarding.consent_grant"))
        self.accept_btn.setFont(QFont("Consolas", 18, QFont.Weight.Bold))
        self.accept_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.accept_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ff3333;
                border: 2px solid #ff3333;
                padding: 15px 40px;
                border-radius: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 51, 51, 0.1);
                color: #ffffff;
                text-shadow: 0 0 10px #ff3333;
            }
        """)
        self.accept_btn.clicked.connect(self._grant_consent)
        
        self.deny_btn = QPushButton("REDDEDİYORUM / EXIT")
        self.deny_btn.setFont(QFont("Consolas", 14))
        self.deny_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.deny_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666;
                border: 1px solid #666;
                padding: 10px 20px;
            }
            QPushButton:hover {
                color: #aaaaaa;
                border: 1px solid #aaaaaa;
            }
        """)
        self.deny_btn.clicked.connect(self._deny_consent)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.deny_btn)
        btn_layout.addWidget(self.accept_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def show_consent(self):
        """Show consent screen with proper error handling"""
        try:
            screen = QApplication.primaryScreen()
            if screen:
                screen_geo = screen.geometry()
                self.setGeometry(screen_geo)
            else:
                # Fallback if screen is not found (unlikely but safe)
                self.resize(1024, 768)
            
            # Fade in animation
            self.setWindowOpacity(0)
            self.showFullScreen()
            self.raise_()
            self.activateWindow()  # Ensure window is active
            
            self.anim = QPropertyAnimation(self, b"windowOpacity")
            self.anim.setDuration(1500)
            self.anim.setStartValue(0)
            self.anim.setEndValue(1)
            self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            self.anim.start()
            
            log_info("Consent screen shown successfully", "UI")
        except Exception as e:
            log_error(f"Error showing screen: {e}", "UI")
            # Even if animation fails, show the window
            self.showFullScreen()
            self.raise_()

    def _grant_consent(self):
        log_info("User accepted the terms.", "UI")
        # Save to config/state maybe?
        self.consent_granted.emit()
        self.close()

    def _deny_consent(self):
        log_info("User denied the terms.", "UI")
        self.consent_denied.emit()
        self.close()
        sys.exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConsentScreen()
    window.show_consent()
    sys.exit(app.exec())
