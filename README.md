![brand_logo](./branding/logo.svg) 

# MorningBloom — Memory & Wellness Assistant (v1)

MorningBloom is a lightweight, extensible AI system designed for older adults to support **daily journaling, memory recall, wellness check-ins, and reminders**.

## 🎬 Demo 
![Demo GIF](./demo/MorningBloom_demo.gif)

## ✨ Highlights
- Simple **Streamlit** UI (web) with large, accessible controls
- Local JSON storage for quick prototyping (no DB required)
- Modular prompts and governance guardrails
- Ready hooks to integrate `llms`, and `external DBs`, `governane` in next iterations

---
## 🚀 Quick Start (Local Prototype)
1) Create a Python 3.11+ venv
2) Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3) create a `.env` from `.env_example` to wire watsonx.
4) Run the app:
   ```bash
   streamlit run code/app.py
   ```

---
## 🔌 watsonx Integration
- `code/config.py`: reads `.env` and exposes llm config
- `code/llm.py`: `generate()` function — to generate using llms
- `code/storage.py`: replace local JSON with a DB - next iterations
- `governance_config/`: rules to validate outputs with some governance tools - next iterations

---
## 📁 Repo Layout
- `branding/` — logo and brand guide
- `code/` — Streamlit app, storage, LLM hooks, prompt templates (check-in, memory, summary, reminders, chat)
- `data_schema/` — JSON schema for logs & reminders
- `governance_config/` — safety policies & evaluation checklist
- `ui_mockup/` — flows and screen notes
- `data/` — local JSON storage (created automatically)

---
## ✅ Current Features (v1)
- Daily Check-In (mood + free-text notes)
- Memory Recall (search recent events: medication, calls, meals)
- Journal Weekly Summary (auto-generated from logs)
- Reminders (stores locally; scheduling hook provided)

---
## 🧱 Next Iterations
- Add voice I/O via Twilio/WebRTC
- Caregiver dashboard and trend charts
- Governance pipeline with automated evaluations

---
## ⚠️ Disclaimer
MorningBloom is **not** a medical device. Do not use for diagnosis or emergencies.
