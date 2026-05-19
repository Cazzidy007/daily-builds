# Pitch Timer

A minimal single-file timer for practicing investor pitches. Pick a duration, hit start, watch the bar drain. Color shifts to yellow at 30 seconds left, red at 10 seconds, and beeps three times when time's up.

## Why I built it

I'm prepping for the AgeTech Collaborative Open Mic Pitch. Most online timers are bloated with ads or require a login. This is one file, runs offline, opens instantly.

## Tech

- Vanilla HTML/CSS/JS — no build step, no dependencies
- Web Audio API for the end-of-time beep (no audio file needed)
- ~150 lines total

## Run it

Open `index.html` in any browser. That's it.

## What I'd add next

- Interval bells (e.g., warn at the 1-minute mark for a 5-min pitch)
- Custom duration input
- Keyboard shortcuts (space to start/pause)
