```python
#!/usr/bin/env python3
"""
Real-time log file monitor with pattern highlighting and filtering.

Usage examples:
    python log_tail.py /var/log/syslog
    python log_tail.py app.log --filter ERROR
    python log_tail.py app.log --highlight "ERROR|WARN" --lines 50
    python log_tail.py server.log --filter "status=5\d{2}" --highlight "500|502|503"
"""

import argparse
import re
import sys
import time
from pathlib import Path

COLORS = {
    'red': '\033[91m',
    'yellow': '\033[93m',
    'reset': '\033[0m',
    'bold': '\033[1m',
}


def highlight_matches(line: str, pattern: re.Pattern) -> str:
    """Highlight matching patterns in the line."""
    def replacer(match):
        return f"{COLORS['bold']}{COLORS['red']}{match.group()}{COLORS['reset']}"
    return pattern.sub(replacer, line)


def tail_file(filepath: Path, num_lines: int) -> list[str]:
    """Get the last n lines of a file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
            return lines[-num_lines:] if len(lines) > num_lines else lines
    except FileNotFoundError:
        return []


def follow_file(filepath: Path, filter_pattern: re.Pattern | None,
                highlight_pattern: re.Pattern | None) -> None:
    """Follow a file and print new lines as they appear."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        f.seek(0, 2)  # Go to end of file
        while True:
            line = f.readline()
            if line:
                if filter_pattern and not filter_pattern.search(line):
                    continue
                output = line.rstrip('\n')
                if highlight_pattern:
                    output = highlight_matches(output, highlight_pattern)
                print(output)
            else:
                time.sleep(0.1)


def main():
    parser = argparse.ArgumentParser(
        description='Monitor log files with filtering and highlighting'
    )
    parser.add_argument('file', type=Path, help='Log file to monitor')
    parser.add_argument('-n', '--lines', type=int, default=10,
                        help='Number of initial lines to show (default: 10)')
    parser.add_argument('-f', '--filter', dest='filter_re',
                        help='Regex pattern to filter lines')
    parser.add_argument('--highlight', dest='highlight_re',
                        help='Regex pattern to highlight in output')
    parser.add_argument('--no-follow', action='store_true',
                        help='Print lines and exit without following')
    args = parser.parse_args()

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    filter_pattern = re.compile(args.filter_re) if args.filter_re else None
    highlight_pattern = re.compile(args.highlight_re) if args.highlight_re else None

    # Show initial lines
    initial_lines = tail_file(args.file, args.lines)
    for line in initial_lines:
        line = line.rstrip('\n')
        if filter_pattern and not filter_pattern.search(line):
            continue
        if highlight_pattern:
            line = highlight_matches(line, highlight_pattern)
        print(line)

    if args.no_follow:
        return

    # Follow the file
    try:
        print(f"{COLORS['yellow']}--- Following {args.file} (Ctrl+C to stop) ---{COLORS['reset']}")
        follow_file(args.file, filter_pattern, highlight_pattern)
    except KeyboardInterrupt:
        print(f"\n{COLORS['yellow']}Stopped.{COLORS['reset']}")


if __name__ == '__main__':
    main()
```
