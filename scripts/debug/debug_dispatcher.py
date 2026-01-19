# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication
import sys
import threading
import time

def debug_priority():
    print("--- START DEBUG ---")
    
    # Initialize QApplication to satisfy Qt requirements
    if not QApplication.instance():
        app = QApplication(sys.argv)
    
    with patch('core.function_dispatcher.FakeUI'), \
         patch('core.function_dispatcher.AudioOut'):
        
        from core.function_dispatcher import FunctionDispatcher 
        
        disp = FunctionDispatcher()
        
        # Kill default workers
        disp.stop_dispatching()
        
        print("Waiting for threads to die...")
        start_wait = time.time()
        while threading.active_count() > 1:
            if time.time() - start_wait > 5:
                print("TIMEOUT waiting for threads!")
                print([t.name for t in threading.enumerate()])
                break
            time.sleep(0.1)
            
        disp._is_shutting_down = False # Force reopen
        disp._workers = []
    
    # Mock dispatchers
    disp.visual_dispatcher = MagicMock()
    disp.system_dispatcher = MagicMock()
    
    disp._action_map = {
        "GDI_FLASH": disp.visual_dispatcher,
        "FILE_DELETE": disp.system_dispatcher,
        "PROCESS_KILL": disp.system_dispatcher
    }
    
    print(f"DEBUG: FILE_DELETE mapper type: {type(disp._action_map['FILE_DELETE'])}")
    
    execution_order = []
    
    def slow_action(action, params, speech):
        print(f"Inside SLOW_ACTION: {action}")
        try:
            time.sleep(0.5)
            execution_order.append("SLOW_LOW")
        except Exception as e:
            print(f"SLOW_ACTION ERROR: {e}")
        print("Finished SLOW_ACTION")
        
    def high_priority(action, params, speech):
        print(f"Inside HIGH_ACTION: {action}")
        execution_order.append("HIGH_PRIORITY")
        
    def fast_low(action, params, speech):
        print(f"Inside FAST_LOW: {action}")
        execution_order.append("FAST_LOW")

    disp.system_dispatcher.dispatch.side_effect = slow_action
    disp.visual_dispatcher.dispatch.side_effect = high_priority

    # Start 1 worker
    print(f"Active Threads before start: {[t.name for t in threading.enumerate()]}")
    print("Starting 1 worker...")
    
    # We need to manually start the loop but catch errors
    t = threading.Thread(target=disp._worker_loop, daemon=True)
    disp._workers.append(t)
    t.start()
    
    # 1. Dispatch Slow
    print("Dispatching FILE_DELETE (Slow)")
    disp._do_dispatch({"action": "FILE_DELETE", "params": {}, "speech": "slow"})
    print(f"Queue Size after Slow: {disp._action_queue.qsize()}")
    time.sleep(0.1) # Wait for pickup
    
    # 2. Dispatch Low
    disp.system_dispatcher.dispatch.side_effect = fast_low # Switch side effect
    print("Dispatching PROCESS_KILL (Fast Low)")
    disp._do_dispatch({"action": "PROCESS_KILL", "params": {}, "speech": "low"})
    print(f"Queue Size after Low: {disp._action_queue.qsize()}")
    
    # 3. Dispatch High
    print("Dispatching GDI_FLASH (High)")
    disp._do_dispatch({"action": "GDI_FLASH", "params": {}, "speech": "high"})
    print(f"Queue Size after High: {disp._action_queue.qsize()}")
    
    print("Waiting for workers...")
    time.sleep(2.0)
    print(f"Final Order: {execution_order}")

if __name__ == "__main__":
    debug_priority()
