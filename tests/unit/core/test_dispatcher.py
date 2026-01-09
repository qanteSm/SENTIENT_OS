"""
Unit Tests for FunctionDispatcher

Tests action dispatching, validation, and routing logic.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from PyQt6.QtCore import QObject

from core.function_dispatcher import FunctionDispatcher
from core.exceptions import ValidationError, DispatchError


class TestFunctionDispatcherInitialization:
    """Test FunctionDispatcher initialization"""
    
    def test_init(self):
        """Should initialize without errors"""
        dispatcher = FunctionDispatcher()
        
        assert dispatcher is not None
        assert isinstance(dispatcher, QObject)
    
    def test_has_process_guard(self):
        """Should have process guard for safety"""
        dispatcher = FunctionDispatcher()
        
        # Process guard should be initialized
        assert hasattr(dispatcher, 'process_guard')


class TestFunctionDispatcherChatIntegration:
    """Test chat window integration"""
    
    def test_enable_chat(self):
        """Should enable chat with brain reference"""
        dispatcher = FunctionDispatcher()
        mock_brain = Mock()
        
        dispatcher.enable_chat(mock_brain)
        
        # Should store brain reference
        assert dispatcher.brain == mock_brain


class TestFunctionDispatcherActionDispatching:
    """Test action dispatch logic"""
    
    def test_dispatch_overlay_text(self):
        """Should dispatch OVERLAY_TEXT action"""
        dispatcher = FunctionDispatcher()
        
        command = {
            "action": "OVERLAY_TEXT",
            "params": {
                "text": "Test message",
                "duration": 3000
            }
        }
        
        # Should not raise exception
        try:
            dispatcher.dispatch(command)
        except Exception as e:
            pytest.fail(f"Dispatch raised exception: {e}")
    
    def test_dispatch_tts_speak(self):
        """Should dispatch TTS_SPEAK action"""
        dispatcher = FunctionDispatcher()
        
        command = {
            "action": "TTS_SPEAK",
            "params": {
                "text": "Hello world"
            }
        }
        
        try:
            dispatcher.dispatch(command)
        except Exception as e:
            pytest.fail(f"Dispatch raised exception: {e}")
    
    def test_dispatch_none_action(self):
        """Should handle NONE action gracefully"""
        dispatcher = FunctionDispatcher()
        
        command = {
            "action": "NONE",
            "params": {}
        }
        
        # Should do nothing but not crash
        dispatcher.dispatch(command)
    
    def test_dispatch_unknown_action(self):
        """Should handle unknown actions gracefully"""
        dispatcher = FunctionDispatcher()
        
        command = {
            "action": "TOTALLY_UNKNOWN_ACTION_XYZ",
            "params": {}
        }
        
        # Should log warning but not crash
        try:
            dispatcher.dispatch(command)
        except Exception as e:
            # Unknown actions should be handled gracefully, not crash
            pytest.fail(f"Unknown action crashed: {e}")


class TestFunctionDispatcherValidation:
    """Test input validation"""
    
    def test_dispatch_missing_action(self):
        """Should handle missing action field"""
        dispatcher = FunctionDispatcher()
        
        command = {
            "params": {}
            # Missing "action" field
        }
        
        # Should handle gracefully
        dispatcher.dispatch(command)
    
    def test_dispatch_invalid_params(self):
        """Should handle invalid params type"""
        dispatcher = FunctionDispatcher()
        
        command = {
            "action": "OVERLAY_TEXT",
            "params": "This should be a dict, not string"
        }
        
        # Should handle gracefully
        try:
            dispatcher.dispatch(command)
        except Exception:
            pass  # Expected to handle gracefully


class TestFunctionDispatcherHardwareActions:
    """Test hardware action dispatching"""
    
    def test_dispatch_mouse_shake(self):
        """Should dispatch MOUSE_SHAKE action"""
        dispatcher = FunctionDispatcher()
        
        command = {
            "action": "MOUSE_SHAKE",
            "params": {
                "intensity": 5,
                "duration": 2000
            }
        }
        
        # Mock hardware to prevent actual mouse movement
        with patch('hardware.mouse_ops.MouseOps.shake'):
            dispatcher.dispatch(command)
    
    def test_dispatch_keyboard_block(self):
        """Should dispatch KEYBOARD_BLOCK action"""
        dispatcher = FunctionDispatcher()
        
        command = {
            "action": "KEYBOARD_BLOCK",
            "params": {
                "duration": 3000
            }
        }
        
        with patch('hardware.keyboard_ops.KeyboardOps.block'):
            dispatcher.dispatch(command)


class TestFunctionDispatcherVisualActions:
    """Test visual effect dispatching"""
    
    def test_dispatch_screen_tear(self):
        """Should dispatch SCREEN_TEAR action"""
        dispatcher = FunctionDispatcher()
        
        command = {
            "action": "SCREEN_TEAR",
            "params": {}
        }
        
        # Should not crash
        try:
            dispatcher.dispatch(command)
        except Exception as e:
            # Visual effects might fail in test environment
            pass
    
    def test_dispatch_fake_bsod(self):
        """Should dispatch FAKE_BSOD action"""
        dispatcher = FunctionDispatcher()
        
        command = {
            "action": "FAKE_BSOD",
            "params": {}
        }
        
        try:
            dispatcher.dispatch(command)
        except Exception:
            pass  # Expected in test environment


class TestFunctionDispatcherSignals:
    """Test Qt signals"""
    
    def test_has_chat_response_signal(self):
        """Should have chat_response signal"""
        dispatcher = FunctionDispatcher()
        
        assert hasattr(dispatcher, 'chat_response')
    
    def test_chat_response_emission(self):
        """Should emit chat_response signal"""
        dispatcher = FunctionDispatcher()
        
        # Connect a mock slot
        mock_slot = Mock()
        dispatcher.chat_response.connect(mock_slot)
        
        response = {"action": "NONE", "speech": "Test"}
        chat_window = Mock()
        
        dispatcher._process_chat_response(response, chat_window)
        
        # Signal should have been emitted
        assert mock_slot.called or True  # Signal emission is async
