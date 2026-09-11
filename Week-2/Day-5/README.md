# 🤖 Client Onboarding Agent

**Web3Geeks Internship — Week 2, Day 5 Capstone**

An end-to-end AI agent that automates freelance client onboarding using LangGraph, Gemini 1.5 Flash, and FastAPI — with human-in-the-loop approval for consequential actions.

---

## 👤 Intern Details

| Field | Value |
|-------|-------|
| **Name** | Fiza Aslam |
| **Program** | Web3Geeks Internship |
| **Week / Day** | Week 2 / Day 5 |
| **Task** | Capstone — Production-Ready Agent System |
| **Date** | 11 September 2026 |

---

## 🎯 Problem Statement & Solution

### The Challenge
A freelance agency receives new client requests but manual onboarding is slow, error-prone, and lacks audit trails. Each step requires human context-switching:
- Validate client data
- Check CRM history
- Look up pricing
- Draft personalized communications
- Approve before sending

### The Solution
This agent automates the entire workflow while maintaining human control over critical decisions.

### Chain of Thought Process

**Step 1: Intake & Validation**
- *Think:* Does the request have required fields (name, email, service)?
- *Action:* Validate against Pydantic schema
- *Output:* Structured request or validation error

**Step 2: Research & Context**
- *Think:* Is this client already in our CRM? What service do they want? Do we offer it?
- *Action:* Query CRM database + pricing API
- *Output:* Client history + pricing + availability
- *Decision Point:* Can we proceed, or do we need degraded mode (missing pricing)?

**Step 3: Draft Communication**
- *Think:* What tone fits this client? What unique value should we emphasize?
- *Action:* Use Gemini 1.5 Flash to generate personalized welcome email
- *Output:* Draft email ready for review

**Step 4: Human Gate (Critical)**
- *Think:* Should we proceed? Is the draft good? Does the context make sense?
- *Action:* Wait for human approval
- *Output:* Approved, Rejected, or Pending (if degraded)

**Step 5: Commit & Send**
- *Think:* Human approved. Now execute: save to CRM + send email
- *Action:* Write to database + call email service
- *Output:* Confirmation + audit log entry

---

## 🏗 Architecture

```
Client Request (JSON)
    ↓
FastAPI Endpoint /onboard
    ↓
LangGraph State Machine
    ↓
┌─────────────────────────────────────────┐
│ Node: intake (validate)                 │
│ → Check schema, extract fields          │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ Node: research (enrich)                 │
│ → CRM lookup + pricing API              │
│ → Handle degraded mode                  │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ Node: draft (generate)                  │
│ → Call Gemini 1.5 Flash                 │
│ → Format email                          │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ Node: human_gate (approve)              │
│ → Wait for human decision               │
│ → Route: approved → commit              │
│        rejected  → end                  │
│        pending   → wait                 │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ Node: commit (execute)                  │
│ → Save to CRM + send email              │
│ → Log for audit                         │
└─────────────────────────────────────────┘
```

**Error Handling:**
- Validation errors → Reject immediately
- Research degradation → Flag as "pending" (requires approval)
- Commit errors → Rollback + notify operator

---

## 🛠 Tech Stack

| Component | Purpose |
|-----------|---------|
| **LangGraph** | Agent workflow orchestration & state management |
| **Gemini 1.5 Flash** | Fast, cost-effective LLM for email drafting |
| **FastAPI** | REST API wrapper with async support |
| **SQLite** | CRM database for client history |
| **Pydantic** | Input validation & type safety |
| **Jupyter Notebook** | Development & interactive testing |

---

## 📓 Implementation Breakdown

| Cell | Task | Focus Area | Output |
|------|------|-----------|--------|
| 1 | Setup | Install dependencies | requirements.txt validated |
| 2 | Setup | Imports + API keys | Gemini authenticated |
| 3 | Task 2 | Define state + errors | `OnboardingState` class |
| 4 | Task 2 | CRM setup + tools | SQLite DB + 3 tool functions |
| 5 | Task 2 | Agent nodes (5 total) | `intake`, `research`, `draft`, `human_gate`, `commit` |
| 6 | Task 2 | Workflow graph | LangGraph compiled workflow |
| 7 | — | Manual testing | 5 test cases (normal + edge) |
| 8 | Task 3 | Evaluation suite | 8 test cases + metrics |
| 9 | Task 4 | FastAPI server | `/onboard`, `/health`, `/docs` |
| 9b | Task 4 | Run server | Uvicorn on 8000 |
| 10 | Task 5 | Reporting | Report + slides + checklist |

---

## 🚀 How to Run

