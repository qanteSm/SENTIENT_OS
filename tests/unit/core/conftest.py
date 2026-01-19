# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import pytest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication

@pytest.fixture(scope="session", autouse=True)
def app():
    """Provides a single QApplication for all tests in this session."""
    return QApplication.instance() or QApplication([])

@pytest.fixture
def mock_memory():
    memory = MagicMock()
    memory.data = {
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
        "discovered_info": {
            "desktop_files_seen": [],
            "apps_detected": []
        }
    }
    memory.get_full_context_for_ai.return_value = "Mock context"
    return memory

@pytest.fixture
def mock_gemini_api():
    with patch('google.generativeai.GenerativeModel') as mock_model:
        yield mock_model
