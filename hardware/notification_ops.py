"""
Fake System Notification Operations
Shows fake Windows toast notifications.
"""
from config import Config
import random

try:
    if Config.IS_MOCK:
        raise ImportError("Mock Mode")
    from win10toast import ToastNotifier
    HAS_TOAST = True
except ImportError:
    HAS_TOAST = False

class NotificationOps:
    """
    Shows fake system notifications.
    """
    
    def __init__(self):
        if HAS_TOAST and not Config.IS_MOCK:
            self.toaster = ToastNotifier()
        else:
            self.toaster = None
    
    def show_fake_system_alert(self, title: str = None, message: str = None, duration: int = 5):
        """
        Shows a fake Windows notification.
        
        Args:
            title: Notification title
            message: Notification message
            duration: How long to show (seconds)
        """
        if Config.IS_MOCK or not self.toaster:
            print(f"[MOCK] NOTIFICATION: {title} - {message}")
            return
        
        # Default scary notifications if not provided
        if not title or not message:
            notifications = [
                ("Sistem Uyarısı", "Bilinmeyen program tespit edildi: C.O.R.E.exe"),
                ("Windows Defender", "Tehdid algılandı ancak kaldırılamıyor"),
                ("Kritik Hata", "Sistem dosyaları bozulmuş olabilir"),
                ("Disk Kontrolü", "Kritik hatalar bulundu. Onarım başarısız."),
                ("Güvenlik Merkezi", "Yetkisiz erişim girişimi tespit edildi"),
                ("Bellek Hatası", "0x00000000 RAM hatası"),
            ]
            title, message = random.choice(notifications)
        
        try:
            # Threaded so it doesn't block
            self.toaster.show_toast(
                title,
                message,
                duration=duration,
                icon_path=None,  # Uses default Windows icon
                threaded=True
            )
            print(f"[NOTIFICATION] Shown: {title}")
        except Exception as e:
            print(f"[NOTIFICATION] Failed: {e}")
