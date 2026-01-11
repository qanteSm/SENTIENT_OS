import pytest
import json
from unittest.mock import MagicMock, patch
from core.gemini_brain import GeminiBrain

class TestGeminiRetry:
    
    @pytest.fixture
    def brain(self):
        # Patch config and model
        with patch('core.gemini_brain.Config') as mock_conf:
            mock_conf.return_value.get.return_value = "fake_key"
            brain = GeminiBrain()
            brain.model = MagicMock()
            brain._offline_mode = False
            brain.mock_mode = False # Force API path
            # Mock build_dynamic_prompt
            brain._build_dynamic_prompt = MagicMock(return_value="prompt")
            # Clear cache
            brain._response_cache = {}
            return brain

    def test_json_retry_mechanism(self, brain):
        """
        Verify that if the AI returns invalid JSON, it retries with a repair prompt.
        """
        # Scenario:
        # Call 1: Returns broken JSON "I am broken {"
        # Call 2: Returns valid JSON
        
        broken_response = MagicMock()
        broken_response.text = "I am broken {"
        
        valid_response = MagicMock()
        valid_response.text = '{"speech": "Fixed", "action": "NONE"}'
        
        # Side effect for generate_content
        brain.model.generate_content.side_effect = [broken_response, valid_response]
        
        # Execute
        result = brain.generate_response("Test input")
        
        # Assertions
        assert result["speech"] == "Fixed"
        assert brain.model.generate_content.call_count == 2
        
        # Verify first call was normal
        args1, _ = brain.model.generate_content.call_args_list[0]
        assert "prompt" in args1[0]
        
        # Verify second call included error instruction
        args2, _ = brain.model.generate_content.call_args_list[1]
        assert "SYSTEM ERROR" in args2[0]
        assert "Expecting value" in args2[0] # JSON error message part

    def test_retry_failure_fallback(self, brain):
        """
        Verify that if it fails twice, it falls back to backup.
        """
        broken_response = MagicMock()
        broken_response.text = "I am broken {"
        
        brain.model.generate_content.return_value = broken_response
        
        # Execute
        result = brain.generate_response("Test input")
        
        # Assertions
        assert "speech" in result
        # Check if fallback used (depends on _backup_response implementation)
        # Typically backup response has generic text
        assert brain.model.generate_content.call_count == 3
