# Week 2 Day 3 — LangGraph Research Assistant Agent

Web3Geek Internship — Agent Foundations track. A stateful, cyclical research-assistant agent
built with LangGraph: it plans, retrieves, drafts, critiques and self-corrects its own answer,
pauses for human approval before publishing, and persists/replays its run history.

## Files in this submission

| File | Description |
|---|---|
| `langgraph_agent_week2_day3.ipynb` | Main deliverable — the full working notebook (Tasks 1–5) |
| `week2_day3_writeup.md` / `.pdf` | Written explanation and comparison sections for each task |
| `langgraph_workflow.png` | Auto-generated diagram of the compiled graph (produced when the notebook runs, if PNG rendering is available) |

## What the agent does

```
plan → retrieve → generate → critique ─┬─→ human_review ─┬─→ publish → END
                     ^                  │                 └─→ reject  → END
                     └── revise ────────┘ (loop while quality < threshold
                                            and revisions < max_revisions)
```

1. **plan** — drafts a short research plan for the incoming query.
2. **retrieve** — fetches supporting snippets (stand-in for the Day 2 `search_web` tool).
3. **generate** — drafts an answer from the plan + retrieved snippets.
4. **critique** — scores the draft (0–1) and gives feedback; a conditional edge either loops
   back to `generate` via `revise` (bounded by `max_revisions`) or moves on.
5. **human_review** — the graph *pauses here* (`interrupt_before`) until a human sets
   `approved: True/False` and the run is resumed.
6. **publish / reject** — the risky action, gated behind approval.

State, checkpoints, and full run history persist via LangGraph's `MemorySaver`, so a thread can
be paused, resumed later, replayed from any earlier checkpoint, or inspected step-by-step.

## Requirements

```bash
pip install langgraph langchain langchain-core google-genai
```

Optional, for the auto-generated PNG diagram cell (skips gracefully without it):
network access to the Mermaid rendering API.

## Setup

The agent's `call_llm()` works two ways:

- **With a Gemini key** — set `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) as an environment variable
  *before* running the notebook, e.g.:
  ```bash
  export GEMINI_API_KEY="your-key-here"
  jupyter notebook langgraph_agent_week2_day3.ipynb
  ```
  Get a free key from [Google AI Studio](https://aistudio.google.com/apikey).
  **Never hardcode the key inside a notebook cell that you intend to submit or commit** — it
  gets baked into the file's saved output and source, and can leak. Set it in your shell, a
  local `.env` file (untracked), or a Colab "Secrets" panel instead.
- **Without a key** — the notebook automatically falls back to a small deterministic mock LLM,
  so every cell still runs end-to-end and every task remains demonstrable without any API cost.

## Running

Run all cells top to bottom. Each task section is self-contained and prints its own output —
state after each node (Task 2), the critique/revision loop trace (Task 3), the interrupt/resume
demo for both a rejection and an approval (Task 4), and the persistence/time-travel walkthrough
(Task 5). The final cells print the graph's Mermaid source and attempt a PNG export.

## Note on mock vs. real LLM behavior

The self-correction loop (Task 3) is guaranteed to fire with the mock LLM (scores climb
`0.55 → 0.75 → 0.95` across revisions by construction). Real Gemini output tends to score well
on the first draft, so the loop's *guard logic* still runs but may not visibly *loop* unless
`QUALITY_THRESHOLD` is raised. See the write-up for details.
