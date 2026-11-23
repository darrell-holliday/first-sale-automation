# Optional: Make.com reminder

This does not send messages. It reminds you who is due.

1. Trigger: every day at 8:00 in your timezone.
2. Module: Google Sheets or a CSV stored in Drive, "search rows" where `next_contact` is less than or equal to today, and `status` is not `won` or `closed`.
3. Module: email yourself, or a Slack DM to yourself, with the name, status, and notes.
4. You open the tracker, run `python due.py --draft`, edit the message, and send it yourself.
