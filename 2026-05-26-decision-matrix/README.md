# Decision Matrix

A single-page weighted decision matrix. Add options, add criteria with weights, score 1–10 in each cell, and the winning option highlights live.

## Why I built it

I make weighted-pro/con decisions in spreadsheets all the time — should I take this offer, prioritize this feature, accept this project. The spreadsheet version takes 10 minutes of formatting. This loads in one click.

## Run it

Open `index.html` in any browser. No server, no build step.

## Tech

- Pure HTML/CSS/JS, no dependencies, no framework
- All state in memory; refresh resets
- ~120 lines

## What I'd add next

- Save state to `localStorage` so refresh doesn't lose work
- Export as Markdown table for pasting into a notes doc
- "Confidence" slider per cell (low-confidence scores are weighted lower)