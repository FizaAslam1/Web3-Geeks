# Day 1 — Foundations of AI Voice Agents and Conversation Design

This day lays the groundwork for a production-grade AI voice agent for a real-estate outreach use case in UrduLish. The focus is on designing the system architecture, conversation logic, tone and persona, and the voice stack before moving into implementation.

## Goal

Build a strong foundation for an AI voice assistant that can:

- handle outbound or inbound real-estate calls
- switch naturally between Urdu and English (UrduLish)
- qualify leads and book appointments
- respond with clear fallback behavior when a caller is silent, unclear, or not interested
- operate with a practical, cost-aware technical stack

## What we covered

- Architecture research for a modular AI voice calling system
- Conversation flow design for leads, seller conversations, and fallback branches
- Persona definition and objection handling in UrduLish
- Voice provider comparison and listening tests
- Production-ready system prompt design
- Free-tier technical stack recommendations and constraints

## Deliverables

| File | Focus |
|---|---|
| `00_README.md` | Overview of Day 1 project outcomes and decisions |
| `01_architecture_research.md` | Architecture research, workflow design, and system diagram |
| `02_conversation_flows.md` | Core call flows, edge cases, and fallback logic |
| `03_urdulish_persona.md` | Agent persona, tone, phrases, objection handling |
| `04_fish_audio_vs_elevenlabs.md` | Voice provider comparison and listening test results |
| `05_system_prompt.md` | Production system prompt for the agent |
| `06_free_tier_tech_stack.md` | Low-cost stack and platform limits |
| `07_voice_provider_decision.md` | Decision record explaining the selected TTS provider |
| `diagrams/` | Architecture and conversation diagrams |

## Key decision

The Day 1 evaluation concluded that ElevenLabs was the best TTS choice for this project. It performed better than Fish Audio on Urdu pronunciation and code-switching quality, which is essential for a fluid UrduLish voice experience.

This decision informs the later implementation and evaluation work in the project timeline.

## Recommended order

To review the work in sequence, start with:

1. `01_architecture_research.md`
2. `02_conversation_flows.md`
3. `03_urdulish_persona.md`
4. `04_fish_audio_vs_elevenlabs.md`
5. `05_system_prompt.md`
6. `06_free_tier_tech_stack.md`
7. `07_voice_provider_decision.md`

## Outcome

Day 1 establishes the product and conversation foundation for the AI voice agent, including the data model, stack decisions, and user-facing behavior. It serves as the blueprint for the implementation work that follows in later days.
