```python
#!/usr/bin/env python3
"""
List files sorted by age with human-readable time info.

Usage:
    python file_age.py                    # current directory, newest first
    python file_age.py /path/to/dir       # specific directory
    python file_age.py -o oldest          # oldest first
    python file_age.py -n 10              # show only 10 files
    python file_age.py -p "*.py"          # only python files
"""

import argparse
import os
import fnmatch
from datetime import datetime
from pathlib import Path


def human_age(seconds):
    """Convert seconds to human-readable age."""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds / 60)}m"
    elif seconds < 86400:
        return f"{int(seconds / 3600)}h"
    elif seconds < 604800:
        return f"{int(seconds / 86400)}d"
    elif seconds < 2592000:
        return f"{int(seconds / 604800)}w"
    else:
        return f"{int(seconds / 2592000)}mo"


def human_size(size):
    """Convert bytes to human-readable size."""
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024:
            return f"{size:6.1f}{unit}"
        size /= 1024
    return f"{size:.1f}P"


def get_files(directory, pattern=None, recursive=False):
    """Get files with their modification times."""
    files = []
    path = Path(directory)
    
    if recursive:
        items = path.rglob('*')
    else:
        items = path.iterdir()
    
    for item in items:
        if item.is_file():
            if pattern and not fnmatch.fnmatch(item.name, pattern):
                continue
            try:
                stat = item.stat()
                files.append((item, stat.st_mtime, stat.st_size))
            except (PermissionError, OSError):
                continue
    return files


def main():
    parser = argparse.ArgumentParser(description='List files sorted by age')
    parser.add_argument('directory', nargs='?', default='.', help='Directory to scan')
    parser.add_argument('-o', '--order', choices=['newest', 'oldest'], 
                        default='newest', help='Sort order')
    parser.add_argument('-n', '--number', type=int, help='Number of files to show')
    parser.add_argument('-p', '--pattern', help='Filename pattern (e.g., "*.txt")')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursive search')
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a directory")
        return 1

    files = get_files(args.directory, args.pattern, args.recursive)
    
    if not files:
        print("No files found")
        return 0

    reverse = args.order == 'newest'
    files.sort(key=lambda x: x[1], reverse=reverse)
    
    if args.number:
        files = files[:args.number]

    now = datetime.now().timestamp()
    
    print(f"{'AGE':>6}  {'SIZE':>7}  {'MODIFIED':<19}  NAME")
    print("-" * 70)
    
    for filepath, mtime, size in files:
        age = human_age(now - mtime)
        size_str = human_size(size)
        mod_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        rel_path = filepath.relative_to(args.directory) if args.recursive else filepath.name
        print(f"{age:>6}  {size_str}  {mod_time}  {rel_path}")

    print(f"\nTotal: {len(files)} files")
    return 0


if __name__ == '__main__':
    exit(main())
```
