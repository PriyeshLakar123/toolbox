```python
#!/usr/bin/env python3
"""
filewatch - Monitor files/directories and run commands on changes

Usage examples:
    python filewatch.py . "echo 'something changed'"
    python filewatch.py ./src --ext .py -- python -m pytest
    python filewatch.py config.json "systemctl restart myapp"
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path


def get_file_state(path: Path, extensions: list[str] | None) -> dict[str, float]:
    """Get modification times for all relevant files."""
    state = {}
    
    if path.is_file():
        state[str(path)] = path.stat().st_mtime
    elif path.is_dir():
        for item in path.rglob("*"):
            if item.is_file():
                if extensions is None or item.suffix in extensions:
                    try:
                        state[str(item)] = item.stat().st_mtime
                    except (OSError, PermissionError):
                        pass
    return state


def detect_changes(old: dict, new: dict) -> list[str]:
    """Return list of changed/added/removed files."""
    changes = []
    
    for path, mtime in new.items():
        if path not in old or old[path] != mtime:
            changes.append(path)
    
    for path in old:
        if path not in new:
            changes.append(path)
    
    return changes


def main():
    parser = argparse.ArgumentParser(
        description="Watch files/directories and run command on changes"
    )
    parser.add_argument("path", help="File or directory to watch")
    parser.add_argument("command", nargs="+", help="Command to run on change")
    parser.add_argument("--ext", action="append", help="File extensions to watch (e.g., .py)")
    parser.add_argument("--interval", type=float, default=1.0, help="Poll interval in seconds")
    parser.add_argument("--initial", action="store_true", help="Run command once at start")
    
    args = parser.parse_args()
    
    watch_path = Path(args.path)
    if not watch_path.exists():
        print(f"Error: {args.path} does not exist", file=sys.stderr)
        sys.exit(1)
    
    command = " ".join(args.command) if len(args.command) > 1 else args.command[0]
    extensions = args.ext
    
    print(f"Watching: {watch_path}")
    print(f"Command: {command}")
    print(f"Press Ctrl+C to stop\n")
    
    state = get_file_state(watch_path, extensions)
    
    if args.initial:
        print("Running initial command...")
        subprocess.run(command, shell=True)
    
    try:
        while True:
            time.sleep(args.interval)
            new_state = get_file_state(watch_path, extensions)
            changes = detect_changes(state, new_state)
            
            if changes:
                print(f"\n[{time.strftime('%H:%M:%S')}] Changes detected:")
                for f in changes[:5]:
                    print(f"  - {f}")
                if len(changes) > 5:
                    print(f"  ... and {len(changes) - 5} more")
                print(f"Running: {command}\n")
                subprocess.run(command, shell=True)
                state = new_state
    except KeyboardInterrupt:
        print("\nStopped watching.")


if __name__ == "__main__":
    main()
```
