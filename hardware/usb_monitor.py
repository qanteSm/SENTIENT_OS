# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

from PyQt6.QtCore import QObject, pyqtSignal
from config import Config
import sys

# Windows imports
try:
    if Config().IS_MOCK:
        raise ImportError("Mock Mode")
    import win32gui
    import win32con
    import win32api
except ImportError:
    win32gui = None
    win32con = None
    win32api = None

class USBMonitor(QObject):
    """
    Detects USB Device Insertion/Removal using Windows Messaging.
    """
    usb_inserted = pyqtSignal()
    usb_removed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.hwnd = None
        self.listening = False

    def start_monitoring(self):
        if Config().IS_MOCK or not win32gui:
            print("[USB] Monitoring Started (Mock Mode).")
            self.listening = True
            
            # FIXED: Auto-simulate USB insertion after 30 seconds in mock mode
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(30000, self._mock_auto_insert)
            return

        # Create a hidden window to receive messages
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self._wnd_proc
        wc.lpszClassName = "SentientUSBWatcher"
        wc.hInstance = win32api.GetModuleHandle(None)
        
        try:
            class_atom = win32gui.RegisterClass(wc)
            self.hwnd = win32gui.CreateWindow(
                class_atom, "USBWatcher", 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None
            )
            print("[USB] Monitoring Started (Windows Native).")
            self.listening = True
        except Exception as e:
            print(f"[USB] Failed to start monitor: {e}")

    def stop_monitoring(self):
        self.listening = False
        if self.hwnd:
            win32gui.DestroyWindow(self.hwnd)
            self.hwnd = None

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        """Windows Message Handler"""
        if msg == win32con.WM_DEVICECHANGE:
            # 0x8000 = DBT_DEVICEARRIVAL
            if wparam == 0x8000:
                print("[USB] Device Inserted!")
                self.usb_inserted.emit()
            # 0x8004 = DBT_DEVICEREMOVECOMPLETE
            elif wparam == 0x8004:
                print("[USB] Device Removed!")
                self.usb_removed.emit()
            return True
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def _mock_auto_insert(self):
        """FIXED: Auto-insert for mock mode testing."""
        if self.listening:
            print("[USB] Mock Mode: Auto-simulating USB insertion...")
            self.usb_inserted.emit()

    def simulate_insertion(self):
        """Call this in Mock Mode or Test to trigger the signal."""
        print("[USB] Simulating Insertion...")
        self.usb_inserted.emit()
