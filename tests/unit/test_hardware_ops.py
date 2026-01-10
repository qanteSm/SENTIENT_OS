import pytest
from unittest.mock import MagicMock, patch
from hardware.keyboard_ops import KeyboardOps
from hardware.mouse_ops import MouseOps

class TestHardwareOps:
    """Tests for core hardware manipulation logic."""

    @patch('keyboard.block_key')
    @patch('keyboard.unhook_all')
    def test_keyboard_block(self, mock_unhook, mock_block):
        """Verifies keyboard locking logic."""
        KeyboardOps.lock_input()
        assert mock_block.called
        
        KeyboardOps.unlock_input()
        assert mock_unhook.called

    @patch('mouse.move')
    def test_mouse_freeze(self, mock_move):
        """Verifies mouse freezing behavior."""
        MouseOps.freeze_cursor()
        assert MouseOps._frozen is True
        
        MouseOps.unfreeze_cursor()
        assert MouseOps._frozen is False

    @patch('mouse.move')
    def test_mouse_shake(self, mock_move):
        """Verifies mouse shaking logic."""
        # Use a mock for _is_safe_to_interact to bypass window checks
        with patch('hardware.mouse_ops.MouseOps._is_safe_to_interact', return_value=True):
            MouseOps.shake_cursor(duration=0.1)
            # Since it runs in a thread, we might need a small sleep or just check if it started
            assert MouseOps._shaking is True

    @patch('hardware.brightness_ops.sbc.set_brightness')
    def test_brightness_flicker(self, mock_set_brightness):
        """Verifies brightness manipulation."""
        from hardware.brightness_ops import BrightnessOps
        BrightnessOps.flicker(times=1)
        assert mock_set_brightness.called
