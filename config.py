"""
Configuration Module for SENTIENT_OS
Provides backward-compatible interface using new YAML-based ConfigManager.
"""
import sys
import platform
import os

# Try to load from config.yaml, fallback to hardcoded defaults
try:
    from core.config_manager import get_config_manager
    _config = get_config_manager()
    _use_yaml = True
except Exception as e:
    print(f"[CONFIG] Warning: Could not load config.yaml, using defaults: {e}")
    _config = None
    _use_yaml = False


class Config:
    """
    Configuration class with YAML support.
    Maintains backward compatibility with hardcoded values as fallback.
    """
    
    # Base directory (always needed)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Environment Detection
    IS_WINDOWS = sys.platform == 'win32'
    IS_MOCK = not IS_WINDOWS
    
    # System Configuration
    @property
    def APP_NAME(self):
        return _config.get('system.app_name', 'SENTIENT_OS') if _use_yaml else 'SENTIENT_OS'
    
    @property
    def VERSION(self):
        return _config.get('system.version', '4.0') if _use_yaml else '4.0'
    
    @property
    def LANGUAGE(self):
        return _config.get('system.language', 'tr') if _use_yaml else 'tr'
    
    # Safety Settings
    @property
    def STREAMER_MODE(self):
        return _config.get('safety.streamer_mode', True) if _use_yaml else True
    
    @property
    def AI_SAFETY_CHECK(self):
        return _config.get('safety.ai_safety_check', True) if _use_yaml else True
    
    @property
    def SAFE_HARDWARE(self):
        return _config.get('safety.safe_hardware', False) if _use_yaml else False
    
    @property
    def CHAOS_LEVEL(self):
        return _config.get('safety.chaos_level', 0) if _use_yaml else 0
    
    @property
    def ENABLE_STROBE(self):
        return _config.get('safety.enable_strobe', False) if _use_yaml else False
    
    # Protected Processes
    @property
    def PROTECTED_PROCESSES(self):
        default = ["obs64.exe", "obs32.exe", "streamlabs.exe", "discord.exe", "chrome.exe", "firefox.exe"]
        return _config.get('protected.processes', default) if _use_yaml else default
    
    # Performance
    @property
    def TARGET_MONITOR_INDEX(self):
        return _config.get('performance.target_monitor', 0) if _use_yaml else 0
    
    # Paths
    @property
    def LOCALES_DIR(self):
        subdir = _config.get('paths.locales', 'locales') if _use_yaml else 'locales'
        return os.path.join(self.BASE_DIR, subdir)
    
    @property
    def LOGS_DIR(self):
        subdir = _config.get('paths.logs', 'logs') if _use_yaml else 'logs'
        return os.path.join(self.BASE_DIR, subdir)
    
    @property
    def CACHE_DIR(self):
        subdir = _config.get('paths.cache', 'cache') if _use_yaml else 'cache'
        return os.path.join(self.BASE_DIR, subdir)
    
    @property
    def ASSETS_DIR(self):
        subdir = _config.get('paths.assets', 'assets') if _use_yaml else 'assets'
        return os.path.join(self.BASE_DIR, subdir)
    
    @staticmethod
    def get_platform_info():
        """Get platform information."""
        return {
            "os": platform.system(),
            "release": platform.release(),
            "is_mock": Config.IS_MOCK
        }
    
    @staticmethod
    def get_config_manager():
        """Get the underlying config manager for advanced operations."""
        return _config if _use_yaml else None


# Create singleton instance
Config = Config()
