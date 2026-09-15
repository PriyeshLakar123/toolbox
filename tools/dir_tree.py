```python
#!/usr/bin/env python3
"""
dir_tree - Print a visual directory tree structure

Usage examples:
    python dir_tree.py                     # Current directory, unlimited depth
    python dir_tree.py /path/to/folder     # Specific directory
    python dir_tree.py -d 2                # Limit depth to 2 levels
    python dir_tree.py -s                  # Show file sizes
    python dir_tree.py -a                  # Include hidden files
    python dir_tree.py -D                  # Directories only
"""

import argparse
import os
from pathlib import Path


def format_size(size_bytes):
    """Format bytes into human readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"


def print_tree(directory, prefix="", depth=None, current_depth=0, 
               show_size=False, show_hidden=False, dirs_only=False):
    """Recursively print directory tree."""
    if depth is not None and current_depth >= depth:
        return
    
    try:
        entries = sorted(Path(directory).iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        print(f"{prefix}[Permission Denied]")
        return
    
    if not show_hidden:
        entries = [e for e in entries if not e.name.startswith('.')]
    
    if dirs_only:
        entries = [e for e in entries if e.is_dir()]
    
    pointers = ['├── '] * (len(entries) - 1) + ['└── '] if entries else []
    
    for pointer, entry in zip(pointers, entries):
        if entry.is_dir():
            print(f"{prefix}{pointer}{entry.name}/")
            extension = '│   ' if pointer == '├── ' else '    '
            print_tree(entry, prefix + extension, depth, current_depth + 1,
                      show_size, show_hidden, dirs_only)
        else:
            size_str = ""
            if show_size:
                try:
                    size_str = f" ({format_size(entry.stat().st_size)})"
                except OSError:
                    size_str = " (?)"
            print(f"{prefix}{pointer}{entry.name}{size_str}")


def main():
    parser = argparse.ArgumentParser(
        description='Print a visual directory tree structure'
    )
    parser.add_argument('directory', nargs='?', default='.',
                        help='Directory to display (default: current)')
    parser.add_argument('-d', '--depth', type=int, default=None,
                        help='Maximum depth to display')
    parser.add_argument('-s', '--size', action='store_true',
                        help='Show file sizes')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Include hidden files and directories')
    parser.add_argument('-D', '--dirs-only', action='store_true',
                        help='Show directories only')
    
    args = parser.parse_args()
    
    root = Path(args.directory).resolve()
    
    if not root.exists():
        print(f"Error: '{args.directory}' does not exist")
        return 1
    
    if not root.is_dir():
        print(f"Error: '{args.directory}' is not a directory")
        return 1
    
    print(f"{root.name}/")
    print_tree(root, "", args.depth, 0, args.size, args.all, args.dirs_only)
    return 0


if __name__ == '__main__':
    exit(main())
```
