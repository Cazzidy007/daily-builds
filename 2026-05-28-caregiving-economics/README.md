# Caregiving Economics

A data viz exercise on the hidden economy of unpaid family caregiving in the US. Takes a small dataset (caregivers, weekly hours, out-of-pocket cost, and estimated economic value by condition) and produces two charts plus an auto-generated written summary.

## Why I built it

I work on a caregiving / end-of-life digital health startup (Good Grief). The economic scale of unpaid caregiving is staggering and under-discussed, and I wanted a clean visual that makes two points: (1) how large the hidden economy is, and (2) that time burden and financial burden don't track together — which has direct product implications.

## Output

- `care_value_by_condition.png` — horizontal bar chart of estimated annual economic value of unpaid care by condition
- `burden_scatter.png` — bubble scatter of weekly care hours vs. monthly out-of-pocket cost, sized by number of caregivers
- `summary.md` — auto-generated headline numbers, the key insight, and caveats

## The key insight

The scatter shows the conditions spread out rather than falling on a clean diagonal. The highest out-of-pocket condition isn't the most time-intensive one. That gap is the product opportunity: some families need financial/logistics relief, others need time/coordination relief. A single one-size caregiving product misses both segments.

## Tech

- **pandas** — DataFrame, sorting, weighted average, idxmax for finding extremes
- **matplotlib** — horizontal bar chart (`barh`) with value labels; bubble scatter with per-point annotations and size-encoded third dimension
- ~120 lines, no notebook required

## Run it

```bash
pip install pandas matplotlib
python caregiving.py
```

## Caveats

All figures are illustrative and rounded from public caregiving research (AARP / National Alliance for Caregiving style estimates). Real numbers vary widely by methodology, region, and how "unpaid care value" is imputed (usually a shadow wage). Directional, not authoritative — I'd never present these as primary-source figures.

## What I'd add next

- Pull real figures from AARP's "Valuing the Invaluable" report and cite line by line
- Add a third axis: caregiver burnout / health-decline rates by condition
- Time series: how the unpaid-care economy has grown over the last decade
- Segment by caregiver age (sandwich generation vs. older spousal caregivers)