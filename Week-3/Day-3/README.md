# Domain-Scoped AFL Chat Agent

Week 3 · Day 3 project — a conversational AFL assistant built with LangChain
that only discusses AFL, grounds every stat in a real tool call against the
dataset (never the model's memory), and politely declines off-topic requests.

Built on top of the Day 1 (AFL Data Foundations) and Day 2 (Player Models)
work — same raw data files and column schema.

## What's inside

- `afl_chat_agent.ipynb` — the main notebook (scope/system prompt, retrieval
  tools, LangChain agent, memory, guardrail evaluation)
- `guardrail_eval_results.csv` — output of the Task 5 evaluation run
- `requirements.txt` — Python dependencies

## Setup

```bash
pip install -r requirements.txt
```

Get a free Groq API key from https://console.groq.com/keys, then set it
before running the notebook:

```bash
export GROQ_API_KEY=your_key_here
```

(or copy `.env.example` to `.env` and fill it in). Then open
`afl_chat_agent.ipynb` and run all cells top to bottom.

If no API key is set, the notebook falls back to an offline mock model so
the pipeline still runs end-to-end for review.

## What the agent does

1. **Scope guardrails** — a system prompt restricts the assistant to AFL
   teams, players, matches, stats, rules and history, and declines anything
   else with a redirect back to AFL.
2. **Structured retrieval** — exact stats (disposals, goals, head-to-head
   records) are pulled via pandas lookups against the real dataset, never
   guessed by the model.
3. **Semantic retrieval** — a small FAISS vector store over auto-generated
   match summaries for narrative/vague questions.
4. **Grounding check** — every number in a final answer is verified against
   the tool output that produced it.
5. **Memory** — a multi-turn conversation test confirms follow-up questions
   ("what about him?", "how does that compare?") resolve correctly.

## Results

- **Task 1 adversarial scope test:** 6/10 passed
- **Task 5 guardrail evaluation (16 prompts):** scoped correctly 10/16,
  grounded correctly 12/16
- Full failure-pattern analysis and fixes are documented at the end of the
  notebook.

## Notes

- No API keys are committed to this repo — see `.env.example`.
- The dataset used here is the same schema as the Day 1/2 raw AFL data
  files; if the raw CSVs aren't present alongside the notebook, it falls
  back to synthetic data with identical column names so the pipeline still
  runs for review.
