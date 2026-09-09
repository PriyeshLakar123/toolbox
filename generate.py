"""
Generates one CLI tool per run and updates the toolkit README.
Prints the git commit message to stdout for the workflow to capture.
"""

import anthropic
import os
import re
import sys
from pathlib import Path


SYSTEM = "You are a pragmatic Python developer who writes small, sharp CLI utilities. Never use em dashes in any text output."

PROMPT = """\
Generate a self-contained Python CLI tool. Pick something genuinely useful — \
a file utility, text processor, data converter, productivity helper, or dev tool.

Avoid these already-generated tools (if any):
{existing_tools}

Respond in this exact format — no extra text:

NAME: <snake_case_tool_name>
DESCRIPTION: <one sentence, what it does>
COMMIT: <git commit message, lowercase, imperative, under 72 chars, no period>
CODE:
<python code here>

Requirements for the code:
- Fully functional, runnable Python
- Uses argparse or sys.argv for CLI interface
- stdlib only (or note pip installs in a comment at the top)
- 40–100 lines, clean and readable
- Includes a usage example in a comment"""


def existing_tools() -> list[str]:
    tools_dir = Path("tools")
    if not tools_dir.exists():
        return []
    return [p.stem for p in tools_dir.glob("*.py")]


def generate(existing: list[str]) -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    tool_list = ", ".join(existing) if existing else "none yet"

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        system=SYSTEM,
        messages=[{"role": "user", "content": PROMPT.format(existing_tools=tool_list)}],
    )

    raw = message.content[0].text.strip()

    name = re.search(r"^NAME:\s*(.+)$", raw, re.MULTILINE)
    desc = re.search(r"^DESCRIPTION:\s*(.+)$", raw, re.MULTILINE)
    commit = re.search(r"^COMMIT:\s*(.+)$", raw, re.MULTILINE)
    code_match = re.search(r"^CODE:\s*\n(.*)", raw, re.MULTILINE | re.DOTALL)

    if not all([name, desc, commit, code_match]):
        print("ERROR: unexpected response format", file=sys.stderr)
        print(raw, file=sys.stderr)
        sys.exit(1)

    return {
        "name": name.group(1).strip(),
        "description": desc.group(1).strip(),
        "commit": commit.group(1).strip(),
        "code": code_match.group(1).strip(),
    }


def save(tool: dict) -> str:
    Path("tools").mkdir(exist_ok=True)
    path = f"tools/{tool['name']}.py"
    with open(path, "w") as f:
        f.write(tool["code"] + "\n")
    return path


def update_readme(tool: dict, path: str) -> None:
    marker = "| --- | --- |\n"
    entry = f"| [{tool['name']}.py]({path}) | {tool['description']} |\n"

    try:
        content = Path("README.md").read_text()
    except FileNotFoundError:
        content = (
            "# CLI Toolkit\n\n"
            "A growing collection of small, useful Python CLI tools — one added every day.\n\n"
            "## Tools\n\n"
            "| Script | Description |\n"
            f"{marker}"
        )

    if entry not in content:
        content = content.replace(marker, marker + entry, 1)
        Path("README.md").write_text(content)


if __name__ == "__main__":
    existing = existing_tools()
    tool = generate(existing)
    path = save(tool)
    update_readme(tool, path)
    # print commit message for the workflow to capture
    print(tool["commit"])
