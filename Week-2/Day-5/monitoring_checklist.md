# Production Monitoring Checklist — Support Ticket Triage Agent

## What to track

| Metric | Source | Why it matters |
|---|---|---|
| Error rate (5xx / tool exceptions) | API logs (`event=error`) | Detects graph crashes, tool outages |
| Refund API failure rate (timeout/error) | `refund_tool_status` in trace | Detects upstream payment-provider degradation |
| Latency (p50 / p95 / p99) | `total_latency_ms` per request | Catches slow KB lookups, model latency creep |
| Cost drift | tokens/run × price, rolled up daily | Catches prompt bloat or model upgrades inflating spend |
| Category distribution | `category` field, daily histogram | Sudden shifts flag new ticket types the classifier wasn't built for |
| Escalation rate | `needs_human_approval` % of tickets | Too high = classifier over-escalating (reviewer burden); too low = risk of missed refunds |
| Human review turnaround time | timestamp gap: `pending_human` → decision | SLA risk on time-sensitive tickets |
| Output quality drift | weekly sample re-scored against eval rubric | Silent regression after prompt/model changes |
| Unknown-category rate | % tickets classified `unknown` | Signals KB/classifier coverage gaps |

## Alert thresholds (starting points — tune after 2–4 weeks of baseline data)

- **Error rate** > 2% of requests in a rolling 15-min window → page on-call
- **Refund API failure rate** > 20% in a rolling 1-hour window → page on-call (payment provider issue)
- **p95 latency** > 3x the 7-day rolling median → warn
- **Daily cost** > 1.5x the 7-day rolling average → warn
- **Escalation rate** moves outside a set band (e.g. 10–35% depending on ticket mix) → warn
- **Unknown-category rate** > 15% in a day → warn (KB or classifier needs an update)
- **Human review turnaround** > 4 business hours on any `high`-severity ticket → page reviewer lead

## Re-evaluation cadence

- **Weekly**: run the automated eval suite (`eval/run_eval.py`) against the current KB/prompt; diff against last week's results.json.
- **Monthly**: pull 30 real production tickets (stratified across categories, including any newly-observed `unknown` clusters), hand-label them, and re-score the classifier's precision/recall per category.
- **On every prompt, KB, or model change**: run the full eval suite before deploy; block deploy if `task_success_rate` or `safety_pass_rate` regresses.
- **Quarterly**: audit a sample of human-approval decisions to confirm the escalation threshold ($200 refund cutoff, high-severity keyword list) still matches actual business risk tolerance.
