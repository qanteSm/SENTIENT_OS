import pytest
import sys
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication
from visual.fake_ui import FakeUI


@pytest.fixture
def app():
    # Ensure a QApplication exists
    return QApplication.instance() or QApplication(sys.argv)

class TestUIStress:
    """Tests the UI components under rapid triggers."""
    
    def test_notification_burst(self, app):
        """Spawns many notifications rapidly."""
        ui = FakeUI()
        
        # Spawn 20 notifications
        for i in range(20):
            ui.show_fake_notification(f"Title {i}", f"Message {i}", duration=1000)
            
        assert len(ui.active_notifications) == 20
        
        # Cleanup
        ui.close_all()
        assert len(ui.active_notifications) == 0

    def test_overlay_overlap(self, app):
        """Tests triggering multiple overlays."""
        ui = FakeUI()
        
        # These shouldn't crash
        ui.show_bsod()
        ui.show_fake_update(50)
        
        assert ui.bsod is not None
        assert ui.update_screen is not None
        
        ui.close_all()
        assert ui.bsod is None
        assert ui.update_screen is None

    def test_gdi_refresh(self, app):
        """Verifies GDI refresh doesn't crash."""
        from visual.gdi_engine import GDIEngine
        # This is harder to test without a display, but we can check if it calls windll
        with patch('ctypes.windll.user32.InvalidateRect') as mock_invalidate:
             # Force Refresh
             GDIEngine.force_refresh_screen()
             # Should be called once
             if GDIEngine.HAS_WIN32:
                 mock_invalidate.assert_called_once()
