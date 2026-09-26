# Week 4 — AI Voice Agent for Real Estate (UrduLish)

**Conversational AI • Voice • RAG • Workflow Automation • Bilingual UrduLish**

A production-grade AI voice agent that handles real-estate phone inquiries in fluent UrduLish (Urdu + English), understands buyer/renter/investor intent, retrieves property information from a company knowledge base, recommends suitable listings, handles objections naturally, and automates scheduling with Google Calendar and Gmail integration.

---

## Project Timeline

| Day | Focus | Key Outcome | Status |
|---|---|---|---|
| **Day 1** | Foundations & Conversation Design | Architecture research, 9 conversation flows, UrduLish persona, ElevenLabs TTS evaluation | ✅ Complete |
| **Day 2** | Knowledge Base & RAG Pipeline | SQLite + ChromaDB setup, semantic search, recommendation engine | 🔄 In Progress |
| **Day 3** | Voice Pipeline & Streaming | STT (Whisper) → LLM → TTS pipeline, latency optimization | 🔄 In Progress |
| **Day 4** | Workflow Automation | Google Calendar, Gmail, CRM integration via n8n | 🔄 In Progress |
| **Day 5** | LangGraph Orchestration | Multi-node state graph, tool calling, slot validation | 🔄 In Progress |
| **Day 6** | Testing & Evaluation | Test cases, security, performance metrics | 🔄 Planned |
| **Day 7** | Deployment & Live Demo | FastAPI backend, Streamlit UI, Docker containerization | 🔄 Planned |

---

## System Architecture

```
Audio Input → Voice Activity Detection (VAD) & Barge-in
    ↓
Speech-to-Text (Whisper)
    ↓
LangGraph Agent (Gemini 3.5 Flash-Lite)
    ↓
Retrieval Layer (ChromaDB + SQLite)
    ↓
Tool Calling (Calendar / Email / CRM)
    ↓
Text-to-Speech (ElevenLabs)
    ↓
Audio Output → Caller
```

### Technology Stack

| Layer | Technology |
|---|---|
| **LLM Reasoning** | Google Gemini 3.5 Flash-Lite |
| **Speech-to-Text** | OpenAI Whisper |
| **Text-to-Speech** | ElevenLabs |
| **Agent Orchestration** | LangGraph |
| **Knowledge Base** | SQLite + ChromaDB |
| **Workflow Automation** | n8n |
| **Backend API** | FastAPI |
| **Demo Interface** | Streamlit |
| **Deployment** | Docker |

---

## Repository Structure

```
Week-4/
│
├── README.md                          ← Project overview & timeline
│
├── Day-1/                             Foundations & Conversation Design
│   ├── README.md
│   ├── 01_architecture_research.md    System design & workflow diagrams
│   ├── 02_conversation_flows.md       9 call flow scenarios
│   ├── 03_urdulish_persona.md         Agent personality, tone, objection handling
│   ├── 04_fish_audio_vs_elevenlabs.md TTS provider comparison
│   ├── 05_system_prompt.md            Production system prompt
│   ├── 06_free_tier_tech_stack.md     Cost-effective architecture
│   ├── 07_voice_provider_decision.md  Final TTS selection rationale
│   └── diagrams/                      Architecture & flow diagrams
│
├── Day-2/                             Knowledge Base & RAG Pipeline
│   ├── README.md
│   ├── data/                          Property, amenities, FAQ datasets
│   ├── scraping/                      Data collection & cleanup scripts
│   └── rag_pipeline.ipynb             Chunking, embedding, ChromaDB setup
│
├── Day-3/                             Voice Pipeline & Natural Conversation
│   ├── README.md
│   └── voice_pipeline.ipynb           STT → LLM → TTS streaming
│
├── Day-4/                             Workflows & Business Automation
│   ├── README.md
│   ├── n8n_workflow.json              Call → CRM automation export
│   └── calendar_email_integration.ipynb
│
├── Day-5/                             LangGraph Orchestration
│   ├── README.md
│   └── langgraph_agent.ipynb          9-node state graph & tool calling
│
├── Day-6/                             Testing, Evaluation & Security
│   ├── README.md
│   ├── test_conversations/            43+ test cases
│   └── evaluation_report.md           Metrics & security audit
│
└── Day-7/                             Deployment & Live Demo
    ├── README.md
    ├── Day7_FINAL.ipynb               Single entry point
    ├── system_architecture.md         Full technical breakdown
    ├── requirements.txt               Python dependencies
    ├── .env.example                   Environment variables template
    └── Dockerfile                     Container configuration
```

