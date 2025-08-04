import sys
# Optional: Avoid torch tracing error
try:
    import torch
    sys.modules['torch.classes'] = None
except ImportError:
    pass
import streamlit as st
import base64
import datetime
import storage
from llm import generate
from prompts import get_prompt

st.set_page_config(page_title="MorningBloom", page_icon="🌅", layout="centered")

# === Embed and center logo ===
def load_svg(path):
    with open(path, "r") as f:
        svg = f.read()
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64}" width="150" style="display:block; margin-left:auto; margin-right:auto;"/>'

logo_svg = load_svg("branding/logo.svg")
st.markdown(logo_svg, unsafe_allow_html=True)

# Title and subtitle (centered)
st.markdown("<h1 style='text-align:center'>🌅 MorningBloom</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; margin-top:-10px;'>A gentle daily companion for memory and wellness.</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; margin-top:-10px;'>...</h3>", unsafe_allow_html=True)


user_id = st.sidebar.text_input("User ID", value="demo-user")
st.sidebar.markdown("---")
st.sidebar.markdown("**Sections**")
# section = st.sidebar.radio("", ["Home", "Check-In", "Memory Recall", "Journal", "Reminders"])
section = st.sidebar.radio(
    "Navigation",
    ["Home", "Check-In", "Memory Recall", "Journal", "Reminders"],
    label_visibility="collapsed"
)

def weekly_summary(logs):
    if not logs:
        return "No entries yet. Try a check-in today, and I'll summarize your week soon."
    moods = [l.get("mood") for l in logs if l.get("mood")]
    mood_line = "You shared a mix of moods this week."
    if moods:
        counts = {m: moods.count(m) for m in set(moods)}
        top = sorted(counts.items(), key=lambda x: -x[1])[0][0]
        mood_line = f"You felt mostly {top.lower()} this week."
    nice = [l.get("journal_entry") for l in logs if l.get("journal_entry")]
    nice = [n for n in nice if n]
    highlight = f"You noted {len(nice)} moments."
    if nice:
        sample = nice[-1]
        highlight = f"One highlight you mentioned: “{sample[:120]}{'...' if len(sample)>120 else ''}”"
    return f"{mood_line} {highlight} Keep going—small daily notes help me remember for you."

if section == "Home":
    st.subheader("Welcome back 👋")
    st.write(generate(get_prompt(section)))
    st.markdown(
        "<p style='text-align: center; font-size: 1.8rem; margin-top: 2rem; color: #555;'>🌱 Choose a section on the left to begin.</p>",
        unsafe_allow_html=True
    )

elif section == "Check-In":
    st.subheader("🧘 Daily Check-In")
    st.write(generate(get_prompt(section)))
    mood = st.radio("How are you feeling today?", ["Happy", "Okay", "Tired", "Confused"], horizontal=True)
    notes = st.text_area("Would you like to share more?", placeholder="Tell me about your day...")
    if st.button("Save Entry"):
        storage.add_log(user_id=user_id, mood=mood, journal_entry=notes)
        st.success("Saved! Thank you for sharing. 💛")

elif section == "Memory Recall":
    st.subheader("🧠 Memory Recall")
    st.write(generate(get_prompt(section)))
    query = st.text_input("Ask about recent events (e.g., “Did I take my pills yesterday?”)")
    if st.button("Ask"):
        logs = storage.list_logs(days=7, user_id=user_id)
        # very simple heuristic: search keywords
        text = []
        for l in logs:
            line = f"{l['date']} {l['time']} mood={l.get('mood')} notes={l.get('journal_entry','')} events={l.get('events', [])}"
            text.append(line)
        context = "\n".join(text)
        answer = generate(get_prompt(section)+"\nQuery:\n{}".format(query), context)
        st.info(answer)

elif section == "Journal":
    st.subheader("📓 Weekly Summary")
    logs = storage.list_logs(days=7, user_id=user_id)
    summary = weekly_summary(logs)
    response = generate(get_prompt(section), summary)
    st.write(response)

elif section == "Reminders":
    st.subheader("⏰ Reminders")
    st.write(generate(get_prompt(section)))
    col1, col2, col3 = st.columns(3)
    with col1:
        task = st.text_input("Task")
    with col2:
        date = st.date_input("Date", datetime.date.today())
    with col3:
        time = st.time_input("Time", datetime.time(10, 0))

    if st.button("Add Reminder"):
        rec = storage.add_reminder(user_id=user_id, task=task, date=str(date), time=str(time))
        st.success(f"Added reminder: {rec['task']} at {rec['date']} {rec['time']}")

    st.markdown("### Scheduled")
    for r in storage.list_reminders(user_id=user_id):
        st.write(f"- {r['date']} {r['time']}: **{r['task']}** ({r['status']})")
