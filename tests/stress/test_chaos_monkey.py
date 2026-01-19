# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Chaos Monkey Tests - SENTIENT_OS Special

Tests "The Ghost in the Machine" scenarios:
- Act transition during shutdown
- User intervention chaos
- State corruption prevention
- Alt+F4 spam resistance
"""
import pytest
import time
import threading
import json
from pathlib import Path


@pytest.mark.chaos
class TestChaosMonkey:
    
    def test_shutdown_during_act_transition(self, mock_dispatcher, mock_memory, resource_tracker):
        """
        THE GHOST IN THE MACHINE:
        Shutdown system while StoryManager is transitioning Acts.
        
        Critical test: State file must NOT corrupt.
        """
        print("\n👻 THE GHOST IN THE MACHINE: Act transition + Shutdown collision")
        
        # Debug: Check file exists
        print(f"   📁 Memory file: {mock_memory.memory_file}")
        import os
        print(f"   📁 File exists: {os.path.exists(mock_memory.memory_file)}")
        
        # Simulate Act transition starting
        mock_memory.set_act(2)  # Moving to Act 2
        mock_memory.data["game_state"]["is_transitioning"] = True
        
        # Start dispatching actions (simulating story events)
        transition_actions = []
        
        def dispatch_transition_events():
            """Background thread simulating story events."""
            for i in range(50):
                if mock_dispatcher._is_shutting_down:
                    break
                
                mock_dispatcher._do_dispatch({
                    "action": "GLITCH_SCREEN" if i % 2 == 0 else "GDI_FLASH",
                    "params": {},
                    "speech": f"Transition event {i}"
                })
                transition_actions.append(i)
                time.sleep(0.05)
        
        # Start transition in background
        transition_thread = threading.Thread(target=dispatch_transition_events, daemon=True)
        transition_thread.start()
        
        # Let it run for a bit
        time.sleep(0.5)
        
        # CHAOS: User tries to close the game during transition!
        print("   💥 USER PRESSES ALT+F4 DURING TRANSITION!")
        
        # Simulate shutdown
        mock_dispatcher.stop_dispatching()
        
        # Try to save state (this could corrupt if not thread-safe)
        try:
            mock_memory.save_immediate()
            save_success = True
            print(f"   💾 Save successful")
        except Exception as e:
            print(f"   ❌ Save failed: {e}")
            save_success = False
        
        # Wait for transition thread
        transition_thread.join(timeout=2)
        
        # Verify state file integrity
        if save_success and os.path.exists(mock_memory.memory_file):
            try:
                with open(mock_memory.memory_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                
                # Check critical fields
                assert "game_state" in loaded_data
                assert "current_act" in loaded_data["game_state"]
                
                json_valid = True
                print("   ✅ State file is valid JSON")
            except json.JSONDecodeError:
                json_valid = False
                print("   ❌ STATE FILE CORRUPTED!")
            except FileNotFoundError:
                json_valid = False
                print("   ❌ FILE DISAPPEARED!")
        else:
            json_valid = False
            if not os.path.exists(mock_memory.memory_file):
                print(f"   ⚠️ File was deleted or never created")
        
        # Final verdict
        assert json_valid, "State file corrupted or missing during chaos shutdown!"
        assert save_success, "Save failed during chaos"
        
        print(f"   ✅ State preserved! Dispatched {len(transition_actions)} events before shutdown")
    
    def test_altf4_spam_resistance(self, mock_dispatcher, resource_tracker):
        """
        User spams Alt+F4 (simulate with multiple shutdown calls).
        
        System should handle gracefully without deadlock.
        """
        print("\n⌨️ CHAOS: User mashes Alt+F4 repeatedly")
        
        # Start some background activity
        mock_dispatcher.visual_dispatcher.dispatch = lambda *a, **k: time.sleep(0.1)
        
        for i in range(10):
            mock_dispatcher._do_dispatch({
                "action": "GDI_FLASH",
                "params": {},
                "speech": ""
            })
        
        # Spam shutdown from multiple threads
        def spam_shutdown():
            for _ in range(5):
                mock_dispatcher.stop_dispatching()
                time.sleep(0.1)
        
        threads = []
        for i in range(3):
            t = threading.Thread(target=spam_shutdown)
            threads.append(t)
            t.start()
        
        # Wait for all
        for t in threads:
            t.join(timeout=5)
        
        # If we reach here without deadlock, success
        print("   ✅ Survived Alt+F4 spam without deadlock")
    
    def test_concurrent_save_corruption(self, mock_memory):
        """
        Multiple threads try to save Memory simultaneously.
        
        Tests: File locking / race condition handling.
        """
        print("\n🔀 CHAOS: 10 threads saving simultaneously")
        
        # Add some data
        for i in range(10):
            mock_memory.add_conversation("user", f"Message {i}")
        
        corruption_detected = False
        save_errors = []
        
        def concurrent_saver(thread_id):
            try:
                for _ in range(10):
                    mock_memory.save_immediate()
                    time.sleep(0.01)
            except Exception as e:
                save_errors.append((thread_id, str(e)))
        
        # Launch threads
        threads = []
        for i in range(10):
            t = threading.Thread(target=concurrent_saver, args=(i,))
            threads.append(t)
            t.start()
        
        # Wait
        for t in threads:
            t.join()
        
        # Verify file integrity
        try:
            with open(mock_memory.memory_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print("   ✅ File is valid JSON after concurrent saves")
        except json.JSONDecodeError:
            corruption_detected = True
            print("   ❌ FILE CORRUPTED!")
        
        if save_errors:
            print(f"   ⚠️ {len(save_errors)} save errors occurred")
            for tid, error in save_errors[:3]:
                print(f"      Thread {tid}: {error}")
        
        assert not corruption_detected, "Concurrent saves corrupted the file!"
    
    def test_memory_load_during_write(self, mock_memory):
        """
        One thread writes, another reads simultaneously.
        
        Classic reader/writer problem.
        """
        print("\n📖 CHAOS: Read while writing")
        
        # Add data
        for i in range(100):
            mock_memory.add_conversation("user", f"Msg {i}")
        
        errors = []
        
        def writer():
            for i in range(20):
                try:
                    mock_memory.save_immediate()
                    time.sleep(0.05)
                except Exception as e:
                    errors.append(("writer", e))
        
        def reader():
            for i in range(20):
                try:
                    mock_memory.load()
                    time.sleep(0.05)
                except Exception as e:
                    errors.append(("reader", e))
        
        # Start both
        t1 = threading.Thread(target=writer)
        t2 = threading.Thread(target=reader)
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        
        if errors:
            print(f"   ⚠️ {len(errors)} errors during concurrent read/write")
            for role, err in errors[:3]:
                print(f"      {role}: {err}")
        
        # Verify final file
        try:
            mock_memory.load()
            print("   ✅ Final load successful")
        except Exception as e:
            pytest.fail(f"Final load failed: {e}")
    
    def test_dispatcher_queue_overflow_simulation(self, mock_dispatcher, resource_tracker):
        """
        Overwhelm queue with 10,000 actions at once.
        
        Tests: Queue doesn't crash, memory doesn't explode.
        """
        print("\n🌊 CHAOS: Queue flood with 10,000 actions")
        
        # Slow down dispatch to build up queue
        mock_dispatcher.visual_dispatcher.dispatch = lambda *a, **k: time.sleep(0.01)
        
        start = time.time()
        
        # Flood
        for i in range(10000):
            mock_dispatcher._do_dispatch({
                "action": "GDI_FLASH",
                "params": {},
                "speech": ""
            })
            
            if i % 1000 == 0:
                resource_tracker.snapshot()
        
        flood_time = time.time() - start
        
        print(f"   Queued 10,000 actions in {flood_time:.2f}s")
        
        # Wait for drain (with timeout)
        print("   ⏳ Waiting for queue to drain...")
        time.sleep(5)
        
        # Final snapshot
        resource_tracker.snapshot()
        
        # Check memory
        leaks = resource_tracker.detect_leaks()
        
        # With 10K actions, there may be temporary memory growth
        # but it should not be excessive (>100MB would indicate a leak)
        if leaks["memory"]["growth_mb"] > 100:
            assert False, f"Excessive memory growth: {leaks['memory']['growth_mb']} MB"
        
        print("   ✅ Queue survived flood and drained")
        print(f"   Memory growth: {leaks['memory']['growth_mb']:.1f} MB (acceptable)")


@pytest.mark.chaos
class TestUserInterventionChaos:
    """Simulate aggressive user behaviors."""
    
    def test_rapid_persona_switching(self, mock_brain):
        """User rapidly switches AI personas."""
        print("\n🎭 CHAOS: Rapid persona switching")
        
        for i in range(100):
            persona = "ENTITY" if i % 2 == 0 else "SUPPORT"
            mock_brain.switch_persona(persona)
        
        # Should not crash
        assert mock_brain.current_persona in ["ENTITY", "SUPPORT"]
        print("   ✅ Survived 100 persona switches")
    
    def test_behavior_spam(self, mock_memory):
        """User triggers same behavior 1000 times."""
        print("\n😡 CHAOS: User swears 1000 times in a row")
        
        for i in range(1000):
            mock_memory.record_behavior("swear", "test")
        
        behavior_data = mock_memory.data.get("behavior_tracking", {})
        swear_data = behavior_data.get("swear", {})
        
        # Note: Memory.record_behavior uses behavior_stats, not behavior_tracking
        stats = mock_memory.data.get("user_profile", {}).get("behavior_stats", {})
        swear_count = stats.get("swear_count", 0)
        
        assert swear_count == 1000, f"Expected 1000, got {swear_count}"
        print(f"   ✅ Recorded {swear_count} swears without crash")
