```python
#!/usr/bin/env python3
"""
Find duplicate files in a directory tree by content hash.

Usage examples:
    python find_dupes.py /path/to/search
    python find_dupes.py . --min-size 1024 --ext .jpg .png
    python find_dupes.py ~/Documents --delete-prompt
"""

import argparse
import hashlib
import os
from collections import defaultdict


def get_file_hash(filepath, chunk_size=8192):
    """Calculate MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (IOError, PermissionError):
        return None


def find_files(directory, min_size=0, extensions=None):
    """Walk directory and yield files matching criteria."""
    for root, _, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(root, name)
            try:
                size = os.path.getsize(filepath)
                if size < min_size:
                    continue
                if extensions:
                    ext = os.path.splitext(name)[1].lower()
                    if ext not in extensions:
                        continue
                yield filepath, size
            except (OSError, PermissionError):
                continue


def find_duplicates(directory, min_size=0, extensions=None):
    """Find duplicate files by first grouping by size, then by hash."""
    size_groups = defaultdict(list)
    
    for filepath, size in find_files(directory, min_size, extensions):
        size_groups[size].append(filepath)
    
    hash_groups = defaultdict(list)
    for size, paths in size_groups.items():
        if len(paths) < 2:
            continue
        for path in paths:
            file_hash = get_file_hash(path)
            if file_hash:
                hash_groups[file_hash].append(path)
    
    return {h: paths for h, paths in hash_groups.items() if len(paths) > 1}


def main():
    parser = argparse.ArgumentParser(description='Find duplicate files by content hash')
    parser.add_argument('directory', help='Directory to search')
    parser.add_argument('--min-size', type=int, default=1, help='Minimum file size in bytes')
    parser.add_argument('--ext', nargs='+', help='File extensions to include (e.g., .jpg .png)')
    parser.add_argument('--delete-prompt', action='store_true', help='Prompt to delete duplicates')
    args = parser.parse_args()

    extensions = set(e.lower() if e.startswith('.') else f'.{e.lower()}' for e in args.ext) if args.ext else None
    
    print(f"Scanning {args.directory}...")
    duplicates = find_duplicates(args.directory, args.min_size, extensions)
    
    if not duplicates:
        print("No duplicates found.")
        return
    
    total_waste = 0
    for file_hash, paths in duplicates.items():
        size = os.path.getsize(paths[0])
        waste = size * (len(paths) - 1)
        total_waste += waste
        print(f"\n[{file_hash[:8]}] {len(paths)} copies, {size:,} bytes each:")
        for i, path in enumerate(paths):
            marker = "(original)" if i == 0 else "(duplicate)"
            print(f"  {marker} {path}")
        
        if args.delete_prompt:
            resp = input("  Delete duplicates? [y/N]: ").strip().lower()
            if resp == 'y':
                for path in paths[1:]:
                    os.remove(path)
                    print(f"    Deleted: {path}")
    
    print(f"\nTotal duplicate sets: {len(duplicates)}")
    print(f"Wasted space: {total_waste:,} bytes ({total_waste / 1024 / 1024:.2f} MB)")


if __name__ == '__main__':
    main()
```
