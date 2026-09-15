# AFL Player Models — Day 2

Two trained models for the chat agent to call as tools:

- **Match Winner** — predicts which of two teams wins, with a probability.
- **Top Player** — ranks players by predicted fantasy score for an upcoming match.

Built on real AFL data (1983–2025), using each team's/player's pre-match form
(rolling averages, win rates, ladder position) as features — no post-match
information is used, so predictions are safe to make before a game is played.

## Folder structure

```
.
├── Day2_Player_Models.ipynb   # training, evaluation, feature importance
├── predict.py                 # callable inference functions
└── models/
    ├── match_winner_model.joblib
    ├── top_player_model.joblib
    ├── team_reference.csv
    ├── team_pair_reference.csv
    ├── player_reference.csv
    └── date_range.csv
```

`predict.py` looks for these six files inside a `models/` folder sitting next
to it — the folder structure above must be kept intact for imports to work.

## Install

```bash
pip install -r requirements.txt
```

Requirements: `pandas`, `numpy`, `scikit-learn`, `joblib`.

## Usage

```python
from predict import predict_match_winner, predict_top_player

predict_match_winner("Richmond Tigers", "Geelong Cats")
# {'winner': 'Geelong Cats', 'probability': 0.61, 'home_team': 'Richmond Tigers', 'away_team': 'Geelong Cats'}

predict_top_player(team="Richmond Tigers", k=5)
# [{'player_id': 12345, 'team': 'Richmond Tigers', 'predicted_score': 97.9}, ...]
```

Both functions raise `ValueError` with a clear message on bad input (unknown
team name, `date` outside the training data's range or badly formatted, `k < 1`),
so an agent framework can surface the error back to the model/user directly.

## Models & results

### Match Winner

Binary classifier: does this team win, given its own pre-match form
(`last5_avg_score`, `last5_win_rate`, `last3_win_rate`, `win_streak`,
`days_rest`, `h2h_win_rate`, `venue_win_rate`, `cum_wins_before_match`,
`ladder_rank_before_match`, `home_away`). Evaluated on the full held-out 2025 season.

| Model | Accuracy | F1 | ROC AUC | Brier Score |
|---|---|---|---|---|
| Baseline (home always wins) | 0.558 | 0.558 | 0.558 | 0.442 |
| Logistic Regression | 0.609 | 0.604 | 0.666 | 0.228 |
| **Gradient Boosting (final)** | **0.623** | **0.605** | **0.672** | **0.228** |

Top features: `home_away`, `last5_win_rate`, `ladder_rank_before_match`,
`venue_win_rate` — matches football intuition (recent form, home advantage,
ladder position, venue history).

### Top Player

Regression: predicts each player's fantasy points for the match from
`last5_avg_disposals`, `last5_avg_goals`, `last5_avg_fantasy`, and `opponent`.
Ranking is produced by sorting predictions within a match. Evaluated on the
held-out 2025 season.

| Model | MAE | RMSE | Top-5 Hit Rate |
|---|---|---|---|
| Baseline (last week's score repeats) | 22.75 | 28.82 | 90.3% |
| **Gradient Boosting Regressor (final)** | **17.92** | **22.56** | **95.4%** |

`last5_avg_fantasy` dominates feature importance, as expected — recent output
is the strongest predictor of near-future output.

**Note on interface:** `predict_top_player` takes `team`/`opponent`/`k` rather
than `match_id`/`stat_type`, and always predicts fantasy points specifically
(the standard AFL "who played well" metric) rather than an arbitrary stat.
This keeps the function usable without a match schedule lookup and matches
what the regression model was actually trained to predict.

## Data range

Models were trained/evaluated on matches from **1983-03-26 to 2025-09-27**.
`predict_match_winner`'s optional `date` argument is validated against this
range.
