"""clinical-trials-snapshot

Pulls the most recent clinical trials for a given condition from the
ClinicalTrials.gov public API (v2) and prints a clean summary.

No API key required.

Usage:
    python trials.py                          # default: alzheimer caregiver
    python trials.py "lung cancer"
    python trials.py "palliative care" --n 5
    python trials.py "type 2 diabetes" --status RECRUITING
"""

import argparse
import sys
import requests

API_URL = "https://clinicaltrials.gov/api/v2/studies"
HEADERS = {
    # Many public APIs reject requests without a User-Agent.
    "User-Agent": "clinical-trials-snapshot/0.1 (daily-builds; learning project)",
    "Accept": "application/json",
}


def fetch_trials(condition, n, status):
    """Query the ClinicalTrials.gov v2 API and return a list of studies."""
    params = {
        "query.cond": condition,
        "pageSize": n,
        "sort": "LastUpdatePostDate:desc",
        "format": "json",
    }
    if status:
        params["filter.overallStatus"] = status

    response = requests.get(API_URL, params=params, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.json().get("studies", [])


def extract_fields(study):
    """Pull the fields we care about out of a single study record."""
    protocol = study.get("protocolSection", {})
    ident = protocol.get("identificationModule", {})
    status = protocol.get("statusModule", {})
    design = protocol.get("designModule", {})
    sponsor = protocol.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {})

    return {
        "nct_id": ident.get("nctId", "—"),
        "title": ident.get("briefTitle", "—"),
        "status": status.get("overallStatus", "—"),
        "phase": ", ".join(design.get("phases", [])) or "—",
        "sponsor": sponsor.get("name", "—"),
        "last_updated": status.get("lastUpdatePostDateStruct", {}).get("date", "—"),
    }


def truncate(text, width):
    """Cut a string to width with an ellipsis if needed."""
    return text if len(text) <= width else text[: width - 1] + "…"


def print_trials(trials, condition):
    if not trials:
        print(f"No trials found for '{condition}'.")
        return

    print(f"\n  Latest trials for: '{condition}'")
    print(f"  Found: {len(trials)} results, sorted by last update\n")
    print("-" * 100)

    for i, study in enumerate(trials, 1):
        f = extract_fields(study)
        print(f"  [{i}] {f['nct_id']}  ·  updated {f['last_updated']}")
        print(f"      {truncate(f['title'], 90)}")
        print(f"      {f['status']}  ·  Phase: {f['phase']}  ·  Sponsor: {truncate(f['sponsor'], 50)}")
        print(f"      https://clinicaltrials.gov/study/{f['nct_id']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Fetch recent clinical trials by condition")
    parser.add_argument(
        "condition", nargs="?", default="alzheimer caregiver",
        help="Condition to search (default: 'alzheimer caregiver')",
    )
    parser.add_argument("--n", type=int, default=10, help="Number of trials (default: 10)")
    parser.add_argument(
        "--status", default=None,
        help="Filter by status: RECRUITING, COMPLETED, ACTIVE_NOT_RECRUITING, etc.",
    )
    args = parser.parse_args()

    try:
        trials = fetch_trials(args.condition, args.n, args.status)
    except requests.exceptions.RequestException as e:
        print(f"  API error: {e}", file=sys.stderr)
        sys.exit(1)

    print_trials(trials, args.condition)


if __name__ == "__main__":
    main()