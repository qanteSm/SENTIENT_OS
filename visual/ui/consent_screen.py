import sys
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QApplication, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPalette, QBrush
from config import Config

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
        header = QLabel("SİSTEM ERİŞİM SÖZLEŞMESİ / SYSTEM ACCESS CONTRACT")
        header.setFont(QFont("Consolas", 28, QFont.Weight.Bold))
        header.setStyleSheet("color: #ff3333; letter-spacing: 2px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Separator Line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #444; border: 1px solid #444;")
        layout.addWidget(line)
        
        # Terms Text
        terms_text = (
            "Bu yazılım, bir 'Korku/Gerilim Simülasyonu' deneyimi olarak tasarlanmıştır.\n\n"
            "DEVAM ETMEDEN ÖNCE ŞUNLARI KABUL ETMELİSİNİZ:\n"
            "1. YAZILIM, EKRAN PARLAKLIĞINI VE DUVAR KAĞIDINI OYUN İÇİNDE DEĞİŞTİREBİLİR.\n"
            "2. GÖRSEL MANİPÜLASYONLAR (EKRAN ERİMESİ, TİTREME) GERÇEKLEŞTİREBİLİR.\n"
            "3. OYUN SÜRESİNCE MOUSE VE PENCERE AKTİVİTENİZİ İZLEYEBİLİR.\n"
            "4. BU ETKİLER SADECE OYUN AÇIKKEN AKTİFTİR VE ÇIKTIĞINIZDA GERİ YÜKLENİR.\n\n"
            "HİÇBİR DOSYANIZ SİLİNMEYECEK VEYA SİSTEMİNİZE KALICI HASAR VERİLMEYECEKTİR.\n\n"
            "----------------------------------------------------------------------------------\n\n"
            "THIS IS A HORROR SIMULATION EXPERIENCE.\n"
            "THE SYSTEM WILL MANIPULATE BRIGHTNESS, WALLPAPER, AND VISUALS FOR IMMERSION.\n"
            "NONE OF YOUR FILES WILL BE DELETED. NO PERMANENT CHANGES WILL BE MADE."
        )
        
        terms = QLabel(terms_text)
        terms.setFont(QFont("Consolas", 14))
        # Dark green/grey (Old terminal feel)
        terms.setStyleSheet("color: #aaddaa; line-height: 1.5;") 
        terms.setWordWrap(True)
        terms.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(terms)
        
        layout.addStretch()
        
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
            
            print("[CONSENT] Screen shown successfully")
        except Exception as e:
            print(f"[CONSENT] Error showing screen: {e}")
            # Even if animation fails, show the window
            self.showFullScreen()
            self.raise_()

    def _grant_consent(self):
        print("[CONSENT] User accepted the terms.")
        # Save to config/state maybe?
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
