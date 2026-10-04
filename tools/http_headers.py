```python
#!/usr/bin/env python3
"""
HTTP Headers Inspector - Fetch and display HTTP response headers for any URL.

Usage examples:
    python http_headers.py https://example.com
    python http_headers.py https://example.com -f content-type server
    python http_headers.py https://example.com --method HEAD
    python http_headers.py https://example.com --json
    python http_headers.py https://example.com -t 5
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from urllib.parse import urlparse


def fetch_headers(url, method="GET", timeout=10, follow_redirects=True):
    """Fetch HTTP headers from a URL."""
    if not urlparse(url).scheme:
        url = "https://" + url
    
    request = urllib.request.Request(url, method=method)
    request.add_header("User-Agent", "http-headers-cli/1.0")
    
    try:
        if follow_redirects:
            response = urllib.request.urlopen(request, timeout=timeout)
        else:
            opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
            response = opener.open(request, timeout=timeout)
        
        return {
            "status": response.status,
            "reason": response.reason,
            "headers": dict(response.headers),
            "url": response.url
        }
    except urllib.error.HTTPError as e:
        return {
            "status": e.code,
            "reason": e.reason,
            "headers": dict(e.headers),
            "url": url
        }


def display_headers(result, filter_keys=None, as_json=False):
    """Display headers in the requested format."""
    headers = result["headers"]
    
    if filter_keys:
        filter_lower = [k.lower() for k in filter_keys]
        headers = {k: v for k, v in headers.items() if k.lower() in filter_lower}
    
    if as_json:
        output = {
            "url": result["url"],
            "status": result["status"],
            "reason": result["reason"],
            "headers": headers
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"URL: {result['url']}")
        print(f"Status: {result['status']} {result['reason']}")
        print("-" * 50)
        for key, value in sorted(headers.items()):
            print(f"{key}: {value}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and display HTTP response headers for any URL"
    )
    parser.add_argument("url", help="URL to fetch headers from")
    parser.add_argument("-f", "--filter", nargs="+", metavar="HEADER",
                        help="Filter to show only specific headers")
    parser.add_argument("-m", "--method", default="GET", choices=["GET", "HEAD"],
                        help="HTTP method to use (default: GET)")
    parser.add_argument("-t", "--timeout", type=int, default=10,
                        help="Request timeout in seconds (default: 10)")
    parser.add_argument("--json", action="store_true",
                        help="Output in JSON format")
    parser.add_argument("--no-follow", action="store_true",
                        help="Do not follow redirects")
    
    args = parser.parse_args()
    
    try:
        result = fetch_headers(
            args.url,
            method=args.method,
            timeout=args.timeout,
            follow_redirects=not args.no_follow
        )
        display_headers(result, filter_keys=args.filter, as_json=args.json)
    except urllib.error.URLError as e:
        print(f"Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```
