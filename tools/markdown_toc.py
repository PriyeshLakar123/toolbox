```python
#!/usr/bin/env python3
"""
Generate a table of contents from markdown file headings.

Usage:
    python markdown_toc.py README.md
    python markdown_toc.py README.md --max-depth 2
    python markdown_toc.py README.md --min-depth 2 --max-depth 3
    python markdown_toc.py README.md --bullet "-"
    python markdown_toc.py README.md --numbered
"""

import argparse
import re
import sys
from pathlib import Path


def slugify(text):
    """Convert heading text to GitHub-style anchor slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')


def extract_headings(content, min_depth=1, max_depth=6):
    """Extract markdown headings from content."""
    headings = []
    in_code_block = False
    
    for line in content.splitlines():
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        
        if in_code_block:
            continue
        
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            
            if min_depth <= level <= max_depth:
                headings.append((level, text))
    
    return headings


def generate_toc(headings, bullet='*', numbered=False, indent_size=2):
    """Generate table of contents from headings."""
    if not headings:
        return ''
    
    min_level = min(h[0] for h in headings)
    lines = []
    counters = {}
    
    for level, text in headings:
        indent = ' ' * ((level - min_level) * indent_size)
        slug = slugify(text)
        
        if numbered:
            counters[level] = counters.get(level, 0) + 1
            for l in list(counters.keys()):
                if l > level:
                    del counters[l]
            prefix = f"{counters[level]}."
        else:
            prefix = bullet
        
        lines.append(f"{indent}{prefix} [{text}](#{slug})")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Generate a table of contents from markdown headings'
    )
    parser.add_argument('file', type=Path, help='Markdown file to process')
    parser.add_argument('--min-depth', type=int, default=1,
                        help='Minimum heading depth to include (default: 1)')
    parser.add_argument('--max-depth', type=int, default=6,
                        help='Maximum heading depth to include (default: 6)')
    parser.add_argument('--bullet', default='*',
                        help='Bullet character for list items (default: *)')
    parser.add_argument('--numbered', action='store_true',
                        help='Use numbered list instead of bullets')
    parser.add_argument('--indent', type=int, default=2,
                        help='Spaces per indent level (default: 2)')
    
    args = parser.parse_args()
    
    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        content = args.file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    headings = extract_headings(content, args.min_depth, args.max_depth)
    
    if not headings:
        print("No headings found in the specified depth range.", file=sys.stderr)
        sys.exit(0)
    
    toc = generate_toc(headings, args.bullet, args.numbered, args.indent)
    print(toc)


if __name__ == '__main__':
    main()
```
