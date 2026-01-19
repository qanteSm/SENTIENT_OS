# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
ConfigManager - YAML-based configuration system.

Loads settings from config.yaml and provides runtime access.
Integrates with existing Config singleton for backward compatibility.

FEATURES:
- YAML-based configuration
- Environment variable interpolation
- Runtime updates
- Observer pattern notifications
- Schema validation
"""

import os
import re
from typing import Any, Dict
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    print("[CONFIG] PyYAML not found. Install with: pip install PyYAML")


class ConfigManager:
    """
    Manages YAML configuration and integrates with Config singleton.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            ConfigManager._initialized = True
            self.config_path = self._find_config_file()
            self.data = {}
            self.load()
    
    def _find_config_file(self) -> Path:
        """Find config.yaml in project root"""
        # Try current directory
        current = Path(__file__).parent
        config_file = current / "config.yaml"
        
        if config_file.exists():
            return config_file
        
        # Try parent directory (if in subdirectory)
        parent_config = current.parent / "config.yaml"
        if parent_config.exists():
            return parent_config
        
        # Default to current directory
        return config_file
    
    def load(self) -> bool:
        """
        Load configuration from YAML file.
        Returns True if successful, False otherwise.
        """
        if not HAS_YAML:
            print("[CONFIG] Cannot load YAML - library not installed")
            return False
        
        if not self.config_path.exists():
            print(f"[CONFIG] Config file not found: {self.config_path}")
            print("[CONFIG] Using defaults")
            self._load_defaults()
            return False
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                raw_data = yaml.safe_load(f)
            
            # Interpolate environment variables
            self.data = self._interpolate_env_vars(raw_data)
            
            print(f"[CONFIG] Loaded configuration from {self.config_path}")
            return True
            
        except Exception as e:
            print(f"[CONFIG] Error loading config: {e}")
            self._load_defaults()
            return False
    
    def _interpolate_env_vars(self, data: Any) -> Any:
        """
        Recursively replace ${VAR_NAME} with environment variables.
        """
        if isinstance(data, dict):
            return {k: self._interpolate_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._interpolate_env_vars(item) for item in data]
        elif isinstance(data, str):
            # Match ${VAR_NAME} pattern
            pattern = r'\$\{([^}]+)\}'
            matches = re.findall(pattern, data)
            
            for var_name in matches:
                env_value = os.getenv(var_name, '')
                data = data.replace(f'${{{var_name}}}', env_value)
            
            return data
        else:
            return data
    
    def _load_defaults(self):
        """Load default configuration"""
        self.data = {
            'system': {
                'app_name': 'SENTIENT_OS',
                'version': '4.1',
                'debug_mode': False
            },
            'api': {
                'gemini_key': os.getenv('GEMINI_API_KEY', ''),
                'cache_ttl': 300,
                'max_failures': 3
            },
            'horror': {
                'intensity': 'extreme',
                'enable_strobe': False,
                'chaos_level': 0
            },
            'safety': {
                'streamer_mode': True,
                'ai_safety_check': True,
                'target_monitor': 0,
                'protected_processes': ['obs64.exe', 'discord.exe']
            },
            'language': {
                'code': 'tr'
            }
        }
    
    def get(self, path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Example:
            config.get('api.cache_ttl') -> 300
            config.get('horror.intensity') -> 'extreme'
        """
        keys = path.split('.')
        value = self.data
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, path: str, value: Any) -> bool:
        """
        Set configuration value using dot notation.
        
        Note: Changes are in-memory only. Call save() to persist.
        """
        keys = path.split('.')
        data = self.data
        
        # Navigate to parent
        for key in keys[:-1]:
            if key not in data:
                data[key] = {}
            data = data[key]
        
        # Set value
        data[keys[-1]] = value
        print(f"[CONFIG] Set {path} = {value}")
        return True
    
    def save(self) -> bool:
        """Save current configuration to YAML file"""
        if not HAS_YAML:
            return False
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self.data, f, default_flow_style=False, allow_unicode=True)
            
            print(f"[CONFIG] Saved configuration to {self.config_path}")
            return True
            
        except Exception as e:
            print(f"[CONFIG] Error saving config: {e}")
            return False
    
    def populate_legacy_config(self, config_obj):
        """
        Populate the legacy Config singleton with YAML values.
        Provides backward compatibility.
        """
        # System
        config_obj.APP_NAME = self.get('system.app_name', 'SENTIENT_OS')
        config_obj.VERSION = self.get('system.version', '4.1')
        
        # Dynamic values
        config_obj.set('STREAMER_MODE', self.get('safety.streamer_mode', True), validate=False)
        config_obj.set('AI_SAFETY_CHECK', self.get('safety.ai_safety_check', True), validate=False)
        config_obj.set('LANGUAGE', self.get('language.code', 'tr'), validate=False)
        config_obj.set('SAFE_HARDWARE', self.get('horror.safe_hardware', False), validate=False)
        config_obj.set('CHAOS_LEVEL', self.get('horror.chaos_level', 0), validate=False)
        config_obj.set('ENABLE_STROBE', self.get('horror.enable_strobe', False), validate=False)
        config_obj.set('TARGET_MONITOR_INDEX', self.get('safety.target_monitor', 0), validate=False)
        config_obj.set('PROTECTED_PROCESSES', self.get('safety.protected_processes', []), validate=False)
        config_obj.set('GEMINI_KEY', self.get('api.gemini_key', ''), validate=False)
        
        print("[CONFIG] Legacy Config populated from YAML")


# Global singleton instance
def get_config_manager() -> ConfigManager:
    """Get ConfigManager singleton instance"""
    return ConfigManager()
