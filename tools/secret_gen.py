```python
#!/usr/bin/env python3
"""
Generate cryptographically secure passwords, tokens, and secrets.

Usage examples:
    python secret_gen.py                      # 16-char password with all chars
    python secret_gen.py -l 32               # 32-char password
    python secret_gen.py -t hex -l 64        # 64-char hex token
    python secret_gen.py -t alpha -l 24      # 24-char alphanumeric
    python secret_gen.py -n 5                # generate 5 passwords
    python secret_gen.py -t urlsafe -l 32    # URL-safe base64 token
    python secret_gen.py --no-symbols        # password without special chars
"""

import argparse
import secrets
import string


def generate_password(length: int, use_symbols: bool = True) -> str:
    """Generate a password with letters, digits, and optionally symbols."""
    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))


def generate_hex_token(length: int) -> str:
    """Generate a hexadecimal token."""
    byte_length = (length + 1) // 2
    return secrets.token_hex(byte_length)[:length]


def generate_urlsafe_token(length: int) -> str:
    """Generate a URL-safe base64 token."""
    byte_length = (length * 3 + 3) // 4
    return secrets.token_urlsafe(byte_length)[:length]


def generate_alphanumeric(length: int) -> str:
    """Generate an alphanumeric string."""
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def generate_numeric_pin(length: int) -> str:
    """Generate a numeric PIN."""
    return ''.join(secrets.choice(string.digits) for _ in range(length))


def main():
    parser = argparse.ArgumentParser(
        description="Generate cryptographically secure passwords and tokens"
    )
    parser.add_argument(
        "-l", "--length", type=int, default=16,
        help="Length of generated secret (default: 16)"
    )
    parser.add_argument(
        "-t", "--type", choices=["password", "hex", "urlsafe", "alpha", "pin"],
        default="password", help="Type of secret to generate (default: password)"
    )
    parser.add_argument(
        "-n", "--count", type=int, default=1,
        help="Number of secrets to generate (default: 1)"
    )
    parser.add_argument(
        "--no-symbols", action="store_true",
        help="Exclude symbols from password generation"
    )
    
    args = parser.parse_args()
    
    if args.length < 1:
        parser.error("Length must be at least 1")
    
    generators = {
        "password": lambda: generate_password(args.length, not args.no_symbols),
        "hex": lambda: generate_hex_token(args.length),
        "urlsafe": lambda: generate_urlsafe_token(args.length),
        "alpha": lambda: generate_alphanumeric(args.length),
        "pin": lambda: generate_numeric_pin(args.length),
    }
    
    generator = generators[args.type]
    
    for _ in range(args.count):
        print(generator())


if __name__ == "__main__":
    main()
```
