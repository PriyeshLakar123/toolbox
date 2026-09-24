```python
#!/usr/bin/env python3
"""
Text statistics analyzer - displays detailed stats about text files.

Usage:
    python text_stats.py file.txt
    python text_stats.py file.txt --top 20
    python text_stats.py file.txt --no-common
    cat file.txt | python text_stats.py -
"""

import argparse
import sys
import re
from collections import Counter

COMMON_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'must', 'it', 'its', 'this', 'that',
    'these', 'those', 'i', 'you', 'he', 'she', 'we', 'they', 'as', 'not'
}


def analyze_text(text, exclude_common=True, top_n=10):
    lines = text.splitlines()
    line_count = len(lines)
    char_count = len(text)
    char_no_space = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
    
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    word_count = len(words)
    
    if word_count > 0:
        avg_word_len = sum(len(w) for w in words) / word_count
    else:
        avg_word_len = 0
    
    if exclude_common:
        filtered_words = [w for w in words if w not in COMMON_WORDS]
    else:
        filtered_words = words
    
    word_freq = Counter(filtered_words).most_common(top_n)
    
    return {
        'lines': line_count,
        'words': word_count,
        'characters': char_count,
        'characters_no_space': char_no_space,
        'avg_word_length': avg_word_len,
        'top_words': word_freq
    }


def main():
    parser = argparse.ArgumentParser(description='Analyze text file statistics')
    parser.add_argument('file', help='Text file to analyze (use - for stdin)')
    parser.add_argument('--top', type=int, default=10, help='Number of top words to show')
    parser.add_argument('--no-common', action='store_true', 
                        help='Exclude common words from frequency analysis')
    args = parser.parse_args()
    
    if args.file == '-':
        text = sys.stdin.read()
        filename = 'stdin'
    else:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
            filename = args.file
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
    
    stats = analyze_text(text, exclude_common=args.no_common, top_n=args.top)
    
    print(f"\n=== Text Statistics: {filename} ===\n")
    print(f"  Lines:                {stats['lines']:,}")
    print(f"  Words:                {stats['words']:,}")
    print(f"  Characters:           {stats['characters']:,}")
    print(f"  Characters (no space):{stats['characters_no_space']:,}")
    print(f"  Avg word length:      {stats['avg_word_length']:.2f}")
    
    if stats['top_words']:
        filter_note = " (excluding common)" if args.no_common else ""
        print(f"\n  Top {len(stats['top_words'])} words{filter_note}:")
        for word, count in stats['top_words']:
            print(f"    {word:<20} {count:>5}")
    print()


if __name__ == '__main__':
    main()
```
