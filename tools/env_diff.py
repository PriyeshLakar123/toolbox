```python
#!/usr/bin/env python3
"""
env_diff - Compare two .env files and show differences

Usage:
    python env_diff.py .env.example .env.local
    python env_diff.py --show-values .env.dev .env.prod
    python env_diff.py --only-keys .env.example .env
"""

import argparse
import sys
from pathlib import Path


def parse_env_file(filepath):
    """Parse a .env file into a dictionary of key-value pairs."""
    env_vars = {}
    path = Path(filepath)
    
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    
    with open(path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            env_vars[key] = value
    
    return env_vars


def compare_envs(env1, env2):
    """Compare two env dictionaries and return differences."""
    keys1 = set(env1.keys())
    keys2 = set(env2.keys())
    
    added = keys2 - keys1
    removed = keys1 - keys2
    common = keys1 & keys2
    changed = {k for k in common if env1[k] != env2[k]}
    unchanged = common - changed
    
    return added, removed, changed, unchanged


def main():
    parser = argparse.ArgumentParser(
        description='Compare two .env files and show differences'
    )
    parser.add_argument('file1', help='First .env file (base)')
    parser.add_argument('file2', help='Second .env file (compare)')
    parser.add_argument('--show-values', '-v', action='store_true',
                        help='Show actual values (not just keys)')
    parser.add_argument('--only-keys', '-k', action='store_true',
                        help='Only show key names, no categories')
    
    args = parser.parse_args()
    
    env1 = parse_env_file(args.file1)
    env2 = parse_env_file(args.file2)
    
    added, removed, changed, unchanged = compare_envs(env1, env2)
    
    if args.only_keys:
        all_diff_keys = sorted(added | removed | changed)
        for key in all_diff_keys:
            print(key)
        return
    
    if added:
        print(f"\n+ ADDED in {args.file2} ({len(added)}):")
        for key in sorted(added):
            if args.show_values:
                print(f"  + {key}={env2[key]}")
            else:
                print(f"  + {key}")
    
    if removed:
        print(f"\n- REMOVED from {args.file2} ({len(removed)}):")
        for key in sorted(removed):
            if args.show_values:
                print(f"  - {key}={env1[key]}")
            else:
                print(f"  - {key}")
    
    if changed:
        print(f"\n~ CHANGED ({len(changed)}):")
        for key in sorted(changed):
            if args.show_values:
                print(f"  ~ {key}: '{env1[key]}' -> '{env2[key]}'")
            else:
                print(f"  ~ {key}")
    
    if not (added or removed or changed):
        print("No differences found.")
    else:
        print(f"\nSummary: {len(added)} added, {len(removed)} removed, "
              f"{len(changed)} changed, {len(unchanged)} unchanged")


if __name__ == '__main__':
    main()
```
