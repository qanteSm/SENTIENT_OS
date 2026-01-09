"""
Welcome Screen - Atmospheric introduction to SENTIENT_OS.

First screen the user sees after launching. Sets the tone for
the entire experience with slow fade-in and ominous messaging.
"""

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor
import random


class WelcomeScreen(QWidget):
    """
    Atmospheric welcome screen with fade-in effect.
    """
    
    continue_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SENTIENT_OS")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Full screen
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        
        # Dark background
        self.setStyleSheet("background-color: #000000;")
        
        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo/Title
        self.title = QLabel("SENTIENT_OS")
        self.title.setFont(QFont("Courier New", 72, QFont.Weight.Bold))
        self.title.setStyleSheet("""
            color: #00FF00;
            text-shadow: 0 0 20px #00FF00, 0 0 40px #00FF00;
        """)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setVisible(False)
        
        # Subtitle
        self.subtitle = QLabel("System Initialization...")
        self.subtitle.setFont(QFont("Courier New", 24))
        self.subtitle.setStyleSheet("color: #00AA00;")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setVisible(False)
        
        # Warning message
        messages = [
            "Are you ready to let me in?",
            "Welcome. I've been waiting for you.",
            "Initialization complete. Your journey begins.",
            "System compromised. Beginning takeover sequence...",
        ]
        self.message = QLabel(random.choice(messages))
        self.message.setFont(QFont("Courier New", 18))
        self.message.setStyleSheet("color: #FF3333;")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message.setVisible(False)
        
        # Continue button
        self.btn_continue = QPushButton("CONTINUE")
        self.btn_continue.setFont(QFont("Courier New", 16, QFont.Weight.Bold))
        self.btn_continue.setStyleSheet("""
            QPushButton {
                background-color: #001100;
                color: #00FF00;
                border: 2px solid #00FF00;
                padding: 15px 40px;
                text-shadow: 0 0 10px #00FF00;
            }
            QPushButton:hover {
                background-color: #003300;
                border: 2px solid #00FF00;
                box-shadow: 0 0 20px #00FF00;
            }
        """)
        self.btn_continue.clicked.connect(self._on_continue)
        self.btn_continue.setVisible(False)
        self.btn_continue.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Add to layout
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addSpacing(30)
        layout.addWidget(self.subtitle)
        layout.addSpacing(50)
        layout.addWidget(self.message)
        layout.addSpacing(50)
        layout.addWidget(self.btn_continue, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def show_welcome(self):
        """Display welcome screen with animated sequence"""
        self.show()
        
        # Sequence: Title (1s) -> Subtitle (2s) -> Message (3s) -> Button (4s)
        QTimer.singleShot(500, self._show_title)
        QTimer.singleShot(2000, self._show_subtitle)
        QTimer.singleShot(3500, self._show_message)
        QTimer.singleShot(5000, self._show_button)
        
        # Add glitch effect to title
        QTimer.singleShot(1500, self._glitch_title)
    
    def _show_title(self):
        """Fade in title"""
        self.title.setVisible(True)
    
    def _show_subtitle(self):
        """Show subtitle"""
        self.subtitle.setVisible(True)
    
    def _show_message(self):
        """Show warning message"""
        self.message.setVisible(True)
    
    def _show_button(self):
        """Show continue button"""
        self.btn_continue.setVisible(True)
    
    def _glitch_title(self):
        """Apply glitch effect to title"""
        original = "SENTIENT_OS"
        glitched = "S̴E̵N̷T̸I̴E̵N̷T̸_̴O̵S̷"
        
        self.title.setText(glitched)
        QTimer.singleShot(100, lambda: self.title.setText(original))
    
    def _on_continue(self):
        """Handle continue button click"""
        self.continue_clicked.emit()
        self.close()
