# Monitoring Checklist — Onboarding Agent

## Metrics to Track
| Metric | Source | Why |
|--------|--------|-----|
| Request count | logs/agent.log | Traffic volume |
| Error rate | 500s / total | Reliability |
| p50/p95 latency | latency_ms | UX |
| Token usage | tokens field | Cost |
| Tool failure rate | errors contains 'tool' | External deps |
| Approval override rate | status=pending | Accuracy |
| Refusal rate | errors contains 'refusal' | Safety |

## Alert Thresholds
| Signal | Warning | Critical |
|--------|---------|----------|
| Error rate | >2% (15min) | >5% |
| p95 latency | >5s | >10s |
| Cost per run | >2x baseline | >5x |
| Refusal rate | >5% | >10% |
| Tool failure rate | >10% | >25% |

## Logging
- Format: JSON
- Destination: console + logs/agent.log
- Retention: 30 days

## Re-evaluation Cadence
- Weekly: 8 automated cases
- Monthly: 20+ cases
- On change: any prompt/model update
- Adversarial: every 2 weeks

## Escalation
- On-call: critical threshold
- Product: override >10%
- ML team: refusal spike
