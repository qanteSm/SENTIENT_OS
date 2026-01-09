from config import Config
try:
    if Config().IS_MOCK:
        raise ImportError("Mock Mode")
    import ctypes
except ImportError:
    ctypes = None

class PeripheralOps:
    """
    Handles CD-ROM eject, Printer, Battery spoofing.
    """
    @staticmethod
    def eject_cd_tray():
        if Config().IS_MOCK or not ctypes:
            print("[MOCK] CD TRAY EJECTED")
            return
        
        try:
            # winmm.dll mciSendStringW
            ctypes.windll.winmm.mciSendStringW("set cdaudio door open", None, 0, None)
            print("[HARDWARE] CD Tray Open Signal Sent")
        except Exception as e:
            print(f"[HARDWARE] CD Eject Failed: {e}")

    @staticmethod
    def close_cd_tray():
        if Config().IS_MOCK or not ctypes:
            print("[MOCK] CD TRAY CLOSED")
            return

        try:
            ctypes.windll.winmm.mciSendStringW("set cdaudio door closed", None, 0, None)
        except Exception:
            pass

    @staticmethod
    def battery_spoof():
        """
        Actually spoofing ACPI is kernel level.
        We will rely on visual/FakeUI to show a 'Low Battery' warning overlay.
        This function just logs it.
        """
        print("[HARDWARE] Battery Spoof Triggered (Requires Visual Overlay)")
