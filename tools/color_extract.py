```python
#!/usr/bin/env python3
"""
Extract color codes from files or stdin.

Usage examples:
    python color_extract.py style.css
    python color_extract.py src/*.css --format hex
    cat index.html | python color_extract.py --format all
    python color_extract.py theme.scss --sort
"""

import argparse
import re
import sys
from collections import defaultdict

# Patterns for different color formats
PATTERNS = {
    'hex': re.compile(r'#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b'),
    'rgb': re.compile(r'rgba?\s*\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*(?:,\s*[\d.]+\s*)?\)'),
    'hsl': re.compile(r'hsla?\s*\(\s*\d{1,3}\s*,\s*\d{1,3}%\s*,\s*\d{1,3}%\s*(?:,\s*[\d.]+\s*)?\)'),
}


def extract_colors(text, formats):
    """Extract colors from text based on specified formats."""
    colors = defaultdict(set)
    for fmt in formats:
        if fmt in PATTERNS:
            matches = PATTERNS[fmt].findall(text)
            for match in matches:
                normalized = match.lower().replace(' ', '')
                colors[fmt].add(normalized)
    return colors


def hex_sort_key(color):
    """Sort key for hex colors by brightness."""
    color = color.lstrip('#')
    if len(color) == 3:
        color = ''.join(c * 2 for c in color)
    elif len(color) == 4:
        color = ''.join(c * 2 for c in color[:3])
    elif len(color) == 8:
        color = color[:6]
    try:
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        return r * 0.299 + g * 0.587 + b * 0.114
    except ValueError:
        return 0


def main():
    parser = argparse.ArgumentParser(description='Extract color codes from files')
    parser.add_argument('files', nargs='*', help='Files to scan (reads stdin if none)')
    parser.add_argument('--format', '-f', choices=['hex', 'rgb', 'hsl', 'all'],
                        default='all', help='Color format to extract (default: all)')
    parser.add_argument('--sort', '-s', action='store_true',
                        help='Sort hex colors by brightness')
    parser.add_argument('--count', '-c', action='store_true',
                        help='Show count of unique colors per format')
    args = parser.parse_args()

    formats = list(PATTERNS.keys()) if args.format == 'all' else [args.format]
    all_colors = defaultdict(set)

    if args.files:
        for filepath in args.files:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    colors = extract_colors(f.read(), formats)
                    for fmt, vals in colors.items():
                        all_colors[fmt].update(vals)
            except FileNotFoundError:
                print(f"Warning: {filepath} not found", file=sys.stderr)
    else:
        text = sys.stdin.read()
        all_colors = extract_colors(text, formats)

    total = 0
    for fmt in formats:
        colors = list(all_colors[fmt])
        if not colors:
            continue
        if args.sort and fmt == 'hex':
            colors.sort(key=hex_sort_key)
        else:
            colors.sort()
        print(f"[{fmt.upper()}]")
        for color in colors:
            print(f"  {color}")
        total += len(colors)
        print()

    if args.count:
        print(f"Total unique colors: {total}")


if __name__ == '__main__':
    main()
```
