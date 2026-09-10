```python
#!/usr/bin/env python3
"""
Bulk rename files using pattern matching with preview mode.

Usage examples:
    # Preview renaming all .txt files to .md
    python bulk_rename.py "*.txt" --pattern "\.txt$" --replace ".md"
    
    # Actually rename (no dry-run)
    python bulk_rename.py "*.txt" --pattern "\.txt$" --replace ".md" --execute
    
    # Add prefix to all jpg files
    python bulk_rename.py "*.jpg" --pattern "^" --replace "photo_" --execute
    
    # Replace spaces with underscores
    python bulk_rename.py "*" --pattern " " --replace "_" --execute
"""

import argparse
import glob
import os
import re
import sys


def bulk_rename(file_glob, pattern, replacement, execute=False, directory="."):
    """Rename files matching glob pattern using regex substitution."""
    search_path = os.path.join(directory, file_glob)
    files = glob.glob(search_path)
    
    if not files:
        print(f"No files matching '{file_glob}' in {directory}")
        return 0
    
    try:
        regex = re.compile(pattern)
    except re.error as e:
        print(f"Invalid regex pattern: {e}", file=sys.stderr)
        return 1
    
    renames = []
    for filepath in sorted(files):
        if os.path.isdir(filepath):
            continue
        
        dirname = os.path.dirname(filepath)
        old_name = os.path.basename(filepath)
        new_name = regex.sub(replacement, old_name)
        
        if old_name != new_name:
            renames.append((filepath, os.path.join(dirname, new_name), old_name, new_name))
    
    if not renames:
        print("No files would be renamed (pattern didn't match any filenames)")
        return 0
    
    print(f"{'EXECUTING' if execute else 'PREVIEW'}: {len(renames)} file(s) to rename\n")
    print(f"{'Old Name':<40} -> {'New Name':<40}")
    print("-" * 84)
    
    errors = 0
    for old_path, new_path, old_name, new_name in renames:
        print(f"{old_name:<40} -> {new_name:<40}")
        
        if execute:
            if os.path.exists(new_path):
                print(f"  ERROR: Target already exists, skipping")
                errors += 1
                continue
            try:
                os.rename(old_path, new_path)
            except OSError as e:
                print(f"  ERROR: {e}")
                errors += 1
    
    print()
    if execute:
        print(f"Renamed {len(renames) - errors} file(s), {errors} error(s)")
    else:
        print("Dry run complete. Use --execute to apply changes.")
    
    return 0 if errors == 0 else 1


def main():
    parser = argparse.ArgumentParser(
        description="Bulk rename files using regex pattern substitution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  %(prog)s '*.txt' --pattern '\\.txt$' --replace '.md'\n"
               "  %(prog)s '*.jpg' --pattern '^' --replace 'photo_' --execute"
    )
    parser.add_argument("glob", help="File glob pattern (e.g., '*.txt', 'IMG_*')")
    parser.add_argument("-p", "--pattern", required=True, help="Regex pattern to match")
    parser.add_argument("-r", "--replace", required=True, help="Replacement string")
    parser.add_argument("-d", "--directory", default=".", help="Directory to search in")
    parser.add_argument("-x", "--execute", action="store_true", 
                        help="Actually rename files (default is dry-run)")
    
    args = parser.parse_args()
    sys.exit(bulk_rename(args.glob, args.pattern, args.replace, args.execute, args.directory))


if __name__ == "__main__":
    main()
```
