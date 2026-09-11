```python
#!/usr/bin/env python3
"""
Remove duplicate lines from text files while preserving order.

Usage examples:
    # Remove duplicates and print to stdout
    python dedupe_lines.py input.txt

    # Remove duplicates and write to a new file
    python dedupe_lines.py input.txt -o output.txt

    # Remove duplicates in place (modifies original file)
    python dedupe_lines.py input.txt -i

    # Case-insensitive deduplication
    python dedupe_lines.py input.txt --ignore-case

    # Ignore leading/trailing whitespace when comparing
    python dedupe_lines.py input.txt --strip
"""

import argparse
import sys
from pathlib import Path


def dedupe_lines(lines, ignore_case=False, strip_whitespace=False):
    """Remove duplicate lines while preserving order of first occurrences."""
    seen = set()
    result = []

    for line in lines:
        # Create comparison key based on options
        key = line
        if strip_whitespace:
            key = key.strip()
        if ignore_case:
            key = key.lower()

        if key not in seen:
            seen.add(key)
            result.append(line)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Remove duplicate lines from text files preserving order."
    )
    parser.add_argument("input", help="Input file path (use - for stdin)")
    parser.add_argument("-o", "--output", help="Output file path (default: stdout)")
    parser.add_argument(
        "-i", "--in-place", action="store_true", help="Modify file in place"
    )
    parser.add_argument(
        "--ignore-case", action="store_true", help="Case-insensitive comparison"
    )
    parser.add_argument(
        "--strip", action="store_true", help="Ignore leading/trailing whitespace"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress statistics output"
    )

    args = parser.parse_args()

    if args.in_place and args.output:
        parser.error("Cannot use both --in-place and --output")

    if args.in_place and args.input == "-":
        parser.error("Cannot use --in-place with stdin")

    # Read input
    if args.input == "-":
        lines = sys.stdin.readlines()
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            sys.stderr.write(f"Error: File not found: {args.input}\n")
            sys.exit(1)
        lines = input_path.read_text().splitlines(keepends=True)

    # Process
    original_count = len(lines)
    deduped = dedupe_lines(lines, args.ignore_case, args.strip)
    removed_count = original_count - len(deduped)

    # Write output
    output_text = "".join(deduped)

    if args.in_place:
        Path(args.input).write_text(output_text)
    elif args.output:
        Path(args.output).write_text(output_text)
    else:
        sys.stdout.write(output_text)

    # Print statistics to stderr
    if not args.quiet:
        sys.stderr.write(
            f"Processed {original_count} lines, removed {removed_count} duplicates\n"
        )


if __name__ == "__main__":
    main()
```
