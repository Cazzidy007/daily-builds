"""gh-profile — analyze a GitHub user's public profile.

Hits the public GitHub REST API to produce a snapshot:
  · Basic profile (name, bio, location, joined date)
  · Repo stats (total, total stars received, forks)
  · Languages used across all repos
  · Top repos by stars
  · Most recently updated repos

No auth required for public data. Rate limit is 60 requests/hour
unauthenticated, which is plenty for one profile.

Usage:
    python gh_profile.py Cazzidy007
    python gh_profile.py torvalds --top 10
"""

import argparse
import sys
from collections import Counter
from datetime import datetime

import requests

API_BASE = "https://api.github.com"
HEADERS = {
    "User-Agent": "gh-profile/0.1 (daily-builds; learning project)",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# ANSI for clean terminal output
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
GREEN = "\033[92m"
RESET = "\033[0m"


def fetch_user(username):
    r = requests.get(f"{API_BASE}/users/{username}", headers=HEADERS, timeout=15)
    if r.status_code == 404:
        print(f"User '{username}' not found.", file=sys.stderr)
        sys.exit(1)
    r.raise_for_status()
    return r.json()


def fetch_all_repos(username):
    """Page through all public repos. GitHub returns 30 by default; we ask for 100."""
    repos = []
    page = 1
    while True:
        r = requests.get(
            f"{API_BASE}/users/{username}/repos",
            headers=HEADERS,
            params={"per_page": 100, "page": page, "sort": "updated"},
            timeout=15,
        )
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        if page > 10:  # safety: cap at ~1000 repos
            break
    return repos


def fmt_date(iso_string):
    """Turn '2026-05-19T12:34:56Z' into '2026-05-19'."""
    return iso_string[:10] if iso_string else "—"


def days_since(iso_string):
    if not iso_string:
        return None
    dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
    return (datetime.now(dt.tzinfo) - dt).days


def print_profile(user, repos, top_n):
    print(f"\n{BOLD}{CYAN}@{user['login']}{RESET} {DIM}— {user.get('name') or '(no name set)'}{RESET}")
    if user.get("bio"):
        print(f"  {user['bio']}")

    print(f"\n  {DIM}Joined:{RESET}    {fmt_date(user.get('created_at'))}")
    print(f"  {DIM}Location:{RESET}  {user.get('location') or '—'}")
    print(f"  {DIM}Followers:{RESET} {user.get('followers', 0):,}   {DIM}Following:{RESET} {user.get('following', 0):,}")

    # Repo aggregates
    total_stars = sum(r["stargazers_count"] for r in repos)
    total_forks = sum(r["forks_count"] for r in repos)
    print(f"\n{BOLD}Repo footprint{RESET}")
    print(f"  Public repos:    {len(repos)}")
    print(f"  Total stars:     {total_stars:,}")
    print(f"  Total forks:     {total_forks:,}")

    # Languages
    lang_counter = Counter(r["language"] for r in repos if r["language"])
    if lang_counter:
        print(f"\n{BOLD}Languages{RESET} {DIM}(repos using each as primary){RESET}")
        for lang, count in lang_counter.most_common(8):
            bar = "█" * count
            print(f"  {lang:<14} {bar} {count}")

    # Top repos by stars
    starred = sorted(repos, key=lambda r: r["stargazers_count"], reverse=True)
    starred = [r for r in starred if r["stargazers_count"] > 0][:top_n]
    if starred:
        print(f"\n{BOLD}Top repos by stars{RESET}")
        for r in starred:
            desc = (r.get("description") or "").strip()
            if len(desc) > 60:
                desc = desc[:59] + "…"
            print(f"  {GREEN}★ {r['stargazers_count']:>4}{RESET}  {r['name']}")
            if desc:
                print(f"            {DIM}{desc}{RESET}")

    # Most recently updated
    recent = repos[:top_n]
    print(f"\n{BOLD}Most recently updated{RESET}")
    for r in recent:
        days = days_since(r["updated_at"])
        when = f"{days}d ago" if days is not None else "—"
        lang = r["language"] or "—"
        print(f"  {when:>8}  {r['name']:<28} {DIM}{lang}{RESET}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Analyze a GitHub user's public profile")
    parser.add_argument("username", help="GitHub username")
    parser.add_argument("--top", type=int, default=5, help="Show N top/recent repos (default 5)")
    args = parser.parse_args()

    try:
        user = fetch_user(args.username)
        repos = fetch_all_repos(args.username)
    except requests.exceptions.RequestException as e:
        print(f"  API error: {e}", file=sys.stderr)
        sys.exit(1)

    print_profile(user, repos, args.top)


if __name__ == "__main__":
    main()