import pytest
from unittest.mock import MagicMock, patch
from core.safety_net import SafetyNet

class TestSafetyNet:
    """Tests for the SafetyNet system."""
    
    @pytest.fixture
    def safety_net(self):
        return SafetyNet()

    def test_emergency_cleanup_signal(self, safety_net):
        """Verifies that cleanup publishes a shutdown signal."""
        with patch('core.safety_net.bus') as mock_bus:
            with patch('core.safety_net.QTimer.singleShot'):
                safety_net.emergency_cleanup()
                mock_bus.publish.assert_called_with("system.shutdown", {"reason": "kill_switch"})

    def test_escape_attempt_logging(self, safety_net):
        """Verifies that Alt+F4 is detected and logged."""
        mock_memory = MagicMock()
        SafetyNet.set_memory(mock_memory)
        
        safety_net._on_escape_attempt_altf4()
        
        assert safety_net.escape_attempts == 1
        mock_memory.record_behavior.assert_called_with("escape_attempt", "Alt+F4")

    @patch('core.safety_net.QTimer.singleShot')
    @patch('core.safety_net.QApplication.instance')
    def test_cleanup_main_thread(self, mock_app_instance, mock_timer, safety_net):
        """Verifies hardware and UI cleanup on main thread."""
        mock_app = MagicMock()
        mock_app_instance.return_value = mock_app
        
        with patch('hardware.keyboard_ops.KeyboardOps.unlock_input') as mock_kb:
            with patch('hardware.mouse_ops.MouseOps.unfreeze_cursor') as mock_mouse:
                with patch('visual.fake_ui.FakeUI') as mock_fake_ui:
                    safety_net._do_cleanup_main_thread()
                    
                    mock_kb.assert_called_once()
                    mock_mouse.assert_called_once()
                    mock_app.quit.assert_called_once()
                    assert mock_timer.called
