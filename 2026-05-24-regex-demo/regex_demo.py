"""regex_demo — a Sunday 'learn one thing' on Python regex.

Three small demos of the `re` module:
  1. Extract email addresses from text
  2. Mask phone numbers (privacy)
  3. Parse structured log lines into fields

Run:
    python regex_demo.py
"""

import re

# ---------------------------------------------------------------
# Demo 1: Extract all email addresses from a chunk of text
# ---------------------------------------------------------------
sample_text = """
Hi team — please reach out to alice@example.com or bob.smith@kellogg.edu
for the agenda. CC mike+events@goodgrief.io if it's about the AgeTech pitch.
"""

email_pattern = r"[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+"
emails = re.findall(email_pattern, sample_text)

print("Demo 1 — Extracted emails")
for e in emails:
    print(f"  · {e}")

# ---------------------------------------------------------------
# Demo 2: Mask US phone numbers to protect privacy
# Matches formats like (312) 555-1234, 312-555-1234, 312.555.1234
# ---------------------------------------------------------------
contact_blob = """
Call Adrienne at 312-555-0142 or text Karen on (847) 555.0193.
Backup: 555.0177 won't match because no area code.
"""

phone_pattern = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
masked = re.sub(phone_pattern, "[REDACTED]", contact_blob)

print("\nDemo 2 — Phone numbers masked")
print(masked.strip())

# ---------------------------------------------------------------
# Demo 3: Parse log lines with named capture groups
# Real-world pattern: turning unstructured logs into rows you can analyze
# ---------------------------------------------------------------
logs = [
    "2026-05-24 09:14:22 INFO  User alice logged in",
    "2026-05-24 09:15:01 WARN  Slow query 1820ms on /api/trials",
    "2026-05-24 09:15:47 ERROR Database connection refused",
]

log_pattern = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>\w+)\s+"
    r"(?P<message>.*)"
)

print("\nDemo 3 — Parsed log lines")
for line in logs:
    match = log_pattern.match(line)
    if match:
        parts = match.groupdict()
        print(f"  [{parts['level']:5}] {parts['date']} {parts['time']} | {parts['message']}")

# ---------------------------------------------------------------
# Takeaway
# ---------------------------------------------------------------
print("\nWhat I learned:")
print("  · re.findall() returns a list of all matches")
print("  · re.sub() replaces matches in place — great for masking")
print("  · Named capture groups (?P<name>...) turn regex into a parser")