# Week 3 · Day 4 — AFL Assistant Agent
**Routing, Retrieval, Prediction & Response Validation**
Web3Geek Internship · Due 14 Sept 2026

## Scenario
This notebook builds a lightweight AFL assistant that can answer user questions in a structured way:

- Prediction queries: match winners and top-player forecasts
- Retrieval queries: recent team stats, scores, and results
- Factual queries: general AFL knowledge
- Off-topic queries: non-AFL questions that should be refused gracefully

The solution combines:
- cleaned AFL match and player datasets
- team alias resolution (`Pies`, `Cats`, `Dogs`, `GWS`, etc.)
- a simple rule-based prediction layer
- a routing graph using `langgraph`
- validation and response formatting before final output

## Files in this deliverable

| File | Description |
|---|---|
| `week3 day4.ipynb` | Main notebook containing all tasks, data preparation, model logic, and sample runs |
| `README.md` | Project overview, setup instructions, and summary of the workflow |

## Required data
Place the raw AFL CSV files in the same folder as the notebook (or update the `PATH` variable in the first code cell if needed). The notebook expects data such as:

- `afl_players_info_raw.csv`
- `afl_players_round_by_round_stats_raw.csv`
- `afl_players_seasonal_stats_raw.csv`
- `team_matches_home_away_raw.csv`

## How to run
1. Install the required packages:
   ```bash
   pip install -q langgraph langchain-google-genai langchain-core pandas python-dotenv
   ```
2. Set your Gemini API key:
   ```bash
   export GEMINI_API_KEY="your_key_here"
   ```
3. Open the notebook and run all cells from top to bottom.
4. The notebook will:
   - clean and normalize AFL data
   - build baseline prediction functions
   - route user queries by intent
   - validate outputs
   - format final responses

## What the notebook covers
1. Data loading and cleaning
   - standardizing team names
   - mapping player IDs to names
   - fixing malformed team aliases and whitespace issues

2. Baseline prediction logic
   - historical win-rate model for match winner predictions
   - average-stat model for top-player forecasts such as goals or disposals

3. Intent routing
   - classifies each question as `prediction`, `retrieval`, `factual`, or `off_topic`
   - uses keyword-based checks and LLM-based routing

4. Graph-based agent flow
   - `router` → chooses the action
   - `prediction` / `retrieval` → runs the relevant logic
   - `validation` → checks if the output is sensible
   - `format` → generates a concise final answer

5. Evaluation and sample queries
   - tests several example requests
   - reports routing accuracy
   - demonstrates a full AFL assistant conversation

## Key design choices
- Team aliases are normalized to canonical AFL names so queries like `Pies`, `Cats`, and `Dogs` work reliably.
- Predictions are intentionally probabilistic rather than presented as certainty.
- Retrieval and prediction are separated so the assistant does not misclassify factual or off-topic questions.
- Validation prevents weak or unsupported answers from being returned.

## Example queries supported
- `Will the Pies beat the Cats this week?`
- `Who will top-score for Richmond this round?`
- `What were Collingwood's stats last round?`
- `How many goals did Geelong kick last week?`
- `What's the best pizza in Carlton?` → correctly classified as off-topic

## Key outcome
The notebook demonstrates an AFL mini-agent that can respond to realistic sports questions using a structured pipeline rather than a single monolithic prompt. This makes the assistant more reliable, interpretable, and easier to extend.

---

**Created for**: Web3-Geeks Learning Program  
**Week**: 3 | **Day**: 4
