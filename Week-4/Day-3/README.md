# Day 3 — Voice Agent & Natural Conversation

Project: Production-Grade AI Voice Agent for Real Estate (UrduLish)

## Files

| File | Task | Status |
|---|---|---|
| `Day3_Voice_Pipeline.ipynb` | Tasks 1–5: streaming pipeline, natural speech behaviors, context memory, objection handling, human evaluation | Complete |

## What's inside

### Task 1 — Streaming Voice Pipeline
Speech → LLM → Voice pipeline implemented and timed end-to-end, against the Day 1 latency budget of under 2 seconds.

**Measured result:** average total latency **1.3 seconds** (target met). One test exceeded 2 seconds; the documented mitigation is shorter replies and filler phrases while tools run (consistent with the system prompt's rules from Day 1).

### Task 2 — Natural Speech Behaviors
Implemented fillers, hesitation, thinking pauses, and acknowledgements ("Hmm...", "Ji bilkul...", "Ek second sir...", "Acha...") consistent with the persona designed in Day 1.

### Task 3 — Context Memory
Tested multi-turn context retention, e.g.:
> "Budget 3 crore hai." → (later) "DHA mein kya options hain?" → (later) "Us se sasti koi option?"

Memory carries budget, city, and area across turns without the caller repeating themselves.

### Task 4 — Objection Handling
Six objection types tested: price, trust, location, investment, builder/developer, and maintenance concerns — each answered with empathy first, then a fact from retrieved data, then a next step (matching the Day 1 objection-handling scripts).

### Task 5 — Human Evaluation
5 recorded conversations scored manually (post-listening) on naturalness, persuasiveness, fluency, latency, and conversation flow.

## Alignment with other days

- **Day 1:** persona phrases, hesitation fillers, and objection scripts used here come directly from `03_urdulish_persona.md`.
- **Day 4:** the memory and objection-handling behaviors tested here carry into the live booking conversations in Day 4.
- **Day 7:** the latency numbers here set the baseline later re-measured in Day 6's evaluation suite and referenced in the executive report.
