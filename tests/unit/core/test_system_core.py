# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import pytest
import os
import json
from unittest.mock import MagicMock, patch
from core.memory import Memory
from core.state_manager import StateManager
from core.gemini_brain import GeminiBrain

class TestSystemCore:
    """Tests for core management and AI components."""

    @pytest.fixture
    def memory(self):
        # Provide a more complete data structure to avoid KeyError
        with patch('core.memory.Config') as mock_config:
            mock_config.return_value.LANGUAGE = "en"
            mem = Memory(filepath=":memory:") # Special path or mocked
            mem.data = {
                "user_profile": {
                    "behavior_stats": {
                        "total_messages": 0,
                        "swear_count": 0,
                        "begged_count": 0,
                        "defiance_count": 0,
                        "escape_attempts": 0,
                        "silence_periods": 0
                    },
                    "memorable_moments": []
                },
                "game_state": {
                    "current_act": 1,
                    "session_start": 0
                },
                "event_log": []
            }
            return mem

    def test_memory_behavior_recording(self, memory):
        """Verifies behavior tracking logic."""
        memory.record_behavior("swear", "some bad word")
        assert memory.data["user_profile"]["behavior_stats"]["swear_count"] == 1
        
    def test_state_manager_persistence(self):
        """Verifies state save/load."""
        sm = StateManager()
        sm.update_state("test_key", "test_val")
        assert sm.get_state("test_key") == "test_val"
        
        # Test cleaning
        sm.remove_state("test_key")
        assert sm.get_state("test_key") is None

    @patch('core.gemini_brain.genai.GenerativeModel')
    def test_brain_generation(self, mock_model_class):
        """Verifies brain sends correct prompt to Gemini."""
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        
        # Mock response to be valid JSON in text attribute
        mock_response = MagicMock()
        mock_response.text = '{"action": "OVERLAY_TEXT", "params": {"text": "Hello"}, "speech": "Hi"}'
        mock_model.generate_content.return_value = mock_response
        
        brain = GeminiBrain(api_key="fake")
        response = brain.generate_response("Test prompt")
        
        assert response["action"] == "OVERLAY_TEXT"
        assert response["params"]["text"] == "Hello"

    def test_memory_act_retrieval(self, memory):
        """Verifies act number logic."""
        memory.set_act(3)
        assert memory.get_act() == 3
