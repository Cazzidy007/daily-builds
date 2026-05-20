# Standup CLI

A minimal command-line tool for logging personal daily standups. I built it because I wanted a frictionless way to track what I'm doing across job search, Good Grief work, and side projects — without opening a notes app or yet another web tool.

## Usage

```bash
# Log what you finished (default type)
python standup.py add "Submitted Bain thank-you email"

# Log what you're currently working on
python standup.py add "Prepping AgeTech pitch deck" --type doing

# Log a blocker
python standup.py add "Waiting on CCA scheduling email" --type blocked

# See today
python standup.py today

# See the last 7 days
python standup.py week
```

## Output

```
2026-05-20
----------------------------------------
  ✓ Submitted Bain thank-you email
  → Prepping AgeTech pitch deck
  ✗ Waiting on CCA scheduling email
```

## Tech

- Python standard library only — no dependencies
- `argparse` for the CLI surface
- JSON file at `~/.standup.json` for persistence (survives across runs, syncs nicely if you put it in Dropbox/iCloud)
- ~60 lines

## What I'd add next

- `standup search "keyword"` to grep history
- Tag support (`--tag job-search`, `--tag good-grief`) for filtering
- Weekly digest export to markdown for actual standup meetings
- Install as a system command so I can type `standup add "..."` from anywhere
