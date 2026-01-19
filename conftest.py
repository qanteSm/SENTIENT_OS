# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Pytest Configuration for SENTIENT_OS
Provides shared fixtures and test utilities.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

import time
import json
import threading
import psutil
from pathlib import Path

# Global storage for profiling
_global_snapshots = []

# Import BEFORE creating fixtures to avoid singleton issues
from config import Config

# ==========================================
# DEBUG LOGGING HOOKS
# ==========================================
DEBUG_LOG_PATH = Path("tests/debug_trace.log")

def log_debug_trace(message):
    try:
        with open(DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            timestamp = time.strftime("%H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")
    except Exception:
        pass

def pytest_sessionstart(session):
    # Create tests dir if not exists
    Path("tests").mkdir(exist_ok=True)
    # Clear previous log
    with open(DEBUG_LOG_PATH, "w", encoding="utf-8") as f:
        f.write("=== SESSION START ===\n")

def pytest_runtest_setup(item):
    log_debug_trace(f"SETUP: {item.nodeid}")

def pytest_runtest_call(item):
    log_debug_trace(f"CALL: {item.nodeid}")

def pytest_runtest_teardown(item, nextitem=None):
    log_debug_trace(f"TEARDOWN: {item.nodeid}")

def pytest_sessionfinish(session, exitstatus):
    log_debug_trace(f"=== SESSION FINISH === Exit Code: {exitstatus}")

def pytest_internalerror(excrepr, excinfo):
    log_debug_trace(f"!!! INTERNAL ERROR !!!\n{excrepr}")

def pytest_keyboard_interrupt(excinfo):
    log_debug_trace("!!! KEYBOARD INTERRUPT !!!")

# ==========================================
# FIXTURES
# ==========================================

@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singleton instances between tests"""
    # Reset Config singleton
    if hasattr(Config, '_instance'):
        Config._instance = None
        Config._initialized = False
    
    # Set TEST_MODE globally for all tests to prevent safety sensors
    Config().set("TEST_MODE", True, validate=False)
    
    # Reset Memory singleton
    try:
        from core.memory import Memory
        if hasattr(Memory, '_instance'):
            Memory._instance = None
            Memory._initialized = False
        # Pre-initialize in test mode to prevent loading from real file
        Memory(test_mode=True)
    except (ImportError, AttributeError) as e:
        # Memory module not available in this test context
        pass
    
    yield
    
    # CRITICAL: Clean up Qt event queue after each test
    # This prevents state pollution from previous tests causing
    # pytest to crash during teardown of Qt widget tests
    try:
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            # Process all pending events
            app.processEvents()
            app.processEvents()  # Call twice for safety
            
            # Close and delete all top-level widgets
            for widget in app.topLevelWidgets():
                try:
                    widget.close()
                    widget.deleteLater()
                except:
                    pass
            
            # Final event processing to handle deleteLater
            app.processEvents()
    except (ImportError, AttributeError):
        # Qt not available in this test
        pass

@pytest.fixture
def mock_config():
    """Provide a test configuration with safe defaults"""
    config = Config()
    # Set values using the proper API
    if hasattr(config, 'set'):
        config.set("STREAMER_MODE", True, validate=False)
        config.set("SAFE_HARDWARE", True, validate=False)
        config.set("CHAOS_LEVEL", 0, validate=False)
        config.set("LANGUAGE", "tr", validate=False)
        config.set("TEST_MODE", True, validate=False)
    return config


@pytest.fixture
def mock_memory():
    """Mock Memory instance"""
    memory = Mock()
    memory.data = {
        "game_state": {"act": 1, "chaos_level": 0},
        "user_profile": {"real_name": "Test User"},
        "conversation_history": []
    }
    memory.get_act.return_value = 1
    memory.get_chaos_level.return_value = 0
    memory.get_full_context_for_ai.return_value = "TEST CONTEXT"
    return memory


@pytest.fixture
def mock_gemini_api():
    """Mock Gemini API responses"""
    with patch('google.generativeai.GenerativeModel') as mock:
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = '{"action": "NONE", "params": {}, "speech": "Test response"}'
        mock_model.generate_content.return_value = mock_response
        mock.return_value = mock_model
        yield mock


@pytest.fixture
def sample_ai_response():
    """Sample AI response for testing"""
    return {
        "action": "OVERLAY_TEXT",
        "params": {
            "text": "Test message",
            "duration": 3000
        },
        "speech": "This is a test"
    }


@pytest.fixture
def sample_context():
    """Sample context dictionary"""
    return {
        "act": 2,
        "chaos_level": 30,
        "user_name": "Test User",
        "last_action": "MOUSE_SHAKE",
        "conversation_history": []
    }
