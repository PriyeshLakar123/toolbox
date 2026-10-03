```python
#!/usr/bin/env python3
"""
Cron expression explainer - converts cron syntax to human-readable text.

Usage:
    python cron_explain.py "*/15 * * * *"
    python cron_explain.py "0 9 * * 1-5" --next 5
    python cron_explain.py "30 2 1 * *"
"""

import argparse
from datetime import datetime, timedelta


def parse_field(field, min_val, max_val, names=None):
    """Parse a single cron field and return description."""
    if field == "*":
        return "every"
    
    if field.startswith("*/"):
        step = field[2:]
        return f"every {step}"
    
    if "-" in field and "/" not in field:
        start, end = field.split("-")
        if names:
            start = names.get(int(start), start)
            end = names.get(int(end), end)
        return f"{start} through {end}"
    
    if "," in field:
        parts = field.split(",")
        if names:
            parts = [names.get(int(p), p) for p in parts]
        return ", ".join(parts)
    
    if names and field.isdigit():
        return names.get(int(field), field)
    
    return field


def explain_cron(expr):
    """Convert cron expression to human-readable text."""
    parts = expr.strip().split()
    if len(parts) != 5:
        return "Invalid cron expression (expected 5 fields)"
    
    minute, hour, day, month, weekday = parts
    
    days_of_week = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
                    4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
    months = {1: "January", 2: "February", 3: "March", 4: "April",
              5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}
    
    result = []
    
    min_desc = parse_field(minute, 0, 59)
    hour_desc = parse_field(hour, 0, 23)
    
    if min_desc == "every" and hour_desc == "every":
        result.append("Every minute")
    elif min_desc.startswith("every ") and hour_desc == "every":
        result.append(f"Every {min_desc.split()[1]} minutes")
    elif min_desc == "every":
        result.append(f"Every minute during hour {hour_desc}")
    else:
        result.append(f"At minute {min_desc} past hour {hour_desc}")
    
    day_desc = parse_field(day, 1, 31)
    month_desc = parse_field(month, 1, 12, months)
    weekday_desc = parse_field(weekday, 0, 7, days_of_week)
    
    if day_desc != "every":
        result.append(f"on day {day_desc} of the month")
    if month_desc != "every":
        result.append(f"in {month_desc}")
    if weekday_desc != "every":
        result.append(f"on {weekday_desc}")
    
    return " ".join(result)


def get_next_runs(expr, count=5):
    """Estimate next run times (simplified, not fully accurate)."""
    parts = expr.strip().split()
    if len(parts) != 5:
        return []
    
    minute, hour = parts[0], parts[1]
    now = datetime.now()
    runs = []
    
    target_min = 0 if minute == "*" or minute.startswith("*/") else int(minute.split(",")[0].split("-")[0])
    target_hour = now.hour if hour == "*" else int(hour.split(",")[0].split("-")[0])
    
    candidate = now.replace(minute=target_min, second=0, microsecond=0)
    if hour != "*":
        candidate = candidate.replace(hour=target_hour)
    
    while len(runs) < count:
        if candidate > now:
            runs.append(candidate)
        candidate += timedelta(hours=1) if hour == "*" else timedelta(days=1)
    
    return runs


def main():
    parser = argparse.ArgumentParser(description="Explain cron expressions in plain English")
    parser.add_argument("expression", help="Cron expression (5 fields)")
    parser.add_argument("--next", "-n", type=int, default=0, help="Show next N run times")
    args = parser.parse_args()
    
    print(f"Expression: {args.expression}")
    print(f"Meaning: {explain_cron(args.expression)}")
    
    if args.next > 0:
        print(f"\nNext {args.next} runs (approximate):")
        for run in get_next_runs(args.expression, args.next):
            print(f"  {run.strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    main()
```
