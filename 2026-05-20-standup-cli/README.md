# Standup CLI

A minimal command-line tool for logging personal daily standups. I built it because I wanted a frictionless way to track what I'm doing across job search, Good Grief work, and side projects — without opening a notes app.

## Usage

```bash
# Log entries with optional tags
python standup.py add "Submitted Bain thank-you" --tag job-search
python standup.py add "Prepping AgeTech pitch" --type doing --tag good-grief
python standup.py add "Waiting on CCA email" --type blocked --tag job-search

# View
python standup.py today
python standup.py week
python standup.py week --tag job-search

# Markdown digest for sharing or pasting into a doc
python standup.py digest
```

## Tech

- Python standard library only — no dependencies
- `argparse` with subcommands
- JSON file at `~/.standup.json` for persistence
- ~110 lines

## Changelog

- **v0.2** (2026-05-23) — Added tag support, filtering by tag, and a weekly markdown digest
- **v0.1** (2026-05-20) — Initial version

## What I'd add next

- `standup search "keyword"` to grep history
- Install as a system command so I can type `standup add ...` from anywhere
- Sync via Git or Dropbox