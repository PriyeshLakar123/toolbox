```python
#!/usr/bin/env python3
"""
Extract code blocks from markdown files and save as individual files.

Usage:
    python snippet_extract.py README.md
    python snippet_extract.py README.md -o snippets/
    python snippet_extract.py README.md --list
    python snippet_extract.py docs/*.md -o extracted/
"""

import argparse
import re
import sys
from pathlib import Path


def extract_code_blocks(content):
    """Extract fenced code blocks with their language identifiers."""
    pattern = r'```(\w+)?\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    blocks = []
    for lang, code in matches:
        lang = lang.strip() if lang else 'txt'
        code = code.rstrip('\n')
        if code:
            blocks.append((lang, code))
    return blocks


def get_extension(lang):
    """Map language identifiers to file extensions."""
    mapping = {
        'python': 'py', 'py': 'py',
        'javascript': 'js', 'js': 'js',
        'typescript': 'ts', 'ts': 'ts',
        'bash': 'sh', 'shell': 'sh', 'sh': 'sh',
        'ruby': 'rb', 'rb': 'rb',
        'rust': 'rs', 'rs': 'rs',
        'go': 'go', 'golang': 'go',
        'java': 'java',
        'c': 'c', 'cpp': 'cpp', 'c++': 'cpp',
        'html': 'html', 'css': 'css',
        'json': 'json', 'yaml': 'yaml', 'yml': 'yml',
        'sql': 'sql', 'xml': 'xml',
        'dockerfile': 'dockerfile',
    }
    return mapping.get(lang.lower(), lang.lower() or 'txt')


def process_file(md_path, output_dir, list_only=False):
    """Process a single markdown file."""
    content = Path(md_path).read_text(encoding='utf-8')
    blocks = extract_code_blocks(content)
    
    if not blocks:
        print(f"No code blocks found in {md_path}")
        return 0
    
    base_name = Path(md_path).stem
    
    for i, (lang, code) in enumerate(blocks, 1):
        ext = get_extension(lang)
        filename = f"{base_name}_{i:02d}.{ext}"
        
        if list_only:
            lines = len(code.splitlines())
            print(f"  [{i}] {lang}: {lines} lines -> {filename}")
        else:
            out_path = output_dir / filename
            out_path.write_text(code + '\n', encoding='utf-8')
            print(f"  Saved: {out_path}")
    
    return len(blocks)


def main():
    parser = argparse.ArgumentParser(
        description='Extract code blocks from markdown files'
    )
    parser.add_argument('files', nargs='+', help='Markdown files to process')
    parser.add_argument('-o', '--output', default='.', 
                        help='Output directory (default: current)')
    parser.add_argument('--list', action='store_true',
                        help='List blocks without extracting')
    
    args = parser.parse_args()
    output_dir = Path(args.output)
    
    if not args.list:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    total = 0
    for pattern in args.files:
        for md_file in Path('.').glob(pattern) if '*' in pattern else [Path(pattern)]:
            if not md_file.exists():
                print(f"File not found: {md_file}", file=sys.stderr)
                continue
            print(f"Processing: {md_file}")
            total += process_file(md_file, output_dir, args.list)
    
    action = "Found" if args.list else "Extracted"
    print(f"\n{action} {total} code block(s)")


if __name__ == '__main__':
    main()
```
