# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import pytest
from unittest.mock import patch, MagicMock
from core.context_observer import ContextObserver

class TestContextObserver:
    @patch('core.context_observer.os.getlogin', return_value="TestUser")
    def test_get_user_name(self, mock_login):
        assert ContextObserver.get_user_name() == "TestUser"
        
    @patch('core.context_observer.datetime.datetime')
    def test_time_logic(self, mock_datetime):
        # Mock Morning (8 AM)
        mock_datetime.now.return_value.hour = 8
        assert ContextObserver.get_time_of_day() == "Morning"
        assert ContextObserver.is_late_night() == False
        
        # Mock Late Night (2 AM)
        mock_datetime.now.return_value.hour = 2
        assert ContextObserver.is_late_night() == True
        
    @patch('core.context_observer.psutil.cpu_percent', return_value=45.5)
    def test_system_load(self, mock_psutil):
        assert "45.5%" in ContextObserver.get_system_load()
        
    @patch('core.context_observer.socket.gethostname', return_value="TEST-PC")
    @patch('core.context_observer.socket.gethostbyname', return_value="127.0.0.1")
    def test_network_info(self, mock_ip, mock_host):
        info = ContextObserver.get_network_info()
        assert info["hostname"] == "TEST-PC"
        assert info["local_ip"] == "127.0.0.1"
        
    @patch('core.context_observer.os.path.exists', return_value=True)
    @patch('core.context_observer.os.listdir', return_value=["file1.txt", "file2.jpg"])
    def test_get_desktop_files(self, mock_listdir, mock_exists):
        files = ContextObserver.get_desktop_files()
        assert "file1.txt" in files
        assert len(files) == 2
