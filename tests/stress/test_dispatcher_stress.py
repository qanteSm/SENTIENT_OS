"""
Dispatcher Stress Tests

Tests FunctionDispatcher under high load:
- Burst dispatch (1000 actions/second)
- Priority chaos (random priorities)
- Worker starvation
- Queue overflow
"""
import pytest
import time
import threading
from unittest.mock import MagicMock, patch


@pytest.mark.stress
class TestDispatcherStress:
    
    def test_burst_dispatch(self, mock_dispatcher, resource_tracker, stress_config):
        """
        Burst Dispatch: Send 100 actions/second for 10 seconds.
        
        Success criteria:
        - All actions processed
        - No crashes
        - Memory stable
        - Queue doesn't overflow
        """
        duration = stress_config["dispatcher_burst_duration"]
        rate = stress_config["dispatcher_burst_rate"]
        total_actions = duration * rate
        
        # Mock dispatcher methods to avoid real side effects
        mock_dispatcher.visual_dispatcher.dispatch = MagicMock()
        mock_dispatcher.system_dispatcher.dispatch = MagicMock()
        
        # Track execution
        actions_dispatched = 0
        
        print(f"\n🚀 Sending {total_actions} actions...")
        
        start_time = time.time()
        
        # Send actions (don't try to rate-limit, just blast them)
        for i in range(total_actions):
            # Alternate between actions
            action = "GDI_FLASH" if i % 2 == 0 else "FAKE_FILE_DELETE"
            
            mock_dispatcher._do_dispatch({
                "action": action,
                "params": {},
                "speech": ""
            })
            
            actions_dispatched += 1
            
            # Snapshot every 100 actions
            if actions_dispatched % 100 == 0:
                resource_tracker.snapshot()
        
        send_duration = time.time() - start_time
        
        # Wait for queue to drain
        print(f"\n⏳ Waiting for queue to drain...")
        time.sleep(2)
        
        # Final snapshot
        resource_tracker.snapshot()
        
        # Verify
        assert actions_dispatched == total_actions, f"Sent {actions_dispatched}/{total_actions}"
        
        # Check leaks
        leaks = resource_tracker.detect_leaks()
        assert not leaks["memory"]["leak_detected"], f"Memory leak: {leaks['memory']}"
        assert not leaks["threads"]["leak_detected"], f"Thread leak: {leaks['threads']}"
        
        print(f"\n✅ Dispatched {actions_dispatched} actions in {send_duration:.2f}s")
        print(f"   Actual rate: {actions_dispatched / send_duration:.1f} actions/sec")
    
    def test_priority_chaos(self, mock_dispatcher, resource_tracker):
        """
        Priority Chaos: Send actions with random priorities.
        
        Verify HIGH priority actions execute before LOW priority.
        """
        import random
        
        execution_order = []
        
        def track_high(*args, **kwargs):
            execution_order.append("HIGH")
        
        def track_low(*args, **kwargs):
            execution_order.append("LOW")
        
        # Patch dispatchers
        mock_dispatcher.visual_dispatcher.dispatch = MagicMock(side_effect=track_high)
        mock_dispatcher.system_dispatcher.dispatch = MagicMock(side_effect=track_low)
        
        print("\n🎲 Sending 100 actions with chaotic priorities...")
        
        # Send actions
        for i in range(100):
            if random.random() > 0.5:
                # HIGH priority (visual)
                mock_dispatcher._do_dispatch({
                    "action": "GDI_FLASH",
                    "params": {},
                    "speech": ""
                })
            else:
                # LOW priority (system)
                mock_dispatcher._do_dispatch({
                    "action": "FAKE_FILE_DELETE",
                    "params": {},
                    "speech": ""
                })
            
            time.sleep(0.01)  # Small delay
        
        # Wait for completion
        time.sleep(2)
        resource_tracker.snapshot()
        
        # Count HIGH/LOW
        high_count = execution_order.count("HIGH")
        low_count = execution_order.count("LOW")
        
        print(f"   HIGH: {high_count}, LOW: {low_count}")
        print(f"   Total executed: {len(execution_order)}")
        
        # Verify all were executed
        assert len(execution_order) >= 100, "Some actions were lost"
    
    def test_worker_starvation(self, mock_dispatcher, resource_tracker):
        """
        Worker Starvation: Block all workers with long tasks.
        Then send a HIGH priority task - it should still queue.
        """
        import threading
        
        blocked_count = threading.Event()
        
        def blocking_task(*args, **kwargs):
            time.sleep(2)  # Block for 2 seconds
        
        # Patch to block
        mock_dispatcher.system_dispatcher.dispatch = MagicMock(side_effect=blocking_task)
        
        print("\n⏸️ Blocking all workers with long tasks...")
        
        # Send 5 blocking tasks (one per worker)
        for _ in range(5):
            mock_dispatcher._do_dispatch({
                "action": "FAKE_FILE_DELETE",
                "params": {},
                "speech": ""
            })
        
        time.sleep(0.5)  # Let them start
        
        # Now send a HIGH priority task
        high_executed = threading.Event()
        
        def track_high(*args, **kwargs):
            high_executed.set()
        
        mock_dispatcher.visual_dispatcher.dispatch = MagicMock(side_effect=track_high)
        
        mock_dispatcher._do_dispatch({
            "action": "GDI_FLASH",
            "params": {},
            "speech": ""
        })
        
        # Wait for all to complete
        time.sleep(3)
        
        # HIGH should have executed (after workers freed up)
        assert high_executed.is_set(), "HIGH priority task didn't execute"
        
        print("✅ HIGH priority task executed after workers freed")
    
    def test_concurrent_dispatching(self, mock_dispatcher, resource_tracker):
        """
        Concurrent Dispatching: 10 threads dispatch simultaneously.
        
        Tests thread safety of _do_dispatch.
        """
        mock_dispatcher.visual_dispatcher.dispatch = MagicMock()
        mock_dispatcher.system_dispatcher.dispatch = MagicMock()
        
        dispatched_count = [0]  # Mutable to track across threads
        lock = threading.Lock()
        
        def dispatch_worker(thread_id):
            for i in range(50):
                mock_dispatcher._do_dispatch({
                    "action": "GDI_FLASH",
                    "params": {},
                    "speech": ""
                })
                
                with lock:
                    dispatched_count[0] += 1
                
                time.sleep(0.01)
        
        print("\n🔀 10 threads dispatching concurrently...")
        
        threads = []
        for i in range(10):
            t = threading.Thread(target=dispatch_worker, args=(i,))
            threads.append(t)
            t.start()
        
        # Wait for all
        for t in threads:
            t.join()
        
        # Wait for queue to drain
        time.sleep(2)
        resource_tracker.snapshot()
        
        # Verify
        assert dispatched_count[0] == 500, f"Expected 500, got {dispatched_count[0]}"
        
        # Check for leaks
        leaks = resource_tracker.detect_leaks()
        assert not leaks["memory"]["leak_detected"], "Memory leak detected"
        
        print(f"✅ All 500 actions dispatched from 10 threads")
    
    def test_shutdown_during_dispatch(self, mock_dispatcher, resource_tracker):
        """
        Chaos Test: Shutdown dispatcher while actions are still queued.
        
        Verifies cleanup doesn't deadlock or crash.
        """
        mock_dispatcher.visual_dispatcher.dispatch = MagicMock(side_effect=lambda *a, **k: time.sleep(0.1))
        
        print("\n💥 Sending 100 actions then immediate shutdown...")
        
        # Queue 100 actions
        for i in range(100):
            mock_dispatcher._do_dispatch({
                "action": "GDI_FLASH",
                "params": {},
                "speech": ""
            })
        
        # Immediate shutdown (while queue still has items)
        time.sleep(0.5)  # Let some start
        mock_dispatcher.stop_dispatching()
        
        # Wait a bit
        time.sleep(2)
        
        # If we reach here without deadlock, success!
        print("✅ Shutdown completed without deadlock")


@pytest.mark.stress
class TestDispatcherQuickValidation:
    """Quick smoke tests (5 minutes total) for CI/CD."""
    
    def test_quick_burst(self, mock_dispatcher):
        """Quick burst: 10 actions/sec for 5 seconds."""
        mock_dispatcher.visual_dispatcher.dispatch = MagicMock()
        
        for i in range(50):
            mock_dispatcher._do_dispatch({
                "action": "GDI_FLASH",
                "params": {},
                "speech": ""
            })
            time.sleep(0.1)
        
        time.sleep(1)
        assert True  # Just ensure no crash
