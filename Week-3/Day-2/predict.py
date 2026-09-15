"""
predict.py — callable inference functions for the Day 2 Player Models (real AFL data).

Wraps the trained Match Winner and Top Player models behind a clean interface,
ready to be exposed as LangChain / LangGraph tools on Day 4.

Expects these artifacts (produced by the Day 2 notebook) in ./models/:
    match_winner_model.joblib
    top_player_model.joblib
    team_reference.csv        (latest known form per team, any opponent — fallback)
    team_pair_reference.csv   (latest known form per team vs a specific opponent — preferred)
    player_reference.csv      (latest known form per player)
    date_range.csv            (single row: min_date, max_date — the span of data the
                               models were trained/evaluated on, used to validate the
                               optional `date` argument to predict_match_winner)
"""

import os
import joblib
import pandas as pd

_MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

_match_model = joblib.load(os.path.join(_MODEL_DIR, "match_winner_model.joblib"))
_player_model = joblib.load(os.path.join(_MODEL_DIR, "top_player_model.joblib"))

_team_ref = pd.read_csv(os.path.join(_MODEL_DIR, "team_reference.csv")).set_index("team_name_norm")
_team_pair_ref = pd.read_csv(os.path.join(_MODEL_DIR, "team_pair_reference.csv")).set_index(
    ["team_name_norm", "opponent_norm"]
)
_player_ref = pd.read_csv(os.path.join(_MODEL_DIR, "player_reference.csv")).set_index("player_id")

# --- Valid date range for the optional `date` arg in predict_match_winner ---
# Read from models/date_range.csv if the notebook has saved it (see Task 5 cell).
# If that file isn't present yet, we still validate the date is a real, parseable
# date — we just skip the range check rather than hard-failing on setup.
_date_range_path = os.path.join(_MODEL_DIR, "date_range.csv")
if os.path.exists(_date_range_path):
    _date_range_df = pd.read_csv(_date_range_path)
    _MIN_DATE = pd.to_datetime(_date_range_df["min_date"].iloc[0])
    _MAX_DATE = pd.to_datetime(_date_range_df["max_date"].iloc[0])
else:
    _MIN_DATE = None
    _MAX_DATE = None

# A handful of players/teams have NaN in their latest snapshot (e.g. early-career
# games with no 5-match history yet) — fill with the reference table's own median
# so single-row inference never breaks on missing values.
_TEAM_NUM_FILL = _team_ref[[
    "last5_avg_score", "last5_win_rate", "last3_win_rate", "win_streak",
    "days_rest", "h2h_win_rate", "venue_win_rate",
    "cum_wins_before_match", "ladder_rank_before_match",
]].median()
_PLAYER_NUM_FILL = _player_ref[["last5_avg_disposals", "last5_avg_goals", "last5_avg_fantasy"]].median()

_MATCH_NUM_FEATURES = [
    "last5_avg_score", "last5_win_rate", "last3_win_rate", "win_streak",
    "days_rest", "h2h_win_rate", "venue_win_rate",
    "cum_wins_before_match", "ladder_rank_before_match",
]
_PLAYER_NUM_FEATURES = ["last5_avg_disposals", "last5_avg_goals", "last5_avg_fantasy"]


def _team_context(team_norm: str, opponent_norm: str) -> pd.Series:
    """Prefer a head-to-head-specific snapshot; fall back to the team's latest overall form."""
    if (team_norm, opponent_norm) in _team_pair_ref.index:
        row = _team_pair_ref.loc[(team_norm, opponent_norm)]
    else:
        row = _team_ref.loc[team_norm, _MATCH_NUM_FEATURES]
    return row.fillna(_TEAM_NUM_FILL)


def _validate_date(date: str) -> pd.Timestamp:
    """
    Parse and validate an ISO date string.

    Raises:
        ValueError: if the string isn't a parseable date, or falls outside the
                    range of data the models were trained/evaluated on.
    """
    parsed = pd.to_datetime(date, errors="coerce")
    if pd.isna(parsed):
        raise ValueError(f"Invalid date format: '{date}'. Expected ISO format, e.g. 'YYYY-MM-DD'.")

    if _MIN_DATE is not None and _MAX_DATE is not None:
        if not (_MIN_DATE <= parsed <= _MAX_DATE):
            raise ValueError(
                f"Date '{date}' is outside the available data range "
                f"({_MIN_DATE.date()} to {_MAX_DATE.date()})."
            )
    return parsed


