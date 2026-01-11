import subprocess
import psutil
import time
import json
import threading
import sys
from pathlib import Path

def run_tests_with_profiling():
    print("===================================================")
    print("   SENTIENT_OS ADVANCED CERTIFICATION SUITE")
    print("===================================================")
    
    report_dir = Path("tests")
    report_dir.mkdir(exist_ok=True)
    json_path = report_dir / "performance_report.json"
    
    snapshots = []
    stop_profiling = threading.Event()
    
    def profile_worker(proc_pid):
        try:
            parent = psutil.Process(proc_pid)
            while not stop_profiling.is_set():
                try:
                    # Capture parent + all children (pytest + test processes)
                    mem = 0
                    cpu = 0
                    threads = 0
                    
                    processes = [parent] + parent.children(recursive=True)
                    for p in processes:
                        if p.is_running():
                            mem += p.memory_info().rss / 1024 / 1024
                            cpu += p.cpu_percent()
                            threads += p.num_threads()
                    
                    snapshots.append({
                        "timestamp": time.time(),
                        "memory_rss_mb": mem,
                        "cpu_percent": cpu,
                        "threads": threads
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                time.sleep(0.5)
        except Exception as e:
            print(f"Profiling error: {e}")

    # Start Pytest process
    cmd = [
        sys.executable, "-m", "pytest", "tests/", 
        "-v", "-m", "not long_run",
        "--html=tests/report.html", "--self-contained-html",
        "--cov=core", "--cov-report=html:tests/coverage_report"
    ]
    
    print(f"🚀 Starting Pytest sweep...")
    start_time = time.time()
    
    # Run pytest
    process = subprocess.Popen(cmd)
    
    # Start profiling thread
    profiler = threading.Thread(target=profile_worker, args=(process.pid,))
    profiler.start()
    
    # Wait for pytest to finish
    exit_code = process.wait()
    stop_profiling.set()
    profiler.join()
    
    end_time = time.time()
    
    if exit_code == 0:
        print(f"\n✅ Pytest finished SUCCESSFULY (Exit: {exit_code})")
    else:
        print(f"\n❌ Pytest finished with FAILURES (Exit: {exit_code})")
    
    if snapshots:
        with open(json_path, "w") as f:
            json.dump({
                "session_start": snapshots[0]["timestamp"],
                "session_end": snapshots[-1]["timestamp"],
                "total_snapshots": len(snapshots),
                "data": snapshots
            }, f, indent=2)
        print(f"📊 Captured {len(snapshots)} snapshots in {end_time - start_time:.1f}s")
        
        # Run graph generator
        print("📈 Generating graphs...")
        subprocess.run([sys.executable, "generate_profiling_graphs.py"])
    
    print("\n===================================================")
    print("   CERTIFICATION COMPLETE")
    print("===================================================")
    
    # Propagate the exit code so the batch file knows it failed
    sys.exit(exit_code)

if __name__ == "__main__":
    run_tests_with_profiling()
