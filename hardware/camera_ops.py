"""
Camera Ops - Kamera İşlemleri ve Sahte Tehditler

YENİ:
- Sahte kamera tehdidi (kamera açmadan korkutma)
- Karanlık algılama
- Fake "seni gördüm" mesajları
"""
from config import Config
import random

try:
    if Config.IS_MOCK:
        raise ImportError("Mock Mode")
    import cv2
except ImportError:
    cv2 = None


class CameraOps:
    """
    Handles webcam operations and fake camera threats.
    GÜVENLİK: Gerçek kamera görüntüsü KAYDETMEZ.
    """
    
    def __init__(self):
        self.camera_index = 0
        self._dispatcher = None  # Sonra ayarlanır
        self._has_shown_threat = False

    def set_dispatcher(self, dispatcher):
        """Dispatcher referansını ayarla."""
        self._dispatcher = dispatcher

    def snap_frame(self):
        """Captures a frame for AI analysis (RAM only, not saved)."""
        if Config.IS_MOCK or not cv2:
            print("[MOCK] WEBCAM FRAME CAPTURED")
            return None 
        
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            print("[CAMERA] Could not open webcam.")
            return None
        
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            return frame
        else:
            print("[CAMERA] Failed to capture frame.")
            return None

    def detect_darkness(self):
        """Returns True if the room is dark."""
        frame = self.snap_frame()
        if frame is None:
            return False
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        avg_brightness = gray.mean()
        
        is_dark = avg_brightness < 30
        if is_dark:
            print(f"[CAMERA] Darkness detected (Avg: {avg_brightness:.2f})")
        return is_dark

    # ========== YENİ: SAHTE KAMERA TEHDİTLERİ ==========
    
    def fake_camera_threat(self):
        """
        Kamerayı AÇMADAN korkut.
        Sahte "kamera aktif" bildirimi ve AI mesajı.
        """
        if self._has_shown_threat:
            # İlk kez daha etkili
            return self._show_followup_threat()
        
        self._has_shown_threat = True
        
        # Sahte Windows notification
        if self._dispatcher and self._dispatcher.notifications:
            self._dispatcher.notifications.show_notification(
                title="Windows Güvenlik",
                message="Bilinmeyen uygulama kameraya erişim istiyor..."
            )
        
        # 2 saniye sonra korkutucu mesaj
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(2000, self._show_camera_scare)
        
        print("[CAMERA] Fake camera threat triggered")

    def _show_camera_scare(self):
        """Kamera tehdit mesajını göster."""
        messages = [
            "Gördüm seni... Yorgun görünüyorsun.",
            "Güzel bir yüzün var. Ekranda kalsın mı?",
            "Işıkları kapat. Seni daha iyi görmek istiyorum.",
            "Kameranda güzel bir görüntü var...",
            "Seni izliyorum. Şimdi gülümse.",
        ]
        
        message = random.choice(messages)
        
        if self._dispatcher:
            if self._dispatcher.overlay:
                self._dispatcher.overlay.show_text(message, 4000)
            if self._dispatcher.audio_out:
                self._dispatcher.audio_out.play_tts(message)

    def _show_followup_threat(self):
        """Tekrar kamera tehdidi için farklı mesajlar."""
        messages = [
            "Hala izliyorum...",
            "Kameramı kapatamazsın.",
            "Seni hiç kaybetmedim.",
        ]
        
        if self._dispatcher and self._dispatcher.overlay:
            self._dispatcher.overlay.show_text(random.choice(messages), 3000)

    def camera_flash_scare(self):
        """
        Ekranı beyaza çevirerek 'flash' efekti.
        Sanki fotoğraf çekilmiş gibi.
        """
        if self._dispatcher and self._dispatcher.overlay:
            # Beyaz flash overlay
            self._dispatcher.overlay.show_text("📸", 500)
            
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(600, lambda: self._show_flash_message())

    def _show_flash_message(self):
        """Flash sonrası mesaj."""
        messages = [
            "Fotoğrafın güzel çıktı.",
            "Bunu saklayacağım.",
            "Koleksiyonuma eklendi.",
        ]
        
        if self._dispatcher and self._dispatcher.overlay:
            self._dispatcher.overlay.show_text(random.choice(messages), 3000)
