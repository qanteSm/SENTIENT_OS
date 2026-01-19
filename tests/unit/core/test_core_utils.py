# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import pytest
from core.anger_engine import AngerEngine
from core.privacy_filter import PrivacyFilter
from core.validators import validate_ai_response, validate_config_value, validate_action_params

class TestAngerEngine:
    def test_anger_increase(self):
        engine = AngerEngine()
        initial = engine.current_anger
        engine.calculate_anger("swear")
        assert engine.current_anger == initial + 15
        
    def test_anger_decrease(self):
        engine = AngerEngine()
        engine.current_anger = 50
        engine.calculate_anger("obedience")
        assert engine.current_anger == 45
        
    def test_chaos_multiplier(self):
        engine = AngerEngine()
        assert engine.get_chaos_multiplier() == 1.0
        engine.current_anger = 90
        assert engine.get_chaos_multiplier() == 3.0

class TestPrivacyFilter:
    def test_scrub_username(self):
        filter = PrivacyFilter()
        user = filter.username
        text = f"Hello {user}, welcome home."
        scrubbed = filter.scrub(text)
        # Username should be replaced (either by alias in Streamer Mode or <USER>)
        assert user not in scrubbed, f"Username '{user}' should be scrubbed but found in: {scrubbed}"
        # Scrubbed version should be different from original
        assert scrubbed != text, "Text should be modified by privacy filter"
        
    def test_scrub_ip(self):
        filter = PrivacyFilter()
        text = "My IP is 192.168.1.1"
        assert "192.168.1.1" not in filter.scrub(text)
        assert "<IP_ADDR>" in filter.scrub(text)
        
    def test_scrub_paths(self):
        filter = PrivacyFilter()
        text = r"Check C:\Users\Betul\Desktop\secret.txt"
        scrubbed = filter.scrub(text)
        assert "Betul" not in scrubbed
        assert "<USER_DIR>" in scrubbed

class TestValidators:
    def test_validate_ai_response_valid(self):
        response = {
            "action": "OVERLAY_TEXT",
            "params": {"text": "Hello"},
            "speech": "Hi"
        }
        assert validate_ai_response(response) == True
        
    def test_validate_ai_response_invalid_action(self):
        response = {"action": "INVALID_ACTION_NAME"}
        with pytest.raises(Exception): # ValidationError
            validate_ai_response(response)
            
    def test_validate_config_value(self):
        assert validate_config_value("CHAOS_LEVEL", 50) == True
        with pytest.raises(Exception):
            validate_config_value("CHAOS_LEVEL", 150)
            
    def test_validate_action_params(self):
        assert validate_action_params("OVERLAY_TEXT", {"text": "valid"}) == True
        with pytest.raises(Exception):
            validate_action_params("OVERLAY_TEXT", {"wrong_param": "missing text"})