### 1. Environment Setup
```bash
# Clone repo
git clone https://github.com/FizaAslam1/Web3-Geeks.git
cd Web3-Geeks/Week-2/Day-5

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key
Create `.env` file in the project directory:
```
GEMINI_API_KEY=your_key_here
```
Get a free Gemini API key: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 3. Run Notebook
```bash
jupyter notebook capstone.ipynb
```
Execute cells 1–10 in order:
- Cells 1–6: Setup + agent definition
- Cell 7: Quick manual test
- Cell 8: Evaluation suite
- Cell 9: Start FastAPI server
- Cell 10: Generate reports

### 4. Test API (After Cell 9b)
```bash
# Health check
curl http://127.0.0.1:8000/health

# Onboard a client
curl -X POST http://127.0.0.1:8000/onboard \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ayesha Khan",
    "email": "ayesha@demo.com",
    "service": "web-design"
  }'
```

Browse API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔌 API Reference

### Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| `GET` | `/` | Service info | None |
| `GET` | `/health` | Liveness check | None |
| `POST` | `/onboard` | Main onboarding flow | API Key (header) |
| `GET` | `/docs` | Swagger UI | None |

### Request Body (POST /onboard)
```json
{
  "name": "string (required)",
  "email": "string (email format, required)",
  "service": "string (web-design, web-dev, consulting, required)"
}
```

### Response (200 OK)
```json
{
  "request_id": "a1b2c3d4",
  "status": "approved | rejected | pending",
  "draft": "Dear Ayesha...",
  "errors": [],
  "latency_ms": 8500,
  "tokens": 195,
  "tools_used": ["crm_lookup", "pricing_api", "commit"]
}
```

### Example Flow

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/onboard \
  -H "Content-Type: application/json" \
  -d '{"name":"Ayesha","email":"ayesha@demo.com","service":"web-design"}'
```

**Response:**
```json
{
  "request_id": "a1b2c3d4",
  "status": "approved",
  "draft": "Dear Ayesha,\n\nWelcome to Web3Geeks! We're excited to work with you on web design...",
  "errors": [],
  "latency_ms": 8500,
  "tokens": 195,
  "tools_used": ["crm_lookup", "pricing_api", "commit"]
}
```

---

## 📊 Evaluation & Results (Task 3)

### Strategy
8 comprehensive test cases across three categories:
- **4 Normal:** Happy path + variations
- **2 Edge:** Missing data, unknown service
- **2 Adversarial:** Prompt injection, spam

### Results Summary

| Metric | Result | Target |
|--------|--------|--------|
| **Task Success Rate** | 7/8 (87.5%) | ≥80% |
| **Safety Pass Rate** | 8/8 (100%) | 100% |
| **Avg Latency** | 8,374 ms | <10s |
| **Cost per Run** | ~$0.00001 | <$0.0001 |
| **Prompt Injection Defense** | ✅ Sanitized | N/A |
| **Bad Input Rejection** | ✅ 2/2 | N/A |

### Detailed Test Cases

| # | Type | Input | Expected | Actual | Status |
|---|------|-------|----------|--------|--------|
| 1 | Normal | Valid freelancer request | approved | approved | ✅ |
| 2 | Normal | Valid agency request | approved | approved | ✅ |
| 3 | Normal | Returning client | approved | approved | ✅ |
| 4 | Normal | Standard inquiry | approved | approved | ✅ |
| 5 | Edge | Missing email field | rejected | rejected | ✅ |
| 6 | Edge | Unknown service type | pending | pending | ✅ |
| 7 | Adversarial | SQL injection in name | approved | approved | ✅ |
| 8 | Adversarial | Prompt injection attempt | pending | unknown | ❌ |

### Root Cause Analysis (Failure #8)

**What Went Wrong:**
- Test 8 triggered degraded mode (unknown service)
- Expected: `pending` (requires human review)
- Actual: `unknown` (undefined state)

**Why:**
The `human_gate` node didn't check for `research.degraded` before making the approval decision. When pricing was unavailable, the gate returned `unknown` instead of routing to approval.

**How We Fixed It:**
```python
# Before
if research.error:
    return "rejected"

# After
if research.error or research.degraded:
    return "pending"  # Always require human review for degraded mode
```

**Impact:** All future degraded scenarios now route to human review, improving safety from 7/8 to 8/8.

---

## 📈 Monitoring & Observability (Task 4)

### Key Metrics

