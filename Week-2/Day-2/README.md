# Agent Foundations — Week 2

Raw-Python and LangChain agents built on the Gemini API, covering Day 1
(build an agent from scratch) and Day 2 (rebuild it with LangChain).

## Setup

```bash
pip install google-genai
pip install langchain langchain-classic langchain-google-genai
```

Get a free API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
(no billing needed), then set it before running any notebook:

```python
import os
os.environ["GEMINI_API_KEY"] = "your-key-here"
```

**Model note:** `gemini-3.5-flash-lite` is used throughout — it has a much
higher free-tier daily quota than the newer `gemini-3.8-flash`. If Google
retires this model name later, swap it for whatever the API error message
recommends at the time.

## Files

| File | What it is |
|---|---|
| `agent_foundations.ipynb` | **Day 1** — a minimal agent built from scratch in raw Python (no framework), covering the ReAct loop, tool calling, a hand-written agent loop with a `max_iterations` guardrail, memory handling, and 4 deliberately-triggered failure modes. |
| `writeup.pdf` | Day 1's 1-page write-up: the ReAct loop, tool schemas, and failure modes observed. |
| `agent_foundations_day2.ipynb` | **Day 2** — the same agent rebuilt with LangChain: `@tool`-decorated tools (including a real local JSON "database"), `create_tool_calling_agent` + `AgentExecutor`, multi-turn memory, structured Pydantic output, and configured tool-error recovery. |
| `writeup_day2.pdf` | Day 2's 1-page write-up: raw-Python vs. LangChain comparison, with a real annotated reasoning trace and 3 documented abstraction-leakiness bugs actually hit while building it. |
| `products.json` | Small local "database" the `get_product_price` tool reads from (auto-created by the Day 2 notebook if missing). |

## Running

Open either notebook in VS Code / Jupyter, set `GEMINI_API_KEY` in the
first cell, then **Run All**. Each notebook is self-contained — no other
files need to be imported.

## What each day covers

**Day 1 — raw Python:**
- `calculator`, `get_weather` (stub), `read_text_file` tools with hand-written JSON schemas
- A `while`-style agent loop: send message → check for a tool call → execute it → append the result → repeat
- Conversation memory (message history) vs. working memory (a tracking scratchpad) explained and logged live
- Failure modes deliberately triggered and handled: ambiguous request, tool error, hallucinated/undefined tool, infinite-loop guardrail

**Day 2 — LangChain:**
- The same tools recreated with the `@tool` decorator, plus a new `get_product_price` tool reading from a real local JSON file
- `create_tool_calling_agent` + `AgentExecutor` (via the `langchain-classic` package, since mainline LangChain 1.x moved to a newer `create_agent` API)
- Multi-turn memory across a 3-question follow-up conversation
- Structured output via `with_structured_output(...)` and a Pydantic model
- Configured graceful tool-error recovery (`handle_tool_error=True` — needed on **both** the individual tools and the `AgentExecutor`)

## Known quirks (documented, not bugs to "fix" further)

- **`RunnableWithMessageHistory` breaks on turn 2** with Gemini's newer
  "thinking" models — it stores the raw output message, which carries a
  signed metadata block that LangChain's message-coercion layer can't
  replay. Worked around by managing memory manually (Day 2 notebook,
  Task 4) — the same idea `ConversationBufferMemory` is built on.
- **`AgentExecutor(handle_tool_error=True)` alone does not catch tool
  exceptions** — each individual `Tool` object needs `handle_tool_error =
  True` set on it too.
- **The agent's final `output` is sometimes a raw list of Gemini content
  blocks**, not a plain string — extract `.text` from the block if you
  need clean text.

These three are called out explicitly in `writeup_day2.pdf` as real,
reproduced examples of LangChain's abstraction leaking.
