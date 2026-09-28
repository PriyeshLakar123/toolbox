```python
#!/usr/bin/env python3
"""
Flatten nested JSON into dot-notation key-value pairs.

Usage:
    echo '{"a": {"b": 1, "c": [2,3]}}' | python json_flatten.py
    python json_flatten.py input.json
    python json_flatten.py input.json -o flat.json
    python json_flatten.py input.json --separator /
"""

import argparse
import json
import sys
from typing import Any


def flatten(obj: Any, parent_key: str = "", sep: str = ".") -> dict:
    """Recursively flatten a nested dict/list structure."""
    items = {}
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            items.update(flatten(value, new_key, sep))
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            new_key = f"{parent_key}[{idx}]"
            items.update(flatten(value, new_key, sep))
    else:
        items[parent_key] = obj
    
    return items


def main():
    parser = argparse.ArgumentParser(
        description="Flatten nested JSON into dot-notation key-value pairs"
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Input JSON file (reads from stdin if not provided)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file (prints to stdout if not provided)"
    )
    parser.add_argument(
        "-s", "--separator",
        default=".",
        help="Key separator (default: '.')"
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Output as key=value lines instead of JSON"
    )
    
    args = parser.parse_args()
    
    # Read input
    if args.input:
        with open(args.input, "r") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)
    
    # Flatten
    flattened = flatten(data, sep=args.separator)
    
    # Format output
    if args.raw:
        output_lines = []
        for key, value in flattened.items():
            if isinstance(value, str):
                output_lines.append(f'{key}="{value}"')
            elif value is None:
                output_lines.append(f"{key}=null")
            elif isinstance(value, bool):
                output_lines.append(f"{key}={str(value).lower()}")
            else:
                output_lines.append(f"{key}={value}")
        output = "\n".join(output_lines)
    else:
        output = json.dumps(flattened, indent=2)
    
    # Write output
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
            f.write("\n")
    else:
        print(output)


if __name__ == "__main__":
    main()
```
