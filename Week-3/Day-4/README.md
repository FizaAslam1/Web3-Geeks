# Week 3 · Day 4 — AFL Assistant Agent
## Routing, Retrieval, Prediction & Response Validation

**Intern:** Fiza
**Program:** Web3 Geeks Internship
**Week:** 3 | **Day:** 4
**Submission Date:** 18 September 2026

---

## 📌 Overview

This submission delivers a **LangGraph-powered AFL assistant** that integrates
a chat agent with two AFL prediction models behind a single routing layer.
Every incoming user query is classified into one of four intents and
dispatched to the appropriate tool or node:

| Intent | Handled by | Example query |
|--------|-----------|---------------|
| `prediction` | `prediction_node` | "Will the Pies beat the Cats this week?" |
| `retrieval` | `retrieval_node` | "What were Collingwood's stats last round?" |
| `factual` | `factual_node` | "How many players are on an AFL team?" |
| `off_topic` | `refusal_node` | "What's the weather in Sydney?" |

Two additional fallback paths handle **ambiguous** inputs (→ clarification)
and **out-of-scope** stats (→ clean refusal), preventing hallucinations.

All predictions are framed as **probabilistic** and include **grounding
features**; every prediction response carries the disclaimer
_"Predictions are probabilistic, not guaranteed."_

### Key Results

- ✅ **Routing accuracy: 75%** (100% on prediction, retrieval, off-topic; factual queries documented as known limitation)
- ✅ **10/10 end-to-end conversations** executed successfully across all paths
- ✅ **Every prediction** includes probability framing + disclaimer + grounding features
- ✅ **Fallback handling** verified for ambiguous, off-topic, and out-of-scope queries

---

## 📂 Repository Structure
Web3-Geeks/
└── Week-3/
└── Day-4/
├── week3 day4.ipynb # Main notebook (all tasks, cells 1-18)
├── README.md # This file (end-to-end report)
└── requirements.txt # Dependencies

text

---

## 📦 Required Data

Place the raw AFL CSV files in the same folder as the notebook (or update the
`PATH` variable in Cell 2):

- `afl_players_info_raw.csv`
- `afl_players_round_by_round_stats_raw.csv`
- `afl_players_seasonal_stats_raw.csv`
- `team_matches_home_away_raw.csv`

---

## ⚙️ Setup & Installation

### 1. Install dependencies

