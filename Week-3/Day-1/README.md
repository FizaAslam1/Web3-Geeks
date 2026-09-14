# Week 3 · Day 1 — AFL Data Foundations
**EDA, Feature Engineering & Prediction Targets**
Web3Geek Internship · Due 14 Sept 2026

## Scenario
Building toward two end goals — a domain-locked AFL chat assistant and a prediction system (match
winners, top players/goal-kickers) — this notebook lays the data foundation both will rely on: deep
data understanding, precise target definitions, EDA, and leakage-safe feature engineering.

## Files in this deliverable

| File | Description |
|---|---|
| `AFL_Data_Foundations_Day1.ipynb` | Main notebook — all 5 tasks, executed end-to-end with outputs/plots |
| `AFL_Data_Dictionary_Day1.pdf` | 1-page data dictionary + target definitions (the second required deliverable) |
| `features_team_v1.csv` | Versioned team-match feature table (15,808 rows) |
| `features_player_v1.csv` | Versioned player-game feature table (274,079 rows) |

## Source data (not included here — place alongside the notebook to re-run)
- `afl_players_info_raw.csv` — player biographical info (one row per player)
- `afl_players_round_by_round_stats_raw.csv` — player-game level stats
- `afl_players_seasonal_stats_raw.csv` — player-season aggregated stats
- `team_matches_home_away_raw.csv` — team-match level, long format (one row per team per match)

## How to run
1. Place the 4 raw CSVs in the same folder as the notebook (or update the `PATH` variable in the first
   code cell to point to wherever they live).
2. Run all cells top to bottom — each task builds on the previous one's output.
3. Re-running regenerates `features_team_v1.csv` and `features_player_v1.csv` in the working directory.

## What the notebook covers
1. **Data Inventory & Understanding** — grain of each table, join logic, missing-value and duplicate
   checks, and a critical data-quality fix: `team_matches` team names were whitespace/tab-corrupted
   (40 raw values → 20 real teams after cleaning).
2. **Prediction Targets** — `target_result` (Home Win / Away Win / Draw, primary classification target)
   and `margin_signed` (regression) for match winner; `is_top_disposals_game`, `is_top_goals_game`, and
   `fantasy_points` for top player.
3. **EDA** — 7 visualizations: win rate by season, home-ground advantage, season score trends, player
   distributions, week-to-week consistency, form vs win rate, rest days vs performance.
4. **Feature Engineering** — rolling form, win streaks, head-to-head record, venue win rate, ladder
   position, and player rolling averages. Every rolling/expanding feature uses `.shift(1)` first so no
   feature ever sees the outcome of the match it's predicting.
5. **Train/Hold-Out Split** — a reusable `get_time_split()` function that holds out the most recent
   season (or last N rounds) instead of a random split, plus a written justification for why random
   splits leak future information in time-series sports data, and a discussion of the realistic
   accuracy ceiling (~65–75%) for AFL win prediction.

## Key findings worth remembering for Day 2+
- `round_stats.score` is 100% NULL — use `fantasy_points` (official, dataset-provided) instead.
- Advanced stats (`hit_outs`, `bounces`, `contested_marks`, `brownlow_votes`) are structurally missing
  in early seasons (not tracked yet), not randomly missing — don't impute these as zero.
- No shared numeric match ID exists between `round_stats` and `team_matches`; matches are linked via a
  synthetic `(match_date, team, opponent)` key.
- Observed home win rate in this dataset: **59.1%** — the baseline any model needs to beat.
