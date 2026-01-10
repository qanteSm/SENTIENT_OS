import pytest
import time
import threading
from unittest.mock import MagicMock, patch
from core.function_dispatcher import FunctionDispatcher

class TestFunctionDispatcher:
    
    @pytest.fixture
    def dispatcher(self):
        """Create a dispatcher with mocked sub-dispatchers and a single worker for priority testing."""
        from PyQt6.QtWidgets import QApplication
        import sys
        if not QApplication.instance():
            self._app = QApplication(sys.argv)

        # Patching init_worker_pool to not start default threads
        # Also patch UI/Audio to avoid Qt errors (and windows popping up)
        with patch.object(FunctionDispatcher, '_init_worker_pool') as mock_init, \
             patch('core.function_dispatcher.FakeUI'), \
             patch('core.function_dispatcher.AudioOut'):
            
            disp = FunctionDispatcher()
            # Manually start 1 worker for deterministic order testing
            disp._workers = []
            t = threading.Thread(target=disp._worker_loop, daemon=True)
            disp._workers.append(t)
            t.start()
            
            # Mock specialized dispatchers
            disp.visual_dispatcher = MagicMock()
            disp.system_dispatcher = MagicMock()
            disp.hardware_dispatcher = MagicMock()
            disp.horror_dispatcher = MagicMock()
            
            # Rebuild map to point to mocks
            disp._action_map = {
                "GDI_FLASH": disp.visual_dispatcher,
                "FILE_DELETE": disp.system_dispatcher,
                "PROCESS_KILL": disp.system_dispatcher
            }
            
            yield disp
            
            # Cleanup
            disp.stop_dispatching()
    
    def test_priority_execution(self, dispatcher):
        """
        Verify that HIGH priority tasks jump ahead of LOW priority tasks.
        """
        execution_order = []
        
        def slow_action(*args, **kwargs):
            time.sleep(0.5)
            execution_order.append("SLOW_LOW")
            
        def fast_action(*args, **kwargs):
            execution_order.append("FAST_LOW")
            
        def high_action(*args, **kwargs):
            execution_order.append("HIGH_PRIORITY")

        # Patch the dispatch methods of the EXISTING dispatchers
        # This avoids reference issues where _action_map points to wrong object
        with patch.object(dispatcher.system_dispatcher, 'dispatch', side_effect=slow_action) as mock_sys, \
             patch.object(dispatcher.visual_dispatcher, 'dispatch', side_effect=high_action) as mock_vis:
            
            # 1. Blocking Task (Low)
            # Use valid action CLIPBOARD_POISON
            dispatcher._do_dispatch({"action": "CLIPBOARD_POISON", "params": {}, "speech": "s"})
            time.sleep(0.1)
            
            # Switch side effect for system dispatcher for second call
            # We assume CLIPBOARD_POISON and OPEN_BROWSER both map to system_dispatcher (verified)
            
            mock_sys.side_effect = fast_action
            
            # 2. Fast Task (Low)
            # Use valid action OPEN_BROWSER
            dispatcher._do_dispatch({"action": "OPEN_BROWSER", "params": {}, "speech": "f"})
            
            # 3. High Priority Task
            # GDI_FLASH is valid
            dispatcher._do_dispatch({"action": "GDI_FLASH", "params": {}, "speech": "h"})
            
            # Wait results
            time.sleep(1.5)
            
            assert execution_order == ["SLOW_LOW", "HIGH_PRIORITY", "FAST_LOW"]

    def test_concurrency_limit(self):
        """Verify that we spawn correct number of threads."""
        # Use a fresh dispatcher - it should auto-start 5 workers
        with patch.object(FunctionDispatcher, '_worker_loop'): # Prevent loop execution for this test
            disp = FunctionDispatcher()
            # Wait a tick for threads to start
            time.sleep(0.1)
            
            # Check worker count
            assert len(disp._workers) == 5
            
            # Check that they are threads
            for t in disp._workers:
                assert isinstance(t, threading.Thread)
            
            disp.stop_dispatching()
