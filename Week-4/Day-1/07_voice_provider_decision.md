# Voice Provider Decision Record

**Status:** Final
**Date:** 23/09/2026
**Decided by:** Project team + one native Urdu speaker (listening evaluation)

## Summary

**ElevenLabs is the TTS provider for this project.** Fish Audio was evaluated and rejected on
quality grounds.

## Evaluation method

- 6 UrduLish sentences, written for realistic real-estate phone calls.
- Both providers tested on their free web playgrounds, same male voice style.
- Sentences 1 and 5 also tested in Urdu script.
- Each sentence scored 1–5 on: pronunciation, naturalness, Urdu-English switching, numbers/dates.
- Reviewed by the team and one native Urdu speaker.

## Results

| Metric | Fish Audio | ElevenLabs |
|---|---|---|
| Average score (all criteria, all sentences) | **2.5 / 5** | **4.0 / 5** |
| Urdu pronunciation | 2.5 / 5 | 4 / 5 |
| Urdu-English code-switching | 2.5 / 5 | 4 / 5 |
| Numbers and dates | 2 / 5 | 4.5 / 5 |
| Roman Urdu vs Urdu script | Poor on both; Roman slightly worse | Roman Urdu preferred |

## Key findings

- Fish Audio mispronounced common real-estate vocabulary: "marla" (said as "marfa"),
  "pachaas lakh", "dopahar", and several numbers.
- ElevenLabs correctly pronounced "marla", "kanal", "crore", "lakh", "DHA Phase 6",
  "Bahria Town", dates and times.
- ElevenLabs' Urdu-English switching sounded like a real Pakistani sales executive.
  Fish Audio's switching was abrupt and heavily accented.

## Trade-offs accepted

| Trade-off | Impact | Mitigation |
|---|---|---|
| Cost: ElevenLabs ~$0.18/min vs Fish Audio ~$0.05/min (reported) | 3–4× higher per-call cost | Text-only mode during development and testing; real TTS only for spot-checks and demo |
| Latency: ElevenLabs ~500 ms vs Fish Audio <200 ms (reported) | Risk to the under-2-second target | Measure in Day 3; shorter replies; filler phrases while TTS generates |
| Free-tier quota | Limited monthly minutes on both | Same text-only policy |

## Fallback

Fish Audio remains the fallback if ElevenLabs becomes unworkable on cost, quota, or latency.
TTS sits behind a single function in the pipeline, so the provider can be swapped without
redesigning the agent.

## Impact on later days

- **Day 3:** voice pipeline uses ElevenLabs streaming. Latency and Urdu quality measured again.
- **Day 6:** evaluation suite includes ElevenLabs-specific checks (latency, quota, failure handling).
- **Day 7:** demo uses ElevenLabs. Executive report notes the cost/quality trade-off and the
  fallback plan.