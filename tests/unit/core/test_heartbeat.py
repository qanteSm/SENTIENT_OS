import pytest
import time
from unittest.mock import MagicMock, patch
from core.heartbeat import Heartbeat

class TestHeartbeat:
    @pytest.fixture
    def heartbeat(self):
        mock_anger = MagicMock()
        mock_brain = MagicMock()
        mock_dispatcher = MagicMock()
        return Heartbeat(mock_anger, mock_brain, mock_dispatcher)
        
    def test_calculate_sleep_time_idle(self, heartbeat):
        # High idle time should result in slower pulses
        heartbeat.last_activity = time.time() - 300 
        heartbeat.anger_engine.get_chaos_multiplier.return_value = 1.0
        
        sleep_time = heartbeat._calculate_sleep_time()
        # random.gauss might vary, but base is 6.0 for idle > 120
        assert sleep_time > 1.0 
        
    def test_calculate_sleep_time_active(self, heartbeat):
        # Recent activity should result in faster pulses
        heartbeat.last_activity = time.time() - 1 
        heartbeat.anger_engine.get_chaos_multiplier.return_value = 1.0
        
        sleep_time = heartbeat._calculate_sleep_time()
        # base_sleep = 15.0 / 1.5 = 10.0
        assert sleep_time < 15.0
        
    def test_persona_shift_logic(self, heartbeat):
        # High anger shift
        heartbeat.anger_engine.current_anger = 80
        heartbeat.brain.current_persona = "SUPPORT"
        
        heartbeat._check_persona_shift()
        heartbeat.brain.switch_persona.assert_called_with("ENTITY")
        
    def test_handle_ai_response(self, heartbeat):
        # Test signal emission on AI response
        mock_slot = MagicMock()
        heartbeat.pulse_signal.connect(mock_slot)
        
        response = {"action": "GLITCH_SCREEN", "speech": "I see you."}
        heartbeat._handle_ai_response(response)
        
        mock_slot.assert_called_with("GLITCH_SCREEN")
        heartbeat.dispatcher.audio_out.play_tts.assert_called_with("I see you.")
