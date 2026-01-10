import pytest
import os
from unittest.mock import MagicMock, patch
from PyQt6.QtCore import QTimer
from core.function_dispatcher import FunctionDispatcher
from core.memory import Memory
from core.gemini_brain import GeminiBrain
from story.story_manager import StoryManager

class TestStoryFlowIntegration:
    """Tests the story manager flow and act transitions."""
    
    @pytest.fixture
    def setup_systems(self):
        # Mock dependencies
        dispatcher = MagicMock() # Use generic mock to allow arbitrary attributes
        dispatcher.overlay = MagicMock()
        dispatcher.audio_out = MagicMock()
        
        memory = MagicMock(spec=Memory)
        memory.get_act.return_value = 1
        memory.data = {"user_profile": {"fear_level": 0, "behavior_stats": {"swear_count": 0}}}
        
        brain = MagicMock(spec=GeminiBrain)
        
        manager = StoryManager(dispatcher, memory, brain)
        return manager, dispatcher, memory

    def test_manager_initialization(self, setup_systems):
        manager, _, memory = setup_systems
        assert manager.current_act_num == 1
        assert manager.current_act_instance is None

    def test_act_transition_lock(self, setup_systems):
        """Verifies that multiple transitions cannot happen simultaneously."""
        manager, dispatcher, _ = setup_systems
        manager.current_act_num = 1
        
        # Mock sub-methods to avoid timer delays
        manager._show_transition_terminal = MagicMock()
        manager._show_act_title = MagicMock()
        manager._actually_load_next_act = MagicMock()
        
        # Trigger first transition
        manager.next_act()
        assert manager._is_transitioning is True
        
        # Trigger second transition immediately
        manager.next_act()
        # Should still be processing the first one, not incremented again
        # The logic inside next_act sets next_act_num = self.current_act_num + 1
        # If it was called twice, it might have caused issues if not for the lock.
        
    @patch('PyQt6.QtCore.QTimer.singleShot')
    def test_full_act_cycle(self, mock_timer, setup_systems):
        """Tests flowing from Act 1 to Act 2."""
        manager, dispatcher, memory = setup_systems
        
        # Start story
        manager._load_act = MagicMock()
        manager.start_story()
        
        manager._load_act.assert_called_with(1)
        
        # Complete Act 1
        print(f"DEBUG: Dispatcher overlay before next_act: {manager.dispatcher.overlay}")
        manager.next_act()
        assert manager._is_transitioning is True
        
        # Verify transition effects
        print(f"DEBUG: flash_color calls: {manager.dispatcher.overlay.flash_color.call_count}")
        assert manager.dispatcher.overlay.flash_color.called
        
        # Simulate transition completion
        manager._actually_load_next_act(2)
        assert manager._is_transitioning is False
        assert manager.current_act_num == 2
        manager._load_act.assert_called_with(2)

    def test_end_game_trigger(self, setup_systems):
        """Tests that game ends after Act 4."""
        manager, dispatcher, memory = setup_systems
        manager.current_act_num = 4
        manager._end_game = MagicMock()
        
        manager.next_act()
        manager._end_game.assert_called_once()
