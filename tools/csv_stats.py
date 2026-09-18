```python
#!/usr/bin/env python3
"""
csv_stats - Compute summary statistics for numeric columns in a CSV file.

Usage:
    python csv_stats.py data.csv
    python csv_stats.py data.csv --columns price,quantity
    python csv_stats.py data.csv -c revenue --no-header
"""

import argparse
import csv
import sys
from statistics import mean, median


def is_numeric(value):
    """Check if a string value can be converted to float."""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def compute_stats(values):
    """Compute statistics for a list of numeric values."""
    if not values:
        return None
    nums = [float(v) for v in values if is_numeric(v)]
    if not nums:
        return None
    return {
        'count': len(nums),
        'min': min(nums),
        'max': max(nums),
        'mean': round(mean(nums), 4),
        'median': round(median(nums), 4),
        'sum': round(sum(nums), 4)
    }


def main():
    parser = argparse.ArgumentParser(
        description='Compute summary statistics for numeric columns in a CSV file.'
    )
    parser.add_argument('file', help='Path to CSV file')
    parser.add_argument('-c', '--columns', help='Comma-separated list of columns to analyze')
    parser.add_argument('--no-header', action='store_true', help='CSV has no header row')
    parser.add_argument('-d', '--delimiter', default=',', help='CSV delimiter (default: comma)')
    args = parser.parse_args()

    try:
        with open(args.file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=args.delimiter)
            rows = list(reader)
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    if not rows:
        print("Error: Empty CSV file", file=sys.stderr)
        sys.exit(1)

    if args.no_header:
        headers = [f'col_{i}' for i in range(len(rows[0]))]
        data_rows = rows
    else:
        headers = rows[0]
        data_rows = rows[1:]

    columns_data = {h: [] for h in headers}
    for row in data_rows:
        for i, val in enumerate(row):
            if i < len(headers):
                columns_data[headers[i]].append(val)

    target_cols = headers
    if args.columns:
        target_cols = [c.strip() for c in args.columns.split(',')]
        invalid = [c for c in target_cols if c not in headers]
        if invalid:
            print(f"Error: Unknown columns: {', '.join(invalid)}", file=sys.stderr)
            sys.exit(1)

    print(f"{'Column':<20} {'Count':>8} {'Min':>12} {'Max':>12} {'Mean':>12} {'Median':>12} {'Sum':>14}")
    print("-" * 92)

    found_numeric = False
    for col in target_cols:
        stats = compute_stats(columns_data[col])
        if stats:
            found_numeric = True
            print(f"{col:<20} {stats['count']:>8} {stats['min']:>12.4g} {stats['max']:>12.4g} "
                  f"{stats['mean']:>12.4g} {stats['median']:>12.4g} {stats['sum']:>14.4g}")

    if not found_numeric:
        print("No numeric columns found.", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
```
