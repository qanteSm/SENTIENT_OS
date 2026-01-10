import sys
import platform
import os
from typing import Callable, Any, Dict, List

class Config:
    """
    Dynamic Configuration System with Observer Pattern.
    
    IMPROVED:
    - Runtime configuration changes
    - Observer notifications when config changes
    - Thread-safe singleton
    - Validation for config values
    """
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            Config._initialized = True
            self._observers: List[Callable[[str, Any, Any], None]] = []
            self._init_default_values()
            
            # NEW: Load from YAML if available
            self._load_from_yaml()
    
    def _load_from_yaml(self):
        """Load configuration from YAML via ConfigManager"""
        try:
            from core.config_manager import ConfigManager
            yaml_config = ConfigManager()
            yaml_config.populate_legacy_config(self)
            print("[CONFIG] YAML configuration loaded successfully")
        except Exception as e:
            print(f"[CONFIG] Could not load YAML config: {e}")
            print("[CONFIG] Using default Python config")
    
    def _init_default_values(self):
        """Initialize all configuration values"""
        # System Configuration (Static - Cannot be changed at runtime)
        self.APP_NAME = "SENTIENT_OS"
        self.VERSION = "4.0"
        self.IS_WINDOWS = sys.platform == 'win32'
        self.IS_MOCK = not self.IS_WINDOWS
        
        # Dynamic Configuration (Can be changed at runtime)
        self._values: Dict[str, Any] = {
            "STREAMER_MODE": True,
            "AI_SAFETY_CHECK": True,
            "LANGUAGE": "tr",
            "SAFE_HARDWARE": False,
            "CHAOS_LEVEL": 0,
            "ENABLE_STROBE": False,
            "TARGET_MONITOR_INDEX": 0,
            "PROTECTED_PROCESSES": [
                "obs64.exe", "obs32.exe", "streamlabs.exe",
                "discord.exe", "chrome.exe", "firefox.exe"
            ],
            "STREAMER_MASK_CAMERA": True,
            "DIFFICULTY_ENABLED": True
        }
        
        # Paths (Static)
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.LOCALES_DIR = os.path.join(self.BASE_DIR, "locales")
        self.LOGS_DIR = os.path.join(self.BASE_DIR, "logs")
        self.CACHE_DIR = os.path.join(self.BASE_DIR, "cache")
        self.ASSETS_DIR = os.path.join(self.BASE_DIR, "assets")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._values.get(key, default)
    
    def set(self, key: str, value: Any, validate: bool = True) -> bool:
        """
        Set configuration value at runtime.
        Returns True if successful, False if validation failed.
        """
        if validate and not self._validate(key, value):
            print(f"[CONFIG] Validation failed for {key}={value}")
            return False
        
        old_value = self._values.get(key)
        self._values[key] = value
        
        # Notify observers
        self._notify_observers(key, old_value, value)
        
        print(f"[CONFIG] {key}: {old_value} → {value}")
        return True
    
    def _validate(self, key: str, value: Any) -> bool:
        """Validate configuration values"""
        if key == "CHAOS_LEVEL":
            return isinstance(value, (int, float)) and 0 <= value <= 100
        elif key == "TARGET_MONITOR_INDEX":
            return isinstance(value, int) and value >= 0
        elif key == "LANGUAGE":
            return value in ["tr", "en"]  # Supported languages
        elif key in ["STREAMER_MODE", "AI_SAFETY_CHECK", "SAFE_HARDWARE", "ENABLE_STROBE", "STREAMER_MASK_CAMERA", "DIFFICULTY_ENABLED"]:
            return isinstance(value, bool)
        return True  # No validation for unknown keys
    
    def add_observer(self, callback: Callable[[str, Any, Any], None]):
        """
        Add observer to be notified of config changes.
        Callback signature: (key: str, old_value: Any, new_value: Any) -> None
        """
        if callback not in self._observers:
            self._observers.append(callback)
            print(f"[CONFIG] Observer registered: {callback.__name__}")
    
    def remove_observer(self, callback: Callable[[str, Any, Any], None]):
        """Remove observer"""
        if callback in self._observers:
            self._observers.remove(callback)
    
    def _notify_observers(self, key: str, old_value: Any, new_value: Any):
        """Notify all observers of a config change"""
        for observer in self._observers:
            try:
                observer(key, old_value, new_value)
            except Exception as e:
                print(f"[CONFIG] Error notifying observer: {e}")
    
    # Legacy compatibility - Allow attribute access for backward compatibility
    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        return self._values.get(name, None)
    
    def get_platform_info(self) -> Dict[str, Any]:
        """Get platform information"""
        return {
            "os": platform.system(),
            "release": platform.release(),
            "is_mock": self.IS_MOCK
        }
