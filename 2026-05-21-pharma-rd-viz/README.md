# Pharma R&D Productivity, 2014–2023

A short data viz exercise: pull big-pharma R&D spend and FDA novel drug approvals over a decade, plot them together, and compute the productivity ratio (approvals per $10B of R&D spend).

## Why I built it

Most "is pharma R&D broken?" conversations cite the same Eroom's Law point — costs going up, output flat. I wanted a clean, current visual I could reference in case prep and in conversations about healthcare strategy.

## Output

Running the script produces:

- `rd_spend_vs_approvals.png` — dual-axis chart showing R&D spend (line) and approvals (bars)
- `rd_productivity.png` — bar chart of approvals per $10B of R&D spend
- `summary.md` — auto-generated headline numbers and caveats

## Tech

- **pandas** — small DataFrame, derived column, indexing for best/worst year
- **matplotlib** — dual-axis chart with `twinx()`, bar chart with value labels
- ~90 lines, no notebook required

## Run it

```bash
pip install pandas matplotlib
python rd_productivity.py
```

## Caveats

The dataset is rounded and aggregated for illustration. R&D spend comes from top-15 pharma 10-K filings; approvals are FDA CDER novel drug counts (NMEs + BLAs). The productivity ratio is intentionally blunt — it doesn't capture peak sales, breakthrough designations, or the 10+ year lag between investment and approval. Directional, not diagnostic.

## What I'd add next

- Pull actual data live from FDA's CDER reports instead of hard-coding
- Break out by therapeutic area (oncology vs. CNS vs. rare disease — productivity varies wildly)
- Layer in industry-wide spend, not just top 15
- Add a third chart: cumulative spend vs. cumulative approvals