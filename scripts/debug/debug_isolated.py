# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import queue
import threading
import time
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass(order=True)
class ActionTask:
    """Task item for the Priority Queue."""
    priority: int
    timestamp: float = field(compare=False)
    action: str = field(compare=False)
    params: Dict[str, Any] = field(compare=False, default_factory=dict)
    speech: str = field(compare=False, default="")

def worker(q):
    print("Worker started")
    while True:
        try:
            task = q.get(timeout=1.0)
            print(f"Got task: {task.action} Priority {task.priority}")
            time.sleep(0.1)
            q.task_done()
        except queue.Empty:
            continue
        except Exception as e:
            print(f"Error: {e}")

def test_prio():
    q = queue.PriorityQueue()
    t = threading.Thread(target=worker, args=(q,), daemon=True)
    t.start()
    
    print("Putting Slow (3)")
    q.put(ActionTask(3, time.time(), "SLOW", {}, ""))
    
    time.sleep(0.05)
    
    print("Putting Low (3)")
    q.put(ActionTask(3, time.time(), "LOW", {}, ""))
    
    print("Putting High (1)")
    q.put(ActionTask(1, time.time(), "HIGH", {}, ""))
    
    time.sleep(2.0)

if __name__ == "__main__":
    test_prio()