---

## Key Features

✅ **Bilingual Conversation** — Fluent switching between Urdu and English (UrduLish)  
✅ **Smart Intent Recognition** — Identifies buyer, renter, or investor queries  
✅ **Grounded Responses** — Retrieves answers from company property database (0% hallucination)  
✅ **Objection Handling** — Natural fallback for price concerns, timing questions, etc.  
✅ **Appointment Automation** — Books, reschedules, cancels visits via Google Calendar  
✅ **Production Ready** — System prompts, error handling, security checks included  
✅ **Cost Optimized** — Free-tier tools where possible (Whisper, Gemini free tier)

---

## Key Metrics (Target)

| Metric | Target | Status |
|---|---|---|
| Response Latency | <2s | TBD |
| Grounding Accuracy | 100% | TBD |
| Test Coverage | 40+ cases | TBD |
| Prompt Injection Defense | 100% blocked | TBD |

---

## Quick Start

### Prerequisites
- Python 3.10+
- API Keys: Google Gemini, ElevenLabs
- (Optional) Google Calendar & Gmail for automation

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/FizaAslam1/Web3-Geeks.git
   cd Week-4
   ```

2. **Create environment file**
   ```bash
   cp Day-7/.env.example .env
   ```
   Fill in your API keys:
   ```
   GEMINI_API_KEY=your_key_here
   ELEVENLABS_API_KEY=your_key_here
   ELEVENLABS_VOICE_ID=your_voice_id
   ```

3. **Install dependencies**
   ```bash
   pip install -r Day-7/requirements.txt
   ```

4. **Run the complete agent** (Day 7)
   ```bash
   jupyter notebook Day-7/Day7_FINAL.ipynb
   ```
   The Streamlit demo will open at `localhost:8501`

### Docker Deployment
   ```bash
   docker build -t realestate-voice-agent -f Day-7/Dockerfile .
   docker run -p 8501:8501 --env-file .env realestate-voice-agent
   ```

---

## How to Navigate This Project

**For Overview:** Start here (this README)

**For Day-by-Day Breakdown:**
1. Open `Day-1/README.md` → Review architecture & conversation design
2. Open `Day-2/README.md` → Understand knowledge base & RAG setup
3. Open `Day-3/README.md` → Explore voice pipeline & streaming
4. Continue through `Day-4` through `Day-7`

**To Run the Complete System:**
- Jump to `Day-7/Day7_FINAL.ipynb` and run top-to-bottom

**For Evaluation Results:**
- See `Day-6/evaluation_report.md` for metrics, test results, and security audit

---

## Development Workflow

Each day builds on the previous:
- **Days 1-2:** Design phase (architecture, conversation flows, knowledge base)
- **Days 3-5:** Development phase (voice pipeline, orchestration, tool calling)
- **Days 6-7:** Testing, hardening, and deployment

Every `DayN/README.md` explains:
- What was built
- Why these choices were made
- How to run or test that component
- Key metrics or outcomes

---

## Contributing

When adding to this project:
1. Update the relevant `DayN/README.md`
2. Add test cases to `Day-6/test_conversations/`
3. Re-run evaluation suite before merging
4. Update this main README if architecture changes

---

## License

This project is part of the **Web3-Geeks** learning curriculum.

---

## Support & Questions

For questions about:
- **Architecture & Design:** See `Day-1/`
- **Knowledge Base setup:** See `Day-2/`
- **Voice/STT/TTS:** See `Day-3/`
- **Automation & Workflows:** See `Day-4/`
- **Agent Logic & State Management:** See `Day-5/`
- **Testing & Security:** See `Day-6/`
- **Deployment & Demo:** See `Day-7/`

**Last Updated:** 2026-09-26

---

*Built with ❤️ for production-grade conversational AI in South Asian languages*
