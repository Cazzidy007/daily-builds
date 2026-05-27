"""case-prep — flashcard CLI for consulting case interview drilling.

Loads cards from cards.json, quizzes in weighted random order
(cards you've gotten wrong come up more often), tracks a running
score across sessions in stats.json.

Usage:
    python case_prep.py              # quiz mode
    python case_prep.py --n 10       # quiz 10 cards then stop
    python case_prep.py --topic math # only cards tagged 'math'
    python case_prep.py stats        # show current accuracy by card
    python case_prep.py reset        # wipe stats and start fresh
"""

import argparse
import json
import random
import sys
from pathlib import Path

CARDS_FILE = Path(__file__).parent / "cards.json"
STATS_FILE = Path(__file__).parent / "stats.json"

# ANSI colors for the terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"


def load_cards():
    if not CARDS_FILE.exists():
        print(f"No cards.json found at {CARDS_FILE}", file=sys.stderr)
        sys.exit(1)
    with open(CARDS_FILE) as f:
        return json.load(f)


def load_stats():
    if not STATS_FILE.exists():
        return {}
    with open(STATS_FILE) as f:
        return json.load(f)


def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)


def weight_for_card(card_id, stats):
    """Cards you've missed get heavier weight. New cards get default."""
    s = stats.get(card_id, {"right": 0, "wrong": 0})
    total = s["right"] + s["wrong"]
    if total == 0:
        return 1.0
    accuracy = s["right"] / total
    return 1.0 + 2.0 * (1.0 - accuracy)


def pick_card(cards, stats):
    weights = [weight_for_card(c["id"], stats) for c in cards]
    return random.choices(cards, weights=weights, k=1)[0]


def quiz(cards, stats, n_limit):
    answered = 0
    session_right = 0
    print(f"\n{BOLD}Case prep — {len(cards)} cards loaded.{RESET}")
    print(f"{DIM}Press Enter to reveal the answer. Type 'q' to quit.{RESET}\n")

    try:
        while n_limit is None or answered < n_limit:
            card = pick_card(cards, stats)
            print(f"{BOLD}Q:{RESET} {card['question']}")
            print(f"{DIM}   [{card.get('topic', 'general')}]{RESET}")

            user = input("   > ").strip().lower()
            if user == "q":
                break

            print(f"{BOLD}A:{RESET} {card['answer']}\n")
            mark = input(f"   Got it right? ({GREEN}y{RESET}/{RED}n{RESET}/skip): ").strip().lower()

            if mark == "y":
                stats.setdefault(card["id"], {"right": 0, "wrong": 0})["right"] += 1
                session_right += 1
                answered += 1
                print(f"   {GREEN}✓{RESET}\n")
            elif mark == "n":
                stats.setdefault(card["id"], {"right": 0, "wrong": 0})["wrong"] += 1
                answered += 1
                print(f"   {RED}✗ — this one will come up more{RESET}\n")
            else:
                print(f"   {DIM}skipped{RESET}\n")

            save_stats(stats)
    except (KeyboardInterrupt, EOFError):
        print()

    if answered:
        pct = 100 * session_right / answered
        color = GREEN if pct >= 70 else YELLOW if pct >= 50 else RED
        print(f"\n{BOLD}Session:{RESET} {session_right}/{answered} ({color}{pct:.0f}%{RESET})")


def show_stats(cards, stats):
    if not stats:
        print("No stats yet. Run a quiz first.")
        return
    print(f"\n{BOLD}Accuracy by card{RESET}\n" + "-" * 60)
    rows = []
    for card in cards:
        s = stats.get(card["id"], {"right": 0, "wrong": 0})
        total = s["right"] + s["wrong"]
        acc = (s["right"] / total * 100) if total else None
        rows.append((card["id"], card["question"][:45], total, acc))
    rows.sort(key=lambda r: (r[3] if r[3] is not None else 999))
    for cid, q, total, acc in rows:
        acc_str = f"{acc:5.0f}%" if acc is not None else "  —  "
        color = (RED if acc is not None and acc < 50 else
                 YELLOW if acc is not None and acc < 75 else
                 GREEN if acc is not None else DIM)
        print(f"  {color}{acc_str}{RESET}  ({total:2}×)  {q}")
    print()


def reset_stats():
    if STATS_FILE.exists():
        STATS_FILE.unlink()
    print("Stats wiped. Starting fresh.")


def main():
    parser = argparse.ArgumentParser(description="Consulting case prep flashcards")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("stats", help="Show accuracy by card")
    sub.add_parser("reset", help="Wipe stats")
    parser.add_argument("--n", type=int, default=None, help="Quiz N cards then stop")
    parser.add_argument("--topic", default=None, help="Filter by topic tag")

    args = parser.parse_args()

    cards = load_cards()
    if args.topic:
        cards = [c for c in cards if c.get("topic") == args.topic]
        if not cards:
            print(f"No cards with topic '{args.topic}'")
            return

    stats = load_stats()

    if args.command == "stats":
        show_stats(cards, stats)
    elif args.command == "reset":
        reset_stats()
    else:
        quiz(cards, stats, args.n)


if __name__ == "__main__":
    main()