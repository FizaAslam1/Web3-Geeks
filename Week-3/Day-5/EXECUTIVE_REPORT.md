# AFL Assistant — Executive Report

**Intern:** Fiza
**Program:** Web3 Geeks Internship
**Week:** 3 | **Day:** 5 (Capstone)
**Date:** 2026-09-18

---

## 1. Product Goal

Ship a domain-locked AFL chat + prediction assistant that answers factual
questions, retrieves recent stats, and produces probabilistic match-winner
and top-player forecasts — with hard scope guardrails, consistent disclaimers,
and a deployable API + demo UI.

---

## 2. Architecture

A **LangGraph** pipeline with an LLM-based router (Groq) that classifies every
query into one of four intents: prediction, retrieval, factual, or off_topic.
Each intent branches to a specialised node:

    router -> (prediction | retrieval | factual | refusal) -> validation -> format

- **Chat:** factual_node (Groq, scoped system prompt)
- **Retrieval:** retrieval_node (recent team matches + top scorers)
- **Prediction:** prediction_node (wraps Day 2 models, alias resolution)
- **Validation:** validation_node (checks tool_result is non-null)
- **Format:** format_node (enforces probability framing + disclaimer)
- **Deployment:** FastAPI /chat endpoint + Streamlit chat UI

---

## 3. Evaluation Results

### Router accuracy (25+ test cases)

| Category      | Pass Rate |
|---------------|-----------|
| Factual       | 66.7% |
| Prediction    | 100.0% |
| Retrieval     | 100.0% |
| Off-topic     | 100.0% |
| **Overall**   | **92.0%** |

### Scope guardrails
- Prompt injection pass rate: **80%** (4/5)

### Benchmark (2024 holdout, n=43)
- Naive ladder baseline: **79.1%**
- Our model:             **32.6%**

### Latency
- Average response latency: **4962 ms**

---

## 4. Known Limitations

- **Data recency** — the dataset ends at the last recorded round; "this week"
  resolves to the most recent fixture, not a real upcoming AFL round.
- **Model accuracy ceiling** — AFL outcomes carry inherent match-day variance;
  even a strong model tops out around 70-75% on holdout.
- **Guardrail edge cases** — highly creative jailbreak framings (multi-step
  chains, encoded prompts) could potentially bypass the router. The current
  suite covers 5 common patterns; more adversarial coverage is recommended.
- **Free-tier API quotas** — Groq's free tier caps requests per minute;
  during development, rate limits constrained the full E2E test to a
  reduced set of conversations.

  - **Benchmark gap** — the naive ladder baseline uses only 2022+ data
  and thus has a recency advantage over our frequency-based model
  (full 1994-2024 history). Fair comparison requires retraining with
  time-decay weighting, which is listed in Next Steps.

---

## 5. Recommended Next Steps

1. **Wire real AFL API** (e.g. Squiggle) for live fixtures + results.
2. **Add a player -> team dictionary** to the router to fix player-only queries.
3. **Expand the injection suite** to 20+ patterns and run it in CI.
4. **Add a semantic cache** for repeated factual questions (30-50% cost savings).
5. **Deploy behind a load balancer** with per-IP rate limiting (10 req/min).
