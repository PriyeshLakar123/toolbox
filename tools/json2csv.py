```python
#!/usr/bin/env python3
"""
Convert JSON to CSV format.

Usage examples:
    # Convert a JSON array file to CSV
    python json2csv.py data.json -o output.csv
    
    # Convert newline-delimited JSON (NDJSON) to CSV
    python json2csv.py logs.ndjson --ndjson -o logs.csv
    
    # Output to stdout
    python json2csv.py data.json
    
    # Select specific fields only
    python json2csv.py data.json --fields name,email,age
"""

import argparse
import csv
import json
import sys
from typing import TextIO


def load_json_records(input_file: TextIO, ndjson: bool = False) -> list[dict]:
    """Load records from JSON array or newline-delimited JSON."""
    if ndjson:
        records = []
        for line in input_file:
            line = line.strip()
            if line:
                records.append(json.loads(line))
        return records
    else:
        data = json.load(input_file)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
        else:
            raise ValueError("JSON must be an array of objects or a single object")


def extract_headers(records: list[dict], fields: list[str] | None = None) -> list[str]:
    """Extract all unique keys from records, preserving order of first appearance."""
    if fields:
        return fields
    
    seen = set()
    headers = []
    for record in records:
        for key in record.keys():
            if key not in seen:
                seen.add(key)
                headers.append(key)
    return headers


def flatten_value(value) -> str:
    """Convert a value to a string suitable for CSV."""
    if value is None:
        return ""
    elif isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    else:
        return str(value)


def convert_json_to_csv(records: list[dict], output: TextIO, fields: list[str] | None = None):
    """Write records as CSV to output stream."""
    if not records:
        return
    
    headers = extract_headers(records, fields)
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(headers)
    
    for record in records:
        row = [flatten_value(record.get(h)) for h in headers]
        writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(
        description="Convert JSON to CSV format",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", help="Input JSON file (use - for stdin)")
    parser.add_argument("-o", "--output", help="Output CSV file (default: stdout)")
    parser.add_argument("--ndjson", action="store_true", 
                        help="Input is newline-delimited JSON")
    parser.add_argument("--fields", 
                        help="Comma-separated list of fields to include")
    
    args = parser.parse_args()
    
    fields = args.fields.split(",") if args.fields else None
    
    try:
        if args.input == "-":
            records = load_json_records(sys.stdin, args.ndjson)
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                records = load_json_records(f, args.ndjson)
        
        if args.output:
            with open(args.output, "w", encoding="utf-8", newline="") as f:
                convert_json_to_csv(records, f, fields)
            print(f"Converted {len(records)} records to {args.output}", file=sys.stderr)
        else:
            convert_json_to_csv(records, sys.stdout, fields)
            
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File not found - {args.input}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```
