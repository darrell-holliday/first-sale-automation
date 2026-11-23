#!/usr/bin/env python3
"""Show leads whose next_contact date is due, and optionally print a draft follow-up.

This script never sends messages. It only prints to the terminal.

Usage:
  python due.py
  python due.py --on 2026-11-23
  python due.py --draft
  python due.py --csv templates/lead-tracker.csv --on 2026-11-23 --draft
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_CSV = ROOT / "templates" / "lead-tracker.csv"
SEQUENCE = ROOT / "templates" / "follow-up-sequence.md"
OPEN_STATUSES = {"follow-up", "new", "overdue", "nurture"}


def parse_day(value: str) -> date:
    return date.fromisoformat(value)


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def due_rows(rows: list[dict[str, str]], today: date) -> list[dict[str, str]]:
    out = []
    for row in rows:
        status = (row.get("status") or "").strip().lower()
        raw = (row.get("next_contact") or "").strip()
        if not raw or status not in OPEN_STATUSES:
            continue
        try:
            when = parse_day(raw)
        except ValueError:
            print(f"skip {row.get('name')}: bad date {raw!r}", file=sys.stderr)
            continue
        if when <= today:
            label = dict(row)
            label["late_by"] = str((today - when).days)
            out.append(label)
    return out


def draft_for(name: str) -> str:
    if not SEQUENCE.exists():
        return "No sequence file found."
    text = SEQUENCE.read_text(encoding="utf-8")
    # Use the Day 2 template as a default draft, still clearly a draft.
    chunk = text.split("## Day 2", 1)[-1].split("## Day 5", 1)[0].strip()
    return (
        chunk.replace("{name}", name)
        .replace("{goal}", "[their goal]")
        .replace("{link}", "[your calendar link]")
        + "\n\n[Edit this before you send it.]"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="List due follow-ups. Does not send anything.")
    parser.add_argument("--csv", default=str(DEFAULT_CSV), help="Path to the lead tracker CSV")
    parser.add_argument("--on", default=None, help="Treat this YYYY-MM-DD as today (for testing)")
    parser.add_argument("--draft", action="store_true", help="Print a draft message for each due lead")
    args = parser.parse_args()

    path = Path(args.csv)
    if not path.exists():
        print(f"No CSV at {path}", file=sys.stderr)
        return 1

    today = parse_day(args.on) if args.on else date.today()
    rows = due_rows(load_rows(path), today)
    if not rows:
        print(f"No follow-ups due on or before {today.isoformat()}.")
        return 0

    print(f"Due on or before {today.isoformat()}: {len(rows)}")
    for row in rows:
        print(
            f"- {row['name']}  status={row['status']}  next={row['next_contact']}  "
            f"days_late={row['late_by']}  source={row.get('source','')}"
        )
        if row.get("notes"):
            print(f"  notes: {row['notes']}")
        if args.draft:
            print()
            print(draft_for(row["name"]))
            print("-" * 40)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
