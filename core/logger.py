"""
SENTIENT_OS Logging Framework
Professional logging system replacing print() statements with structured logs.
"""
import logging
import os
import sys
from datetime import datetime
from config import Config

class SentientLogger:
    """
    Centralized logging for SENTIENT_OS.
    
    Provides file and console output with different log levels.
    Uses Python's built-in logging framework for robust log management.
    
    Features:
        - Daily rotating log files
        - Console and file output
        - Module-based tagging
        - Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Example:
        >>> from core.logger import log_info, log_error
        >>> log_info("System initialized", module="KERNEL")
        >>> log_error("Failed to connect to API", module="GEMINI")
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if SentientLogger._initialized:
            return
        
        SentientLogger._initialized = True
        
        # Create logs directory
        self.logs_dir = Config.LOGS_DIR
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger("SENTIENT_OS")
        self.logger.setLevel(logging.DEBUG if Config.IS_MOCK else logging.INFO)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = logging.Formatter(
            '[%(levelname)s] %(message)s'
        )
        
        # File handler - daily log file
        log_filename = f"sentient_{datetime.now().strftime('%Y%m%d')}.log"
        log_path = os.path.join(self.logs_dir, log_filename)
        
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info(f"SENTIENT_OS v{Config.VERSION} - Logging initialized")
    
    def debug(self, message: str, module: str = "CORE"):
        """Log debug message (detailed diagnostic information)."""
        self.logger.debug(f"[{module}] {message}")
    
    def info(self, message: str, module: str = "CORE"):
        """Log info message (general informational messages)."""
        self.logger.info(f"[{module}] {message}")
    
    def warning(self, message: str, module: str = "CORE"):
        """Log warning message (warning about potential issues)."""
        self.logger.warning(f"[{module}] {message}")
    
    def error(self, message: str, module: str = "CORE"):
        """Log error message (error events that might still allow continued operation)."""
        self.logger.error(f"[{module}] {message}")
    
    def critical(self, message: str, module: str = "CORE"):
        """Log critical message (serious errors requiring immediate attention)."""
        self.logger.critical(f"[{module}] {message}")


# Global logger instance
_logger = None

def get_logger() -> SentientLogger:
    """
    Get the global logger instance (singleton).
    
    Returns:
        SentientLogger: Global logger instance
    """
    global _logger
    if _logger is None:
        _logger = SentientLogger()
    return _logger

# Convenience functions
def log_debug(message: str, module: str = "CORE"):
    """
    Log debug message.
    
    Args:
        message: Message to log
        module: Module name for tagging
    """
    get_logger().debug(message, module)

def log_info(message: str, module: str = "CORE"):
    """
    Log info message.
    
    Args:
        message: Message to log
        module: Module name for tagging
    """
    get_logger().info(message, module)

def log_warning(message: str, module: str = "CORE"):
    """
    Log warning message.
    
    Args:
        message: Message to log
        module: Module name for tagging
    """
    get_logger().warning(message, module)

def log_error(message: str, module: str = "CORE"):
    """
    Log error message.
    
    Args:
        message: Message to log
        module: Module name for tagging
    """
    get_logger().error(message, module)

def log_critical(message: str, module: str = "CORE"):
    """
    Log critical message.
    
    Args:
        message: Message to log
        module: Module name for tagging
    """
    get_logger().critical(message, module)
