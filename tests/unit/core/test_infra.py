# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import pytest
import os
from unittest.mock import MagicMock, patch
from core.event_bus import EventBus
from core.state_manager import StateManager
from config import Config

class TestCoreInfra:
    def test_event_bus_pub_sub(self):
        bus = EventBus()
        mock_callback = MagicMock()
        
        bus.subscribe("test_event", mock_callback)
        bus.publish("test_event", data="payload")
        
        mock_callback.assert_called_with("payload")

    def test_state_manager_persistence(self):
        state = StateManager()
        state.update_state("progress", 50)
        assert state.get_state("progress") == 50
        
        # Test missing
        assert state.get_state("non_existent") is None

    def test_config_loading(self):
        cfg = Config()
        # Should have some default keys
        assert hasattr(cfg, "LANGUAGE")
        assert cfg.get("CHAOS_LEVEL") is not None