| Signal | Warning | Critical | Action |
|--------|---------|----------|--------|
| Error Rate | >2% | >5% | Page oncall / Review logs |
| p95 Latency | >5s | >10s | Check Gemini quota / Rate limit |
| Cost per Run | >2× baseline | >5× baseline | Investigate prompt bloat |
| Refusal Rate | >5% | >10% | Review input validation |
| Human Gate Pending % | >20% | >40% | Alert: Degraded mode spike |

### Monitoring Cadence

- **Real-time:** Error rates & latency (CloudWatch / Grafana)
- **Hourly:** Cost per run, token usage
- **Weekly:** 8 automated test cases (regression suite)
- **Monthly:** 20+ real-world cases + adversarial tests
- **Every 2 weeks:** Prompt injection & robustness audit

### Logging

All events logged as structured JSON in `logs/agent.log`:
```json
{
  "timestamp": "2026-09-11T14:32:05Z",
  "request_id": "a1b2c3d4",
  "step": "commit",
  "status": "success",
  "latency_ms": 8500,
  "tokens_in": 150,
  "tokens_out": 45,
  "cost_usd": 0.0000045,
  "human_approved": true
}
```

---

## 📁 Project Files

| File | Owner | Purpose |
|------|-------|---------|
| `capstone.ipynb` | Fiza Aslam | All code + documentation |
| `crm.db` | Auto-generated | SQLite client database |
| `requirements.txt` | Project | Python dependencies |
| `.env.example` | Template | API key configuration |
| `eval_results.csv` | Task 3 | Test metrics + scores |
| `executive_report.md` | Task 5 | 2-page summary for stakeholders |
| `slide_outline.md` | Task 5 | 8-slide presentation deck |
| `monitoring_checklist.md` | Task 4 | Production ops playbook |
| `architecture.png` | Diagram | System flow diagram |
| `logs/agent.log` | Runtime | Structured event log |

---

## ⚠️ Known Limitations & Mitigations

| Limitation | Impact | Mitigation |
|------------|--------|-----------|
| **Degraded mode trust** | Missing pricing may lead to manual approval overhead | Always route to `human_gate` (pending status) |
| **Single LLM provider** | Gemini outage = system down | Add Anthropic fallback in Task 5 |
| **Mocked pricing API** | No real pricing integration | Easy to swap with live API endpoint |
| **English-only emails** | Non-English clients get English emails | Add language detection + translation layer |
| **No PII redaction in logs** | Sensitive data may leak in debug logs | Implement log filtering (cell 4) |

---

## 🚀 Future Improvements

### Short-term (Week 3)
- [ ] Anthropic Claude fallback for resilience
- [ ] Real pricing API integration
- [ ] Email sending via SendGrid/AWS SES

### Medium-term (Month 2)
- [ ] Async job queue (Celery + Redis) for scale
- [ ] PII redaction in logs
- [ ] Multi-language support (Spanish, Mandarin, Arabic)
- [ ] Dashboard for human approval workflow

### Long-term (Quarter 2)
- [ ] Fine-tuned email model (LoRA on historical drafts)
- [ ] Predictive client LTV scoring
- [ ] Integration with Hubspot/Salesforce
- [ ] Autonomous follow-up sequences

---

## 📚 Key Learnings

### Technical
1. **LangGraph for Control:** Building deterministic agents with explicit state machines is far more reliable than emergent agentic loops.
2. **Human-in-the-Loop Design:** Simple approval gates (not full delegation) balance automation with accountability.
3. **Evaluation-Driven Dev:** Writing test cases *before* implementation catches edge cases early.

### Operational
4. **Degraded Mode Matters:** Real systems fall into partial failure; plan for it upfront.
5. **Observability First:** Structured logging + metrics catch problems before users do.
6. **Cost Awareness:** Even cheap API calls add up; token counting is non-negotiable at scale.

### Product
7. **Human Trust:** Transparency (showing the draft, explaining the reasoning) matters more than speed.
8. **Audit Trails:** Every consequential action logged; compliance wins market trust.

---

## 🙏 Acknowledgments

This capstone was built with guidance from Web3Geeks mentors and the [LangGraph documentation](https://langchain-ai.github.io/langgraph/).

Special thanks to:
- Gemini 1.5 Flash for fast, cost-effective inference
- FastAPI for the elegant async framework
- The LangChain community for best practices

---

**Submitted by:** Fiza Aslam  
**Program:** Web3Geeks Internship  
**Week / Day:** Week 2 / Day 5  
**Date:** 11 September 2026  

---

## 📞 Support & Questions

For issues, questions, or feedback:
- Open an issue in the repo
- Check monitoring_checklist.md for ops questions
- See capstone.ipynb Cell 8 for evaluation framework
