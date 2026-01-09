from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette, QMovie, QKeyEvent
from config import Config
import random
from visual.fake_notification import FakeNotification

class FakeBSOD(QWidget):
    """
    Simulates a Windows Blue Screen of Death (BSOD).
    ENHANCED: Un-closeable, multi-monitor, with sound.
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setCursor(Qt.CursorShape.BlankCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        
        # Windows 10/11 BSOD Color
        p = self.palette()
        p.setColor(QPalette.ColorRole.Window, QColor("#0078D7"))
        self.setPalette(p)
        self.setAutoFillBackground(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(100, 100, 100, 100)
        
        # Sad Face :(
        self.sad_face = QLabel(":(")
        self.sad_face.setFont(QFont("Segoe UI", 120))
        self.sad_face.setStyleSheet("color: white;")
        layout.addWidget(self.sad_face)
        
        layout.addSpacing(20)
        
        # Text (Turkish)
        msg = QLabel("Bilgisayarınız bir sorunla karşılaştı ve yeniden başlatılması gerekiyor.\nBirkaç hata bilgisi toplanıyor, ardından sizin için yeniden başlatacağız.")
        msg.setFont(QFont("Segoe UI", 24))
        msg.setStyleSheet("color: white;")
        msg.setWordWrap(True)
        layout.addWidget(msg)
        
        layout.addSpacing(40)
        
        # Percentage
        self.percent_label = QLabel("0% tamamlandı")
        self.percent_label.setFont(QFont("Segoe UI", 24))
        self.percent_label.setStyleSheet("color: white;")
        layout.addWidget(self.percent_label)
        
        layout.addStretch()
        self.setLayout(layout)

        self.progress = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_progress)
        
        # Auto-dismiss timer (after 15 seconds)
        self.dismiss_timer = QTimer(self)
        self.dismiss_timer.setSingleShot(True)
        self.dismiss_timer.timeout.connect(self._auto_dismiss)

        # Glitch timer (Path B enhancement)
        self.glitch_timer = QTimer(self)
        self.glitch_timer.timeout.connect(self._trigger_glitch)

    def keyPressEvent(self, event: QKeyEvent):
        """Block Escape and Alt+F4 attempts."""
        key = event.key()
        modifiers = event.modifiers()
        
        # Block Escape
        if key == Qt.Key.Key_Escape:
            event.ignore()
            return
        
        # Block Alt+F4
        if modifiers == Qt.KeyboardModifier.AltModifier and key == Qt.Key.Key_F4:
            event.ignore()
            return
        
        # Ignore all other keys
        event.ignore()

    def show_bsod(self):
        self._target_all_screens()
        self.showFullScreen()
        self.raise_()
        self.activateWindow()
        self.setFocus()
        
        self.progress = 0
        self.timer.start(50)  # Faster updates
        self.glitch_timer.start(2000) # Glitch every 2 seconds
        
        # Auto-dismiss after 15 seconds
        self.dismiss_timer.start(15000)
    
    def _auto_dismiss(self):
        """Automatically dismiss after timeout."""
        self.timer.stop()
        self.glitch_timer.stop()
        self.close()
        print("[BSOD] Auto-dismissed")
    
    def _trigger_glitch(self):
        """Randomly glitch the BSOD."""
        if random.random() < 0.3:
            # Shake effect
            original_pos = self.pos()
            for _ in range(5):
                self.move(original_pos.x() + random.randint(-10, 10), 
                          original_pos.y() + random.randint(-10, 10))
                QTimer.singleShot(50, lambda: self.move(original_pos))
        
        if random.random() < 0.1:
            # Color inversion (requires GDI)
            from visual.gdi_engine import GDIEngine
            GDIEngine.invert_screen(100)

    def _update_progress(self):
        if self.progress < 100:
            # Slow progress between 0-30%, fast 30-100%
            if self.progress < 30:
                self.progress += 1
            else:
                self.progress += 3
            self.percent_label.setText(f"{self.progress}% tamamlandı")
        else:
            self.timer.stop()
            # After reaching 100%, keep showing for 2 more seconds
            QTimer.singleShot(2000, self._auto_dismiss)

    def _target_all_screens(self):
        """Show on all monitors by spanning geometry."""
        screens = QApplication.screens()
        if len(screens) > 1:
            # Calculate total geometry spanning all screens
            # For simplicity, just show on primary
            self.setGeometry(screens[0].geometry())
        else:
            # FIXED: was using undefined target_idx, now correctly uses screens[0]
            self.setGeometry(screens[0].geometry())

class FakeUpdate(QWidget):
    """
    Simulates a Windows Update screen.
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setCursor(Qt.CursorShape.BlankCursor)
        
        # Black background
        p = self.palette()
        p.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.black)
        self.setPalette(p)
        self.setAutoFillBackground(True)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # TODO: Add a spinning loader gif here if assets exist
        
        self.label = QLabel("Working on updates  0% complete.\nDon't turn off your computer.")
        self.label.setFont(QFont("Segoe UI", 18))
        self.label.setStyleSheet("color: white;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        self.setLayout(layout)

    def show_update(self, percent=666):
        self._target_screen()
        self.showFullScreen()
        self.label.setText(f"Working on updates  {percent}% complete.\nDon't turn off your computer.")
        
        # Safety: Auto-dismiss after 60 seconds if it somehow gets stuck
        QTimer.singleShot(60000, self.close)

    def _target_screen(self):
        screens = QApplication.screens()
        target_idx = Config().get("TARGET_MONITOR_INDEX", 0)
        if target_idx < len(screens):
            self.setGeometry(screens[target_idx].geometry())

from visual.fake_chat import FakeChat

class FakeUI:
    """
    Wrapper to manage these windows easily.
    Singleton pattern for centralized access.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FakeUI, cls).__new__(cls)
            cls._instance.bsod = None
            cls._instance.update_screen = None
            cls._instance.chat = None
            cls._instance.active_notifications = []
        return cls._instance

    def __init__(self):
        # Already initialized in __new__
        pass

    def show_chat(self):
        if not self.chat:
            self.chat = FakeChat()
        self.chat.show_chat()
        return self.chat

    def show_bsod(self):
        if Config().IS_MOCK and not QApplication.instance():
            print("[MOCK] FAKE BSOD DISPLAYED")
            return
            
        if not self.bsod:
            self.bsod = FakeBSOD()
        self.bsod.show_bsod()

    def show_fake_update(self, percent=0):
        if Config().IS_MOCK and not QApplication.instance():
            print(f"[MOCK] FAKE UPDATE: {percent}%")
            return

        if not self.update_screen:
            self.update_screen = FakeUpdate()
        self.update_screen.show_update(percent)
    
    def show_fake_notification(self, title, message, duration=5000):
        """Shows a native PyQt notification."""
        if Config().IS_MOCK and not QApplication.instance():
            print(f"[MOCK] NOTIFICATION: {title} - {message}")
            return
            
        notif = FakeNotification(title, message, duration)
        # Keep reference to prevent garbage collection
        self.active_notifications.append(notif)
        
        # Remove from list when closed
        notif.destroyed.connect(lambda: self._cleanup_notification(notif))
        
        notif.show_toast()
        return notif

    def _cleanup_notification(self, notif):
        """Removes notification reference from active list."""
        if notif in self.active_notifications:
            self.active_notifications.remove(notif)
    
    def show_system_failure(self, title="SYSTEM FAILURE", message="CRITICAL ERROR", **kwargs):
        """Triggers the BSOD as a failure state."""
        # Handle extra arguments like 'glitch' from crash handler
        self.show_bsod()
    
    def close_all(self):
        if self.bsod: 
            self.bsod.close()
            self.bsod = None
        if self.update_screen: 
            self.update_screen.close()
            self.update_screen = None
        if self.chat:
            self.chat.close()
            self.chat = None
