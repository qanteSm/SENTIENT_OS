"""
Unit Tests for GeminiBrain

Tests AI response generation, caching, persona switching, and offline mode.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import json

from core.gemini_brain import GeminiBrain
from core.exceptions import APIConnectionError, AIResponseError


class TestGeminiBrainInitialization:
    """Test GeminiBrain constructor and initialization"""
    
    def test_init_with_api_key(self, mock_gemini_api):
        """Should initialize with valid API key"""
        brain = GeminiBrain(api_key="test_key_123")
        
        assert brain is not None
        assert brain._offline_mode == False
    
    def test_init_without_gemini_library(self):
        """Should handle missing Gemini library gracefully"""
        with patch('core.gemini_brain.HAS_GEMINI', False):
            brain = GeminiBrain(api_key="test_key")
            
            assert brain.mock_mode == True
    
    def test_set_memory(self, mock_gemini_api, mock_memory):
        """Should accept memory reference"""
        brain = GeminiBrain(api_key="test_key")
        brain.set_memory(mock_memory)
        
        assert brain.memory == mock_memory


class TestGeminiBrainCaching:
    """Test response caching functionality"""
    
    def test_cache_response(self, mock_gemini_api):
        """Should cache response correctly"""
        brain = GeminiBrain(api_key="test_key")
        
        key = "test_cache_key"
        response = {"action": "TEST", "params": {}}
        
        brain._cache_response(key, response)
        cached = brain._get_cached_response(key)
        
        assert cached == response
    
    def test_cache_expiry(self, mock_gemini_api):
        """Should expire cache after TTL"""
        brain = GeminiBrain(api_key="test_key")
        
        key = "test_key"
        response = {"action": "TEST", "params": {}}
        
        # Set cache with timestamp in the past
        brain._response_cache[key] = (
            response,
            0  # Very old timestamp
        )
        
        cached = brain._get_cached_response(key)
        assert cached is None  # Should be expired
    
    def test_cache_key_generation(self, mock_gemini_api):
        """Should generate consistent cache keys"""
        brain = GeminiBrain(api_key="test_key")
        
        context = {"act": 1, "chaos_level": 10}
        key1 = brain._get_cache_key("hello", context)
        key2 = brain._get_cache_key("hello", context)
        
        assert key1 == key2
        assert isinstance(key1, str)
        assert len(key1) > 0


class TestGeminiBrainPersonas:
    """Test persona switching"""
    
    def test_default_persona(self, mock_gemini_api):
        """Should start with Entity persona"""
        brain = GeminiBrain(api_key="test_key")
        
        assert brain.current_persona == "ENTITY"
    
    def test_switch_to_support(self, mock_gemini_api):
        """Should switch to Support persona"""
        brain = GeminiBrain(api_key="test_key")
        brain.switch_persona("SUPPORT")
        
        assert brain.current_persona == "SUPPORT"
    
    def test_get_entity_prompt(self, mock_gemini_api):
        """Should return Entity system prompt"""
        brain = GeminiBrain(api_key="test_key")
        prompt = brain._get_entity_prompt()
        
        assert isinstance(prompt, str)
        assert len(prompt) > 100
        assert "C.O.R.E" in prompt or "entity" in prompt.lower()
    
    def test_get_support_prompt(self, mock_gemini_api):
        """Should return Support system prompt"""
        brain = GeminiBrain(api_key="test_key")
        prompt = brain._get_support_prompt()
        
        assert isinstance(prompt, str)
        assert len(prompt) > 50
        assert "asistan" in prompt.lower() or "güvenlik" in prompt.lower()


class TestGeminiBrainResponseGeneration:
    """Test AI response generation"""
    
    def test_generate_response_success(self, mock_gemini_api, mock_memory):
        """Should generate valid response from API"""
        brain = GeminiBrain(api_key="test_key", memory=mock_memory)
        
        response = brain.generate_response("test input", {})
        
        assert response is not None
        assert isinstance(response, dict)
        assert "action" in response
    
    def test_generate_response_with_context(self, mock_gemini_api, mock_memory):
        """Should include context in prompt"""
        brain = GeminiBrain(api_key="test_key", memory=mock_memory)
        
        context = {"act": 2, "chaos_level": 50}
        response = brain.generate_response("test", context)
        
        assert response is not None
    
    def test_offline_mode_fallback(self, mock_gemini_api):
        """Should fallback to offline mode on API failure"""
        brain = GeminiBrain(api_key="test_key")
        brain._offline_mode = True
        
        response = brain._offline_response("hello", {})
        
        assert response is not None
        assert "action" in response
        assert response["action"] in ["NONE", "GLITCH_SCREEN", "OVERLAY_TEXT", "GDI_FLASH", "MOUSE_SHAKE"]


class TestGeminiBrainErrorHandling:
    """Test error handling"""
    
    def test_api_connection_error(self, mock_gemini_api):
        """Should handle API connection errors"""
        brain = GeminiBrain(api_key="test_key")
        
        # Mock API to raise exception
        mock_gemini_api.return_value.generate_content.side_effect = ConnectionError("Network error")
        
        # Should not crash, should fallback
        response = brain.generate_response("test", {})
        assert response is not None
    
    def test_invalid_json_response(self, mock_gemini_api):
        """Should handle invalid JSON from API"""
        brain = GeminiBrain(api_key="test_key")
        
        # Mock API to return invalid JSON
        mock_response = Mock()
        mock_response.text = "This is not JSON"
        mock_gemini_api.return_value.generate_content.return_value = mock_response
        
        # Should fallback to mock response
        response = brain.generate_response("test", {})
        assert response is not None
        assert isinstance(response, dict)


class TestGeminiBrainBehaviorAnalysis:
    """Test user behavior analysis"""
    
    def test_analyze_user_behavior(self, mock_gemini_api, mock_memory):
        """Should analyze user input and return behavior type"""
        brain = GeminiBrain(api_key="test_key", memory=mock_memory)
        
        # Test different inputs
        result1 = brain.analyze_user_behavior("help me please")
        result2 = brain.analyze_user_behavior("what are you?")
        result3 = brain.analyze_user_behavior("salak herif")
        
        # Test different inputs - expects actual behavior categories or None
        assert result1 is None # "help me please" doesn't match current keywords
        assert result2 is None
        assert result3 == "swear"


class TestGeminiBrainSnippetSafety:
    """Test snippet safety validation"""
    
    def test_validate_safe_snippet(self, mock_gemini_api):
        """Should validate safe code snippets"""
        brain = GeminiBrain(api_key="test_key")
        
        safe_snippet = {
            "content": "def hello():\n    print('Hello')",
            "language": "python"
        }
        
        # Mock AI response as safe (YES)
        mock_response = MagicMock()
        mock_response.text = "YES"
        mock_gemini_api.return_value.generate_content.return_value = mock_response
        
        result = brain.validate_snippet_safety(safe_snippet)
        assert result == True
    
    def test_validate_unsafe_snippet(self, mock_gemini_api):
        """Should detect unsafe snippets"""
        brain = GeminiBrain(api_key="test_key")
        
        unsafe_snippet = {
            "content": "password = 'mySecretPassword123'",
            "language": "python"
        }
        
        # Mock AI response as unsafe (NO)
        mock_response = MagicMock()
        mock_response.text = "NO"
        mock_gemini_api.return_value.generate_content.return_value = mock_response
        
        result = brain.validate_snippet_safety(unsafe_snippet)
        assert result == False
