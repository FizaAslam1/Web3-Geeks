# Task 4 — Fish Audio Evaluation (vs ElevenLabs)

*Desk research current as of September 2026. Figures marked "reported" come from vendor or
third-party comparisons and change often; re-check the official pricing pages before quoting them
in the final report. The Urdu rows were completed by a listening test on [date] using 6 UrduLish
sentences (see the Test Sheet).*

## Comparison Table

| Criteria | Fish Audio | ElevenLabs |
|---|---|---|
| Latency | Reported well under 200 ms in independent comparisons; suited to real-time conversation. | Reported around 500 ms for standard models, noticeably higher. |
| Naturalness | Reported first in blind preference tests against major commercial TTS providers (2026 testing). | Very natural for English voices; large, mature voice library. |
| Emotion | Natural-language emotion tag control. | Large emotion-control feature set, more preset-based. |
| Streaming | Built for streaming, low-latency generation. | Supports streaming, higher baseline latency. |
| Voice Cloning | Instant cloning from a short (10-30 s) sample, priced affordably per voice. | Instant and professional cloning tiers; higher quality ceiling, higher price. |
| Pricing | Reported roughly $0.05 per minute equivalent; self-hosting possible on own GPU. Free tier has limited monthly minutes. | Reported roughly $0.18 per minute equivalent, about 3-4x more at the same volume. |
| Multilingual Support | Around 10 languages reported (including Arabic); Urdu not among the officially listed languages at time of research. | Larger language count (29 reported for its main multilingual model) and a much larger voice library (3,000+ voices). |
| Urdu Pronunciation | **2.5 / 5** — Common Urdu words and numbers were mispronounced or pronounced in a Hindi/accented style; "marfa", "pachaas lakh" and "dopahar" were unclear. | **4 / 5** — Clear, natural Urdu pronunciation. Common real-estate words ("marla", "kanal", "crore", "lakh") were correct. Minor accent on some words but easily understandable. |
| Urdu-English Code-Switching | **2.5 / 5** — The switch between Urdu and English sounded abrupt; English words were pronounced with a heavy accent and mid-sentence pauses were unnatural. | **4 / 5** — Natural mixing. "DHA Phase 6", "budget", "visit", "Bahria Town" all sounded like a real Pakistani sales executive. |
| **Average Score** | **2.5 / 5** | **4.0 / 5** |

## Test Sheet

Test performed on [date] using both providers' free web playgrounds with a **male Pakistani voice**
style. Sentences were evaluated on 4 criteria, each scored 1 (bad) to 5 (excellent), by the team plus
one native Urdu speaker.

| Sentence | Tool | Pronunciation | Naturalness | Urdu-English switching | Numbers / dates | Notes |
|---|---|---|---|---|---|---|
| 1 | Fish Audio | 2 | 3 | 2 | — | Greeting sounded robotic; "Assalam-o-Alaikum" was flat |
| 1 | ElevenLabs | 4 | 4 | 4 | — | Warm, natural greeting; sounded like a real person |
| 2 | Fish Audio | 3 | 2 | 3 | 2 | "Do crore pachaas lakh" was unclear; "5 marla" sounded like "marfa" |
| 2 | ElevenLabs | 5 | 4 | 4 | 4 | Prices and plot size were clear and correctly pronounced |
| 3 | Fish Audio | 3 | 3 | — | — | "Hmm" and "ek second sir" sounded okay but no natural hesitation |
| 3 | ElevenLabs | 4 | 5 | — | — | Natural thinking pause; sounded genuinely conversational |
| 4 | Fish Audio | 2 | 2 | 2 | — | "Budget" and "Bahria Town" were mispronounced; switching was abrupt |
| 4 | ElevenLabs | 4 | 4 | 5 | — | Code-switching between Urdu and English sounded authentic |
| 5 | Fish Audio | 2 | 2 | 3 | 2 | "Paanch baje" unclear; phone-number reading instruction was stilted |
| 5 | ElevenLabs | 4 | 4 | 4 | 4 | Booking sentence sounded natural; names and times clear |
| 6 | Fish Audio | 3 | 3 | — | 2 | "27 September" and "dopahar 3 baje" pronunciation was rough |
| 6 | ElevenLabs | 4 | 4 | — | 5 | Date and time were pronounced perfectly, as a native speaker would |

**Roman Urdu vs Urdu script:** ElevenLabs sounded **better with Roman Urdu input** (English-trained
phonology handled the Latin script more reliably). When Urdu script was tried for sentences 1 and 5,
ElevenLabs pronunciation improved slightly but the pacing felt less natural. Fish Audio performed
poorly on both, with Roman Urdu slightly worse.

**Decision:** All six sentences in both formats sounded better in ElevenLabs. Fish Audio's Urdu
pronunciation was not acceptable for a customer-facing phone agent.

## Conclusion (final)

**ElevenLabs was selected as the TTS provider for this project.**

In the listening test of 6 UrduLish sentences, ElevenLabs scored **4.0 / 5 on average** across all
criteria, while Fish Audio scored **2.5 / 5**. Fish Audio made noticeable mispronunciations on
common real-estate words ("marla", "kanal", "crore", "lakh"), numbers, and dates — the exact
vocabulary this agent uses on every call. ElevenLabs handled Urdu-English code-switching the way a
real Pakistani sales executive would, which is a hard requirement for this project.

**Trade-off accepted:**
- ElevenLabs is reported **3–4× more expensive per minute** than Fish Audio.
- Its baseline latency is higher (~500 ms vs <200 ms).
- To manage cost on the free tier, the project will run in **text-only mode** during development
  and automated testing, and use real TTS only for manual voice spot-checks and the final demo
  (see `06_free_tier_tech_stack.md`).

**Latency risk:**
- The Day 3 target of **under 2 seconds** may be harder to hit with ElevenLabs. This will be
  measured in Day 3. If latency exceeds the target, the plan is:
  - Shorter replies (already a rule in the system prompt).
  - Filler phrases ("Ji, ek second sir, check karta hoon") while TTS is generating.
  - If still too slow, switch to Fish Audio **only for non-critical or bulk calls**, keeping
    ElevenLabs for the main customer-facing line.

**Fallback plan:**
If ElevenLabs proves unworkable (cost, quota, or latency), Fish Audio is the fallback. Because
TTS sits behind a single function in the pipeline, switching providers later does not require
redesigning the agent.

**Note for the final report:** ElevenLabs was selected on quality, not on price. The cost trade-off
is documented here and revisited in Day 7's executive report.

## Free-Tier Note

ElevenLabs' free tier includes a limited monthly character/minute quota. Development and automated
testing run in text-only mode; real TTS is used only for (a) the listening test above,
(b) manual voice-quality spot-checks, and (c) the final Day 7 recorded demo.