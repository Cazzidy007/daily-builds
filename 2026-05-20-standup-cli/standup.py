"""standup — a tiny CLI for personal daily standups.

Usage:
    python standup.py add "Finished Bain thank-you note"
    python standup.py add "Prepping for AgeTech pitch" --type doing
    python standup.py add "Waiting on recruiter reply" --type blocked
    python standup.py today
    python standup.py week
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

LOG_FILE = Path.home() / ".standup.json"


def load_entries():
    if not LOG_FILE.exists():
        return []
    with open(LOG_FILE) as f:
        return json.load(f)


def save_entries(entries):
    with open(LOG_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def add_entry(text, entry_type):
    entries = load_entries()
    entries.append({
        "timestamp": datetime.now().isoformat(),
        "type": entry_type,
        "text": text,
    })
    save_entries(entries)
    print(f"  [{entry_type}] {text}")


def show_entries(since_days):
    entries = load_entries()
    cutoff = datetime.now() - timedelta(days=since_days)
    recent = [e for e in entries if datetime.fromisoformat(e["timestamp"]) >= cutoff]

    if not recent:
        print(f"No entries in the last {since_days} day(s).")
        return

    # Group by date
    by_date = {}
    for entry in recent:
        date = entry["timestamp"][:10]
        by_date.setdefault(date, []).append(entry)

    icons = {"done": "✓", "doing": "→", "blocked": "✗"}
    for date in sorted(by_date.keys(), reverse=True):
        print(f"\n{date}")
        print("-" * 40)
        for entry in by_date[date]:
            icon = icons.get(entry["type"], "·")
            print(f"  {icon} {entry['text']}")


def main():
    parser = argparse.ArgumentParser(description="Personal daily standup logger")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Add an entry")
    add.add_argument("text", help="What did you do / are doing / are blocked on")
    add.add_argument(
        "--type", "-t",
        choices=["done", "doing", "blocked"],
        default="done",
        help="Entry type (default: done)",
    )

    sub.add_parser("today", help="Show today's entries")
    sub.add_parser("week", help="Show this week's entries")

    args = parser.parse_args()

    if args.command == "add":
        add_entry(args.text, args.type)
    elif args.command == "today":
        show_entries(since_days=1)
    elif args.command == "week":
        show_entries(since_days=7)


if __name__ == "__main__":
    main()
