# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
SENTIENT_OS Logging Framework
Proper logging instead of print() statements.
"""
import logging
import os
import sys
import threading
from datetime import datetime
from config import Config

class SentientLogger:
    """
    Centralized logging for SENTIENT_OS.
    Supports file and console output with different log levels.
    """
    
    _instance = None
    _initialized = False
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SentientLogger, cls).__new__(cls)
            return cls._instance
    
    def __init__(self):
        with self._lock:
            if SentientLogger._initialized:
                return
            
            # Create logs directory
            self.logs_dir = Config().LOGS_DIR
            os.makedirs(self.logs_dir, exist_ok=True)
            
            # Create logger
            self.logger = logging.getLogger("SENTIENT_OS")
            self.logger.setLevel(logging.DEBUG if Config().IS_MOCK else logging.INFO)
            
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
            
            self.logger.info(f"SENTIENT_OS v{Config().get('VERSION', '0.8.0')} - Logging initialized")
            SentientLogger._initialized = True
    
    def debug(self, message: str, module: str = "CORE"):
        self.logger.debug(f"[{module}] {message}")
    
    def info(self, message: str, module: str = "CORE"):
        self.logger.info(f"[{module}] {message}")
    
    def warning(self, message: str, module: str = "CORE"):
        self.logger.warning(f"[{module}] {message}")
    
    def error(self, message: str, module: str = "CORE"):
        self.logger.error(f"[{module}] {message}")
    
    def critical(self, message: str, module: str = "CORE"):
        self.logger.critical(f"[{module}] {message}")


# Global logger instance
_logger = None

def get_logger() -> SentientLogger:
    """Returns the global logger instance."""
    global _logger
    if _logger is None:
        _logger = SentientLogger()
    return _logger

# Convenience functions
def log_debug(message: str, module: str = "CORE"):
    get_logger().debug(message, module)

def log_info(message: str, module: str = "CORE"):
    get_logger().info(message, module)

def log_warning(message: str, module: str = "CORE"):
    get_logger().warning(message, module)

def log_error(message: str, module: str = "CORE"):
    get_logger().error(message, module)

def log_critical(message: str, module: str = "CORE"):
    get_logger().critical(message, module)
