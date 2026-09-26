# Free-Tier Tech Stack Reference

This project uses only free-tier or open-source components: no paid subscriptions and no
credit-card-based services. This is the single source of truth for the stack used in every later
Day, so all code (Day 2 onward) should follow it.

## Chosen Stack

| Component | Choice | Why |
|---|---|---|
| LLM | **Gemini 3.5 Flash-Lite** (Google AI Studio API) | Free tier without a credit card, low latency, suited to a high-volume conversational agent |
| Speech-to-Text | **Whisper (local, open-source)** | Runs on local compute, zero API cost, no rate limits |
| Text-to-Speech | **ElevenLabs (free tier)** | Selected after the Task 4 listening test: scored 4.0 / 5 vs Fish Audio's 2.5 / 5 on Urdu pronunciation and UrduLish code-switching |
| Vector Database | **ChromaDB (local)** | Runs locally, no hosting cost, no account needed |
| Agent Framework | **LangGraph** | Open-source, free |
| Backend | **FastAPI** | Open-source, free |
| Database | **SQLite** (dev) / local PostgreSQL | Free, no cloud hosting cost |
| Calendar | **Google Calendar API** | Free tier is enough for small-scale use |
| Email | **Gmail API** or **Resend (free tier)** | Both have usable free tiers |
| Workflow Automation | **n8n (self-hosted, local / Docker)** | Free. Avoid n8n Cloud (paid) |
| Telephony (demo) | **Browser microphone / Streamlit voice UI** | Real phone numbers via telephony providers are paid; a real number is a production step, not a demo requirement |
| Deployment (dev/demo) | **Local machine** or free-tier Render / Railway | Free cloud hosts sleep when inactive, so allow a short wake-up delay before live demos |

## Gemini 3.5 Flash-Lite — Free Tier Limits

Verify the real numbers on your own dashboard (`aistudio.google.com`, your project, rate limits);
they change often.

- A free, rate-limited tier exists for Gemini 3.5 Flash-Lite with no credit card required.
- Exact published request-per-minute and request-per-day figures for this model were not found in
  one clear table at the time of writing. Google has cut free-tier limits several times through late
  2025 and 2026, and some users report figures as low as about 20 requests per day.
- Earlier Flash-Lite tiers ranged roughly 15-30 requests per minute and 200-1,000 per day. Treat
  this only as a rough starting expectation.

**Rate-limiting rules of thumb:**
- Add a 1-2 second delay between consecutive LLM calls during development and testing.
- One conversation turn can use more than one API call (retrieval, reasoning, tool follow-up), so
  real throughput is lower than the raw requests-per-minute number.

**Backup plan for the 40+ test conversations (Day 6):**
- Spread testing across several days instead of assuming a fixed daily budget.
- Run most tests in text-only mode and reserve voice for a small subset.
- If the daily limit blocks progress, switch to a second free LLM provider or a small local model
  for bulk test runs, and keep the LLM call behind one function so switching is a one-line change.

## ElevenLabs Free Tier — Main Constraint

ElevenLabs' free tier includes a limited monthly character/minute quota. TTS is called on every
agent reply, so this is the tightest budget in the stack. Check the exact quota on the team's own
ElevenLabs dashboard; it changes over time.

**Rule carried into every later Day:**
- During development and automated testing (Day 3, Day 6 suites), run in **text-only mode**: skip
  the TTS call and log or print what would have been spoken.
- Make real TTS calls only for (a) the listening test in Task 4 (done), (b) manual voice-quality
  spot-checks and (c) the final Day 7 recorded demo.

## ElevenLabs Latency Note

ElevenLabs is reported to have a higher baseline latency (~500 ms) than Fish Audio (<200 ms). The
Day 3 target is under 2 seconds from end-of-speech to first audio of the reply. This will be
measured in Day 3. If ElevenLabs pushes past the target, the mitigations are:
- Shorter replies (already a rule in the system prompt).
- Filler phrases ("Ji, ek second sir, check karta hoon") while TTS generates.
- Fallback to Fish Audio for non-critical or bulk calls only.

## Hardware Note for Local Whisper

Whisper runs locally, so speed depends on the machine. A GPU makes it fast; on CPU only, use a
smaller model (for example small or base) and check Urdu accuracy, because smaller models are weaker
on Urdu. Measure this in Day 3 and record the result.

## Limitations to Mention in the Final Report

- Free tiers are suitable for a capstone demo, not for a real client deployment. A production
  system needs paid plans with guaranteed limits and uptime.
- On free API tiers, provider terms may allow inputs to be used to improve their products. Real
  customer calls contain personal data, so a client deployment needs a paid tier with appropriate
  data-handling terms. Demo and test conversations should use fictional callers only.
- ElevenLabs is 3–4× more expensive per minute than Fish Audio at production volume; this cost
  trade-off is documented in `04_fish_audio_vs_elevenlabs.md` and `07_voice_provider_decision.md`.

## Alignment With Other Day 1 Documents

- **Task 1 (Architecture):** lists Whisper, Gemini 3.5 Flash-Lite, ElevenLabs, ChromaDB, n8n and a
  browser-based demo input, consistent with this table.
- **Task 4 (Fish Audio vs ElevenLabs):** ElevenLabs is selected on listening-test quality; Fish
  Audio is the documented fallback.
- **Task 5 (System prompt):** keeps replies short and does not assume unlimited LLM calls.