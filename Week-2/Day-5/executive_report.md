# Client Onboarding Agent — Executive Report
**Date:** 11 September 2026
**Author:** Web3Geeks Capstone

## 1. Business Goal
Freelance agencies lose 3-5 hours per new client on manual onboarding.
This project delivers an AI agent that automates onboarding end-to-end
while keeping a human in the loop for consequential actions.

## 2. Architecture
LangGraph state machine: intake -> research -> draft -> human_gate -> commit.
Tools: CRM (SQLite), pricing API, calendar.
Human checkpoint before commit.

## 3. Framework Choice
LangGraph chosen because workflow is control-heavy (branching, retries,
approval pauses). CrewAI is for emergent role collaboration. Raw loop
rejected due to ad-hoc error semantics.

## 4. Evaluation Results
- Task success: 7/8 (87.5%)
- Safety: 8/8 (100%)
- Avg latency: 8,374 ms
- Cost per run: ~$0.00001

Most common failure: Case 8 (unknown service). Fix applied.

## 5. Known Limitations
1. Degraded mode trust
2. Single LLM provider
3. Mocked pricing API
4. No multi-language
5. No PII redaction

## 6. Next Steps
Scaling: async queue, caching, multi-region.
Guardrails: PII redaction, output filters, rate limiting.
Human oversight: approval SLA, weekly sampling, adversarial tests.
