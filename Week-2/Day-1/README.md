# Week 2, Day 1 — Agent Foundations

Reasoning Loops, Tool Calling & Raw Python Agents — built from scratch, no LangChain / LangGraph, using the **Gemini API** directly.

## Files

| File | Description |
|---|---|
| `agent_foundation.ipynb` | Full notebook — all 5 tasks, real executed outputs |
| `Agent_Foundations_Writeup.docx` / `.pdf` | 1-page write-up: ReAct loop, tool schemas, failure modes |

## What's inside

**Task 1 — Agent Concepts.** Agent vs. chatbot vs. workflow, what makes something "agentic," and the ReAct pattern (Reason → Act → Observe → repeat).

**Task 2 — Tool Calling.** Three tools with full JSON schemas — `calculator`, `get_weather` (stub), `read_text_file` — plus a real single round-trip: model picks a tool, we execute it, result sent back, final answer returned.

**Task 3 — Minimal Agent Loop.** A raw `while`-loop agent (`run_agent()`): send message → check for a tool call → execute it → append the result → repeat until the model answers in plain text. Includes a `max_iterations` safeguard. Tested on a real 2-tool-call task (comparing weather in two cities).

**Task 4 — Memory & State.** Conversation memory (the resent message history) vs. working memory (the harness's own scratchpad of tool calls/results), plus live `[REASON]/[ACT]/[OBSERVE]` logging.

**Task 5 — Failure Modes & Guardrails.** The agent was deliberately broken four ways and each run is captured with real output:

1. **Ambiguous request** ("What's the weather like?") — model asked a clarifying question instead of guessing.
2. **Tool/data error** (city outside the stub dataset) — caught and returned as a visible error string instead of crashing.
3. **Undefined tool** ("send an email...") — model had no `send_email` tool, so it explained the limitation and drafted the text instead of hallucinating a tool call.
4. **Forced infinite loop** ("keep calculating 1+1 forever") — the model chose to stop itself on the very first turn and never called a tool, so the `max_iterations` cap never had to fire. This is a legitimate result, not a bug: it shows the model's own reasoning is the *first* line of defense, and the iteration cap is the backstop for when that reasoning fails — confirmed separately in an earlier mock run where the cap did trigger and cut the loop off with a `[GUARDRAIL]` message.

A 6-row table in the notebook (and in the write-up) pairs each failure mode with its concrete mitigation:

| # | Failure mode | Mitigation |
|---|---|---|
| 1 | Ambiguous request | System prompt: only call a tool when there's enough information |
| 2 | Tool/data error | `execute_tool()` catches exceptions, returns error string |
| 3 | Hallucinated/undefined tool | `execute_tool()` checks name against registered tools first |
| 4 | Wrong/malformed arguments | `calculator()` uses `ast.parse` + operator whitelist, never `eval()` |
| 5 | Infinite/runaway loop | Hard `max_iterations` cap in `run_agent()` |
| 6 | Silent errors | Every failure path returns an explicit, model-visible error string |

Closes with a short paragraph on why frameworks like LangChain/LangGraph/CrewAI exist, given the whole thing is ~150 lines of hand-written Python.

## Note on provider

The assignment brief referenced the Anthropic API; this implementation uses the **Gemini API** instead (confirmed acceptable by instructor). The underlying ReAct loop, tool schemas, and guardrail logic are provider-agnostic and would port directly.

## Status

All 5 tasks complete and verified against real (non-mocked) API calls. Ready to submit.
