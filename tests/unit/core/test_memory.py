"""
Unit Tests for Memory Module

Tests memory storage, conversation history, and behavior tracking.
Uses actual Memory API (data dictionary, not set/get).
"""
import pytest
from unittest.mock import Mock, patch
import os
import json

from core.memory import Memory


class TestMemoryInitialization:
    """Test Memory initialization"""
    
    def test_init(self):
        """Should initialize with data dictionary"""
        memory = Memory()
        
        assert memory is not None
        assert hasattr(memory, 'data')
        assert isinstance(memory.data, dict)
        assert "user_profile" in memory.data
        assert "game_state" in memory.data
    
    def test_singleton_pattern(self):
        """Should implement singleton pattern"""
        memory1 = Memory()
        memory2 = Memory()
        
        # Should be same instance
        assert memory1 is memory2


class TestMemoryConversationHistory:
    """Test conversation history tracking"""
    
    def test_add_conversation(self):
        """Should track conversation history"""
        memory = Memory()
        
        initial_count = len(memory.data["conversation_history"])
        
        memory.add_conversation("user", "Hello")
        memory.add_conversation("ai", "Hi there")
        
        assert len(memory.data["conversation_history"]) == initial_count + 2
        
        last_conv = memory.data["conversation_history"][-1]
        assert last_conv["role"] == "ai"
        assert last_conv["content"] == "Hi there"
    
    def test_conversation_for_gemini(self):
        """Should format conversation for Gemini API"""
        memory = Memory()
        
        memory.add_conversation("user", "Merhaba")
        memory.add_conversation("ai", "Selam")
        
        formatted = memory.get_conversation_for_gemini(last_n=2)
        
        assert isinstance(formatted, str)
        assert "KULLANICI" in formatted or "user" in formatted.lower()


class TestMemoryBehaviorTracking:
    """Test behavior tracking"""
    
    def test_record_behavior_swear(self):
        """Should track swear count"""
        memory = Memory()
        
        initial_count = memory.data["user_profile"]["behavior_stats"]["swear_count"]
        
        memory.record_behavior("swear", "test swear")
        
        assert memory.data["user_profile"]["behavior_stats"]["swear_count"] == initial_count + 1
    
    def test_record_behavior_beg(self):
        """Should track beg count"""
        memory = Memory()
        
        initial_count = memory.data["user_profile"]["behavior_stats"]["begged_count"]
        
        memory.record_behavior("beg", "please stop")
        
        assert memory.data["user_profile"]["behavior_stats"]["begged_count"] == initial_count + 1
    
    def test_add_memorable_moment(self):
        """Should store memorable moments"""
        memory = Memory()
        
        moment = "User tried Alt+F4"
        memory.add_memorable_moment(moment)
        
        moments = memory.data["user_profile"]["memorable_moments"]
        assert len(moments) > 0
        assert moments[-1]["description"] == moment


class TestMemoryEventLogging:
    """Test event logging system"""
    
    def test_log_event(self):
        """Should log events"""
        memory = Memory()
        
        initial_count = len(memory.data["event_log"])
        
        memory.log_event("TEST_EVENT", {"data": "test"})
        
        assert len(memory.data["event_log"]) == initial_count + 1
        
        last_event = memory.data["event_log"][-1]
        assert last_event["type"] == "TEST_EVENT"
        assert last_event["data"]["data"] == "test"


class TestMemoryDiscoveredInfo:
    """Test discovered information tracking"""
    
    def test_record_desktop_file(self):
        """Should track discovered desktop files"""
        memory = Memory()
        
        memory.record_discovered_info("desktop_file", ("test.txt", 10))
        
        files = memory.data["discovered_info"]["desktop_files_seen"]
        # Now it's a list of dicts or strings (robust)
        # Check if any entry has the name
        def match(f):
            if isinstance(f, dict):
                return f.get("name") == "test.txt"
            return str(f) == "test.txt"
            
        assert any(match(f) for f in files)
    
    def test_record_hostname(self):
        """Should track hostname"""
        memory = Memory()
        
        memory.record_discovered_info("hostname", "TEST-PC")
        
        assert memory.data["discovered_info"]["hostname"] == "TEST-PC"


class TestMemoryGameState:
    """Test game state management"""
    
    def test_get_chaos_level(self):
        """Should get chaos level"""
        memory = Memory()
        
        chaos = memory.get_chaos_level()
        
        assert isinstance(chaos, (int, float))
        assert chaos >= 0
    
    def test_set_chaos_level(self):
        """Should set chaos level"""
        memory = Memory()
        
        memory.set_chaos_level(50)
        
        assert memory.data["game_state"]["chaos_level"] == 50
    
    def test_get_act(self):
        """Should get current act"""
        memory = Memory()
        
        act = memory.get_act()
        
        assert isinstance(act, int)
        assert act >= 1
    
    def test_set_act(self):
        """Should set current act"""
        memory = Memory()
        
        memory.set_act(2)
        
        assert memory.data["game_state"]["current_act"] == 2


class TestMemoryContext:
    """Test context generation for AI"""
    
    def test_get_full_context_for_ai(self):
        """Should generate full context string"""
        memory = Memory()
        
        # Add some data
        memory.record_behavior("swear", "test")
        memory.add_memorable_moment("Test moment")
        memory.add_conversation("user", "Test")
        
        context = memory.get_full_context_for_ai()
        
        assert isinstance(context, str)
        assert len(context) > 0


class TestMemoryPersistence:
    """Test save/load functionality"""
    
    def test_save_immediate(self):
        """Should save immediately"""
        memory = Memory()
        
        memory.data["game_state"]["chaos_level"] = 99
        
        # Should not raise exception
        try:
            memory.save_immediate()
        except Exception as e:
            pytest.fail(f"save_immediate raised exception: {e}")
    
    def test_load(self):
        """Should load from disk"""
        memory = Memory()
        
        # Should not raise exception
        try:
            memory.load()
        except Exception as e:
            pytest.fail(f"load raised exception: {e}")
