# Regex Demo

A Sunday "learn one thing" exercise: get comfortable with Python's `re` module by working through three real-world patterns.

## What I learned

Three things clicked while writing this:

1. **`re.findall()`** returns all matches as a list — no manual loop needed.
2. **`re.sub()`** does find-and-replace with patterns, useful for masking PII like phone numbers.
3. **Named capture groups** (`(?P<name>...)`) turn a regex into a mini-parser: each named group becomes a field in a dict. This is how unstructured log lines become structured data you can analyze.

## Three demos in one file

- Extract all email addresses from a blob of text
- Mask US phone numbers (any common format) to `[REDACTED]`
- Parse log lines into `{date, time, level, message}` dicts

## Run

```bash
python regex_demo.py
```

No dependencies — uses only the standard library.

## Where this is useful

For me, this comes up in two places: scraping (find all NCT IDs in a page), and any time I need to clean up freeform user input into something structured. Tag #1 in a digital-health product context: extracting medication names or dosages from doctor's notes.