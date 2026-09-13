```python
#!/usr/bin/env python3
"""
Simple TCP port scanner with multithreading support.

Usage examples:
    python port_scanner.py localhost
    python port_scanner.py 192.168.1.1 -p 20-100
    python port_scanner.py example.com -p 80,443,8080
    python port_scanner.py 10.0.0.1 -p 1-1000 -t 0.5 -w 50
"""

import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple


def parse_ports(port_spec: str) -> List[int]:
    """Parse port specification like '80', '20-100', or '80,443,8080'."""
    ports = []
    for part in port_spec.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-', 1)
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return sorted(set(ports))


def scan_port(host: str, port: int, timeout: float) -> Tuple[int, bool]:
    """Attempt to connect to a single port. Returns (port, is_open)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return (port, result == 0)
    except (socket.error, OSError):
        return (port, False)


def scan_ports(host: str, ports: List[int], timeout: float, workers: int) -> List[int]:
    """Scan multiple ports using thread pool. Returns list of open ports."""
    open_ports = []
    total = len(ports)
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(scan_port, host, port, timeout): port for port in ports}
        
        for i, future in enumerate(as_completed(futures), 1):
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
                print(f"  Port {port}: OPEN")
            
            if i % 100 == 0 or i == total:
                print(f"  Progress: {i}/{total} ports scanned", end='\r')
    
    print()  # Clear progress line
    return sorted(open_ports)


def main():
    parser = argparse.ArgumentParser(
        description='Scan a host for open TCP ports.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('host', help='Target hostname or IP address')
    parser.add_argument('-p', '--ports', default='1-1024',
                        help='Port specification: single (80), range (20-100), or list (80,443,8080)')
    parser.add_argument('-t', '--timeout', type=float, default=1.0,
                        help='Connection timeout in seconds (default: 1.0)')
    parser.add_argument('-w', '--workers', type=int, default=100,
                        help='Number of concurrent threads (default: 100)')
    
    args = parser.parse_args()
    
    try:
        ports = parse_ports(args.ports)
    except ValueError as e:
        print(f"Error parsing ports: {e}")
        return 1
    
    print(f"Scanning {args.host} ({len(ports)} ports)...")
    print(f"Timeout: {args.timeout}s, Workers: {args.workers}")
    print("-" * 40)
    
    open_ports = scan_ports(args.host, ports, args.timeout, args.workers)
    
    print("-" * 40)
    if open_ports:
        print(f"Found {len(open_ports)} open port(s): {', '.join(map(str, open_ports))}")
    else:
        print("No open ports found.")
    
    return 0


if __name__ == '__main__':
    exit(main())
```
