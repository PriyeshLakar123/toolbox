```python
#!/usr/bin/env python3
"""
Monitor processes by PID or name with optional CPU/memory thresholds.

Usage:
    # Watch a specific PID until it exits
    python proc_watch.py --pid 1234
    
    # Watch for a process by name
    python proc_watch.py --name firefox
    
    # Alert if CPU exceeds 80% or memory exceeds 500MB
    python proc_watch.py --pid 1234 --cpu 80 --mem 500
    
    # Check every 2 seconds (default is 1)
    python proc_watch.py --name python --interval 2
"""

import argparse
import subprocess
import sys
import time
from datetime import datetime


def get_process_info(pid=None, name=None):
    """Get process info using ps command."""
    try:
        cmd = ["ps", "-eo", "pid,comm,%cpu,%mem,rss", "--no-headers"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        processes = []
        
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 5:
                proc = {
                    "pid": int(parts[0]),
                    "name": parts[1],
                    "cpu": float(parts[2]),
                    "mem_pct": float(parts[3]),
                    "mem_mb": int(parts[4]) / 1024
                }
                if pid and proc["pid"] == pid:
                    return [proc]
                if name and name.lower() in proc["name"].lower():
                    processes.append(proc)
        
        return processes if name else []
    except Exception as e:
        print(f"Error reading process info: {e}", file=sys.stderr)
        return []


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def main():
    parser = argparse.ArgumentParser(description="Monitor processes with alerts")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pid", type=int, help="Process ID to watch")
    group.add_argument("--name", type=str, help="Process name to watch")
    parser.add_argument("--cpu", type=float, help="CPU threshold percentage")
    parser.add_argument("--mem", type=float, help="Memory threshold in MB")
    parser.add_argument("--interval", type=float, default=1, help="Check interval in seconds")
    args = parser.parse_args()

    log(f"Watching {'PID ' + str(args.pid) if args.pid else 'name: ' + args.name}")
    if args.cpu:
        log(f"CPU threshold: {args.cpu}%")
    if args.mem:
        log(f"Memory threshold: {args.mem}MB")

    was_running = False
    
    try:
        while True:
            procs = get_process_info(pid=args.pid, name=args.name)
            is_running = len(procs) > 0
            
            if is_running and not was_running:
                log(f"STARTED - found {len(procs)} matching process(es)")
            elif not is_running and was_running:
                log("STOPPED - process no longer running")
                if args.pid:
                    break
            
            for proc in procs:
                alerts = []
                if args.cpu and proc["cpu"] > args.cpu:
                    alerts.append(f"CPU {proc['cpu']:.1f}% > {args.cpu}%")
                if args.mem and proc["mem_mb"] > args.mem:
                    alerts.append(f"MEM {proc['mem_mb']:.1f}MB > {args.mem}MB")
                
                if alerts:
                    log(f"ALERT PID {proc['pid']} ({proc['name']}): {', '.join(alerts)}")
                elif is_running:
                    status = f"CPU: {proc['cpu']:.1f}%, MEM: {proc['mem_mb']:.1f}MB"
                    print(f"\r[{datetime.now().strftime('%H:%M:%S')}] PID {proc['pid']}: {status}    ", end="", flush=True)
            
            was_running = is_running
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()
```