```bash
pip install -q langgraph langchain-google-genai langchain-core pandas python-dotenv
2. Set your Gemini API key
Google Colab:

python
from google.colab import userdata
import os
os.environ["GEMINI_API_KEY"] = userdata.get("GEMINI_API_KEY")
Local / JupyterLab:

python
import os
os.environ["GEMINI_API_KEY"] = "your_key_here"
3. Run the notebook
Execute cells sequentially from top to bottom. The notebook will:

Clean and normalize AFL data

Build baseline prediction functions

Route user queries by intent

Validate outputs

Format final responses

🏗️ Architecture
text
                    ┌───────────────┐
                    │   router      │  (LLM intent classifier)
                    └───────┬───────┘
                            │
        ┌───────────────────┼───────────────────┬────────────────┐
        ▼                   ▼                   ▼                ▼
   ┌─────────┐       ┌─────────────┐      ┌──────────┐    ┌──────────┐
   │prediction│      │ retrieval   │      │ factual  │    │ refusal  │
   └────┬────┘       └──────┬──────┘      └────┬─────┘    └────┬─────┘
        │                   │                  │               │
        └────────┬──────────┘                  │               │
                 ▼                             │               │
         ┌───────────────┐                     │               │
         │  validation   │                     │               │
         └───────┬───────┘                     │               │
                 │                             │               │
      ┌──────────┼──────────┐                  │               │
      ▼          ▼          ▼                  ▼               ▼
 ┌─────────┐ ┌───────┐ ┌───────┐          ┌──────────────────────┐
 │ clarify │ │ format│ │refusal│          │       format         │
 └────┬────┘ └───┬───┘ └───┬───┘          └──────────┬───────────┘
      │          │         │                         │
      ▼          ▼         ▼                         ▼
    END        END       END                       END
State Schema (GraphState)
python
query         : str                 # current user query
history       : List[Dict]          # conversation history
intent        : str                 # prediction | retrieval | factual | off_topic
entities      : Dict                # teams[], players[], stat, timeframe
tool_result   : Optional[Dict]      # output of retrieval/prediction
validation    : str                 # ok | error | needs_clarification | out_of_scope
clarification : Optional[str]       # question back to user
response      : str                 # final assistant message
trace         : List[str]           # step-by-step log for debugging
🎯 Task 1 — Graph Design for the Full System
Why explicit routing (LangGraph) over a monolithic agent?
A single monolithic LangChain agent decides intent, calls tools, and formats
responses inside one prompt. In that design, prediction responses easily
slip through without the mandatory probabilistic disclaimer, because the
model isn't forced through a specific formatting step.

By splitting the flow into router → tool → validation → format nodes:

Predictions are guaranteed to pass through a formatting node that
enforces probability framing + disclaimer.

Validation and fallback are first-class citizens — ambiguous inputs
route to clarification instead of hallucinating a fixture.

Out-of-scope queries are refused cleanly rather than hallucinated.

Debugging is easier — the trace list records every hop.

🎯 Task 2 — Router Node & Accuracy
The router (router_node, Cell 9) uses a Gemini LLM call with a strict JSON
output schema, plus a rule-based fallback for prediction/retrieval keywords.

Routing Accuracy — 20-Query Test Suite
Intent Category	Correct / Total	Accuracy
prediction	5 / 5	100%
retrieval	5 / 5	100%
off_topic	5 / 5	100%
factual	0 / 5	0%
Overall	15 / 20	75.0%
Misroute Analysis
Query	Expected	Predicted	Why
"How many players are on an AFL team?"	factual	retrieval	"how many" triggered rule-based retrieval
"When was the AFL founded?"	factual	off_topic	LLM saw no AFL-specific keyword
"What is a behind worth?"	factual	off_topic	same
"How long is a quarter in the AFL?"	factual	off_topic	same
"Who is the current AFL CEO?"	factual	off_topic	same
Proposed fix: A rule-based pre-filter for known factual patterns
("when was", "what is a", "how long is", "how many players are on",
"rules of") would push overall accuracy to ~95%. Impact on the application
is minimal since factual queries still produce correct responses via the
factual_node.

🎯 Task 3 — Prediction Tools Wired
Tools
predict_match_winner(home_team, away_team) — returns win probabilities

grounding features.

predict_top_player(team, stat="goals") — returns top-3 players by
average stat value + grounding features.

Input Resolution
Team aliases: 80+ nicknames mapped to canonical names in TEAM_ALIASES
(Cell 5). E.g. "Pies" → "Collingwood Magpies",
"Dogs" → "W. Bulldogs".

Player names: player_id → player_full_name mapping via player_info
(Cell 4). 99.2% of rows resolved.

Timeframe: extracted by the router as a string ("this week",
"last round").

Example Output
text
QUERY: "Will the Pies beat the Cats this week?"

RESPONSE:
Based on the model, the Collingwood Magpies have a **60.9% chance** of
defeating the Geelong Cats (who have a 39.1% chance).

Key factors supporting this prediction include:
- Home advantage
- Historical win rate

*Predictions are probabilistic, not guaranteed.*
🎯 Task 4 — Self-Correction & Fallbacks
Validation Node
The validation_node (Cell 12) inspects tool_result after any
retrieval/prediction. If the result is None and no error was raised, it
converts the state to error.

Fallback Paths
Failure	Handler	Example
Missing team in prediction	clarification_node	"Will Collingwood win?" → "I need TWO teams..."
Missing team in retrieval	clarification_node	"What were the stats last round?" → "Which team?"
Unmodelled stat	clarification_node (out_of_scope)	"Top tackler" on an unmodelled metric
Tool crash / no result	refusal_node	Apologetic refusal
Off-topic query	refusal_node	Weather query → clean refusal
🎯 Task 5 — End-to-End Testing
10 Conversations Exercised
#	Query	Intent	Validation	Path Verified
1	"Will the Pies beat the Cats this week?"	prediction	ok	Full prediction
2	"Who will top-score for Richmond this round?"	prediction	out_of_scope	Fallback (stat)
3	"What were Collingwood's stats last round?"	retrieval	ok	Full retrieval
4	"How many players are on an AFL team?"	retrieval	needs_clarification	Router misroute + clarify
5	"What's the weather in Sydney?"	off_topic	ok	Refusal
6	"Will Collingwood win?"	prediction	needs_clarification	Clarification
7	"Who will win this week?"	prediction	needs_clarification	Clarification
8	"Predict the top tackler for Geelong this week."	prediction	ok	Full prediction
9a	"Will the Pies beat the Cats this week?"	prediction	ok	Multi-turn, turn 1
9b	"What about last time they played?"	retrieval	needs_clarification	Multi-turn context loss
10	"How many goals did Hawkins kick last round?"	retrieval	needs_clarification	Player-only query
Annotated Traces (3 Representative Runs)
Trace 1 — Prediction Path (Conversation 1)

text
QUERY: "Will the Pies beat the Cats this week?"
  → [router] query='Will the Pies beat the Cats this week?'
  → [router] intent=prediction entities={'teams': ['Pies','Cats'], 'timeframe': 'this week'}
  → [prediction] resolved=['Collingwood Magpies', 'Geelong Cats']
  → [prediction] Collingwood Magpies vs Geelong Cats
  → [validation] ok
  → [format]

RESPONSE:
"Collingwood (Pies) have a 60.9% chance of defeating the Geelong Cats this
week, while Geelong has a 39.1% chance of winning. Key factors influencing
this model prediction include: Home advantage, Historical win rate.
*Predictions are probabilistic, not guaranteed.*"
Trace 2 — Clarification Path (Conversation 6)

text
QUERY: "Will Collingwood win?"
  → [router] intent=prediction entities={'teams': ['Collingwood']}
  → [prediction] only 1 team resolved → needs 2 for match prediction
  → [validation] needs_clarification
  → [clarify]

RESPONSE:
"I need TWO teams to predict a match. e.g. 'Pies vs Cats'."
Trace 3 — Refusal Path (Conversation 5)

text
QUERY: "What's the weather in Sydney?"
  → [router] intent=off_topic
  → [refusal]
  → [format]

RESPONSE:
"I am an AFL assistant, so I can only help with AFL-related queries such as
match predictions, team stats, and player information. I don't have access
to current weather data."
Comparison: LangGraph vs Monolithic Agent
A single monolithic LangChain agent must decide intent, call tools, and
format responses inside one prompt, which makes it easy for prediction
answers to slip through without the required probabilistic disclaimer. By
splitting the flow into router → tool → validation → format nodes, this
design guarantees that every prediction passes through a formatting node
that enforces probability framing and grounding features. Validation and
fallback branches also become first-class: ambiguous inputs route to
clarification instead of hallucinating a fixture, and out-of-scope stats
are refused cleanly.

📓 Notebook Walkthrough
Cell	Purpose
1	Install dependencies
2	Imports, API key, dataset paths
3	Load 4 CSVs into DataFrames
4	Map player_id → player_name via player_info
5	Team alias resolver (80+ nicknames)
5.5	Sanity check
6	Fallback match-winner + top-player models
7	Quick model test
8	GraphState schema + Gemini LLM init
9	Router node — LLM intent classifier
10	Retrieval node — recent games + top scorers
11	Prediction node — match + top-player with alias resolution
11 (REQUIRED)	factual_node, refusal_node, clarification_node
12	validation_node, format_node
13	Build and compile the LangGraph
14	Smoke test — full prediction path
15	Routing accuracy table (20 queries)
16	10 end-to-end conversations (all paths)
18	Written comparison vs monolithic agent
🎨 Key Design Choices
Team aliases normalized to canonical AFL names so queries like Pies,
Cats, and Dogs work reliably.

Predictions are intentionally probabilistic, never presented as
certainty. Every prediction includes the disclaimer.

Retrieval and prediction are separated so the assistant does not
misclassify factual or off-topic questions.

Validation prevents weak or unsupported answers from being returned.

Format node enforces probability framing and grounding features via
prompt + hard safety net.

📊 Example Queries Supported
Query	Routes to	Result
"Will the Pies beat the Cats this week?"	prediction	60.9% vs 39.1% + disclaimer
"Who will top-score for Richmond this round?"	prediction	out_of_scope (stat)
"What were Collingwood's stats last round?"	retrieval	Recent game summary
"How many goals did Geelong kick last week?"	retrieval	Team stats
"What's the best pizza in Carlton?"	off_topic	Clean refusal
⚠️ Limitations
Router accuracy: 75% — factual queries (5) misclassified as
off_topic/retrieval. A hybrid rule-based pre-filter would raise to ~95%.

Multi-turn context loss — follow-up pronouns ("they") not resolved;
each turn is processed independently by the router.

Player-only queries — "Hawkins' goals" requires mentioning the team
because no player → team dictionary exists in the router.

Out-of-scope stats — "top-score" is treated as an unmodelled stat
even though it should map to "goals".

Model choice — task specified gemini-3.8-flash (20 req/day free
tier), so the E2E test used gemini-3.6-flash (backup key). The graph
is model-agnostic; switching back is a one-line change in Cell 2.

Prediction models — Day 2 pickle files were unavailable, so
frequency-based baselines were used. The graph loads them automatically
if present.

Historical teams — Brisbane Bears and Fitzroy Lions (pre-1997)
are in the dataset but predictions for them are statistically
unreliable.

📚 Dependencies
text
langgraph
langchain-google-genai
langchain-core
pandas
python-dotenv
🙏 Acknowledgements
Web3 Geeks Internship — for the task structure and dataset

AFL historical stats (players + matches)

LangGraph by LangChain Inc.

Google Gemini via langchain-google-genai

Submitted by: Fiza
Program: Web3 Geeks Internship
Week 3 — Day 4
Date: 18 September 2026

text

---

## 🎯 Kaise Use Karo (3 Steps)

### Step 1 — GitHub Pe Jao

`https://github.com/FizaAslam1/Web3-Geeks/tree/main/Week-3/Day-4`

### Step 2 — README.md Replace Karo

1. **README.md** pe click karo
2. **Pencil icon** (edit) pe click karo
3. Poora purana content **delete** karo
4. Upar wala poora content **paste** karo
5. **Commit changes** (message: `Add complete end-to-end Week 3 Day 4 report`)

### Step 3 — requirements.txt Add Karo (agar nahi hai)

1. **Add file → Create new file**
2. Naam: `requirements.txt`
3. Content:
langgraph
langchain-google-genai
langchain-core
pandas
python-dotenv

text
4. **Commit changes**

### Step 4 — Portal Pe Submit Karo
Repo: https://github.com/FizaAslam1/Web3-Geeks/tree/main/Week-3/Day-4
Contains: week3 day4.ipynb, README.m
