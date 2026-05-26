# Clinical Trials Snapshot

A small CLI that pulls the most recently updated clinical trials for a given condition from the [ClinicalTrials.gov](https://clinicaltrials.gov/) public API and prints a clean summary table. No API key required.

## Why I built it

I work on a digital health startup in the caregiving / end-of-life space (Good Grief), and I want to keep a finger on what's being trialed adjacent to us — caregiver-support interventions, palliative care models, dementia outcomes. Most websites that surface trial data are clunky. A 60-line script that runs in 2 seconds is faster than any of them.

## Usage

```bash
# Default search — alzheimer caregiver trials, 10 most recently updated
python trials.py

# Any condition
python trials.py "lung cancer"
python trials.py "palliative care" --n 5

# Filter by status (RECRUITING, COMPLETED, ACTIVE_NOT_RECRUITING, etc.)
python trials.py "type 2 diabetes" --status RECRUITING
```

## Tech

- **requests** — standard Python HTTP library
- **argparse** — for the CLI surface
- ClinicalTrials.gov **API v2** (REST, JSON, no auth required)
- Custom `User-Agent` header — many public APIs reject requests without one
- Graceful error handling on network failures

## Install and run

```bash
pip install requests
python trials.py "your condition here"
```

## What I'd add next

- Output as CSV (`--csv` flag) so I can paste into a tracker
- Caching responses to disk so repeat runs don't hit the API
- Multi-condition mode for adjacent-space scanning
- Notify-on-new-trial: store seen NCT IDs, surface only the new ones each run