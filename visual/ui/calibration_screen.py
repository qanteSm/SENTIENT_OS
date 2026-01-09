"""
Calibration Screen - Horror Intensity Selection.

Gives user illusion of control by letting them choose intensity.
Saves selection to config.yaml.
"""

from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QButtonGroup, QRadioButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class CalibrationScreen(QWidget):
    """
    Let user choose horror intensity level.
    Provides sense of control (psychological trick).
    """
    
    calibration_complete = pyqtSignal(str)  # Emits selected intensity
    
    INTENSITIES = {
        "mild": {
            "title": "🌙 Mild",
            "desc": "Subtle psychological elements\nMinimal jump scares\nRecommended for first-time players"
        },
        "medium": {
            "title": "👁️ Medium", 
            "desc": "Balanced horror experience\nImmersive atmosphere\nModerate system manipulation"
        },
        "extreme": {
            "title": "💀 Extreme",
            "desc": "Full psychological manipulation\nMaximum immersion\nNot for the faint of heart"
        }
    }
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calibration")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        
        # Full screen
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        
        # Dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #0a0a0a;
                color: #00FF00;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(100, 80, 100, 80)
        
        # Title
        title = QLabel("⚙️ SYSTEM CALIBRATION")
        title.setFont(QFont("Courier New", 48, QFont.Weight.Bold))
        title.setStyleSheet("color: #00FF00; text-shadow: 0 0 20px #00FF00;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Instructions
        instructions = QLabel("Select your preferred horror intensity level:")
        instructions.setFont(QFont("Courier New", 20))
        instructions.setStyleSheet("color: #00AA00;")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        main_layout.addWidget(title)
        main_layout.addSpacing(40)
        main_layout.addWidget(instructions)
        main_layout.addSpacing(60)
        
        # Intensity options
        options_layout = QHBoxLayout()
        options_layout.setSpacing(40)
        
        self.button_group = QButtonGroup()
        self.selected_intensity = "extreme"  # Default
        
        for intensity_key, intensity_data in self.INTENSITIES.items():
            option_widget = self._create_intensity_option(
                intensity_key,
                intensity_data["title"],
                intensity_data["desc"]
            )
            options_layout.addWidget(option_widget)
        
        main_layout.addLayout(options_layout)
        main_layout.addSpacing(80)
        
        # Warning
        warning = QLabel("⚠️ Your selection will affect system behavior")
        warning.setFont(QFont("Courier New", 14))
        warning.setStyleSheet("color: #FF3333;")
        warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Confirm button
        btn_confirm = QPushButton("CONFIRM SELECTION")
        btn_confirm.setFont(QFont("Courier New", 18, QFont.Weight.Bold))
        btn_confirm.setStyleSheet("""
            QPushButton {
                background-color: #001100;
                color: #00FF00;
                border: 3px solid #00FF00;
                padding: 20px 60px;
                text-shadow: 0 0 10px #00FF00;
            }
            QPushButton:hover {
                background-color: #003300;
                box-shadow: 0 0 30px #00FF00;
            }
        """)
        btn_confirm.clicked.connect(self._on_confirm)
        btn_confirm.setCursor(Qt.CursorShape.PointingHandCursor)
        
        main_layout.addWidget(warning)
        main_layout.addSpacing(20)
        main_layout.addWidget(btn_confirm, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(main_layout)
    
    def _create_intensity_option(self, key: str, title: str, description: str) -> QWidget:
        """Create intensity option widget"""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #0f0f0f;
                border: 2px solid #003300;
                border-radius: 10px;
                padding: 20px;
            }
            QWidget:hover {
                border: 2px solid #00FF00;
                background-color: #1a1a1a;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Radio button
        radio = QRadioButton(title)
        radio.setFont(QFont("Courier New", 24, QFont.Weight.Bold))
        radio.setStyleSheet("""
            QRadioButton {
                color: #00FF00;
                spacing: 10px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
        """)
        radio.setProperty("intensity", key)
        radio.toggled.connect(lambda checked, k=key: self._on_selection(k) if checked else None)
        
        # Set default selection
        if key == "extreme":
            radio.setChecked(True)
        
        self.button_group.addButton(radio)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Courier New", 12))
        desc_label.setStyleSheet("color: #888888;")
        desc_label.setWordWrap(True)
        
        layout.addWidget(radio)
        layout.addSpacing(10)
        layout.addWidget(desc_label)
        
        widget.setLayout(layout)
        widget.setMinimumWidth(300)
        widget.setMaximumWidth(400)
        
        return widget
    
    def _on_selection(self, intensity: str):
        """Handle intensity selection"""
        self.selected_intensity = intensity
        print(f"[CALIBRATION] Selected intensity: {intensity}")
    
    def _on_confirm(self):
        """Save selection and proceed"""
        # Save to config
        try:
            from core.config_manager import ConfigManager
            config = ConfigManager()
            config.set('horror.intensity', self.selected_intensity)
            config.save()
            print(f"[CALIBRATION] Saved intensity: {self.selected_intensity}")
        except Exception as e:
            print(f"[CALIBRATION] Error saving config: {e}")
        
        # Emit signal
        self.calibration_complete.emit(self.selected_intensity)
        self.close()
