# Day 1 — Foundations of AI Voice Agents & Conversation Design

Project: Production-Grade AI Voice Agent for Real Estate (UrduLish)

## Files

| File | Task | Status |
|---|---|---|
| `01_architecture_research.md` | Task 1: Architecture research, system diagram, workflow diagram | Complete |
| `02_conversation_flows.md` | Task 2: 7 required flowcharts + seller flow + fallback flow | Complete |
| `03_urdulish_persona.md` | Task 3: Persona, phrases, objection handling | Complete |
| `04_fish_audio_vs_elevenlabs.md` | Task 4: Comparison table, listening test, **ElevenLabs selected** | Complete |
| `05_system_prompt.md` | Task 5: Production system prompt | Complete |
| `06_free_tier_tech_stack.md` | Supporting: free-tier stack and limits | Complete |
| `07_voice_provider_decision.md` | Supporting: one-page decision record | Complete |

## What's inside

### Task 1 — Architecture Research
Full pipeline documented: Telephony/Audio Input → VAD & Barge-in → Speech-to-Text (Whisper, local) → LLM Reasoning (Gemini 3.5 Flash-Lite) → Retrieval (SQL + ChromaDB) → Tool Calling → Memory (short-term + long-term) → Text-to-Speech (ElevenLabs) → Workflow Orchestration (LangGraph + n8n). Includes a latency budget (target: under 2 seconds, end-of-speech to first audio).

### Task 2 — Conversation Flow Design
9 flowcharts total: the 7 required (buyer, rental, commercial, investment, returning customer, rescheduling, cancellation), plus 2 extra added to cover the Day 6 test suite — a seller flow and a shared fallback flow (unclear speech, off-topic, silence, angry callers, prompt injection, "are you an AI?").

### Task 3 — UrduLish Persona Engineering
Persona: "Ahmed", a warm, professional, patient, persuasive Pakistani property consultant. Golden rules: never translate directly from English, never state a fact outside the knowledge base, short sentences, always end with a question or next step. Includes greeting variations, confirmations, hesitation phrases, and objection-handling scripts for price, trust, location, investment, builder, and maintenance concerns — each with a fallback line for when data isn't available.

### Task 4 — Fish Audio vs ElevenLabs Evaluation
A real listening test (6 UrduLish sentences, scored on pronunciation, naturalness, code-switching, and numbers/dates) found **ElevenLabs scored 4.0/5 average vs Fish Audio's 2.5/5**. ElevenLabs was selected despite being reported as 3–4× more expensive per minute and having higher baseline latency (~500ms vs <200ms) — the trade-off is documented and revisited in Day 7's executive report.

### Task 5 — System Prompt
Production system prompt covering scope, goal priority order, voice/style rules, spoken-output formatting (no markdown, numbers written as spoken), grounding guardrails, security guardrails (prompt-injection resistance, no fake bookings), AI-disclosure honesty rule, persuasion rules, appointment booking policy, and escalation rules.

## Key decision: Voice provider

**ElevenLabs was selected as the TTS provider** after Fish Audio's Urdu pronunciation and UrduLish code-switching scored poorly on real-estate vocabulary ("marla", "kanal", "crore", "lakh"). This decision affects Day 3 (voice pipeline), Day 6 (evaluation), and Day 7 (demo). Full test results in `04_fish_audio_vs_elevenlabs.md` and `07_voice_provider_decision.md`.
