import pytest
from unittest.mock import MagicMock, patch
from visual.glitch_logic import GlitchLogic

class TestGlitchHorror:
    @pytest.fixture
    def glitch_logic(self):
        mock_dispatcher = MagicMock()
        return GlitchLogic(mock_dispatcher)

    @patch('hardware.window_ops.WindowOps.get_active_window_info')
    def test_glitch_on_task_manager(self, mock_info, glitch_logic):
        # Target: Escape attempt
        mock_info.return_value = {'process': 'taskmgr.exe', 'class': 'TaskManagerWindow'}
        
        glitch_logic._on_window_changed({})
        
        # Should trigger aggressive glitch
        glitch_logic.dispatcher.dispatch.assert_called_with({"action": "SCREEN_MELT"})

    @patch('hardware.window_ops.WindowOps.get_active_window_info')
    def test_glitch_on_uninstaller(self, mock_info, glitch_logic):
        # Target: Uninstaller
        mock_info.return_value = {'process': 'msiexec.exe', 'title': 'programı kaldır'}
        
        glitch_logic._on_window_changed({})
        
        # Should trigger modification warning
        assert glitch_logic.dispatcher.dispatch.called
        # Check one of the calls
        glitch_logic.dispatcher.dispatch.assert_any_call({"action": "GDI_LINE"})
