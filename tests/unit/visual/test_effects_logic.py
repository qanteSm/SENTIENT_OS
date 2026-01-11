import pytest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPixmap, QColor

class TestVisualEffectsLogic:
    """Tests for individual visual effect units."""

    @pytest.fixture
    def app(self):
        """Standardized QApplication fixture."""
        return QApplication.instance() or QApplication([])

    def test_screen_melter_lifecycle(self, app):
        """Verifies ScreenMelter setup and timer cleanup."""
        # Use deep mocking to avoid native crashes
        with patch('visual.effects.screen_melter.QTimer') as mock_timer, \
             patch('visual.effects.screen_melter.QApplication') as mock_qapp, \
             patch('PyQt6.QtWidgets.QWidget.showFullScreen'):
            
            # Setup Safe Mock for Screen
            mock_screen = MagicMock()
            mock_screen.grabWindow.return_value = QPixmap(10, 10)
            # CRITICAL: setGeometry requires a valid QRect, not a Mock object
            mock_screen.geometry.return_value = QRect(0, 0, 1920, 1080)
            mock_qapp.primaryScreen.return_value = mock_screen
            
            # Mock GDIEngine to prevent force_refresh_screen calls during close()
            with patch('visual.gdi_engine.GDIEngine') as mock_gdi:
                from visual.effects.screen_melter import ScreenMelter
                melter = ScreenMelter()
                
                # Verify Timer Started
                assert mock_timer.return_value.start.called
                
                # CRITICAL FIX: Do NOT use WA_DeleteOnClose in tests!
                # It causes Qt event loop conflicts with mocked QApplication
                # causing pytest to terminate before teardown hooks execute
                # melter.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)  # ❌ REMOVED
                
                # Stop timer before closing to prevent any pending events
                melter.timer.stop()
                melter.life_timer.stop()
                
                # Close the widget
                melter.close()
                
                # Verify refresh was requested safely
                mock_gdi.force_refresh_screen.assert_called_once()
                
                # Explicit cleanup - delete the widget manually
                del melter
                
                # Force Qt event processing to clear any queued events
                from PyQt6.QtWidgets import QApplication as QApp
                if QApp.instance():
                    QApp.processEvents()
                    QApp.processEvents()  # Call twice for safety

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
