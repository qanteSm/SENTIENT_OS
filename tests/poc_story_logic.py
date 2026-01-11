
import sys
import unittest
from unittest.mock import MagicMock, patch

# Completely mock everything Qt first
sys.modules['PyQt6'] = MagicMock()
sys.modules['PyQt6.QtCore'] = MagicMock()
sys.modules['PyQt6.QtWidgets'] = MagicMock()
sys.modules['PyQt6.QtGui'] = MagicMock()

# Mock dependencies
sys.modules['core.memory'] = MagicMock()
sys.modules['core.function_dispatcher'] = MagicMock()
sys.modules['core.gemini_brain'] = MagicMock()
sys.modules['core.checkpoint_manager'] = MagicMock()
sys.modules['core.logger'] = MagicMock()
sys.modules['core.localization_manager'] = MagicMock()
sys.modules['story.act_1_infection'] = MagicMock()
sys.modules['story.act_2_awakening'] = MagicMock()
sys.modules['story.act_3_torment'] = MagicMock()
sys.modules['story.act_4_exorcism'] = MagicMock()

# Need to make QObject usable in class definition
sys.modules['PyQt6.QtCore'].QObject = object
sys.modules['PyQt6.QtCore'].pyqtSignal = lambda *args: MagicMock()

# Import
from story.story_manager import StoryManager

class TestStoryManager(unittest.TestCase):
    def setUp(self):
        self.mock_dispatcher = MagicMock()
        self.mock_memory = MagicMock()
        self.mock_brain = MagicMock()
        self.sm = StoryManager(self.mock_dispatcher, self.mock_memory, self.mock_brain)

    def test_transition_logic(self):
        """
        Verify that next_act increments act number and loads correct act.
        """
        self.sm.current_act_num = 1

        # Mocking methods to avoid side effects
        self.sm._show_transition_terminal = MagicMock()
        self.sm._show_act_title = MagicMock()
        self.sm._actually_load_next_act = MagicMock()
        self.sm._end_game = MagicMock()

        # Trigger transition
        self.sm.next_act()

        # Verify transition flag is locked
        self.assertTrue(self.sm._is_transitioning)

        # Simulate timer callback for loading act
        # next_act(1) -> expect act 2
        self.sm._actually_load_next_act(2)

        # Verify
        self.assertFalse(self.sm._is_transitioning)
        self.assertEqual(self.sm.current_act_num, 2)
        self.sm._actually_load_next_act.assert_called_with(2)

    def test_act_out_of_bounds(self):
        """
        Verify game end trigger on act > 4.
        """
        self.sm.current_act_num = 4
        self.sm._end_game = MagicMock()

        self.sm.next_act()

        self.sm._end_game.assert_called()

if __name__ == '__main__':
    unittest.main()
