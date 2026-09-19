```python
#!/usr/bin/env python3
"""
Simple CLI todo tracker with persistent JSON storage.

Usage examples:
    python todo_tracker.py add "Buy groceries"
    python todo_tracker.py add "Finish report" --priority high
    python todo_tracker.py list
    python todo_tracker.py list --filter pending
    python todo_tracker.py done 1
    python todo_tracker.py delete 2
    python todo_tracker.py clear --completed
"""

import argparse
import json
from pathlib import Path
from datetime import datetime

TODO_FILE = Path.home() / ".todos.json"


def load_todos():
    if TODO_FILE.exists():
        return json.loads(TODO_FILE.read_text())
    return []


def save_todos(todos):
    TODO_FILE.write_text(json.dumps(todos, indent=2))


def add_todo(args):
    todos = load_todos()
    todo = {
        "id": max((t["id"] for t in todos), default=0) + 1,
        "task": args.task,
        "priority": args.priority,
        "done": False,
        "created": datetime.now().isoformat()
    }
    todos.append(todo)
    save_todos(todos)
    print(f"Added todo #{todo['id']}: {args.task}")


def list_todos(args):
    todos = load_todos()
    if args.filter == "pending":
        todos = [t for t in todos if not t["done"]]
    elif args.filter == "completed":
        todos = [t for t in todos if t["done"]]
    
    if not todos:
        print("No todos found.")
        return
    
    for t in todos:
        status = "[x]" if t["done"] else "[ ]"
        pri = f"({t['priority'][0].upper()})" if t.get("priority") != "normal" else "   "
        print(f"{t['id']:3} {status} {pri} {t['task']}")


def mark_done(args):
    todos = load_todos()
    for t in todos:
        if t["id"] == args.id:
            t["done"] = True
            save_todos(todos)
            print(f"Marked #{args.id} as done.")
            return
    print(f"Todo #{args.id} not found.")


def delete_todo(args):
    todos = load_todos()
    new_todos = [t for t in todos if t["id"] != args.id]
    if len(new_todos) == len(todos):
        print(f"Todo #{args.id} not found.")
    else:
        save_todos(new_todos)
        print(f"Deleted todo #{args.id}.")


def clear_todos(args):
    todos = load_todos()
    if args.completed:
        todos = [t for t in todos if not t["done"]]
        save_todos(todos)
        print("Cleared completed todos.")
    else:
        save_todos([])
        print("Cleared all todos.")


def main():
    parser = argparse.ArgumentParser(description="Simple CLI todo tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_p = subparsers.add_parser("add", help="Add a new todo")
    add_p.add_argument("task", help="Task description")
    add_p.add_argument("--priority", "-p", choices=["low", "normal", "high"], default="normal")
    add_p.set_defaults(func=add_todo)

    list_p = subparsers.add_parser("list", help="List todos")
    list_p.add_argument("--filter", "-f", choices=["all", "pending", "completed"], default="all")
    list_p.set_defaults(func=list_todos)

    done_p = subparsers.add_parser("done", help="Mark todo as completed")
    done_p.add_argument("id", type=int, help="Todo ID")
    done_p.set_defaults(func=mark_done)

    del_p = subparsers.add_parser("delete", help="Delete a todo")
    del_p.add_argument("id", type=int, help="Todo ID")
    del_p.set_defaults(func=delete_todo)

    clear_p = subparsers.add_parser("clear", help="Clear todos")
    clear_p.add_argument("--completed", "-c", action="store_true", help="Only clear completed")
    clear_p.set_defaults(func=clear_todos)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
```
