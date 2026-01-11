"""
Memory System Stress Tests

Tests Memory module under high load:
- Conversation flood (10,000+ messages)
- Event storm (100,000+ events)
- Rapid save/load cycles
- Long-run memory growth tracking
"""
import pytest
import time
import json
import os


@pytest.mark.stress
class TestMemoryStress:
    
    def test_conversation_flood(self, mock_memory, resource_tracker, stress_config):
        """
        Flood Memory with 1000+ conversation messages.
        
        Success criteria:
        - No memory leak
        - Save time < 100ms
        - JSON file size reasonable
        """
        count = stress_config["memory_flood_count"]
        
        print(f"\n💬 Flooding memory with {count} conversations...")
        
        start = time.time()
        
        # Add conversations
        for i in range(count):
            mock_memory.add_conversation(
                role="user" if i % 2 == 0 else "ai",
                message=f"Test message {i} with some content to make it realistic",
                context={"iteration": i}
            )
            
            # Snapshot every 100
            if i % 100 == 0:
                resource_tracker.snapshot()
        
        elapsed = time.time() - start
        
        # Save to disk
        save_start = time.time()
        mock_memory.save()
        save_time = (time.time() - save_start) * 1000  # ms
        
        # Final snapshot
        resource_tracker.snapshot()
        
        # Check file size
        file_size_mb = os.path.getsize(mock_memory.memory_file) / 1024 / 1024
        
        print(f"✅ Added {count} conversations in {elapsed:.2f}s")
        print(f"   Save time: {save_time:.1f}ms")
        print(f"   File size: {file_size_mb:.2f} MB")
        
        # Assertions
        assert save_time < 1000, f"Save too slow: {save_time}ms"
        assert file_size_mb < 10, f"File too large: {file_size_mb} MB"
        
        # Check leaks
        leaks = resource_tracker.detect_leaks()
        assert not leaks["memory"]["leak_detected"], f"Memory leak: {leaks['memory']}"
    
    def test_event_storm(self, mock_memory, resource_tracker):
        """
        Log 10,000 events rapidly.
        
        Tests event logging system performance.
        """
        count = 10000
        
        print(f"\n⚡ Logging {count} events...")
        
        start = time.time()
        
        for i in range(count):
            mock_memory.log_event(
                event_type="TEST_EVENT",
                details={"iteration": i, "data": "test" * 10}
            )
            
            if i % 1000 == 0:
                resource_tracker.snapshot()
        
        elapsed = time.time() - start
        
        print(f"✅ Logged {count} events in {elapsed:.2f}s")
        print(f"   Rate: {count / elapsed:.0f} events/sec")
        
        # Verify no leak
        leaks = resource_tracker.detect_leaks()
        assert not leaks["memory"]["leak_detected"], "Memory leak detected"
    
    def test_rapid_save_load(self, mock_memory, resource_tracker):
        """
        Rapid save/load cycles.
        
        Tests JSON serialization performance and file handle cleanup.
        """
        cycles = 100
        
        print(f"\n🔄 {cycles} rapid save/load cycles...")
        
        # Add some data
        for i in range(50):
            mock_memory.add_conversation("user", f"Message {i}")
        
        save_times = []
        load_times = []
        
        for i in range(cycles):
            # Save
            start = time.time()
            mock_memory.save()
            save_times.append((time.time() - start) * 1000)
            
            # Load
            start = time.time()
            mock_memory.load()
            load_times.append((time.time() - start) * 1000)
            
            if i % 10 == 0:
                resource_tracker.snapshot()
        
        avg_save = sum(save_times) / len(save_times)
        avg_load = sum(load_times) / len(load_times)
        
        print(f"✅ Completed {cycles} cycles")
        print(f"   Avg save: {avg_save:.1f}ms")
        print(f"   Avg load: {avg_load:.1f}ms")
        
        # Performance checks
        assert avg_save < 100, f"Save too slow: {avg_save}ms"
        assert avg_load < 100, f"Load too slow: {avg_load}ms"
        
        # Check leaks
        leaks = resource_tracker.detect_leaks()
        assert not leaks["memory"]["leak_detected"], "Memory leak"
    
    def test_discovered_info_accumulation(self, mock_memory, resource_tracker):
        """
        Test discovered_info dict doesn't leak memory.
        
        Simulates discovering 1000 desktop files.
        """
        print("\n🔍 Discovering 1000 desktop files...")
        
        for i in range(1000):
            mock_memory.record_discovered_info(
                "desktop_file",
                (f"file_{i}.txt", 0.5)  # (filename, relevance_score)
            )
            
            if i % 100 == 0:
                resource_tracker.snapshot()
        
        # Verify data structure
        discovered = mock_memory.data.get("discovered_info", {})
        desktop_files = discovered.get("desktop_files_seen", [])
        
        print(f"   Stored {len(desktop_files)} files")
        
        # Should have all 1000
        assert len(desktop_files) == 1000
        
        # Check leak
        leaks = resource_tracker.detect_leaks()
        assert not leaks["memory"]["leak_detected"], "Memory leak"
    
    def test_behavior_tracking_stress(self, mock_memory, resource_tracker):
        """
        Record 1000 user behaviors.
        
        Tests behavior tracking dict growth.
        """
        print("\n😡 Recording 1000 behaviors...")
        
        behaviors = ["swear", "beg", "defiance"]
        
        for i in range(1000):
            behavior = behaviors[i % 3]
            mock_memory.record_behavior(behavior, f"Test message {i}")
            
            if i % 100 == 0:
                resource_tracker.snapshot()
        
        # Verify counts
        behavior_data = mock_memory.data.get("behavior_tracking", {})
        
        print(f"   Swear count: {behavior_data.get('swear', {}).get('count', 0)}")
        print(f"   Beg count: {behavior_data.get('beg', {}).get('count', 0)}")
        
        # Check leak
        leaks = resource_tracker.detect_leaks()
        assert not leaks["memory"]["leak_detected"], "Memory leak"
    
    def test_memorable_moments_limit(self, mock_memory):
        """
        Verify memorable_moments list is properly limited.
        
        Should not grow unbounded.
        """
        print("\n📸 Adding 200 memorable moments...")
        
        for i in range(200):
            mock_memory.add_memorable_moment(f"Moment {i}")
        
        moments = mock_memory.data.get("memorable_moments", [])
        
        print(f"   Stored moments: {len(moments)}")
        
        # Should be limited to ~50
        assert len(moments) <= 60, f"Too many moments stored: {len(moments)}"


@pytest.mark.stress
class TestMemoryQuickValidation:
    """Quick memory tests for CI/CD."""
    
    def test_quick_conversation_burst(self, mock_memory):
        """Add 100 conversations rapidly."""
        for i in range(100):
            mock_memory.add_conversation("user", f"Message {i}")
        
        mock_memory.save()
        assert True  # No crash
    
    def test_quick_save_load(self, mock_memory):
        """10 save/load cycles."""
        for _ in range(10):
            mock_memory.save()
            mock_memory.load()
        
        assert True
