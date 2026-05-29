# GH Profile

A Python CLI that analyzes any GitHub user's public profile and prints a clean terminal summary: basic info, repo footprint, languages used, top repos by stars, and most recently updated repos.

## Why I built it

I wanted a quick way to size up a GitHub profile before networking calls — recruiters, founders, prospective collaborators. The GitHub website shows a lot, but scattered across tabs. A one-shot terminal summary is faster.

Self-serving second reason: pointing it at my own username gave me an at-a-glance view of how my daily-builds practice is showing up publicly. Useful feedback loop.

## Usage

```bash
# Your own profile
python gh_profile.py Cazzidy007

# Any user
python gh_profile.py torvalds

# Show 10 top/recent repos instead of the default 5
python gh_profile.py gvanrossum --top 10
```

## Tech

- **requests** — REST API client (already installed from Day 4)
- **GitHub REST API v3**, unauthenticated — 60 req/hour rate limit
- Pagination across `/users/{user}/repos` (100 per page)
- `collections.Counter` for language tallies
- `datetime` math for "N days ago"
- ANSI color in the terminal
- ~120 lines

## Rate limits

Unauthenticated calls are limited to 60 requests/hour. One profile uses ~2-11 requests, so fine for normal use. Adding a personal access token to the headers raises the limit to 5000/hour if needed.

## What I'd add next

- `--compare user1 user2` for side-by-side profiles
- Pull commit frequency for real activity signal
- Markdown output for pasting into networking notes