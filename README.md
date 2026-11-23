# First-Sale Follow-Up Template

A lightweight follow-up system for a new online business. Most early sales are lost because nobody follows up. This fixes that with a sheet, a few drafted messages, and a script that tells you who is due.

The script never sends messages.

## What's inside

```
templates/
  lead-tracker.csv          Name, source, last contact, next step, status
  follow-up-sequence.md     Day 0, 2, 5, 10 messages (drafts you edit and send)
  call-notes.md             What they said, the real reason, next step
due.py                      Lists who is due today; optional --draft
automation/
  make-scenario.md          Optional Make.com reminder to yourself
  zapier-zap.md             Same thing in Zapier
```

## Run it

```
python due.py
python due.py --on 2026-11-23 --draft
```

The sample CSV is fictional. Replace it with your own leads. Never commit real client data to a public repo.

## How it works

1. Every conversation goes in the tracker.
2. Each row has a next-contact date.
3. Run `python due.py` (or get a daily reminder from Make or Zapier).
4. If you want a starting point, add `--draft`. Then edit the message and send it yourself.

License: MIT
