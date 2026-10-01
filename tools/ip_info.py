```python
#!/usr/bin/env python3
"""
IP Info - Display local network interface information.

Usage:
    python ip_info.py              # Show all interfaces
    python ip_info.py -i eth0      # Show specific interface
    python ip_info.py --json       # Output as JSON
    python ip_info.py -4           # Show only IPv4 addresses
"""

import argparse
import json
import socket
import struct
import fcntl
import array
import sys

def get_interfaces():
    """Get list of network interface names."""
    max_interfaces = 128
    bytes_needed = max_interfaces * 32
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', b'\0' * bytes_needed)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        sock.fileno(),
        0x8912,  # SIOCGIFCONF
        struct.pack('iL', bytes_needed, names.buffer_info()[0])
    ))[0]
    namestr = names.tobytes()
    interfaces = []
    for i in range(0, outbytes, 40):
        name = namestr[i:i+16].split(b'\0', 1)[0].decode('utf-8')
        if name:
            interfaces.append(name)
    return list(set(interfaces))

def get_ip_address(ifname):
    """Get IPv4 address for interface."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            sock.fileno(), 0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24])
    except OSError:
        return None

def get_netmask(ifname):
    """Get netmask for interface."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            sock.fileno(), 0x891b,  # SIOCGIFNETMASK
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24])
    except OSError:
        return None

def get_mac_address(ifname):
    """Get MAC address for interface."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(sock.fileno(), 0x8927,  # SIOCGIFHWADDR
                          struct.pack('256s', ifname[:15].encode('utf-8')))
        return ':'.join('%02x' % b for b in info[18:24])
    except OSError:
        return None

def get_interface_info(ifname):
    """Get all info for a single interface."""
    return {
        'name': ifname,
        'ipv4': get_ip_address(ifname),
        'netmask': get_netmask(ifname),
        'mac': get_mac_address(ifname)
    }

def main():
    parser = argparse.ArgumentParser(description='Display network interface information')
    parser.add_argument('-i', '--interface', help='Show specific interface only')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('-4', '--ipv4-only', action='store_true', dest='ipv4_only',
                        help='Show only interfaces with IPv4 addresses')
    args = parser.parse_args()

    interfaces = get_interfaces()
    if args.interface:
        if args.interface not in interfaces:
            print(f"Error: Interface '{args.interface}' not found", file=sys.stderr)
            sys.exit(1)
        interfaces = [args.interface]

    results = [get_interface_info(iface) for iface in sorted(interfaces)]
    if args.ipv4_only:
        results = [r for r in results if r['ipv4']]

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for info in results:
            print(f"\n{info['name']}:")
            print(f"  IPv4:    {info['ipv4'] or 'N/A'}")
            print(f"  Netmask: {info['netmask'] or 'N/A'}")
            print(f"  MAC:     {info['mac'] or 'N/A'}")

if __name__ == '__main__':
    main()
```
