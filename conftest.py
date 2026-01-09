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

# Import BEFORE creating fixtures to avoid singleton issues
from config import Config


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singleton instances between tests"""
    # Reset Config singleton
    if hasattr(Config, '_instance'):
        Config._instance = None
        Config._initialized = False
    
    # Reset Memory singleton
    try:
        from core.memory import Memory
        if hasattr(Memory, '_instance'):
            Memory._instance = None
            Memory._initialized = False
    except:
        pass
    
    yield


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
