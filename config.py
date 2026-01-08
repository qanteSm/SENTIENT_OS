import sys
import platform
import os

class Config:
    # System Configuration
    APP_NAME = "SENTIENT_OS"
    VERSION = "4.0"
    
    # Environment Detection
    # If we are on Linux/Mac, or if we cannot import win32 libs, we force Mock Mode.
    IS_WINDOWS = sys.platform == 'win32'
    IS_MOCK = not IS_WINDOWS
    
    # Settings from Spec
    STREAMER_MODE = True  # TRUE: Hide names, protect OBS/Discord
    AI_SAFETY_CHECK = True # TRUE: Double-check snippets with AI before showing
    LANGUAGE = "tr"
    SAFE_HARDWARE = False # If True, avoid physically damaging actions (even if capable)
    CHAOS_LEVEL = 0
    
    # Protected Processes (Publisher Protection)
    # The AI cannot kill these or draw over them if possible
    PROTECTED_PROCESSES = [
        "obs64.exe", "obs32.exe", "streamlabs.exe", 
        "discord.exe", "chrome.exe", "firefox.exe"
    ]
    
    # Target Monitor
    # 0 = Primary Monitor. Others are "Safe Zones".
    TARGET_MONITOR_INDEX = 0

    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOCALES_DIR = os.path.join(BASE_DIR, "locales")
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    CACHE_DIR = os.path.join(BASE_DIR, "cache")
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")

    @staticmethod
    def get_platform_info():
        return {
            "os": platform.system(),
            "release": platform.release(),
            "is_mock": Config.IS_MOCK
        }
