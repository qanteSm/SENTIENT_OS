import time
import queue
import threading
import argparse
import sys
import os
from PyQt6.QtWidgets import QApplication

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock environment if needed
from unittest.mock import MagicMock, patch

try:
    from core.function_dispatcher import FunctionDispatcher
except ImportError:
    print("Error: run from project root")
    sys.exit(1)

def run_stress_test(num_tasks=50, delay=0.01):
    print(f"--- STARTING STRESS TEST ({num_tasks} tasks) ---")
    
    # Initialize App
    if not QApplication.instance():
        app = QApplication(sys.argv)
    
    # Mock UI components to avoid windows
    with patch('core.function_dispatcher.FakeUI'), \
         patch('core.function_dispatcher.AudioOut'):
        
        disp = FunctionDispatcher()
        
        # Track completion
        completed_count = 0
        start_time = time.time()
        
        # Patch execution to just count
        original_execute = disp._execute_action
        
        executed_tasks = []
        
        def mock_execute(action, params, speech):
            nonlocal completed_count
            # Simulate work based on action
            if "HEAVY" in action:
                time.sleep(0.1)
            executed_tasks.append(action)
            completed_count += 1
            if completed_count % 10 == 0:
                print(f"Progress: {completed_count}/{num_tasks}")
                
        disp._execute_action = mock_execute
        
        # Flood Queue
        print("Flooding queue...")
        for i in range(num_tasks):
            if i % 5 == 0:
                action = "GDI_FLASH" # High Priority
            else:
                action = "CLIPBOARD_POISON" # Low Priority
                
            disp._do_dispatch({"action": action, "params": {}, "speech": "test"})
            time.sleep(delay)
            
        print("Queue flood complete. Waiting for processing...")
        
        # Wait for completion
        max_wait = 30
        while completed_count < num_tasks:
            if time.time() - start_time > max_wait:
                print("TIMEOUT!")
                break
            time.sleep(0.1)
            
        duration = time.time() - start_time
        print(f"--- TEST COMPLETE in {duration:.2f}s ---")
        print(f"Processed: {completed_count}/{num_tasks}")
        
        # Verify Priority Distribution
        # We expect GDI_FLASH to be processed "soon" after queued, not stuck behind all 50 low priority items
        # But this is hard to measure without timestamp analysis.
        # Just checking throughput here.
        
        disp.stop_dispatching()

if __name__ == "__main__":
    run_stress_test()
