import json, os, uuid, datetime
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LOGS_PATH = os.path.join(DATA_DIR, "logs.json")
REMINDERS_PATH = os.path.join(DATA_DIR, "reminders.json")

os.makedirs(DATA_DIR, exist_ok=True)
for p in [LOGS_PATH, REMINDERS_PATH]:
    if not os.path.exists(p):
        with open(p, "w") as f:
            json.dump([], f)

def _read(path):
    with open(path, "r") as f:
        return json.load(f)

def _write(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def add_log(user_id, mood=None, journal_entry=None, events=None):
    logs = _read(LOGS_PATH)
    now = datetime.datetime.now()
    rec = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "mood": mood,
        "journal_entry": journal_entry,
        "events": events or []
    }
    logs.append(rec)
    _write(LOGS_PATH, logs)
    return rec

def list_logs(days=7, user_id=None):
    logs = _read(LOGS_PATH)
    if user_id:
        logs = [l for l in logs if l["user_id"] == user_id]
    if days is None:
        return logs
    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    out = []
    for l in logs:
        dt = datetime.datetime.strptime(l["date"] + " " + l["time"], "%Y-%m-%d %H:%M")
        if dt >= cutoff:
            out.append(l)
    return out

def add_reminder(user_id, task, date, time):
    reminders = _read(REMINDERS_PATH)
    rec = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "task": task,
        "date": date,
        "time": time,
        "status": "scheduled"
    }
    reminders.append(rec)
    _write(REMINDERS_PATH, reminders)
    return rec

def list_reminders(user_id=None):
    reminders = _read(REMINDERS_PATH)
    if user_id:
        reminders = [r for r in reminders if r["user_id"] == user_id]
    return reminders
