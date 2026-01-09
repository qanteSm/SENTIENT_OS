"""
Configuration Manager for SENTIENT_OS
Handles loading and managing configuration from YAML file with environment variable substitution.
"""
import yaml
import os
import re
from pathlib import Path


class ConfigManager:
    """Manages application configuration from YAML file."""
    
    def __init__(self, config_path="config.yaml"):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to YAML configuration file
        """
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        """
        Load configuration from YAML file with environment variable substitution.
        
        Returns:
            dict: Parsed configuration dictionary
        
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        config_file = Path(self.config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Substitute environment variables
        return self._substitute_env_vars(config)
    
    def _substitute_env_vars(self, obj):
        """
        Recursively substitute environment variables in configuration.
        
        Supports ${VAR_NAME} syntax for environment variable substitution.
        
        Args:
            obj: Configuration object (dict, list, or str)
            
        Returns:
            object: Configuration with substituted values
        """
        if isinstance(obj, dict):
            return {key: self._substitute_env_vars(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._substitute_env_vars(item) for item in obj]
        elif isinstance(obj, str):
            # Match ${VAR_NAME} pattern
            pattern = r'\$\{([^}]+)\}'
            matches = re.findall(pattern, obj)
            result = obj
            for match in matches:
                env_value = os.getenv(match, '')
                result = result.replace(f'${{{match}}}', env_value)
            return result
        else:
            return obj
    
    def get(self, key_path, default=None):
        """
        Get configuration value using dot-notation path.
        
        Args:
            key_path: Dot-separated path to config value (e.g., 'system.language')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
            
        Example:
            >>> config.get('system.language', 'en')
            'tr'
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path, value):
        """
        Set configuration value using dot-notation path.
        
        Args:
            key_path: Dot-separated path to config value
            value: Value to set
            
        Example:
            >>> config.set('safety.chaos_level', 5)
        """
        keys = key_path.split('.')
        target = self.config
        
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        
        target[keys[-1]] = value
    
    def save_config(self, output_path=None):
        """
        Save current configuration to YAML file.
        
        Args:
            output_path: Path to save config (defaults to original path)
        """
        save_path = output_path or self.config_path
        
        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
    
    def reload(self):
        """Reload configuration from file."""
        self.config = self.load_config()


# Global configuration manager instance
_config_manager = None


def get_config_manager():
    """
    Get global configuration manager instance (singleton).
    
    Returns:
        ConfigManager: Global configuration manager
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
