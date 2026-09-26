# System Architecture — RealEstate Hub Voice Agent

## Pipeline
Telephony/Audio → VAD/Barge-in → STT (Whisper) → LangGraph Agent (Gemini 3.5 Flash-Lite)
→ RAG (ChromaDB) + SQL (structured facts) → Tool calls (Calendar/Email/CRM via n8n)
→ TTS (ElevenLabs) → Caller

## Components deployed
- FastAPI backend (day7_api.py) — /chat, /health, /metrics
- Streamlit live-call demo (streamlit_app.py) — mic input, Whisper STT, agent reply, autoplay TTS
- LangGraph: 9-node graph — see Day 5
- Knowledge base: SQLite + ChromaDB — see Day 2
- Workflow automation: n8n — see Day 4
- Voice: Whisper (STT) + ElevenLabs (TTS) — see Day 1 Task 4 decision record
