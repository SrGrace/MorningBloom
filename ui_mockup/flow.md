# UI Flow (MorningBloom)
- Home: Check-In | Memory Recall | Journal | Reminders
- Check-In:
    * Mood (Happy/Okay/Tired/Confused)
    * Notes (textarea)
    * Save -> stored to local JSON (data/logs.json)
- Memory Recall:
    * Query input ("Did I take my pills yesterday?")
    * Returns best guess from logs (last 7 days)
- Journal:
    * Weekly summary generated from logs
- Reminders:
    * Task + Date + Time -> saved to data/reminders.json
    * Placeholder for scheduler integration
