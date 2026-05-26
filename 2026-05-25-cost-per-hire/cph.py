"""cost-per-hire — quick recruiting math from a CSV.

Reads a CSV with columns:
  role, hires, recruiting_spend, days_open

Computes:
  · Cost per hire (recruiting_spend / hires)
  · Avg days to fill (days_open / hires)
  · Totals across all roles

Run:
    python cph.py sample_hires.csv

If no file is passed, runs with a built-in sample.
"""

import argparse
import csv
import sys
from io import StringIO

SAMPLE_CSV = """role,hires,recruiting_spend,days_open
Engineer,8,42000,360
Product Manager,3,21000,180
Designer,2,9000,90
Data Scientist,4,28000,240
Sales,6,18000,300
"""


def load_rows(path):
    if path:
        with open(path) as f:
            reader = csv.DictReader(f)
            return list(reader)
    # Use embedded sample
    return list(csv.DictReader(StringIO(SAMPLE_CSV)))


def analyze(rows):
    print(f"\n  {'Role':<20}{'Hires':>8}{'Spend ($)':>14}{'CPH ($)':>12}{'Avg days':>12}")
    print("  " + "-" * 66)

    total_hires = 0
    total_spend = 0
    total_days = 0

    for row in rows:
        hires = int(row["hires"])
        spend = float(row["recruiting_spend"])
        days = int(row["days_open"])

        cph = spend / hires if hires else 0
        avg_days = days / hires if hires else 0

        print(f"  {row['role']:<20}{hires:>8}{spend:>14,.0f}{cph:>12,.0f}{avg_days:>12.1f}")

        total_hires += hires
        total_spend += spend
        total_days += days

    print("  " + "-" * 66)
    overall_cph = total_spend / total_hires if total_hires else 0
    overall_days = total_days / total_hires if total_hires else 0
    print(f"  {'TOTAL':<20}{total_hires:>8}{total_spend:>14,.0f}{overall_cph:>12,.0f}{overall_days:>12.1f}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Cost-per-hire calculator")
    parser.add_argument("csv_file", nargs="?", default=None, help="Path to CSV (optional)")
    args = parser.parse_args()

    try:
        rows = load_rows(args.csv_file)
    except FileNotFoundError:
        print(f"Error: file not found: {args.csv_file}", file=sys.stderr)
        sys.exit(1)

    analyze(rows)


if __name__ == "__main__":
    main()