# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import pytest
from unittest.mock import MagicMock, patch
from hardware.camera_ops import CameraOps
from hardware.clipboard_ops import ClipboardOps
from hardware.notepad_ops import NotepadOps
from hardware.window_ops import WindowOps

class TestMoreHardware:
    @patch('hardware.camera_ops.Config')
    def test_camera_mock_behavior(self, mock_config):
        mock_config.return_value.IS_MOCK = True
        ops = CameraOps()
        assert ops.snap_frame() is None
        
    def test_camera_threat_dispatch(self):
        ops = CameraOps()
        mock_dispatcher = MagicMock()
        ops.set_dispatcher(mock_dispatcher)
        
        with patch('PyQt6.QtCore.QTimer.singleShot'):
            ops.fake_camera_threat()
            assert ops._has_shown_threat is True
            # Should have triggered notification if dispatcher has notification_ops
            assert mock_dispatcher.notifications.show_notification.called

    @patch('pyperclip.copy')
    def test_clipboard_poisoning(self, mock_copy):
        with patch('hardware.clipboard_ops.HAS_CLIPBOARD', True):
            ClipboardOps.poison_clipboard("TEST MESSAGE")
            mock_copy.assert_called_with("TEST MESSAGE")

    @patch('subprocess.Popen')
    def test_notepad_hijack_type(self, mock_popen):
        with patch('hardware.notepad_ops.Config') as mock_cfg:
            mock_cfg.return_value.IS_MOCK = False
            # Mock the missing library in sys.modules
            mock_app = MagicMock()
            with patch.dict('sys.modules', {'pywinauto': MagicMock(), 'pywinauto.application': mock_app}):
                with patch('hardware.notepad_ops.HAS_PYWINAUTO', True):
                    # We also need to mock the 'application' name in the notepad_ops namespace
                    with patch('hardware.notepad_ops.application', mock_app, create=True):
                        with patch('time.sleep'):
                            NotepadOps.hijack_and_type("test")
                            assert mock_popen.called

    @patch('hardware.window_ops.HAS_WIN32', True)
    @patch('win32gui.EnumWindows')
    def test_window_corruption_trigger(self, mock_enum,):
        WindowOps.corrupt_all_windows()
        assert mock_enum.called
