# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import pytest
import time
from unittest.mock import MagicMock, patch
from story.act_1_infection import Act1Infection
from story.act_2_awakening import Act2Awakening

class TestActEventLogic:
    """Tests for act-specific event scheduling and cleanup."""

    @pytest.fixture
    def mock_dispatcher(self):
        return MagicMock()

    @pytest.fixture
    def mock_brain(self):
        return MagicMock()

    def test_act1_initialization(self, mock_dispatcher, mock_brain):
        """Verifies Act 1 timeline setup."""
        act = Act1Infection(mock_dispatcher, mock_brain)
        act.start()
        assert len(act.timers) > 0 
        
    def test_act1_event_trigger(self, mock_dispatcher, mock_brain):
        """Verifies event dispatching in Act 1."""
        act = Act1Infection(mock_dispatcher, mock_brain)
        # Use an actual trigger_event call
        act.trigger_event("MOUSE_SHAKE", {"duration": 0.5}, "")
        mock_dispatcher.dispatch.assert_called_with({"action": "MOUSE_SHAKE", "params": {"duration": 0.5}, "speech": ""})

    def test_act2_cleanup(self, mock_dispatcher, mock_brain):
        """Verifies that stopping an act stops all timers."""
        act = Act2Awakening(mock_dispatcher, mock_brain)
        
        # Simulate active timers
        mock_timer = MagicMock()
        act.timers.append(mock_timer)
        
        act.stop()
        mock_timer.stop.assert_called_once()
        assert len(act.timers) == 0

    def test_act1_progression(self, mock_dispatcher, mock_brain):
        """Verifies that act completion signal is eventual."""
        act = Act1Infection(mock_dispatcher, mock_brain)
        # Mock finishing signal
        mock_signal = MagicMock()
        act.act_finished.connect(mock_signal)
        
        act.finish()
        assert mock_signal.called
