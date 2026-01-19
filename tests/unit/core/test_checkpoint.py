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
from core.checkpoint_manager import CheckpointManager

class TestCheckpointManager:
    @pytest.fixture
    def manager(self, mock_memory):
        return CheckpointManager(mock_memory)
        
    def test_create_checkpoint(self, manager):
        with patch('os.makedirs'):
            with patch('builtins.open', create=True) as mock_open:
                result = manager.create("test_cp")
                assert result is True
                assert mock_open.called
                
    def test_list_checkpoints(self, manager):
        with patch('os.listdir', return_value=["cp_100_start.json", "cp_200_mid.json"]):
            checkpoints = manager._list_checkpoints()
            assert len(checkpoints) == 2
            assert checkpoints[0]["timestamp"] == 100
            assert checkpoints[1]["timestamp"] == 200
            
    def test_restore_latest(self, manager):
        mock_data = {"test": 123}
        with patch.object(manager, 'get_latest', return_value={"data": mock_data, "_checkpoint_meta": {"name": "test"}}):
            result = manager.restore_latest()
            assert result is True
            assert manager.memory.data == mock_data
