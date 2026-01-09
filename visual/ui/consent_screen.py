"""
Enhanced Consent Screen for SENTIENT_OS
Provides detailed safety information, emergency controls, and customization options.
"""
import sys
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QApplication, QFrame, QCheckBox,
                             QSlider, QComboBox, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPalette, QBrush
from config import Config
from core.config_manager import get_config_manager

class ConsentScreen(QWidget):
    """
    Enhanced Mandatory Ethical/Legal Consent Screen.
    
    Features:
        - Detailed safety warnings with photosensitivity information
        - Emergency kill switch demonstration (Ctrl+Shift+Q)
        - Intensity level customization
        - Language selection
        - Strobe effect toggle
        
    Ensures the user explicitly approves system-level effects before starting.
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
        
        # User preferences
        self.intensity_level = "medium"
        self.enable_strobe = False
        self.selected_language = "tr"
        
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(80, 60, 80, 60)
        layout.setSpacing(20)
        
        # Header (Creepy but professional)
        header = QLabel("SİSTEM ERİŞİM SÖZLEŞMESİ / SYSTEM ACCESS CONTRACT")
        header.setFont(QFont("Consolas", 24, QFont.Weight.Bold))
        header.setStyleSheet("color: #ff3333; letter-spacing: 2px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Separator Line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #444; border: 1px solid #444;")
        layout.addWidget(line)
        
        # Safety Warning Box
        warning_box = self._create_warning_box()
        layout.addWidget(warning_box)
        
        # Emergency Controls Info
        emergency_box = self._create_emergency_box()
        layout.addWidget(emergency_box)
        
        # Customization Options
        options_box = self._create_options_box()
        layout.addWidget(options_box)
        
        layout.addStretch()
        
        # Agreement Checkbox
        self.agree_checkbox = QCheckBox("Yukarıdaki tüm uyarıları okudum ve anladım / I have read and understand all warnings above")
        self.agree_checkbox.setFont(QFont("Consolas", 12))
        self.agree_checkbox.setStyleSheet("color: #aaddaa;")
        layout.addWidget(self.agree_checkbox)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(50)
        
        self.accept_btn = QPushButton("KABUL EDİYORUM / I ACCEPT")
        self.accept_btn.setFont(QFont("Consolas", 18, QFont.Weight.Bold))
        self.accept_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.accept_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                color: #ff3333;
                border: 2px solid #ff3333;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #330000;
                color: #ffffff;
            }
            QPushButton:disabled {
                background-color: #1a1a1a;
                color: #663333;
                border: 2px solid #663333;
            }
        """)
        self.accept_btn.clicked.connect(self._grant_consent)
        self.accept_btn.setEnabled(False)
        
        # Enable accept button only when checkbox is checked
        self.agree_checkbox.stateChanged.connect(
            lambda state: self.accept_btn.setEnabled(state == Qt.CheckState.Checked.value)
        )
        
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

    def _create_warning_box(self):
        """Create photosensitivity and safety warning box."""
        box = QGroupBox()
        box.setStyleSheet("""
            QGroupBox {
                background-color: #2a0000;
                border: 2px solid #ff3333;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout()
        
        warning_title = QLabel("⚠️ ÖNEMLİ UYARI / IMPORTANT WARNING")
        warning_title.setFont(QFont("Consolas", 14, QFont.Weight.Bold))
        warning_title.setStyleSheet("color: #ff3333;")
        layout.addWidget(warning_title)
        
        warning_text = QLabel(
            "🔴 FOTOSENSİTİF EPİLEPSİ UYARISI:\n"
            "Bu oyun YANIP SÖNEN IŞIKLAR, hızlı renk değişimleri ve yoğun görsel bozulmalar içerir.\n"
            "Epilepsi veya nöbet geçmişiniz varsa OYNAMAYIN!\n\n"
            "🔴 PHOTOSENSITIVE EPILEPSY WARNING:\n"
            "This experience contains FLASHING LIGHTS, rapid color changes, and intense visual distortions.\n"
            "DO NOT PLAY if you have a history of epilepsy or seizures!\n\n"
            "• Sistem parlaklığını, duvar kağıdını geçici olarak değiştirir\n"
            "• Mouse ve pencere aktivitelerini izler\n"
            "• Hiçbir dosya silinmez, kalıcı değişiklik yapılmaz\n"
            "• Tüm değişiklikler kapanışta geri yüklenir"
        )
        warning_text.setFont(QFont("Consolas", 11))
        warning_text.setStyleSheet("color: #ffcccc;")
        warning_text.setWordWrap(True)
        layout.addWidget(warning_text)
        
        box.setLayout(layout)
        return box
    
    def _create_emergency_box(self):
        """Create emergency controls information box."""
        box = QGroupBox()
        box.setStyleSheet("""
            QGroupBox {
                background-color: #1a1a1a;
                border: 1px solid #666;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        
        emergency_title = QLabel("🆘 ACİL DURUM KONTROLLERI / EMERGENCY CONTROLS")
        emergency_title.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        emergency_title.setStyleSheet("color: #ffaa00;")
        layout.addWidget(emergency_title)
        
        emergency_text = QLabel(
            "Acil Kapatma Tuşu / Emergency Kill Switch:\n"
            "   ➤ CTRL + SHIFT + Q  (Herhangi bir anda basın / Press at any time)\n\n"
            "Otomatik Güvenlik / Automatic Safety:\n"
            "   ➤ CPU > 85% veya RAM > 80% ise sistem otomatik kapanır\n"
            "   ➤ Auto-shutdown if CPU > 85% or RAM > 80%"
        )
        emergency_text.setFont(QFont("Consolas", 10))
        emergency_text.setStyleSheet("color: #aaddaa;")
        layout.addWidget(emergency_text)
        
        box.setLayout(layout)
        return box
    
    def _create_options_box(self):
        """Create customization options box."""
        box = QGroupBox()
        box.setStyleSheet("""
            QGroupBox {
                background-color: #1a1a1a;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        
        options_title = QLabel("⚙️ ÖZELLEŞTİRME / CUSTOMIZATION")
        options_title.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        options_title.setStyleSheet("color: #66ccff;")
        layout.addWidget(options_title)
        
        # Intensity selection
        intensity_label = QLabel("Yoğunluk Seviyesi / Intensity Level:")
        intensity_label.setFont(QFont("Consolas", 10))
        intensity_label.setStyleSheet("color: #aaddaa;")
        layout.addWidget(intensity_label)
        
        self.intensity_combo = QComboBox()
        self.intensity_combo.addItems(["Hafif / Mild", "Orta / Medium", "Aşırı / Extreme"])
        self.intensity_combo.setCurrentIndex(1)  # Default: Medium
        self.intensity_combo.setFont(QFont("Consolas", 10))
        self.intensity_combo.setStyleSheet("""
            QComboBox {
                background-color: #2a2a2a;
                color: #aaddaa;
                border: 1px solid #666;
                padding: 5px;
            }
        """)
        self.intensity_combo.currentIndexChanged.connect(self._on_intensity_changed)
        layout.addWidget(self.intensity_combo)
        
        # Strobe toggle
        self.strobe_checkbox = QCheckBox("Hızlı yanıp sönme efektlerini etkinleştir / Enable strobe effects")
        self.strobe_checkbox.setFont(QFont("Consolas", 10))
        self.strobe_checkbox.setStyleSheet("color: #ffccaa;")
        self.strobe_checkbox.setChecked(False)
        self.strobe_checkbox.stateChanged.connect(self._on_strobe_changed)
        layout.addWidget(self.strobe_checkbox)
        
        # Language selection
        lang_label = QLabel("Dil / Language:")
        lang_label.setFont(QFont("Consolas", 10))
        lang_label.setStyleSheet("color: #aaddaa;")
        layout.addWidget(lang_label)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Türkçe", "English"])
        self.lang_combo.setCurrentIndex(0)  # Default: Turkish
        self.lang_combo.setFont(QFont("Consolas", 10))
        self.lang_combo.setStyleSheet("""
            QComboBox {
                background-color: #2a2a2a;
                color: #aaddaa;
                border: 1px solid #666;
                padding: 5px;
            }
        """)
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)
        layout.addWidget(self.lang_combo)
        
        box.setLayout(layout)
        return box
    
    def _on_intensity_changed(self, index):
        """Handle intensity level change."""
        levels = ["mild", "medium", "extreme"]
        self.intensity_level = levels[index]
        print(f"[CONSENT] Intensity level changed to: {self.intensity_level}")
    
    def _on_strobe_changed(self, state):
        """Handle strobe effect toggle."""
        self.enable_strobe = (state == Qt.CheckState.Checked.value)
        print(f"[CONSENT] Strobe effects: {self.enable_strobe}")
    
    def _on_language_changed(self, index):
        """Handle language selection."""
        langs = ["tr", "en"]
        self.selected_language = langs[index]
        print(f"[CONSENT] Language changed to: {self.selected_language}")

    def show_consent(self):
        screen_geo = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geo)
        
        # Fade in animation
        self.setWindowOpacity(0)
        self.showFullScreen()
        self.raise_()
        
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(1500)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.start()

    def _grant_consent(self):
        """Handle user acceptance and save preferences."""
        print("[CONSENT] User accepted the terms.")
        
        # Save user preferences to config
        try:
            config = get_config_manager()
            
            # Map intensity to chaos level
            intensity_map = {"mild": 3, "medium": 5, "extreme": 8}
            chaos_level = intensity_map.get(self.intensity_level, 5)
            
            config.set('safety.chaos_level', chaos_level)
            config.set('safety.enable_strobe', self.enable_strobe)
            config.set('system.language', self.selected_language)
            config.save_config()
            
            print(f"[CONSENT] Preferences saved: chaos={chaos_level}, strobe={self.enable_strobe}, lang={self.selected_language}")
        except Exception as e:
            print(f"[CONSENT] Warning: Could not save preferences: {e}")
        
        self.consent_granted.emit()
        self.close()

    def _deny_consent(self):
        print("[CONSENT] User denied the terms.")
        self.consent_denied.emit()
        self.close()
        sys.exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConsentScreen()
    window.show_consent()
    sys.exit(app.exec())
