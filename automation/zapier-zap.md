# Optional: Zapier reminder

Same idea as the Make.com version. No auto-send.

1. Schedule trigger, daily.
2. Google Sheets: lookup rows where `next_contact` ≤ today.
3. Email by Zapier, to you only, listing the due names.
4. You run `python due.py --draft` and send the message yourself.