def predict_match_winner(team_a: str, team_b: str, date: str | None = None) -> dict:
    """
    Predict the winner between two teams, using each team's latest known
    form (preferring head-to-head history against this specific opponent).

    Args:
        team_a: assumed home team.
        team_b: assumed away team.
        date: optional ISO date string. Validated for format and, if
              models/date_range.csv is present, checked against the range of
              data the models were trained/evaluated on. Informational only
              beyond that — inference always uses each team's most recent
              known form snapshot, not a form snapshot "as of" this date.

    Returns:
        {"winner": str, "probability": float, "home_team": str, "away_team": str}

    Raises:
        ValueError: if either team name is not found in the reference data,
                    or if `date` is invalid / outside the known data range.
    """
    a_norm, b_norm = team_a.strip().lower(), team_b.strip().lower()
    for name, norm in [(team_a, a_norm), (team_b, b_norm)]:
        if norm not in _team_ref.index:
            known = sorted(_team_ref["team_name"].unique().tolist())
            raise ValueError(f"Unknown team '{name}'. Known teams include: {known[:10]} ...")

    if date is not None:
        _validate_date(date)

    row_a = _team_context(a_norm, b_norm)
    row_b = _team_context(b_norm, a_norm)

    X_a = pd.DataFrame([{**row_a[_MATCH_NUM_FEATURES].to_dict(), "home_away": "H"}])
    X_b = pd.DataFrame([{**row_b[_MATCH_NUM_FEATURES].to_dict(), "home_away": "A"}])

    proba_a = float(_match_model.predict_proba(X_a)[0, 1])
    proba_b = float(_match_model.predict_proba(X_b)[0, 1])

    # Normalise the two independent "this team wins" probabilities to sum to 1
    total = proba_a + proba_b
    p_a_final = proba_a / total if total > 0 else 0.5

    winner = team_a if p_a_final >= 0.5 else team_b
    probability = p_a_final if winner == team_a else 1 - p_a_final

    return {
        "winner": winner,
        "probability": round(probability, 3),
        "home_team": team_a,
        "away_team": team_b,
    }


def predict_top_player(team: str | None = None, opponent: str | None = None, k: int = 5) -> list[dict]:
    """
    Rank players by predicted fantasy points for an upcoming match, using
    each player's latest known form.

    Args:
        team: restrict to players from this team (matched against each
              player's most recent recorded team). If None, considers all
              players in the reference set.
        opponent: opposing team, used as a matchup signal for the model.
                  If None, falls back to each player's most recently faced
                  opponent (a neutral-ish default).
        k: number of top players to return.

    Returns:
        List of {"player_id": int, "team": str, "predicted_score": float},
        sorted descending by predicted_score, length <= k.

    Raises:
        ValueError: if `team` is given but not found, or k < 1.
    """
    if k < 1:
        raise ValueError("k must be >= 1")

    pool = _player_ref.copy()
    if team is not None:
        matches = pool["team"].str.strip().str.lower() == team.strip().lower()
        if not matches.any():
            known = sorted(pool["team"].unique().tolist())
            raise ValueError(f"Unknown team '{team}'. Known teams include: {known[:10]} ...")
        pool = pool[matches]

    if pool.empty:
        raise ValueError("No players available for the given filters.")

    X = pool[_PLAYER_NUM_FEATURES].fillna(_PLAYER_NUM_FILL).copy()
    X["opponent"] = opponent if opponent is not None else pool["opponent"].values

    pool = pool.copy()
    pool["predicted_score"] = _player_model.predict(X)
    pool = pool.sort_values("predicted_score", ascending=False).head(k)

    return [
        {"player_id": int(pid), "team": r["team"], "predicted_score": round(float(r["predicted_score"]), 1)}
        for pid, r in pool.iterrows()
    ]
