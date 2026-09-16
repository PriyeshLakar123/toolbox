```python
#!/usr/bin/env python3
"""
Hash Check - Compute and verify file checksums.

Usage examples:
    # Compute SHA256 hash (default)
    python hash_check.py myfile.txt
    
    # Compute MD5 hash
    python hash_check.py myfile.txt -a md5
    
    # Verify a file against a known hash
    python hash_check.py myfile.txt -v abc123def456...
    
    # Hash multiple files
    python hash_check.py file1.txt file2.txt file3.txt
    
    # Output in format suitable for checksum files
    python hash_check.py *.txt --format bsd
"""

import argparse
import hashlib
import sys
from pathlib import Path


def compute_hash(filepath: Path, algorithm: str, buffer_size: int = 65536) -> str:
    """Compute hash of a file using the specified algorithm."""
    hasher = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        while chunk := f.read(buffer_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def main():
    parser = argparse.ArgumentParser(
        description='Compute and verify file checksums',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('files', nargs='+', type=Path, help='Files to hash')
    parser.add_argument(
        '-a', '--algorithm',
        choices=['md5', 'sha1', 'sha256', 'sha512'],
        default='sha256',
        help='Hash algorithm (default: sha256)'
    )
    parser.add_argument(
        '-v', '--verify',
        metavar='HASH',
        help='Verify file against expected hash (single file only)'
    )
    parser.add_argument(
        '--format',
        choices=['simple', 'bsd'],
        default='simple',
        help='Output format: simple (hash  filename) or bsd (ALGO (file) = hash)'
    )
    
    args = parser.parse_args()
    
    if args.verify and len(args.files) > 1:
        print('Error: --verify can only be used with a single file', file=sys.stderr)
        sys.exit(1)
    
    exit_code = 0
    
    for filepath in args.files:
        if not filepath.exists():
            print(f'Error: {filepath} not found', file=sys.stderr)
            exit_code = 1
            continue
        
        if not filepath.is_file():
            print(f'Error: {filepath} is not a file', file=sys.stderr)
            exit_code = 1
            continue
        
        try:
            file_hash = compute_hash(filepath, args.algorithm)
        except PermissionError:
            print(f'Error: Permission denied reading {filepath}', file=sys.stderr)
            exit_code = 1
            continue
        
        if args.verify:
            expected = args.verify.lower().strip()
            if file_hash == expected:
                print(f'{filepath}: OK')
            else:
                print(f'{filepath}: FAILED')
                print(f'  Expected: {expected}')
                print(f'  Got:      {file_hash}')
                exit_code = 1
        else:
            if args.format == 'bsd':
                algo_name = args.algorithm.upper()
                print(f'{algo_name} ({filepath}) = {file_hash}')
            else:
                print(f'{file_hash}  {filepath}')
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
```
