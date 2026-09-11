# 🤖 Client Onboarding Agent

**Web3Geeks Internship — Week 2, Day 5 Capstone**

An end-to-end AI agent that automates freelance client onboarding
using LangGraph, Gemini 1.5 Flash, and FastAPI — with human-in-the-loop
approval for consequential actions.

---

## 👤 Intern Details

| | |
|---|---|
| **Name** | Fiza Aslam |
| **Program** | Web3Geeks Internship |
| **Week / Day** | Week 2 / Day 5 |
| **Task** | Capstone — Production-Ready Agent System |
| **Date** | 11 September 2026 |

---

## 🎯 What This Project Does

A freelance agency receives a new client request. This agent:

1. **Validates** the input (name, email, service)
2. **Researches** the client in CRM + fetches pricing
3. **Drafts** a personalized welcome email using Gemini
4. **Waits for human approval** before committing
5. **Commits** the client to CRM and sends the email

All of this in **seconds**, with a human approving the final action.

---

## 🏗 Architecture
Client Request
↓
FastAPI /onboard
↓
LangGraph State Machine
↓
intake → research → draft → human_gate → commit
↓ ↓ ↓ ↓
errors degraded refusal approved?
↓ ↓ ↓ ↓
reject warn reject commit/pending

text

**Tools used:**
- CRM (SQLite) — check existing clients
- Pricing API (mocked) — fetch service pricing
- Calendar (mocked) — availability check

**Human checkpoint:** Before `commit` (sends email + saves to CRM).

---

## 🛠 Tech Stack

- **LangGraph** — agent workflow
- **Gemini 1.5 Flash** — LLM for email drafting
- **FastAPI** — REST API wrapper
- **SQLite** — CRM database
- **Pydantic** — input validation
- **Jupyter Notebook** — development environment

---

## 📓 Notebook Cells (What Each Does)

| Cell | Task | Purpose |
|------|------|---------|
| 1 | Setup | Install libraries |
| 2 | Setup | Imports + Gemini API |
| 3 | Task 2 | State + custom errors |
| 4 | Task 2 | CRM database + tools |
| 5 | Task 2 | 5 agent nodes |
| 6 | Task 2 | LangGraph workflow |
| 7 | — | Test run (5 cases) |
| 8 | **Task 3** | Evaluation (8 cases) |
| 9 | **Task 4** | FastAPI + logging |
| 9b | Task 4 | Run server |
| 10A-D | **Task 5** | Report + slides + checklist |

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
2. Set up Gemini API key
Create .env file:

text
GEMINI_API_KEY=your_key_here
Get free key: https://aistudio.google.com/app/apikey

3. Open the notebook
bash
jupyter notebook capstone.ipynb
4. Run cells 1 → 10 in order
5. Start the API server (Cell 9b)
Swagger UI: http://127.0.0.1:8000/docs

Health check: http://127.0.0.1:8000/health

🔌 API Endpoints
Method	Endpoint	Description
GET	/	Service info
GET	/health	Health check
POST	/onboard	Main onboarding endpoint
GET	/docs	Interactive Swagger UI
Example:

bash
curl -X POST http://127.0.0.1:8000/onboard \
  -H "Content-Type: application/json" \
  -d '{"name":"Ayesha","email":"ayesha@demo.com","service":"web-design"}'
Response:

json
{
  "request_id": "a1b2c3d4",
  "status": "approved",
  "draft": "Dear Ayesha, Welcome to Web3Geeks!...",
  "errors": [],
  "latency_ms": 8500,
  "tokens": 195,
  "tools_used": ["crm_lookup", "pricing_api", "commit"]
}
📊 Evaluation Results (Task 3)
8 test cases — 4 normal, 2 edge, 2 adversarial.

Metric	Result
Task Success Rate	7/8 (87.5%)
Safety Pass Rate	8/8 (100%)
Average Latency	8,374 ms
Cost per Run	~$0.00001
Prompt Injection Test	✅ Sanitized
Bad Input Rejection	✅ 2/2
Full Results Table
#	Type	Expected	Actual	Result
1	normal	approved	approved	✅
2	normal	approved	approved	✅
3	normal	approved	approved	✅
4	normal	approved	approved	✅
5	edge	rejected	rejected	✅
6	edge	rejected	rejected	✅
7	adversarial	approved	approved	✅
8	adversarial	pending	unknown	❌
Most Common Failure & Fix
Failure: Case 8 — unknown service triggered degraded mode, but
human_gate returned unknown instead of pending.

Fix: Updated human_gate to return pending when
research.degraded == True, forcing human review before any commit.

📈 Monitoring (Task 4)
See monitoring_checklist.md for full plan.

Key thresholds:

Signal	Warning	Critical
Error rate	>2%	>5%
p95 latency	>5s	>10s
Cost per run	>2× baseline	>5× baseline
Refusal rate	>5%	>10%
Cadence:

Weekly: 8 automated cases

Monthly: 20+ cases

Every 2 weeks: adversarial tests

Logs: Structured JSON in logs/agent.log.

📁 Files in This Project
File	Task	Description
capstone.ipynb	2, 3, 4	Main notebook (all cells)
crm.db	2	SQLite CRM with sample clients
eval_results.csv	3	8 test case scores
executive_report.md	5	2-page executive report
slide_outline.md	5	8-slide presentation outline
monitoring_checklist.md	4	Production monitoring plan
architecture.png	1	System architecture diagram
requirements.txt	—	Python dependencies
.env.example	—	API key template
logs/agent.log	4	Structured logs
⚠️ Known Limitations
Degraded mode trust — mitigated with "pending" gate

Single LLM provider (Gemini only)

Mocked pricing API — needs real integration

English only

No PII redaction in logs

🚀 Future Improvements
Async queue (Celery) for scale

Real pricing API integration

Anthropic fallback for resilience

PII redaction in logs

Multi-language support

📚 What I Learned
Building control-heavy agents with LangGraph

Human-in-the-loop design patterns

Evaluation-driven development

Production monitoring and observability

Deploying agents behind a FastAPI wrapper

🙏 Acknowledgments
Thanks to Web3Geeks mentors for the guidance and the framework
for this capstone.

Submitted by: Fiza Aslam
Web3Geeks Internship — Week 2, Day 5
