
import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.memory import Memory

def reproduce_memory_crash():
    print("--- Starting Reproduction Script ---")
    
    # Mimic the fixture
    print("Setting up memory...")
    try:
        with patch('core.memory.Config') as mock_config:
            mock_config.return_value.LANGUAGE = "en"
            
            # 1. Initialize Memory
            print("Initializing Memory(:memory:)...")
            mem = Memory(filepath=":memory:") 
            
            # 2. Set Data
            print("Setting initial data...")
            mem.data = {
                "user_profile": {
                    "behavior_stats": {
                        "total_messages": 0,
                        "swear_count": 0,
                        "begged_count": 0,
                        "defiance_count": 0,
                        "escape_attempts": 0,
                        "silence_periods": 0
                    },
                    "memorable_moments": []
                },
                "game_state": {
                    "current_act": 1,
                    "session_start": 0,
                     # Missing chaos_level? No, test fixture didn't have it but code might expect it?
                     # In test_system_core.py, the fixture provides:
                     # "game_state": { "current_act": 1, "session_start": 0 }
                     # Let's check if set_act accesses chaos_level logging?
                },
                "event_log": []
            }
            
            # 3. Execute 'set_act'
            print("Calling set_act(3)...")
            mem.set_act(3)
            print("set_act(3) returned.")
            
            # 4. Verify
            print("Calling get_act()...")
            val = mem.get_act()
            print(f"get_act() returned {val}")
            
            assert val == 3
            print("Assertion passed.")
            
    except Exception as e:
        print(f"!!! EXCEPTION CAUGHT: {e}")
        import traceback
        traceback.print_exc()
        
    print("--- End of Script ---")

if __name__ == "__main__":
    reproduce_memory_crash()
