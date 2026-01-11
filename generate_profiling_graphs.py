import json
import matplotlib.pyplot as plt
from pathlib import Path
import datetime

def generate_graphs(json_path="tests/performance_report.json"):
    if not Path(json_path).exists():
        print(f"[ERROR] Report file {json_path} not found!")
        return

    with open(json_path, "r") as f:
        data = json.load(f)

    snapshots = data["data"]
    if not snapshots:
        print("[ERROR] No data points in report!")
        return

    # Extract data
    timestamps = [s["timestamp"] - data["session_start"] for s in snapshots]
    ram = [s["memory_rss_mb"] for s in snapshots]
    cpu = [s["cpu_percent"] for s in snapshots]
    threads = [s["threads"] for s in snapshots]

    # Create figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    fig.suptitle(f"SENTIENT_OS Performance Profile - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", fontsize=16)

    # RAM Plot
    ax1.plot(timestamps, ram, color='blue', label='RAM Usage (MB)')
    ax1.set_ylabel('Memory (MB)')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left')
    ax1.set_title("Memory Usage (RSS)")
    
    # Highlight max RAM
    max_ram = max(ram)
    max_ram_time = timestamps[ram.index(max_ram)]
    ax1.annotate(f'Peak: {max_ram:.1f} MB', xy=(max_ram_time, max_ram), xytext=(max_ram_time+5, max_ram+5),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    # CPU & Thread Plot
    ax2.plot(timestamps, cpu, color='red', label='CPU Usage (%)')
    ax2.set_ylabel('CPU (%)')
    ax2.set_xlabel('Time (seconds since start)')
    ax2.grid(True, alpha=0.3)
    
    ax3 = ax2.twinx()
    ax3.step(timestamps, threads, color='green', where='post', label='Thread Count')
    ax3.set_ylabel('Threads')
    
    # Combined Legend for ax2 and ax3
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax3.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    ax2.set_title("System Load & Threading")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save chart
    chart_path = "tests/performance_profile.png"
    plt.savefig(chart_path)
    print(f"✅ Performance graph saved to {Path(chart_path).absolute()}")
    
    # Also generate a summary markdown table
    summary_path = "tests/performance_summary.md"
    with open(summary_path, "w") as f:
        f.write("# Performance Summary\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"| :--- | :--- |\n")
        f.write(f"| **Peak RAM** | {max(ram):.2f} MB |\n")
        f.write(f"| **Avg RAM** | {sum(ram)/len(ram):.2f} MB |\n")
        f.write(f"| **Peak CPU** | {max(cpu):.1f} % |\n")
        f.write(f"| **Peak Threads** | {max(threads)} |\n")
        f.write(f"| **Duration** | {timestamps[-1]:.1f} s |\n\n")
        f.write(f"![Performance Profile](performance_profile.png)\n")
    
    print(f"✅ Summary report saved to {Path(summary_path).absolute()}")

if __name__ == "__main__":
    generate_graphs()
