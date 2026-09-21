```python
#!/usr/bin/env python3
"""
Converts between Unix timestamps and human-readable dates.

Usage examples:
    # Convert Unix timestamp to readable date
    python timestamp_convert.py 1699574400
    
    # Convert date string to Unix timestamp
    python timestamp_convert.py "2023-11-10 12:00:00"
    
    # Specify output format
    python timestamp_convert.py 1699574400 -f "%Y-%m-%d"
    
    # Use specific timezone offset (hours from UTC)
    python timestamp_convert.py 1699574400 -z -5
    
    # Get current timestamp
    python timestamp_convert.py --now
"""

import argparse
import sys
import time
from datetime import datetime, timezone, timedelta


def parse_input(value, tz_offset=0):
    """Try to parse input as timestamp or date string."""
    tz = timezone(timedelta(hours=tz_offset))
    
    # Try parsing as Unix timestamp
    try:
        ts = float(value)
        # Handle milliseconds
        if ts > 1e12:
            ts = ts / 1000
        dt = datetime.fromtimestamp(ts, tz=tz)
        return ("timestamp", ts, dt)
    except ValueError:
        pass
    
    # Try parsing as date string with common formats
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y",
        "%Y%m%d%H%M%S",
        "%Y%m%d",
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(value, fmt)
            dt = dt.replace(tzinfo=tz)
            ts = dt.timestamp()
            return ("datetime", ts, dt)
        except ValueError:
            continue
    
    return (None, None, None)


def format_output(ts, dt, fmt, input_type):
    """Format the conversion output."""
    lines = []
    
    if input_type == "timestamp":
        lines.append(f"Input timestamp: {int(ts)}")
        lines.append(f"Datetime: {dt.strftime(fmt)}")
    else:
        lines.append(f"Input datetime: {dt.strftime(fmt)}")
        lines.append(f"Unix timestamp: {int(ts)}")
        lines.append(f"Milliseconds: {int(ts * 1000)}")
    
    lines.append(f"ISO 8601: {dt.isoformat()}")
    lines.append(f"UTC: {dt.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Convert between Unix timestamps and human-readable dates"
    )
    parser.add_argument("value", nargs="?", help="Timestamp or date string to convert")
    parser.add_argument("-f", "--format", default="%Y-%m-%d %H:%M:%S",
                        help="Output date format (default: %%Y-%%m-%%d %%H:%%M:%%S)")
    parser.add_argument("-z", "--timezone", type=float, default=0,
                        help="Timezone offset from UTC in hours (default: 0)")
    parser.add_argument("--now", action="store_true", help="Show current timestamp")
    
    args = parser.parse_args()
    
    if args.now:
        now = datetime.now(timezone(timedelta(hours=args.timezone)))
        print(f"Current timestamp: {int(time.time())}")
        print(f"Current datetime: {now.strftime(args.format)}")
        print(f"ISO 8601: {now.isoformat()}")
        return 0
    
    if not args.value:
        parser.print_help()
        return 1
    
    input_type, ts, dt = parse_input(args.value, args.timezone)
    
    if input_type is None:
        print(f"Error: Could not parse '{args.value}' as timestamp or date", file=sys.stderr)
        return 1
    
    print(format_output(ts, dt, args.format, input_type))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
