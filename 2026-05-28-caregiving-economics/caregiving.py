"""Caregiving economics — unpaid care burden by condition.

Takes a small dataset of US family caregiving estimates and produces:

  1. Horizontal bar chart — estimated annual economic value of unpaid
     care, by condition.
  2. Bubble scatter — weekly care hours vs. monthly out-of-pocket cost,
     bubble size = number of caregivers (millions).

Figures are illustrative, rounded from public caregiving research
(AARP / National Alliance for Caregiving style estimates). Directional,
not authoritative.

Run:
    python caregiving.py
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------------
# Data (illustrative, rounded)
#   caregivers_m     : caregivers in millions
#   weekly_hours     : avg hours of unpaid care per week
#   oop_monthly      : avg monthly out-of-pocket cost ($)
#   value_annual_bn  : estimated annual economic value of the unpaid
#                      care for this group ($ billions)
# ---------------------------------------------------------------
data = {
    "condition": [
        "Dementia / Alzheimer's",
        "Cancer",
        "Stroke / cardiovascular",
        "Frailty / aging",
        "Mental health",
        "Developmental disability",
    ],
    "caregivers_m":    [11.0,  4.0,  3.5, 14.0,  6.0,  4.5],
    "weekly_hours":    [27,    23,   25,  21,    18,   32],
    "oop_monthly":     [340,   410,  300, 260,   210,  390],
    "value_annual_bn": [272,   95,   88,  300,   120,  140],
}

df = pd.DataFrame(data)

# ---------------------------------------------------------------
# Chart 1: Horizontal bar — annual economic value by condition
# ---------------------------------------------------------------
df_sorted = df.sort_values("value_annual_bn")

fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.barh(df_sorted["condition"], df_sorted["value_annual_bn"], color="#0ea5e9")
ax.set_xlabel("Estimated annual value of unpaid care ($B)")
ax.set_title("Unpaid caregiving is a hidden economy", pad=15, fontsize=13)
ax.grid(axis="x", alpha=0.3)

for bar, value in zip(bars, df_sorted["value_annual_bn"]):
    ax.text(value + 4, bar.get_y() + bar.get_height()/2,
            f"${value}B", va="center", fontsize=9, color="#444")

fig.tight_layout()
plt.savefig("care_value_by_condition.png", dpi=140, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------
# Chart 2: Bubble scatter — hours vs out-of-pocket, sized by caregivers
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
sizes = df["caregivers_m"] * 80  # scale bubbles for visibility

scatter = ax.scatter(
    df["weekly_hours"], df["oop_monthly"],
    s=sizes, alpha=0.55, color="#8b5cf6", edgecolors="#5b21b6", linewidth=1.5,
)

for _, row in df.iterrows():
    ax.annotate(
        row["condition"],
        (row["weekly_hours"], row["oop_monthly"]),
        textcoords="offset points", xytext=(0, 12),
        ha="center", fontsize=8.5, color="#333",
    )

ax.set_xlabel("Avg weekly hours of unpaid care")
ax.set_ylabel("Avg monthly out-of-pocket cost ($)")
ax.set_title("Time burden vs. money burden (bubble = caregivers, millions)", pad=15, fontsize=13)
ax.grid(alpha=0.3)
ax.margins(0.15)

fig.tight_layout()
plt.savefig("burden_scatter.png", dpi=140, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------
total_caregivers = df["caregivers_m"].sum()
total_value = df["value_annual_bn"].sum()
avg_hours = (df["weekly_hours"] * df["caregivers_m"]).sum() / total_caregivers
highest_value = df.loc[df["value_annual_bn"].idxmax()]
highest_oop = df.loc[df["oop_monthly"].idxmax()]
highest_hours = df.loc[df["weekly_hours"].idxmax()]

summary = f"""# Caregiving Economics — Summary

## Headlines

- Across these six categories, roughly **{total_caregivers:.0f} million** Americans
  provide unpaid care, representing an estimated **${total_value:,.0f}B** in annual
  economic value.
- Weighted average care load is about **{avg_hours:.0f} hours per week** — most of a
  part-time job, unpaid.

## Where the burden concentrates

- **Highest economic value:** {highest_value['condition']} (~${highest_value['value_annual_bn']}B/yr),
  driven by {highest_value['caregivers_m']:.0f}M caregivers.
- **Highest out-of-pocket:** {highest_oop['condition']} (~${highest_oop['oop_monthly']}/mo).
- **Most time-intensive:** {highest_hours['condition']} (~{highest_hours['weekly_hours']} hrs/wk).

## Why it matters for digital health

Out-of-pocket cost and time burden don't move together — the highest-cost
condition isn't the most time-intensive one. That gap is exactly where
caregiving-support products can target: some families need money/logistics
relief, others need time/coordination relief. A one-size product misses both.

## Caveats

All figures are illustrative and rounded from public caregiving research
(AARP / National Alliance for Caregiving style estimates). Real numbers vary
widely by methodology, region, and how "unpaid care value" is imputed
(typically a shadow wage). Directional, not authoritative.
"""

Path("summary.md").write_text(summary)

print("Done.")
print("  care_value_by_condition.png")
print("  burden_scatter.png")
print("  summary.md")