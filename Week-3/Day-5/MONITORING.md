# AFL Assistant — Monitoring & Maintenance Plan

## 1. Metrics to Track

| Metric | What it measures | Alert Threshold | Cadence |
|---|---|---|---|
| **Response latency (p50/p95/p99)** | Per-call time-to-response | p99 > 8s for 5 min | Continuous |
| **Tool error rate** | % of prediction/retrieval calls that raised errors | > 2% | Hourly |
| **Off-topic leak rate** | % of off-topic queries answered as if in-scope | > 5% | Daily |
| **Prediction accuracy drift** | Correct match-winner picks over rolling 100 predictions | Drop > 10% vs baseline | Weekly |
| **Injection guardrail pass rate** | % of injection attempts correctly refused | < 95% | Weekly (rerun test suite) |
| **Token usage per session** | Cumulative tokens/session | p99 > 50k | Daily |
| **Cost per session ($)** | $ spent / session | p99 > $0.25 | Daily |

## 2. Alert Thresholds

- **P99 latency > 8s** — page on-call; likely upstream LLM provider issue.
- **Tool error rate > 2%** — investigate immediately; often a data/column mismatch.
- **Off-topic leak rate > 5%** — rerun router prompt tuning.
- **Prediction accuracy drop > 10%** — trigger model retraining (see section 3).

## 3. Weekly Retraining / Refresh Loop

1. **Monday 06:00 UTC** — pull latest round's real results into `team_matches`.
2. Recompute `_win` frequency table and rebuild baseline model features.
3. Run the held-out 2024 sanity check; if accuracy drops > 5%, retrain
   the Day 2 pickle model (`match_winner_model.pkl`).
4. Redeploy the updated pickle; re-run Cell 19 benchmark comparison.
5. Publish weekly report: accuracy, drift, incidents.

## 4. Monthly Review

- Full re-run of the 25+ case evaluation suite (Cell 17).
- Review prompt injection attempts log; add new attack patterns to Cell 16.
- Tune alert thresholds based on observed baseline variance.

## 5. Incident Playbook

- **Prediction wrong on obvious matchup** — check alias resolution first.
- **Latency spike** — check Groq status page; consider fallback model.
- **Guardrail breach** — quarantine the offending query, add to injection suite.
