# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import psutil
import os
import time
import threading
from core.event_bus import bus

class ResourceGuard:
    """
    Monitors the system resource usage of the SENTIENT_OS process.
    If usage exceeds safe limits, it triggers an emergency shutdown via EventBus.
    This prevents the game from accidentally freezing the host computer.
    """
    def __init__(self, cpu_limit=85.0, mem_limit_mb=1024):
        self.process = psutil.Process(os.getpid())
        self.cpu_limit = cpu_limit
        self.mem_limit_mb = mem_limit_mb
        self.is_running = False
        self._monitor_thread = None
        
        # Stats tracking
        self.cpu_violation_count = 0
        self.max_violations = 5 # 5 consecutive violations = SHUTDOWN

    def start(self):
        """Starts the background monitoring thread."""
        self.is_running = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        print(f"[RESOURCE_GUARD] Monitoring started. (CPU Limit: {self.cpu_limit}%, RAM Limit: {self.mem_limit_mb}MB)")

    def stop(self):
        """Stops the monitoring thread."""
        self.is_running = False

    def _monitor_loop(self):
        while self.is_running:
            try:
                # 1. Check CPU Usage
                cpu_usage = self.process.cpu_percent(interval=1.0)
                
                # 2. Check Memory Usage (RSS)
                mem_info = self.process.memory_info()
                mem_usage_mb = mem_info.rss / (1024 * 1024)
                
                # print(f"[GUARD] CPU: {cpu_usage}% | RAM: {mem_usage_mb:.1f}MB")
                
                # 3. Validation Logic
                triggered = False
                
                if cpu_usage > self.cpu_limit:
                    self.cpu_violation_count += 1
                    if self.cpu_violation_count >= self.max_violations:
                        print(f"[RESOURCE_GUARD] CRITICAL: CPU usage exceeded {self.cpu_limit}% for {self.max_violations} seconds!")
                        triggered = True
                else:
                    self.cpu_violation_count = 0 # Reset on normal usage

                if mem_usage_mb > self.mem_limit_mb:
                    print(f"[RESOURCE_GUARD] CRITICAL: Memory usage exceeded {self.mem_limit_mb}MB!")
                    triggered = True

                # 4. Emergency Action
                if triggered:
                    print("[RESOURCE_GUARD] Triggering EMERGENCY SHUTDOWN due to resource pressure.")
                    # Publish shutdown event
                    bus.publish("system.shutdown", {"reason": "resource_exhaustion", "cpu": cpu_usage, "ram": mem_usage_mb})
                    # Also directly trigger safety net cleanup just in case bus is hung
                    from core.safety_net import SafetyNet
                    sn = SafetyNet()
                    sn.emergency_cleanup()
                    break

            except Exception as e:
                print(f"[RESOURCE_GUARD] Error in loop: {e}")
            
            time.sleep(2) # Sample every 2 seconds

    @staticmethod
    def get_system_stats():
        """Returns overall system stats (not just this process)."""
        return {
            "total_cpu": psutil.cpu_percent(),
            "available_ram_gb": psutil.virtual_memory().available / (1024**3)
        }
