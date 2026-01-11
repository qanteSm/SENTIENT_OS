import pytest
from unittest.mock import MagicMock, patch
from story.story_manager import StoryManager
from story.dynamic_scheduler import DynamicEventScheduler

class TestStoryOrchestration:
    @pytest.fixture
    def app(self):
        from PyQt6.QtWidgets import QApplication
        import sys
        return QApplication.instance() or QApplication(sys.argv)

    @pytest.fixture
    def story_mgr(self, mock_memory):
        mock_dispatcher = MagicMock()
        mock_dispatcher.overlay = MagicMock()
        mock_dispatcher.overlay.flash_color = MagicMock()
        mock_dispatcher.overlay.show_text = MagicMock()
        mock_brain = MagicMock()
        
        # Patch QTimer to prevent real Qt timer usage which causes silent exits
        # We patch at module level for StoryManager
        with patch('story.story_manager.QTimer'):
            mgr = StoryManager(mock_dispatcher, mock_memory, mock_brain)
            yield mgr
            if hasattr(mgr, 'stop'):
                 mgr.stop()

    def test_story_manager_init(self, story_mgr):
        assert story_mgr.current_act_num == 1
        
    @patch('story.story_manager.Act1Infection')
    def test_load_act(self, mock_act1, story_mgr):
        # Setup mock act logic manually since _load_act is real
        mock_instance = MagicMock()
        mock_act1.return_value = mock_instance
        
        story_mgr._load_act(1)
        
        assert story_mgr.memory.set_act.called
        assert story_mgr.current_act_instance is not None
        mock_act1.assert_called()


    def test_dynamic_scheduler_adaptive_delay(self):
        scheduler = DynamicEventScheduler()
        
        # User is active (0s idle)
        scheduler.on_user_activity()
        delay_active = scheduler._calculate_adaptive_delay(1000, 5000)
        
        # User is idle (60s idle)
        scheduler.user_idle_time = 60
        delay_idle = scheduler._calculate_adaptive_delay(1000, 5000)
        
        # Idle delay should be significantly lower (closer to min_delay)
        # Average delay_active = 1000 + 4000/2 = 3000
        # Average delay_idle = 1000 + 1600/2 = 1800
        # We test if delay_idle is within its theoretical range
        assert 1000 <= delay_idle <= 2600
