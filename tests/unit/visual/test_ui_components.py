# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import pytest
from unittest.mock import MagicMock, patch
from visual.fake_chat import FakeChat
from visual.overlay_manager import OverlayManager


class TestUIComponents:
    @pytest.fixture
    def app(self):
        from PyQt6.QtWidgets import QApplication
        import sys
        return QApplication.instance() or QApplication(sys.argv)

    def test_fake_chat_moods(self, app):
        chat = FakeChat()
        chat.set_mood("ANGRY")
        assert chat._current_mood == "ANGRY"
        # Check if stylesheet was updated (contains red color)
        assert "#FF0000" in chat.input_field.styleSheet()

    def test_fake_chat_submission(self, app):
        chat = FakeChat()
        mock_slot = MagicMock()
        chat.message_sent.connect(mock_slot)
        
        chat.input_field.setText("hello world")
        chat.on_submit()
        
        mock_slot.assert_called_with("hello world")
        assert chat.input_field.text() == ""

    def test_overlay_text_display(self, app):
        overlay = OverlayManager()
        overlay.show_text("SPOOKY", duration=100)
        # Should set text to its internal label
        assert overlay.label.text() == "SPOOKY"
        overlay.clear_overlays()
        assert overlay.label.isVisible() is False
