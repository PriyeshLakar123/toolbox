```python
#!/usr/bin/env python3
"""
Generate .gitignore files from built-in templates.

Usage:
    python gitignore_gen.py python           # Print Python gitignore to stdout
    python gitignore_gen.py python node -o   # Write combined template to .gitignore
    python gitignore_gen.py --list           # List available templates
    python gitignore_gen.py python --append  # Append to existing .gitignore
"""

import argparse
import sys
from pathlib import Path

TEMPLATES = {
    "python": """__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
*.egg-info/
dist/
build/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/""",
    "node": """node_modules/
npm-debug.log*
yarn-error.log
.npm
.yarn/cache
dist/
.env
.env.local""",
    "rust": """target/
Cargo.lock
**/*.rs.bk""",
    "go": """bin/
pkg/
*.exe
*.test
*.out
vendor/""",
    "java": """*.class
*.jar
*.war
target/
.gradle/
build/
.idea/
*.iml""",
    "c": """*.o
*.a
*.so
*.out
*.exe
build/
cmake-build-*/""",
    "general": """.DS_Store
Thumbs.db
*.swp
*.swo
*~
.idea/
.vscode/
*.log
.env
.env.local""",
}


def list_templates():
    print("Available templates:")
    for name in sorted(TEMPLATES.keys()):
        lines = len(TEMPLATES[name].strip().split("\n"))
        print(f"  {name:12} ({lines} patterns)")


def generate_gitignore(names):
    sections = []
    for name in names:
        if name not in TEMPLATES:
            print(f"Warning: unknown template '{name}', skipping", file=sys.stderr)
            continue
        sections.append(f"# --- {name} ---\n{TEMPLATES[name]}")
    return "\n\n".join(sections)


def main():
    parser = argparse.ArgumentParser(
        description="Generate .gitignore files from templates"
    )
    parser.add_argument("templates", nargs="*", help="Template names to include")
    parser.add_argument("--list", "-l", action="store_true", help="List templates")
    parser.add_argument("--output", "-o", action="store_true", help="Write to .gitignore")
    parser.add_argument("--append", "-a", action="store_true", help="Append to .gitignore")

    args = parser.parse_args()

    if args.list:
        list_templates()
        return

    if not args.templates:
        parser.print_help()
        return

    content = generate_gitignore(args.templates)
    if not content:
        sys.exit(1)

    if args.output or args.append:
        gitignore = Path(".gitignore")
        mode = "a" if args.append else "w"
        prefix = "\n\n" if args.append and gitignore.exists() else ""
        with open(gitignore, mode) as f:
            f.write(prefix + content + "\n")
        action = "Appended to" if args.append else "Created"
        print(f"{action} .gitignore with: {', '.join(args.templates)}")
    else:
        print(content)


if __name__ == "__main__":
    main()
```
