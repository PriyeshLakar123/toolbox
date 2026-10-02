```python
#!/usr/bin/env python3
# pip install pyperclip
"""
Clipboard history tracker - monitors and stores clipboard entries.

Usage examples:
    python clipboard_history.py watch          # Start monitoring clipboard
    python clipboard_history.py list           # Show recent entries
    python clipboard_history.py list -n 20     # Show last 20 entries
    python clipboard_history.py search "text"  # Search history
    python clipboard_history.py get 3          # Get entry #3
    python clipboard_history.py clear          # Clear history
"""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

try:
    import pyperclip
except ImportError:
    print("Install pyperclip: pip install pyperclip")
    exit(1)

HISTORY_FILE = Path.home() / ".clipboard_history.json"


def load_history():
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text())
    return []


def save_history(history):
    HISTORY_FILE.write_text(json.dumps(history, indent=2))


def watch_clipboard(interval=0.5):
    """Monitor clipboard and save new entries."""
    print(f"Watching clipboard (Ctrl+C to stop)...")
    history = load_history()
    last_content = pyperclip.paste()
    
    try:
        while True:
            current = pyperclip.paste()
            if current != last_content and current.strip():
                entry = {
                    "content": current,
                    "timestamp": datetime.now().isoformat(),
                }
                history.insert(0, entry)
                history = history[:500]  # Keep last 500 entries
                save_history(history)
                preview = current[:50].replace("\n", " ")
                print(f"[{len(history)}] Saved: {preview}...")
                last_content = current
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\nStopped. {len(history)} entries in history.")


def list_entries(n=10):
    history = load_history()
    for i, entry in enumerate(history[:n]):
        preview = entry["content"][:60].replace("\n", " ")
        ts = entry["timestamp"][:19].replace("T", " ")
        print(f"{i}: [{ts}] {preview}")


def search_history(query):
    history = load_history()
    for i, entry in enumerate(history):
        if query.lower() in entry["content"].lower():
            preview = entry["content"][:60].replace("\n", " ")
            print(f"{i}: {preview}")


def get_entry(index):
    history = load_history()
    if 0 <= index < len(history):
        content = history[index]["content"]
        pyperclip.copy(content)
        print(f"Copied to clipboard:\n{content}")
    else:
        print(f"Invalid index. History has {len(history)} entries.")


def clear_history():
    save_history([])
    print("Clipboard history cleared.")


def main():
    parser = argparse.ArgumentParser(description="Clipboard history tracker")
    sub = parser.add_subparsers(dest="cmd", required=True)
    
    sub.add_parser("watch", help="Monitor clipboard")
    
    list_p = sub.add_parser("list", help="List recent entries")
    list_p.add_argument("-n", type=int, default=10, help="Number of entries")
    
    search_p = sub.add_parser("search", help="Search history")
    search_p.add_argument("query", help="Search term")
    
    get_p = sub.add_parser("get", help="Get and copy entry by index")
    get_p.add_argument("index", type=int, help="Entry index")
    
    sub.add_parser("clear", help="Clear history")
    
    args = parser.parse_args()
    
    if args.cmd == "watch":
        watch_clipboard()
    elif args.cmd == "list":
        list_entries(args.n)
    elif args.cmd == "search":
        search_history(args.query)
    elif args.cmd == "get":
        get_entry(args.index)
    elif args.cmd == "clear":
        clear_history()


if __name__ == "__main__":
    main()
```
