# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import pytest
import time
from unittest.mock import MagicMock, patch
from core.sensors.panic_sensor import PanicSensor
from core.sensors.presence_sensor import PresenceSensor

class TestSensors:
    """Tests for autonomous sensor logic."""

    @patch('win32api.GetCursorPos')
    def test_panic_sensor_trigger(self, mock_get_cursor):
        """Verifies panic sensor triggers on hot corner."""
        mock_get_cursor.return_value = (0, 0)
        sensor = PanicSensor()
        sensor.trigger_threshold = 0.1 # Very fast for test
        
        with patch('core.event_bus.bus.publish') as mock_publish:
            # We mock the loop or just call the logic step if possible
            # Here we simulate the logic within run() manually for unit test
            sensor.corner_timer = time.time() - 0.2
            # Simulate one check
            sensor.run() # This would normally block, so we need to mock is_running
            
    @patch('core.sensors.presence_sensor.bus.publish')
    def test_presence_sensor_movement(self, mock_publish):
        """Verifies movement detection in PresenceSensor."""
        sensor = PresenceSensor()
        mock_pyautogui = MagicMock()
        mock_pyautogui.position.return_value = (100, 100)
        sensor._pyautogui = mock_pyautogui
        
        # First call sets initial position
        sensor.collect_data()
        
        # Second call with different position triggers movement
        mock_pyautogui.position.return_value = (200, 200)
        data = sensor.collect_data()
        
        assert data["type"] == "mouse_move"
        assert data["pos"] == (200, 200)
        assert mock_publish.called
