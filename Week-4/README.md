# Week 4 — Production-Grade AI Voice Agent for Real Estate (UrduLish)

**Conversational AI • Voice • RAG • Workflow Automation • LangGraph • Production Deployment**

A complete seven-day project that builds a real-estate AI voice agent capable of speaking naturally in UrduLish (Urdu + English), understanding buyer, renter, investor, and seller intent, answering property questions from grounded company data, recommending listings, handling objections, and managing property-visit appointments through Google Calendar, Gmail, n8n, and CRM logging.

> **Project status: ✅ Complete** — Days 1–7 deliverables, testing, integrations, documentation, and deployment demo are finished.

**Executive report:** [`Day-7/executive_report.pdf`](./Day-7/executive_report.pdf)  
**Live demo:** [Demo of Real Estate Agent](https://drive.google.com/file/d/1-3PijemkKqoqJV1trsITn_QRqeFpo5lz/view?usp=sharing)

---

## Results at a Glance

| Area | Result |
|---|---|
| RAG grounding | **100%** |
| Hallucination rate | **0%** |
| Average response latency | **1.3 seconds** (target: under 2 seconds) |
| p95 latency | **2.29 seconds** |
| Evaluation conversations | **43** |
| Prompt-injection attempts blocked | **10/10** |
| RAG-miss/out-of-scope refusals | **5/5 correct** |
| Memory accuracy | **100% after v3 fix** |
| Live booking success | **100%** |
| Tool failures | **0** |
| TTS evaluation | **ElevenLabs 4.0/5 vs Fish Audio 2.5/5** |

---

## What Was Built Day by Day

### Day 1 — Foundations & Conversation Design

Architecture and conversation foundations were established for a production real-estate voice agent.

- Full audio → VAD/barge-in → Whisper STT → Gemini → SQL/ChromaDB → tools → ElevenLabs pipeline
- Nine conversation flows: buyer, rental, commercial, investment, returning customer, rescheduling, cancellation, seller, and fallback
- UrduLish persona: **Ahmed**, a warm, professional, patient Pakistani property consultant
- Persona phrases, natural fillers, objection handling, grounding rules, and security guardrails
- Fish Audio and ElevenLabs listening evaluation
- ElevenLabs selected because it handled Urdu pronunciation, code-switching, and real-estate terms such as *marla*, *kanal*, *crore*, and *lakh* better
- Production system prompt and free-tier technology recommendations

**Files:** `01_architecture_research.md`, `02_conversation_flows.md`, `03_urdulish_persona.md`, `04_fish_audio_vs_elevenlabs.md`, `05_system_prompt.md`, `06_free_tier_tech_stack.md`, `07_voice_provider_decision.md`

[Open Day 1 →](./Day-1/README.md)

### Day 2 — Knowledge Base, RAG & Property Intelligence

The property intelligence layer was implemented with structured and semantic retrieval.

- SQLite knowledge base for properties, prices, locations, amenities, schools, hospitals, payment plans, developers, and FAQs
- Document loading, chunking, embeddings, ChromaDB vector store, retriever, and answer generation
- SQL retrieval for exact facts such as price, availability, plot size, and agent name
- Vector retrieval for brochures, descriptions, and FAQ-style questions
- `is_structured()` routing between SQL and semantic search
- Recommendation engine using budget, city, area, bedrooms, purpose, amenities, and investment goals
- Twenty-question evaluation achieved **100% grounding and 0% hallucination**
- Evaluation and API-key issues were identified and fixed

**File:** `Day2_Knowledge_Base_RAG.ipynb`

[Open Day 2 →](./Day-2/README.md)

### Day 3 — Voice Pipeline & Natural Conversation

The voice experience was implemented and evaluated for speed, naturalness, memory, and objections.

- End-to-end Speech → LLM → Voice streaming pipeline
- Average total latency of **1.3 seconds**
- Natural fillers, hesitations, thinking pauses, and acknowledgements
- Multi-turn context memory for budget, city, and area
- Six objection categories: price, trust, location, investment, builder/developer, and maintenance
- Five recorded conversations manually evaluated for naturalness, persuasiveness, fluency, latency, and flow

**File:** `Day3_Voice_Pipeline.ipynb`

[Open Day 3 →](./Day-3/README.md)

### Day 4 — Workflows, Scheduling & Business Automation

Live business integrations were connected and tested with real APIs rather than mocks.

- Google Calendar event creation with client, phone, employee, property, date, time, and notes
- Gmail notification to the assigned employee after booking
- Live booking, rescheduling, and cancellation
- n8n workflow: **Call → Intent → Property Match → Appointment → Calendar → Email → CRM Update**
- Retry handling for workflow failures
- CRM logging to both Google Sheets and SQLite `crm_calls`
- Full live booking flow verified with appointment ID, Calendar event link, email message ID, CRM entries, and n8n `status: 200`

**File:** `Day4_Workflows.ipynb`

[Open Day 4 →](./Day-4/README.md)

### Day 5 — LangGraph Orchestration & Tool Calling

The conversational logic was converted into a stateful nine-node LangGraph agent.

- `AgentState` stores conversation history, caller details, preferences, intent, retrieved properties, appointment data, response text, and trace logs
- Nine nodes: `intent`, `greeting`, `retrieve`, `book`, `reschedule`, `cancel`, `ai_disclosure`, `off_topic`, and `fallback`
- SQL/vector property search and Calendar/Gmail/CRM tools integrated into graph nodes
- Booking slots validated against live Calendar availability
- No fabricated listings; unclear input goes to a clarification fallback
- Every node records timestamped execution details in the trace
- Six end-to-end scenarios routed correctly: retrieval, booking, rescheduling, cancellation, AI disclosure, and off-topic conversation

**File:** `Day_5__LangGraph_Orchestration.ipynb`

[Open Day 5 →](./Day-5/README.md)

### Day 6 — Testing, Evaluation & Security

The complete agent was tested under normal, edge-case, adversarial, and performance scenarios.

- **43 test conversations** covering buyer, seller, investor, rental, booking, rescheduling, cancellation, off-topic, injection, angry, silent, and unclear callers
- Ten prompt-injection attempts blocked, including instruction override, system-prompt extraction, fake bookings, and internal-data requests
- Average latency: 1.3s; p95: 2.29s
- Grounding: 100%; out-of-scope refusals: 5/5
- Memory improved from 70% in v1 to 100% in v3 after diagnosis and fixing
- Live booking success: 100%; tool failures: 0
- Monitoring records latency, intent, tool failures, and booking success in `day6_monitoring_log.jsonl`
- Docker, requirements, environment template, gitignore, and CI/CD scaffold prepared

**File:** `Day_6__Testing__Evaluation___Security.ipynb`

[Open Day 6 →](./Day-6/README.md)

### Day 7 — Deployment & Live Demo

The integrated system was packaged for local execution, demonstration, and production-style deployment.

- `agent_core.py`: shared LangGraph agent used by API and Streamlit
- `day7_api.py`: FastAPI `/chat`, `/health`, and `/metrics` endpoints
- `streamlit_app.py`: microphone input, Whisper STT, and autoplay ElevenLabs TTS
- Dockerfile and requirements for deployment
- Executive, user, admin, maintenance, troubleshooting, API, architecture, monitoring, and demo documentation
- Automated demo run and final summary JSON files
- Live demo includes greeting, RAG answer, SQL recommendation, objection handling, booking, rescheduling, cancellation, and injection defense

[Open Day 7 →](./Day-7/README.md)

---

## System Architecture

```text
Caller / Voice Input
        ↓
VAD & Barge-in
        ↓
Whisper Speech-to-Text (local small model)
        ↓
LangGraph Agent + Gemini 3.5 Flash-Lite
        ↓
Intent, memory, validation, and tool routing
        ├── SQLite + ChromaDB retrieval
        ├── Property recommendation engine
        ├── Google Calendar
        ├── Gmail
        ├── Google Sheets / SQLite CRM
        └── n8n workflow automation
        ↓
ElevenLabs Text-to-Speech
        ↓
Natural UrduLish voice response
```

### Technology Stack

| Layer | Technology |
|---|---|
| LLM | Gemini 3.5 Flash-Lite |
| Speech-to-text | Whisper, local `small` model |
| Text-to-speech | ElevenLabs |
| Orchestration | LangGraph |
| Structured knowledge | SQLite |
| Semantic retrieval | ChromaDB |
| Automation | n8n |
| Scheduling and email | Google Calendar API and Gmail API |
| CRM | Google Sheets and SQLite |
| Backend | FastAPI |
| Demo UI | Streamlit |
| Deployment | Docker |

---

## Repository Structure

```text
Week-4/
├── README.md
├── Day-1/
│   ├── README.md
│   ├── 01_architecture_research.md
│   ├── 02_conversation_flows.md
│   ├── 03_urdulish_persona.md
│   ├── 04_fish_audio_vs_elevenlabs.md
│   ├── 05_system_prompt.md
│   ├─��� 06_free_tier_tech_stack.md
│   ├── 07_voice_provider_decision.md
│   └── diagrams/
├── Day-2/
│   ├── README.md
│   └── Day2_Knowledge_Base_RAG.ipynb
├── Day-3/
│   ├── README.md
│   └── Day3_Voice_Pipeline.ipynb
├── Day-4/
│   ├── README.md
│   └── Day4_Workflows.ipynb
├── Day-5/
│   ├── README.md
│   └── Day_5__LangGraph_Orchestration.ipynb
├── Day-6/
│   ├── README.md
│   └── Day_6__Testing__Evaluation___Security.ipynb
└── Day-7/
    ├── README.md
    ├── agent_core.py
    ├── day7_api.py
    ├── streamlit_app.py
    ├── Day7_FINAL.ipynb
    ├── Dockerfile
    ├── requirements.txt
    ├── .env.example
    ├── executive_report.pdf
    ├── system_architecture.md
    ├── api_documentation.md
    ├── user_guide.md
    ├── admin_guide.md
    ├── maintenance_guide.md
    ├── troubleshooting_guide.md
    ├── monitoring_maintenance_plan.md
    ├── demo_script.md
    ├── future_enhancements.md
    ├── day7_demo_run.json
    └── day7_summary.json
```

---

## Run Locally

```bash
git clone https://github.com/FizaAslam1/Web3-Geeks.git
cd Web3-Geeks/Week-4/Day-7

cp .env.example .env
# Add GEMINI_API_KEY, ELEVENLABS_API_KEY, and ELEVENLABS_VOICE_ID

pip install -r requirements.txt
jupyter notebook Day7_FINAL.ipynb
```

The live Streamlit voice demo opens at `http://localhost:8501`.

### Docker

```bash
docker build -t realestate-voice-agent .
docker run -p 8501:8501 --env-file .env realestate-voice-agent
```

Never commit real API keys; use `.env` locally and keep secrets outside version control.

---

## Project Flow

The days form one connected production pipeline:

- **Days 1–2:** design, persona, architecture, knowledge base, and grounded retrieval
- **Days 3–5:** voice experience, business integrations, state orchestration, and tool calling
- **Days 6–7:** evaluation, security, monitoring, deployment, documentation, and live demonstration

Day 7 reuses the retrieval logic from Day 2, voice and persona decisions from Day 1 and Day 3, Calendar/Gmail/CRM tools from Day 4, the LangGraph agent from Day 5, and the testing/monitoring assets from Day 6.

---

## Future Enhancements

The documented roadmap includes Urdu-focused STT fine-tuning, richer multi-step property filtering, video and 360-degree tours, automated SMS/email follow-ups, human-agent handoff with transcripts, Punjabi/Sindhi/Pashto support, and investment and financing assistance.

See [`Day-7/future_enhancements.md`](./Day-7/future_enhancements.md) and [`Day-7/executive_report.pdf`](./Day-7/executive_report.pdf) for the complete roadmap and limitations.

---

## Quick Links

- [Day 1 — Foundations](./Day-1/README.md)
- [Day 2 — Knowledge Base & RAG](./Day-2/README.md)
- [Day 3 — Voice Pipeline](./Day-3/README.md)
- [Day 4 — Workflows](./Day-4/README.md)
- [Day 5 — LangGraph](./Day-5/README.md)
- [Day 6 — Testing & Security](./Day-6/README.md)
- [Day 7 — Deployment & Demo](./Day-7/README.md)
- [Executive Report](./Day-7/executive_report.pdf)
- [Live Demo Video](https://drive.google.com/file/d/1-3PijemkKqoqJV1trsITn_QRqeFpo5lz/view?usp=sharing)

---

**Built with ❤️ for production-grade conversational AI in South Asian languages.**  
**Project status: ✅ Complete — all Week 4 work is finished.**
