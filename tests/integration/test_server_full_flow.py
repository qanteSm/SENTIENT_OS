# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import pytest
import time
import uuid
from unittest.mock import MagicMock, patch, AsyncMock
from core.gemini_brain import GeminiBrain
from core.config_manager import ConfigManager
from sdk.sentientos.models import InferenceResponse

class MockSentientClient:
    def __init__(self, responses=None):
        self.responses = responses or []
        self.call_count = 0
        self.base_url = "http://mock"
        self.token = "mock"
        self.device_id = "mock"

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def infer(self, message, context, request_id=None):
        self.call_count += 1
        self.last_request_id = request_id
        if self.call_count <= len(self.responses):
            resp = self.responses[self.call_count - 1]
            if isinstance(resp, Exception):
                raise resp
            return resp
        return InferenceResponse(text="Default", actions=[], cache="miss")

@pytest.fixture
def mock_config():
    with patch('core.gemini_brain.ConfigManager') as mock:
        config_inst = mock.return_value
        config_inst.get.side_effect = lambda key, default=None: {
            'server.enabled': True,
            'server.edge_url': 'http://localhost:8000',
            'server.jwt_token': 'test_token',
            'server.device_id': 'test_device',
            'api.gemini_key': 'test_key'
        }.get(key, default)
        yield config_inst

@pytest.fixture
def brain(mock_config):
    with patch('core.gemini_brain.HAS_SDK', True), \
         patch('google.generativeai.configure'), \
         patch('google.generativeai.GenerativeModel'):
        return GeminiBrain()

def test_server_success_flow(brain):
    """Test standard successful server response."""
    mock_resp = InferenceResponse(text="Hello from server", actions=[{"type": "GLITCH", "payload": {}}], cache="miss")
    
    with patch('core.gemini_brain.SentientClient', return_value=MockSentientClient([mock_resp])):
        response = brain.generate_response("Hi")
        assert response["speech"] == "Hello from server"
        assert response["action"] == "GLITCH"

def test_server_retry_and_success(brain):
    """Test that it retries on error and eventually succeeds."""
    mock_resp = InferenceResponse(text="Success after retry", actions=[], cache="miss")
    # Fail once with exception, then succeed
    responses = [Exception("Temporary Error"), mock_resp]
    
    # Speed up the test by mocking time.sleep
    with patch('core.gemini_brain.SentientClient', return_value=MockSentientClient(responses)), \
         patch('time.sleep', return_value=None):
        
        response = brain.generate_response("Hi")
        assert response["speech"] == "Success after retry"

def test_server_all_fail_fallback(brain):
    """Test that all server failures lead to direct Gemini fallback (or mock)."""
    responses = [Exception("Fail 1"), Exception("Fail 2"), Exception("Fail 3")]
    
    with patch('core.gemini_brain.SentientClient', return_value=MockSentientClient(responses)), \
         patch('time.sleep', return_value=None), \
         patch.object(GeminiBrain, '_backup_response') as mock_fallback:
        
        mock_fallback.return_value = {"speech": "Fallback response", "action": "NONE"}
        
        # Force mock_mode or similar if genai is not configured
        brain.mock_mode = True 
        
        response = brain.generate_response("Hi")
        assert response["speech"] == "Fallback response"
        assert mock_fallback.called

def test_request_id_propagation(brain):
    """Verify that Request ID is propagated correctly."""
    mock_client = MockSentientClient([InferenceResponse(text="OK", actions=[], cache="miss")])
    
    with patch('core.gemini_brain.SentientClient', return_value=mock_client):
        response = brain.generate_response("Hi")
        assert mock_client.call_count == 1
        assert mock_client.last_request_id is not None
        assert len(mock_client.last_request_id) == 8
