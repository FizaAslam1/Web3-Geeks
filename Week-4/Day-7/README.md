## Day 7 — Deployment & Live Demo

**Live voice call demo video:** [Demo of Real Estate agent.mp4](https://drive.google.com/file/d/1-3PijemkKqoqJV1trsITn_QRqeFpo5lz/view?usp=sharing)

The demo covers:
- Greeting (UrduLish tone)
- Property inquiry — RAG-grounded factual answer
- Property recommendation (SQL-filtered results)
- Objection handling
- Live appointment booking (Google Calendar event + employee email)
- Reschedule and cancellation (live calendar update)
- Security — one prompt-injection attempt declined

## Files (Day 7)

| File | Purpose |
|---|---|
| `agent_core.py` | Shared LangGraph agent (Day 5 logic) — imported by both API and Streamlit app |
| `day7_api.py` | FastAPI backend — `/chat`, `/health`, `/metrics` |
| `streamlit_app.py` | Live voice call UI — mic input, Whisper STT, autoplay TTS |
| `Dockerfile`, `requirements.txt` | Production deployment |
| `system_architecture.md`, `api_documentation.md` | Technical docs |
| `user_guide.md`, `admin_guide.md`, `maintenance_guide.md`, `troubleshooting_guide.md` | Executive documentation |
| `monitoring_maintenance_plan.md` | Monitoring thresholds, refresh schedule, backup plan |
| `demo_script.md` | stakeholder demo script |
| `future_enhancements.md` | Roadmap |
| `day7_demo_run.json`, `day7_summary.json` | Automated end-to-end test run + final checklist |

## How to run locally
1. Create `.env` with `GEMINI_API_KEY`, `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`
2. `pip install -r requirements.txt`
3. Run `Day7_FINAL.ipynb` top to bottom
4. Browser opens automatically at `localhost:8501` for the live call demo
