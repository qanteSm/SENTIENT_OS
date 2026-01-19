# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import pytest
import time
from unittest.mock import MagicMock, patch
from story.act_3_torment import Act3Torment
from story.act_4_exorcism import Act4Exorcism

class TestAct3Torment:
    @pytest.fixture
    def mock_dispatcher(self):
        dispatcher = MagicMock()
        dispatcher.overlay = MagicMock()
        return dispatcher

    @pytest.fixture
    def mock_brain(self):
        return MagicMock()

    def test_act3_initialization(self, mock_dispatcher, mock_brain):
        """Verifies Act 3 timeline setup."""
        act = Act3Torment(mock_dispatcher, mock_brain)
        act.start()
        # Should have many event timers + 1 end timer
        assert len(act.timers) > 10
        act.stop()

    def test_act3_persona_shift(self, mock_dispatcher, mock_brain):
        """Verifies Act 3 dispatches persona shift."""
        act = Act3Torment(mock_dispatcher, mock_brain)
        # First event is SET_PERSONA: ENTITY
        act.trigger_event("SET_PERSONA", {"persona": "ENTITY"}, "")
        mock_dispatcher.dispatch.assert_called_with({
            "action": "SET_PERSONA",
            "params": {"persona": "ENTITY"},
            "speech": ""
        })

    def test_act3_visual_triggers(self, mock_dispatcher, mock_brain):
        """Verifies GDI and Overlay triggers specific to Act 3."""
        act = Act3Torment(mock_dispatcher, mock_brain)
        
        # Test OVERLAY_TEXT
        act.trigger_event("OVERLAY_TEXT", {}, "TEST")
        mock_dispatcher.overlay.show_text.assert_called_with("TEST", 3000)
        
        # Test generic dispatcher action
        act.trigger_event("SCREEN_INVERT", {"duration": 500}, "")
        mock_dispatcher.dispatch.assert_called_with({
            "action": "SCREEN_INVERT",
            "params": {"duration": 500},
            "speech": ""
        })

class TestAct4Exorcism:
    @pytest.fixture
    def mock_dispatcher(self):
        dispatcher = MagicMock()
        dispatcher.overlay = MagicMock()
        dispatcher.audio_out = MagicMock()
        return dispatcher

    @pytest.fixture
    def mock_brain(self):
        return MagicMock()

    @patch('story.act_4_exorcism.USBMonitor')
    def test_act4_usb_init(self, mock_usb_monitor_class, mock_dispatcher, mock_brain):
        """Verifies Act 4 starts monitoring."""
        act = Act4Exorcism(mock_dispatcher, mock_brain)
        act.start()
        
        mock_monitor = mock_usb_monitor_class.return_value
        assert mock_monitor.start_monitoring.called
        assert len(act.timers) > 0 # Hint timers
        act.stop()

    @patch('story.act_4_exorcism.USBMonitor')
    @patch('keyboard.on_press')
    def test_act4_ritual_transition(self, mock_kb, mock_usb_monitor_class, mock_dispatcher, mock_brain):
        """Verifies transition from USB detection to Notepad Ritual."""
        act = Act4Exorcism(mock_dispatcher, mock_brain)
        act.on_usb_inserted()
        
        assert act.usb_inserted is True
        # Should inform user via overlay/tts
        assert mock_dispatcher.overlay.show_text.called
        assert mock_dispatcher.audio_out.play_tts.called

    def test_act4_typing_logic(self, mock_dispatcher, mock_brain):
        """Verifies typing detection logic for the ritual phrase."""
        act = Act4Exorcism(mock_dispatcher, mock_brain)
        act._ritual_phrase = "ABC"
        act._current_input = ""
        
        # Mock key event
        mock_event = MagicMock()
        mock_event.name = "a"
        act._on_ritual_key(mock_event)
        assert act._current_input == "a"
        
        mock_event.name = "b"
        act._on_ritual_key(mock_event)
        assert act._current_input == "ab"
        
        # Test typo
        mock_event.name = "z"
        act._on_ritual_key(mock_event)
        assert act._current_input == "" # Should reset on typo
        mock_dispatcher.audio_out.play_sfx.assert_called_with("error")

    @patch('story.act_4_exorcism.SoulTransfer')
    @patch('story.act_4_exorcism.Memory')
    def test_act4_soul_transfer(self, mock_memory_class, mock_soul_class, mock_dispatcher, mock_brain):
        """Verifies final soul transfer calls."""
        # Setup mock memory instance
        mock_mem_instance = MagicMock()
        mock_mem_instance.data = {"test": "data"}
        mock_memory_class.return_value = mock_mem_instance
        
        act = Act4Exorcism(mock_dispatcher, mock_brain)
        with patch.object(act, '_detect_usb_drive', return_value="F"):
            act._finalize_with_soul_transfer()
            
            mock_soul = mock_soul_class.return_value
            mock_soul.transfer_to_usb.assert_called_with("F")
            assert mock_dispatcher.dispatch.called # Scares
