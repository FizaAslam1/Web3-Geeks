# Day 1 — Foundations of AI Voice Agents and Conversation Design

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
| `diagrams/` | 11 PNG diagrams (architecture, workflow, flows 1-9) | Complete |

## Voice provider decision

The Task 4 listening test is complete. **ElevenLabs was selected** as the TTS provider because it
scored clearly higher than Fish Audio on Urdu pronunciation and UrduLish code-switching
(ElevenLabs **4.0 / 5** vs Fish Audio **2.5 / 5** across 6 test sentences).

This decision affects Day 3 (voice pipeline), Day 6 (evaluation) and Day 7 (demo). The full test
results and the accepted trade-offs (higher cost and latency) are documented in
`04_fish_audio_vs_elevenlabs.md` and `07_voice_provider_decision.md`.

## What changed from the first draft

- Persona: removed ungrounded claims ("fully verified", "area developed in 2 years"), added agent
  name and gender, added investment / builder / maintenance objections and a missing-data fallback line.
- Flows: added "not interested", "unclear", "no appointment found" and privacy-check branches; added
  seller flow and a shared fallback flow.
- Architecture: added VAD and barge-in, n8n, structured-vs-vector retrieval, demo audio input, and
  a Call-to-CRM workflow diagram with retries. TTS provider updated to ElevenLabs.
- System prompt: added UrduLish style, spoken-output format, privacy rule for returning callers,
  AI-disclosure rule, runtime date and office hours, silence and off-topic handling.
- Free-tier doc: TTS choice updated to ElevenLabs; backup plan for testing limits, Whisper hardware
  note and report limitations included.
- Task 4: listening test completed; Fish Audio evaluation finalised with ElevenLabs as the chosen
  provider. Decision record added as `07_voice_provider_decision.md`.