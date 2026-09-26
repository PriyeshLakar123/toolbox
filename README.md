# CLI Toolkit

A growing collection of small, useful Python CLI tools =

Powered by [Claude](https://anthropic.com).

## Tools

| Script | Description |
| --- | --- |
| [url_extract.py](tools/url_extract.py) | Extracts and deduplicates all URLs from text files or stdin, with optional filtering by domain. |
| [snippet_extract.py](tools/snippet_extract.py) | Extracts code blocks from markdown files and saves them as individual files with proper extensions. |
| [text_stats.py](tools/text_stats.py) | Analyzes text files and displays word count, character count, line count, average word length, and most common words. |
| [find_dupes.py](tools/find_dupes.py) | Finds duplicate files in a directory tree by comparing file hashes, with options to filter by size or extension. |
| [timestamp_convert.py](tools/timestamp_convert.py) | Converts between Unix timestamps and human-readable dates in various formats and timezones. |
| [env_diff.py](tools/env_diff.py) | Compares two .env files and shows added, removed, and changed variables between them. |
| [todo_tracker.py](tools/todo_tracker.py) | A lightweight CLI todo list manager with add, list, complete, and delete operations stored in a JSON file. |
| [csv_stats.py](tools/csv_stats.py) | Quickly compute summary statistics (count, min, max, mean, median) for numeric columns in a CSV file. |
| [log_tail.py](tools/log_tail.py) | Monitors log files in real-time with optional pattern highlighting and filtering. |
| [hash_check.py](tools/hash_check.py) | Computes and verifies file checksums using MD5, SHA1, or SHA256 algorithms. |
| [dir_tree.py](tools/dir_tree.py) | Prints a visual directory tree structure with optional depth limit and file size display. |
| [filewatch.py](tools/filewatch.py) | Monitors a file or directory for changes and executes a command when modifications are detected. |
| [port_scanner.py](tools/port_scanner.py) | Scans a host for open TCP ports within a specified range with configurable timeout and threading. |
| [json2csv.py](tools/json2csv.py) | Converts JSON files (array of objects or newline-delimited JSON) to CSV format with automatic header detection. |
| [dedupe_lines.py](tools/dedupe_lines.py) | Removes duplicate lines from text files while preserving the original order of first occurrences. |
| [bulk_rename.py](tools/bulk_rename.py) | Batch rename files using pattern matching with preview and regex support. |
