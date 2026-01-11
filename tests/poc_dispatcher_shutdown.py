import threading
import queue
import time
import unittest
from unittest.mock import MagicMock, patch
import sys

# Completely mock PyQt6 and other dependencies first
sys.modules['PyQt6'] = MagicMock()
sys.modules['PyQt6.QtCore'] = MagicMock()
sys.modules['PyQt6.QtWidgets'] = MagicMock()
sys.modules['config'] = MagicMock()
sys.modules['core.process_guard'] = MagicMock()
sys.modules['hardware.audio_out'] = MagicMock()
sys.modules['visual.fake_ui'] = MagicMock()
sys.modules['core.dispatchers.visual_dispatcher'] = MagicMock()
sys.modules['core.dispatchers.hardware_dispatcher'] = MagicMock()
sys.modules['core.dispatchers.horror_dispatcher'] = MagicMock()
sys.modules['core.dispatchers.system_dispatcher'] = MagicMock()
sys.modules['core.exceptions'] = MagicMock()
sys.modules['core.validators'] = MagicMock()
sys.modules['core.logger'] = MagicMock()

# Since FunctionDispatcher inherits from QObject, we need to mock that base correctly
# But imports happen at file level.
# We'll use a trick: redefine QObject in the mocked module to be object
sys.modules['PyQt6.QtCore'].QObject = object
sys.modules['PyQt6.QtCore'].pyqtSignal = lambda *args: MagicMock()

# Now import
from core.function_dispatcher import FunctionDispatcher

class TestDispatcherShutdown(unittest.TestCase):
    def setUp(self):
        # Initialize directly
        self.dispatcher = FunctionDispatcher()
        # Ensure queue is real
        self.dispatcher._action_queue = queue.PriorityQueue()
        # Ensure workers list is empty to avoid real threads from init
        self.dispatcher._workers = []

    def test_shutdown_latency(self):
        """
        Test if stop_dispatching returns reasonably quickly and threads exit.
        """
        print("\nStarting Shutdown Latency Test...")
        start_time = time.time()

        # Simulate running state
        self.dispatcher._is_shutting_down = False

        # Trigger shutdown
        self.dispatcher.stop_dispatching()

        duration = time.time() - start_time
        print(f"Shutdown signal took: {duration:.4f}s")

        # Verify flag is set
        self.assertTrue(self.dispatcher._is_shutting_down)
        self.assertLess(duration, 0.1, "Signal setting should be instant")

    def test_worker_loop_exit(self):
        """
        Simulate a worker loop and ensure it exits on flag.
        """
        self.dispatcher._is_shutting_down = False

        # We need to bind the method to the instance for the thread
        worker_thread = threading.Thread(target=self.dispatcher._worker_loop, daemon=True)
        worker_thread.start()

        # Let it run for a bit
        time.sleep(0.1)

        # Signal shutdown
        self.dispatcher.stop_dispatching()

        # Join thread with timeout
        worker_thread.join(timeout=1.5)

        if worker_thread.is_alive():
            print("FAILURE: Worker thread did not exit within 1.5s (likely stuck on timeout)")
        else:
            print("SUCCESS: Worker thread exited correctly.")

        self.assertFalse(worker_thread.is_alive(), "Worker thread should have exited")

if __name__ == '__main__':
    unittest.main()
