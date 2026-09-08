# Agent Foundations — Week 2, Day 2
## LangChain Agent Implementation with Gemini API

This directory contains a complete LangChain-based agent built on the Google Gemini API, extending the raw Python agent from Day 1 with production-ready patterns.

## Overview

**Day 2 builds on Day 1** by replacing hand-written agent logic with LangChain's structured abstractions:
- **Day 1** (raw Python): Manual ReAct loop, explicit tool calling, custom agent loop
- **Day 2** (LangChain): `create_tool_calling_agent` + `AgentExecutor`, decorator-based tools, built-in memory management

## Quick Start

### 1. Install Dependencies
```bash
pip install google-genai
pip install langchain langchain-classic langchain-google-genai
```

### 2. Get Your API Key
1. Visit [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Generate a free API key (no billing required)
3. Set it in the notebook's first cell:
```python
import os
os.environ["GEMINI_API_KEY"] = "your-key-here"
```

### 3. Run the Notebook
Open `langchain.ipynb` in VS Code or Jupyter, then **Run All**. The notebook is self-contained — no external imports needed.

---

## Files

| File | Purpose |
|------|---------|
| **`langchain.ipynb`** | Complete Day 2 implementation: `@tool`-decorated functions, `create_tool_calling_agent` + `AgentExecutor`, multi-turn memory, structured output, and tool error handling. |
| **`writeup_day2.pdf`** | 1-page technical summary: raw Python vs. LangChain comparison, annotated reasoning traces, and 3 real abstraction-leakiness bugs found during development. |
| **`products.json`** | Local JSON "database" used by the `get_product_price` tool. Auto-created if missing. |

---

## What's Covered

### Tools
- `calculator` — Simple arithmetic  
- `get_weather` — Stub weather lookup  
- `read_text_file` — File I/O  
- `get_product_price` — Real data from `products.json` (new in Day 2)

### Key Concepts
- **`@tool` decorator** — Cleaner tool definitions vs. hand-written JSON schemas
- **`create_tool_calling_agent`** — LangChain's high-level agent factory
- **`AgentExecutor`** — The orchestration layer that manages the agent loop
- **Multi-turn conversations** — Persistent memory across 3+ turns of dialogue
- **Structured output** — Pydantic models + `with_structured_output(...)`
- **Graceful error handling** — Tool errors caught and recovered, not crashing the agent

### Real Bug Examples
The `writeup_day2.pdf` documents **3 actual bugs** encountered and fixed:
1. `RunnableWithMessageHistory` fails on turn 2 with Gemini's "thinking" models
2. `AgentExecutor(handle_tool_error=True)` doesn't catch tool exceptions alone
3. Agent's final output is sometimes a raw list of Gemini content blocks, not plain text

---

## Model Notes

**`gemini-3.5-flash-lite`** is used throughout because it has:
- Higher free-tier daily quota than the newer `gemini-3.8-flash`
- Sufficient capability for agent reasoning

If Google retires this model, the API error will suggest a replacement — just swap the model name in the first cell.

---

## Tips for Learning

1. **Read the writeup first** — `writeup_day2.pdf` gives you the conceptual map
2. **Run the notebook cell-by-cell** — observe how the agent evolves
3. **Compare to Day 1** — open `agent_foundations.ipynb` (from `Week-2/Day-1`) to see how much LangChain abstracts away
4. **Experiment** — modify the tools, add new ones, change the prompt — see how the agent behaves

---

## Known Quirks (Documented, Not Bugs)

These are real LangChain behaviors, not errors to fix:

1. **`RunnableWithMessageHistory` + Gemini "thinking" models = turn 2 failure**  
   - Gemini's newer models return signed metadata that LangChain can't replay
   - **Workaround**: Manage memory manually (shown in the notebook) using the same pattern `ConversationBufferMemory` uses

2. **`AgentExecutor(handle_tool_error=True)` alone doesn't catch tool errors**  
   - Must set `handle_tool_error=True` on **each individual `Tool` object** too
   - Otherwise exceptions bubble up and crash the agent

3. **Agent's final output is sometimes raw Gemini content blocks, not a string**  
   - Extract `.text` from the block if you need clean text
   - This happens when the model returns multiple content types

All three are documented with reproducible examples in `writeup_day2.pdf`.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'langchain'` | Run `pip install langchain langchain-classic langchain-google-genai` |
| `APIError: API key not set` | Set `GEMINI_API_KEY` in the first cell before running |
| Agent crashes on tool error | Ensure both `AgentExecutor` and each `Tool` have `handle_tool_error=True` |
| `products.json` not found | The notebook auto-creates it on first run |

---

## Next Steps

- **Day 1 (raw Python)**: See `Week-2/Day-1/agent_foundations.ipynb` to understand the foundations
- **Extend the agent**: Add more tools, change the system prompt, or switch to a different model
- **Deploy**: Wrap the agent in an API (FastAPI, Flask) or chat interface (Streamlit, Discord bot)

---

## References

- [LangChain Docs](https://python.langchain.com/)
- [Gemini API Docs](https://ai.google.dev/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629) — The reasoning loop behind agent behavior
