```python
#!/usr/bin/env python3
"""
Extract URLs from text files or stdin.

Usage examples:
    # Extract URLs from a file
    python url_extract.py document.txt

    # Extract URLs from multiple files
    python url_extract.py file1.txt file2.txt file3.html

    # Extract from stdin
    cat webpage.html | python url_extract.py

    # Filter by domain
    python url_extract.py logs.txt --domain github.com

    # Show only unique URLs (default), with counts
    python url_extract.py access.log --count

    # Include all occurrences (not deduplicated)
    python url_extract.py data.txt --all
"""

import argparse
import re
import sys
from collections import Counter
from urllib.parse import urlparse


URL_PATTERN = re.compile(
    r'https?://'
    r'(?:[\w-]+\.)+[a-zA-Z]{2,}'
    r'(?::\d+)?'
    r'(?:/[^\s<>"\'\)]*)?',
    re.IGNORECASE
)


def extract_urls(text):
    """Extract all URLs from text."""
    return URL_PATTERN.findall(text)


def filter_by_domain(urls, domain):
    """Filter URLs to only include those matching the given domain."""
    filtered = []
    for url in urls:
        parsed = urlparse(url)
        if parsed.netloc == domain or parsed.netloc.endswith('.' + domain):
            filtered.append(url)
    return filtered


def process_input(files):
    """Read from files or stdin and yield lines."""
    if not files or files == ['-']:
        yield from sys.stdin
    else:
        for filepath in files:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    yield from f
            except FileNotFoundError:
                print(f"Warning: file not found: {filepath}", file=sys.stderr)
            except PermissionError:
                print(f"Warning: permission denied: {filepath}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description='Extract URLs from text files or stdin.'
    )
    parser.add_argument('files', nargs='*', default=['-'],
                        help='Input files (default: stdin)')
    parser.add_argument('-d', '--domain', type=str,
                        help='Filter URLs by domain')
    parser.add_argument('-c', '--count', action='store_true',
                        help='Show occurrence count for each URL')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Show all URLs including duplicates')

    args = parser.parse_args()

    all_urls = []
    for line in process_input(args.files):
        all_urls.extend(extract_urls(line))

    if args.domain:
        all_urls = filter_by_domain(all_urls, args.domain)

    if not all_urls:
        return

    if args.all:
        for url in all_urls:
            print(url)
    elif args.count:
        counts = Counter(all_urls)
        for url, count in counts.most_common():
            print(f"{count:6d}  {url}")
    else:
        seen = set()
        for url in all_urls:
            if url not in seen:
                seen.add(url)
                print(url)


if __name__ == '__main__':
    main()
```
