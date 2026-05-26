"""standup — a tiny CLI for personal daily standups.

Usage:
    python standup.py add "Finished Bain thank-you" --tag job-search
    python standup.py add "Prepping AgeTech pitch" --type doing --tag good-grief
    python standup.py today
    python standup.py week
    python standup.py week --tag job-search
    python standup.py digest         # weekly markdown digest to stdout
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


def add_entry(text, entry_type, tag):
    entries = load_entries()
    entries.append({
        "timestamp": datetime.now().isoformat(),
        "type": entry_type,
        "tag": tag,
        "text": text,
    })
    save_entries(entries)
    tag_str = f" #{tag}" if tag else ""
    print(f"  [{entry_type}]{tag_str} {text}")


def filter_recent(entries, since_days, tag=None):
    cutoff = datetime.now() - timedelta(days=since_days)
    recent = [e for e in entries if datetime.fromisoformat(e["timestamp"]) >= cutoff]
    if tag:
        recent = [e for e in recent if e.get("tag") == tag]
    return recent


def show_entries(since_days, tag=None):
    recent = filter_recent(load_entries(), since_days, tag)
    if not recent:
        msg = f"No entries in the last {since_days} day(s)"
        if tag:
            msg += f" for tag '{tag}'"
        print(msg + ".")
        return

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
            tag_str = f" #{entry['tag']}" if entry.get("tag") else ""
            print(f"  {icon}{tag_str} {entry['text']}")


def weekly_digest():
    recent = filter_recent(load_entries(), since_days=7)
    if not recent:
        print("# Weekly digest\n\nNo entries this week.")
        return

    done = [e for e in recent if e["type"] == "done"]
    doing = [e for e in recent if e["type"] == "doing"]
    blocked = [e for e in recent if e["type"] == "blocked"]

    print("# Weekly digest")
    print(f"\n_{len(recent)} entries across the last 7 days._\n")

    for label, items in [("Shipped", done), ("In progress", doing), ("Blocked", blocked)]:
        if not items:
            continue
        print(f"\n## {label}\n")
        for e in items:
            tag = f" `#{e['tag']}`" if e.get("tag") else ""
            print(f"- {e['text']}{tag}")


def main():
    parser = argparse.ArgumentParser(description="Personal daily standup logger")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Add an entry")
    add.add_argument("text", help="What did you do / are doing / are blocked on")
    add.add_argument("--type", "-t", choices=["done", "doing", "blocked"], default="done")
    add.add_argument("--tag", default=None, help="Optional tag, e.g. job-search, good-grief")

    today = sub.add_parser("today", help="Show today's entries")
    today.add_argument("--tag", default=None)

    week = sub.add_parser("week", help="Show this week's entries")
    week.add_argument("--tag", default=None)

    sub.add_parser("digest", help="Print a weekly markdown digest")

    args = parser.parse_args()

    if args.command == "add":
        add_entry(args.text, args.type, args.tag)
    elif args.command == "today":
        show_entries(1, args.tag)
    elif args.command == "week":
        show_entries(7, args.tag)
    elif args.command == "digest":
        weekly_digest()


if __name__ == "__main__":
    main()