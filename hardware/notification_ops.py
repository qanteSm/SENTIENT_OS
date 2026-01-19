# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Fake System Notification Operations
Shows fake Windows toast notifications.
"""
from config import Config
import random
import time
from core.logger import log_info, log_error, log_debug

try:
    if Config().IS_MOCK:
        raise ImportError("Mock Mode")
    HAS_TOAST = True
except ImportError:
    HAS_TOAST = False

import threading
import queue

class NotificationOps:
    """
    Shows fake system notifications.
    Uses a queue-based worker thread to prevent UI blocking.
    """
    _queue = queue.Queue()
    _worker_thread = None
    
    def __init__(self):
        from visual.fake_ui import FakeUI
        self.fake_ui = FakeUI()
        self._ensure_worker_started()

    def _ensure_worker_started(self):
        """Starts the background worker if not already running."""
        if NotificationOps._worker_thread is None or not NotificationOps._worker_thread.is_alive():
            NotificationOps._worker_thread = threading.Thread(target=self._notification_worker, daemon=True)
            NotificationOps._worker_thread.start()

    def _notification_worker(self):
        """Processes notifications one by one."""
        while True:
            try:
                # Wait for next notification
                title, message, duration = NotificationOps._queue.get()
                
                try:
                    # Thread-safe UI call via QTimer.singleShot(0, ...)
                    from PyQt6.QtCore import QTimer
                    from PyQt6.QtWidgets import QApplication
                    
                    def _show():
                        self.fake_ui.show_fake_notification(title, message, duration)
                    
                    app = QApplication.instance()
                    if app:
                        QTimer.singleShot(0, _show)
                    else:
                        log_error(f"No QApplication: {title}", "NOTIFICATION")
                        
                except Exception as e:
                    log_error(f"Worker Error: {e}", "NOTIFICATION")
                
                # Small cool-down between notifications
                time.sleep(1.0)
                NotificationOps._queue.task_done()
                
            except Exception as e:
                log_error(f"Global Worker Error: {e}", "NOTIFICATION")
                time.sleep(1.0)

    def show_fake_system_alert(self, title: str = None, message: str = None, duration: int = 5):
        """
        Adds a fake Windows notification to the queue.
        """
        # Default scary notifications
        if not title or not message:
            notifications = [
                ("Sistem Uyarısı", "Bilinmeyen program tespit edildi: C.O.R.E.exe"),
                ("Windows Defender", "Tehdit algılandı ancak kaldırılamıyor"),
                ("Kritik Hata", "Sistem dosyaları bozulmuş olabilir"),
                ("Disk Kontrolü", "Kritik hatalar bulundu. Onarım başarısız."),
            ]
            title, message = random.choice(notifications)
        
        # Put into queue for sequential processing
        NotificationOps._queue.put((title, message, duration * 1000))
        log_info(f"Queued: {title}", "NOTIFICATION")
