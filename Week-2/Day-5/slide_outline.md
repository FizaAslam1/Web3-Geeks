# Stakeholder Presentation — Slide Outline

## Slide 1: Problem (30s)
Manual onboarding = 3-5 hours per client.

## Slide 2: Live Demo (60s)
POST /onboard with valid client -> welcome email in seconds.

## Slide 3: Architecture (60s)
intake -> research -> draft -> human_gate -> commit.
Human in loop before commitment.

## Slide 4: Framework Choice (30s)
LangGraph for control-heavy workflow.

## Slide 5: Evaluation (60s)
7/8 success, 8/8 safety, 8.4s latency, $0.00001/run.

## Slide 6: Failure & Fix (60s)
Adversarial case: unknown service -> fixed with pending gate.

## Slide 7: Monitoring (45s)
JSON logs, thresholds, weekly re-eval.

## Slide 8: Roadmap & Ask (45s)
Q4: real API, Anthropic fallback. Q1: async queue, PII redaction.
