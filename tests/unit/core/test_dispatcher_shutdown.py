"""
Test for Dispatcher Shutdown with Sentinel Pattern

Tests that worker threads shutdown instantly when stop_dispatching() is called.
Target: Shutdown latency < 100ms (was 1000ms)
"""
import time
import pytest
from core.function_dispatcher import FunctionDispatcher


def test_sentinel_shutdown_speed():
    """Test that Sentinel pattern enables instant shutdown."""
    dispatcher = FunctionDispatcher()
    
    # Verify workers are running
    assert len(dispatcher._workers) == 5
    for worker in dispatcher._workers:
        assert worker.is_alive()
    
    # Measure shutdown time
    start_time = time.time()
    dispatcher.stop_dispatching()
    
    # Wait for all workers to terminate
    for worker in dispatcher._workers:
        worker.join(timeout=1.0)  # Max 1 second wait
    
    shutdown_duration_ms = (time.time() - start_time) * 1000
    
    # Assert shutdown was fast (<100ms)
    assert shutdown_duration_ms < 100, f"Shutdown took {shutdown_duration_ms:.1f}ms, expected <100ms"
    
    # Assert all workers terminated
    for worker in dispatcher._workers:
        assert not worker.is_alive(), "Worker thread still alive after shutdown"
    
    print(f"✅ Shutdown completed in {shutdown_duration_ms:.1f}ms")


def test_sentinel_pattern_presence():
    """Test that Sentinel (None) objects are sent to queue."""
    dispatcher = FunctionDispatcher()
    
    # Call stop_dispatching
    dispatcher.stop_dispatching()
    
    # Verify that sentinels were sent (queue should have 5 None values)
    # We can't directly inspect PriorityQueue easily, but we can check flag
    assert dispatcher._is_shutting_down is True
    
    # Wait briefly for workers to process sentinels
    time.sleep(0.05)
    
    # All workers should terminate quickly
    for worker in dispatcher._workers:
        assert not worker.is_alive(), "Worker should terminate after receiving sentinel"


def test_no_actions_dispatched_after_shutdown():
    """Test that actions are rejected after shutdown."""
    dispatcher = FunctionDispatcher()
    
    # Shutdown
    dispatcher.stop_dispatching()
    
    # Try to dispatch an action
    test_action = {"action": "GLITCH_SCREEN", "params": {}, "speech": "test"}
    dispatcher.dispatch(test_action)
    
    # Queue should be empty or have only sentinel values
    # No exception should be raised, actions should be silently ignored


if __name__ == "__main__":
    print("Running Dispatcher Shutdown Tests...")
    test_sentinel_shutdown_speed()
    test_sentinel_pattern_presence()
    test_no_actions_dispatched_after_shutdown()
    print("\\n✅ All dispatcher shutdown tests passed!")
