"""Pharma R&D spend vs. FDA novel drug approvals (2014–2023).

Pulls in a small embedded dataset of aggregate big-pharma R&D spending
and FDA CDER novel drug (NME + BLA) approvals, then produces two charts:

  1. R&D spend and approvals over time (dual axis)
  2. Approvals per $10B of R&D spend — the "productivity" ratio

Run:
    python rd_productivity.py

Output:
    rd_spend_vs_approvals.png
    rd_productivity.png
    summary.md
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------------
# Data
# Sources: company 10-K filings (aggregated top 15 pharma R&D spend)
# and FDA CDER novel drug approval reports.
# Figures are approximate, illustrative, and rounded.
# ---------------------------------------------------------------
data = {
    "year":         [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "rd_spend_bn":  [ 104,  110,  113,  118,  127,  136,  151,  165,  180,  191],
    "novel_approvals": [41,   45,   22,   46,   59,   48,   53,   50,   37,   55],
}

df = pd.DataFrame(data)
df["productivity"] = df["novel_approvals"] / (df["rd_spend_bn"] / 10)

# ---------------------------------------------------------------
# Chart 1: Dual-axis time series
# ---------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(10, 5.5))

color_spend = "#2563eb"
color_appr = "#16a34a"

ax1.set_xlabel("Year")
ax1.set_ylabel("R&D spend, top 15 pharma ($B)", color=color_spend)
ax1.plot(df["year"], df["rd_spend_bn"], color=color_spend, marker="o", linewidth=2)
ax1.tick_params(axis="y", labelcolor=color_spend)
ax1.grid(alpha=0.3)

ax2 = ax1.twinx()
ax2.set_ylabel("FDA novel drug approvals", color=color_appr)
ax2.bar(df["year"], df["novel_approvals"], color=color_appr, alpha=0.25, width=0.6)
ax2.tick_params(axis="y", labelcolor=color_appr)

plt.title("Pharma R&D spend keeps rising. Approvals are choppy.", pad=15, fontsize=13)
fig.tight_layout()
plt.savefig("rd_spend_vs_approvals.png", dpi=140, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------
# Chart 2: Productivity ratio
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5))

bars = ax.bar(df["year"], df["productivity"], color="#7c3aed", alpha=0.85)
ax.set_xlabel("Year")
ax.set_ylabel("Approvals per $10B of R&D spend")
ax.set_title("R&D productivity has trended down over the decade", pad=15, fontsize=13)
ax.grid(axis="y", alpha=0.3)

# Label each bar
for bar, value in zip(bars, df["productivity"]):
    ax.text(bar.get_x() + bar.get_width()/2, value + 0.05,
            f"{value:.1f}", ha="center", fontsize=9, color="#444")

fig.tight_layout()
plt.savefig("rd_productivity.png", dpi=140, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------
spend_start, spend_end = df["rd_spend_bn"].iloc[0], df["rd_spend_bn"].iloc[-1]
spend_growth = (spend_end / spend_start - 1) * 100

prod_start, prod_end = df["productivity"].iloc[0], df["productivity"].iloc[-1]
prod_change = (prod_end / prod_start - 1) * 100

best_year = df.loc[df["productivity"].idxmax()]
worst_year = df.loc[df["productivity"].idxmin()]

summary = f"""# Pharma R&D Productivity, 2014–2023

## Headlines

- Aggregate top-15 pharma R&D spend grew from ~${spend_start}B to ~${spend_end}B, a **{spend_growth:.0f}% increase** over the decade.
- FDA novel drug approvals ranged from {df['novel_approvals'].min()} to {df['novel_approvals'].max()} per year, with no clear upward trend.
- Productivity (approvals per $10B of R&D) **{'fell' if prod_change < 0 else 'rose'} by {abs(prod_change):.0f}%** between 2014 and 2023.

## Best and worst years

- Best: **{int(best_year['year'])}** — {best_year['productivity']:.1f} approvals per $10B
- Worst: **{int(worst_year['year'])}** — {worst_year['productivity']:.1f} approvals per $10B

## Caveats

Aggregate R&D spend and approval counts are blunt instruments. They don't
account for therapeutic value, peak sales, breakthrough designations, or
the long tail between investment and approval (often 10+ years). This is
directional, not diagnostic.

## Data sources

- R&D spend: aggregated from company 10-K filings (top 15 by R&D)
- Approvals: FDA CDER Novel Drug Approval reports
"""

Path("summary.md").write_text(summary)

print("Done.")
print("  rd_spend_vs_approvals.png")
print("  rd_productivity.png")
print("  summary.md")