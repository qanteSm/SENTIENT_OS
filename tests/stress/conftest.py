"""
Stress Test Fixtures and Utilities

Provides resource tracking, leak detection, and performance monitoring.
"""
import pytest
import psutil
import time
import gc
import tracemalloc
import threading
from dataclasses import dataclass
from typing import Dict, List, Optional
import json
from pathlib import Path

# Windows GDI Handle tracking (platform-specific)
try:
    import win32api
    import win32process
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False


@dataclass
class ResourceSnapshot:
    """Snapshot of system resources at a point in time."""
    timestamp: float
    memory_rss_mb: float
    memory_vms_mb: float
    thread_count: int
    gdi_handles: int
    user_handles: int
    cpu_percent: float
    tracemalloc_current_mb: Optional[float] = None
    tracemalloc_peak_mb: Optional[float] = None


class ResourceTracker:
    """
    Tracks system resource usage over time.
    
    Critical for detecting:
    - Memory leaks (RSS/VMS growth)
    - GDI handle leaks (Windows limit: 10,000 per process)
    - Thread leaks
    - CPU spikes
    """
    
    def __init__(self, enable_tracemalloc: bool = True):
        self.snapshots: List[ResourceSnapshot] = []
        self.process = psutil.Process()
        self.enable_tracemalloc = enable_tracemalloc
        
        if self.enable_tracemalloc:
            tracemalloc.start()
    
    def snapshot(self) -> ResourceSnapshot:
        """Take a resource snapshot."""
        # Force GC before snapshot for accurate memory reading
        gc.collect()
        
        mem = self.process.memory_info()
        
        # GDI/USER handle count (Windows only)
        gdi_handles = 0
        user_handles = 0
        if HAS_WIN32:
            try:
                # GetGuiResources: 0=GDI, 1=USER
                handle = win32api.OpenProcess(win32process.PROCESS_QUERY_INFORMATION, False, self.process.pid)
                gdi_handles = win32process.GetGuiResources(handle, 0)
                user_handles = win32process.GetGuiResources(handle, 1)
                win32api.CloseHandle(handle)
            except Exception:
                pass  # Fallback to 0 if not available
        
        # Tracemalloc (if enabled)
        tm_current = None
        tm_peak = None
        if self.enable_tracemalloc:
            current, peak = tracemalloc.get_traced_memory()
            tm_current = current / 1024 / 1024  # MB
            tm_peak = peak / 1024 / 1024
        
        snapshot = ResourceSnapshot(
            timestamp=time.time(),
            memory_rss_mb=mem.rss / 1024 / 1024,
            memory_vms_mb=mem.vms / 1024 / 1024,
            thread_count=threading.active_count(),
            gdi_handles=gdi_handles,
            user_handles=user_handles,
            cpu_percent=self.process.cpu_percent(interval=0.1),
            tracemalloc_current_mb=tm_current,
            tracemalloc_peak_mb=tm_peak
        )
        
        self.snapshots.append(snapshot)
        return snapshot
    
    def detect_leaks(self) -> Dict[str, any]:
        """
        Analyze snapshots for leaks.
        
        Returns:
            dict with leak detection results
        """
        if len(self.snapshots) < 2:
            return {"status": "insufficient_data"}
        
        first = self.snapshots[0]
        last = self.snapshots[-1]
        
        # Memory growth
        memory_growth_mb = last.memory_rss_mb - first.memory_rss_mb
        memory_growth_percent = (memory_growth_mb / first.memory_rss_mb) * 100 if first.memory_rss_mb > 0 else 0
        
        # GDI handle growth
        gdi_growth = last.gdi_handles - first.gdi_handles
        
        # Thread growth
        thread_growth = last.thread_count - first.thread_count
        
        # Leak detection heuristics
        has_memory_leak = memory_growth_mb > 50  # 50MB+ growth is suspicious
        has_gdi_leak = gdi_growth > 100  # 100+ handles is suspicious
        has_thread_leak = thread_growth > 5  # 5+ threads is suspicious
        
        # Check for "staircase effect" in memory
        memory_trend_increasing = all(
            self.snapshots[i].memory_rss_mb <= self.snapshots[i + 1].memory_rss_mb
            for i in range(len(self.snapshots) - 1)
        ) if len(self.snapshots) > 2 else False
        
        return {
            "status": "analyzed",
            "duration_seconds": last.timestamp - first.timestamp,
            "memory": {
                "growth_mb": round(memory_growth_mb, 2),
                "growth_percent": round(memory_growth_percent, 2),
                "staircase_trend": memory_trend_increasing,
                "leak_detected": has_memory_leak or memory_trend_increasing
            },
            "gdi_handles": {
                "growth": gdi_growth,
                "final_count": last.gdi_handles,
                "leak_detected": has_gdi_leak,
                "critical": last.gdi_handles > 5000  # Approaching Windows limit
            },
            "threads": {
                "growth": thread_growth,
                "final_count": last.thread_count,
                "leak_detected": has_thread_leak
            }
        }
    
    def save_report(self, filepath: str):
        """Save detailed report to JSON."""
        report = {
            "snapshots": [
                {
                    "timestamp": s.timestamp,
                    "memory_rss_mb": s.memory_rss_mb,
                    "gdi_handles": s.gdi_handles,
                    "thread_count": s.thread_count,
                    "cpu_percent": s.cpu_percent
                }
                for s in self.snapshots
            ],
            "leak_analysis": self.detect_leaks()
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
    
    def stop(self):
        """Stop tracemalloc."""
        if self.enable_tracemalloc:
            tracemalloc.stop()


@pytest.fixture
def resource_tracker():
    """
    Fixture that tracks resources during test execution.
    
    Usage:
        def test_something(resource_tracker):
            # Your test code
            pass
        
        # After test, check resource_tracker.detect_leaks()
    """
    tracker = ResourceTracker(enable_tracemalloc=True)
    tracker.snapshot()  # Initial snapshot
    
    yield tracker
    
    tracker.snapshot()  # Final snapshot
    
    # Auto-detect leaks
    leaks = tracker.detect_leaks()
    if leaks["status"] == "analyzed":
        if leaks["memory"]["leak_detected"]:
            print(f"\n⚠️ MEMORY LEAK DETECTED: +{leaks['memory']['growth_mb']} MB")
        if leaks["gdi_handles"]["leak_detected"]:
            print(f"\n⚠️ GDI HANDLE LEAK: +{leaks['gdi_handles']['growth']} handles")
        if leaks["threads"]["leak_detected"]:
            print(f"\n⚠️ THREAD LEAK: +{leaks['threads']['growth']} threads")
    
    tracker.stop()


@pytest.fixture
def stress_config():
    """
    Configuration for stress tests.
    Can be overridden via pytest CLI args.
    """
    return {
        "dispatcher_burst_duration": 10,  # seconds
        "dispatcher_burst_rate": 100,  # actions/second
        "memory_flood_count": 1000,  # number of items
        "long_run_duration": 3600,  # 1 hour
        "api_request_count": 100,
        "visual_spam_count": 500
    }


@pytest.fixture
def mock_dispatcher():
    """Create a mock dispatcher for testing."""
    from unittest.mock import MagicMock, patch
    from PyQt6.QtWidgets import QApplication
    import sys
    
    # Ensure QApplication exists
    if not QApplication.instance():
        app = QApplication(sys.argv)
    
    with patch('core.function_dispatcher.FakeUI'), \
         patch('core.function_dispatcher.AudioOut'):
        from core.function_dispatcher import FunctionDispatcher
        
        disp = FunctionDispatcher()
        yield disp
        
        # Cleanup
        disp.stop_dispatching()


@pytest.fixture
def mock_brain():
    """Create a mock GeminiBrain for testing."""
    from core.gemini_brain import GeminiBrain
    from unittest.mock import Mock
    
    # Force mock mode
    brain = GeminiBrain(api_key=None)
    brain.mock_mode = True
    
    yield brain


@pytest.fixture
def mock_memory():
    """Create a fresh Memory instance for testing."""
    from core.memory import Memory
    import tempfile
    import shutil
    
    # Create temp directory for memory files
    temp_dir = tempfile.mkdtemp()
    
    # Override memory file path
    memory = Memory()
    memory.filepath = f"{temp_dir}/test_memory.json"
    memory.memory_file = memory.filepath  # Alias for compatibility
    
    # Initial save to create file
    memory.save_immediate()
    
    yield memory
    
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


# Mark for stress tests
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "stress: mark test as a stress test (may be slow)"
    )
    config.addinivalue_line(
        "markers", "long_run: mark test as a long-running test (1+ hour)"
    )
    config.addinivalue_line(
        "markers", "chaos: mark test as a chaos/random failure test"
    )
