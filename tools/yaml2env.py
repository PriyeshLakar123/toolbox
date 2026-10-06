```python
#!/usr/bin/env python3
# pip install pyyaml
"""
Convert YAML config files to shell environment variable exports.

Usage:
    python yaml2env.py config.yaml
    python yaml2env.py config.yaml --prefix APP
    python yaml2env.py config.yaml --export
    python yaml2env.py config.yaml --output .env
    
    # Source directly in bash:
    eval "$(python yaml2env.py config.yaml --export)"
"""

import argparse
import sys

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def flatten_dict(d, parent_key='', sep='_'):
    """Flatten nested dict into single-level dict with joined keys."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        elif isinstance(v, list):
            items.append((new_key, ','.join(str(i) for i in v)))
        else:
            items.append((new_key, v))
    return dict(items)


def to_env_name(key, prefix=None):
    """Convert key to valid env var name (uppercase, underscores)."""
    name = key.upper().replace('-', '_').replace('.', '_')
    name = ''.join(c if c.isalnum() or c == '_' else '_' for c in name)
    if prefix:
        return f"{prefix.upper()}_{name}"
    return name


def format_value(value):
    """Format value for shell, quoting strings with spaces or special chars."""
    if value is None:
        return '""'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    str_val = str(value)
    if not str_val or any(c in str_val for c in ' \t\n"\'$`\\!'):
        escaped = str_val.replace("'", "'\"'\"'")
        return f"'{escaped}'"
    return str_val


def main():
    parser = argparse.ArgumentParser(
        description='Convert YAML config to environment variables'
    )
    parser.add_argument('file', help='YAML file to convert')
    parser.add_argument('--prefix', '-p', help='Prefix for all variable names')
    parser.add_argument('--export', '-e', action='store_true',
                        help='Add export keyword for shell sourcing')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    args = parser.parse_args()

    try:
        with open(args.file, 'r') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, dict):
        print("Error: YAML root must be a mapping/dict", file=sys.stderr)
        sys.exit(1)

    flat = flatten_dict(data)
    lines = []
    
    for key, value in flat.items():
        env_name = to_env_name(key, args.prefix)
        env_value = format_value(value)
        if args.export:
            lines.append(f"export {env_name}={env_value}")
        else:
            lines.append(f"{env_name}={env_value}")

    output = '\n'.join(lines)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output + '\n')
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
```
