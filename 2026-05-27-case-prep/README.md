# Case Prep CLI

A terminal flashcard tool for consulting case interview drilling. Loads a deck of cards (frameworks, market sizing facts, case math, interview-skill prompts) and quizzes you in weighted random order — cards you've gotten wrong come up more often.

## Why I built it

I'm prepping for BCG / Bain. Anki is great but heavy; I wanted something I could fire from the terminal in two seconds, drill 10 cards over coffee, and walk away. Building it was also a way to internalize the deck — you remember things better when you've typed them out as data.

## Usage

```bash
python case_prep.py              # quiz mode, run until 'q'
python case_prep.py --n 10       # drill 10 cards then stop
python case_prep.py --topic math # filter by topic
python case_prep.py stats        # accuracy by card, weakest first
python case_prep.py reset        # wipe stats
```

## How the weighting works

Each card has a pick weight: