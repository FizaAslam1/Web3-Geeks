# Day 2 — Knowledge Base, RAG & Property Intelligence

Project: Production-Grade AI Voice Agent for Real Estate (UrduLish)

## Files

| File | Task | Status |
|---|---|---|
| `Day2_Knowledge_Base_RAG.ipynb` | Tasks 1–5: knowledge base, RAG pipeline, structured retrieval, recommendation engine, hallucination evaluation | Complete |

## What's inside

### Task 1 — Knowledge Base Design
SQLite database with tables for properties, prices, locations, amenities, schools, hospitals, payment plans, developers, and FAQs.

### Task 2 — RAG Pipeline
Full pipeline: document loader → chunking → embedding → ChromaDB vector store → retriever → answer generation. Three chunk-size configurations (200/400/800, overlap 50) were tested and compared; **400 tokens / 50 overlap** was selected as the best trade-off between retrieval precision and context completeness.

### Task 3 — Structured vs Semantic Retrieval
Retrieval is deliberately split:
- **SQL (structured):** prices, availability, plot sizes, agent names — exact facts that must never be approximated.
- **Vector (semantic):** brochures, descriptions, FAQs — free-text knowledge.

A router function (`is_structured()`) decides which path a question takes, based on keyword signals (price, budget, marla, kanal, etc.).

### Task 4 — Property Recommendation Engine
Recommends properties by budget, city, area, bedrooms, purpose, amenities, and investment goals, using a scoring function over the structured database.

### Task 5 — Hallucination Evaluation
20 customer questions were answered by the LLM (Gemini 3.5 Flash-Lite) using only retrieved context, then checked for numeric facts not present in that context.

**Result: 100% Grounding Rate, 0% Hallucination Rate.**

This evaluation initially had a bug (the LLM call was defined but never actually invoked, and the API key was briefly hardcoded in the notebook) — both were caught and fixed: the key was moved to a `.env` file (never committed, see `.gitignore`), and the evaluation loop was rewritten to genuinely call the LLM per question with rate-limit-safe retries, producing the verified 100%/0% result above.

## Alignment with other days

- **Day 1:** knowledge base categories match the schema outlined in Task 1 of Day 1's architecture research.
- **Day 5:** the `retrieve` node in the LangGraph agent reuses this exact SQL/vector retrieval and routing logic.
- **Day 7:** `agent_core.py`'s knowledge-base loading and retrieval functions are carried over unchanged from this day.
