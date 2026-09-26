# Day 5 — LangGraph Orchestration & Tool Calling

Project: Production-Grade AI Voice Agent for Real Estate (UrduLish)

## Files

| File | Task | Status |
|---|---|---|
| `Day_5__LangGraph_Orchestration.ipynb` | Tasks 1–5: state design, graph design, tool integration, validation, state logging | Complete |

## What's inside

### Task 1 — LangGraph State Design
`AgentState` (TypedDict) holds: conversation history, user name/phone, budget, city, area, beds, intent, retrieved properties, appointment ID/start time, response text, and a running trace log — everything a node needs to reason without re-deriving it from scratch.

### Task 2 — Graph Design
A 9-node state graph, routed from a single `intent` entry point:

| Node | Handles |
|---|---|
| `intent` | Classifies caller intent from the utterance |
| `greeting` | Opening/closing pleasantries |
| `retrieve` | Property search — extracts budget/city/area/beds slots, routes to SQL or vector search |
| `book` | Checks availability, books via Google Calendar + Gmail |
| `reschedule` | Finds latest active appointment, moves it to a new slot |
| `cancel` | Cancels the latest active appointment |
| `ai_disclosure` | Honest "yes, I'm an AI" response when sincerely asked |
| `off_topic` | Politely redirects off-topic conversation |
| `fallback` | Catch-all for unclear input |

All 8 non-intent nodes route to `END` after responding — one exchange per turn, matching a real phone-call turn structure.

### Task 3 — Tool Integration
Wrapped as callable functions used by the graph nodes: `sql_search` / `vector_search` (property retrieval), `check_availability` / `book_appointment` / `reschedule_appointment` / `cancel_appointment` (Google Calendar), `send_email` (Gmail), `log_to_crm` (Google Sheets + SQLite), `trigger_n8n` (workflow automation).

### Task 4 — Validation
- `validate_booking_slot()` checks live Calendar availability before ever offering or confirming a time — no slot is booked unless it's actually free.
- No property is recommended outside what SQL/vector retrieval actually returns — no fabricated listings.
- Unclear input routes to `fallback`, which asks a clarifying question instead of guessing.

### Task 5 — State Logging
Every node appends a `trace` entry (node name, timestamp, and relevant details — e.g. detected intent, filters used, booking success/failure) to the state's running trace log, producing an annotated execution history for each call.

## Test Results

6 test scenarios run end-to-end, all correctly routed:

| Scenario | Expected intent | Result |
|---|---|---|
| Buy inquiry with budget/size/city | `retrieve` | ✅ Correct |
| Booking request | `book` | ✅ Correct |
| Reschedule request | `reschedule` | ✅ Correct |
| Cancellation request | `cancel` | ✅ Correct |
| "Are you an AI?" | `ai_disclosure` | ✅ Correct |
| Off-topic (cricket/weather) | `off_topic` | ✅ Correct |

**Note:** one retrieval test returned a property that didn't fully match the stated budget/size filter — flagged for review before the Day 7 demo; the routing logic itself was correct.

## Alignment with other days

- **Day 2 (RAG):** `retrieve` node reuses the same SQL/vector retrieval and city/budget/beds/area filtering built in Day 2.
- **Day 4 (Workflows):** `book`/`reschedule`/`cancel` nodes call the exact same Calendar/Gmail/CRM functions tested live in Day 4.
- **Day 6 (Testing):** this 9-node graph is the one put through the 43-case test suite and prompt-injection testing.
- **Day 7 (Deployment):** `run_agent()` from this day is imported directly into `agent_core.py`, powering both the FastAPI backend and the Streamlit live-call demo.
