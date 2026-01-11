import pytest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap, QColor

class TestVisualEffectsLogic:
    """Tests for individual visual effect units."""

    @pytest.fixture
    def app(self):
        return QApplication.instance() or QApplication([])

    def test_screen_melter_lifecycle(self, app):
        """Verifies ScreenMelter setup and timer cleanup."""
        # Use deep mocking to avoid native crashes
        with patch('PyQt6.QtWidgets.QWidget.showFullScreen'):
            with patch('PyQt6.QtGui.QScreen.grabWindow', return_value=QPixmap(10, 10)):
                from visual.effects.screen_melter import ScreenMelter
                melter = ScreenMelter()
                assert melter.timer.isActive()
                melter.close()

    @patch('visual.effects.pixel_melt.QTimer.singleShot')
    @patch('visual.effects.pixel_melt.windll.user32.GetDC')
    @patch('visual.effects.pixel_melt.windll.user32.ReleaseDC')
    @patch('visual.effects.pixel_melt.win32ui.CreateDCFromHandle')
    @patch('visual.effects.pixel_melt.win32ui.CreateBitmap')
    def test_pixel_melt_logic(self, mock_create_bitmap, mock_create_dc, mock_release_dc, mock_get_dc, mock_timer, app):
        """Verifies PixelMelt trigger doesn't crash."""
        from visual.effects.pixel_melt import PixelMelt
        with patch('visual.effects.pixel_melt.windll.user32.GetSystemMetrics', return_value=1000):
            PixelMelt.melt_region(x=0, y=0, width=10, height=10)
            assert mock_timer.called

    @patch('visual.effects.screen_tear.QTimer.singleShot')
    @patch('visual.effects.screen_tear.windll.user32.GetDC')
    @patch('visual.effects.screen_tear.windll.user32.ReleaseDC')
    @patch('visual.effects.screen_tear.win32ui.CreateDCFromHandle')
    @patch('visual.effects.screen_tear.win32ui.CreateBitmap')
    def test_screen_tear_trigger(self, mock_create_bitmap, mock_create_dc, mock_release_dc, mock_get_dc, mock_timer, app):
        """Verifies ScreenTear trigger logic."""
        from visual.effects.screen_tear import ScreenTear
        with patch('visual.effects.screen_tear.windll.user32.GetSystemMetrics', return_value=1000):
            ScreenTear.tear_screen(intensity=1, duration=100)
            assert mock_timer.called
