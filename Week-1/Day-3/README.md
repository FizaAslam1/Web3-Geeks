# Week 1 — Day 3

## Overview
Day 3 focuses on feature engineering, cross‑validation, and model comparison using the UCI Adult (Census Income) dataset. The goal is to expand the feature set with principled engineering and evaluate models using robust cross‑validation and statistical tests.

## Files
| File | Description |
|---|---|
| week1_day3.ipynb | Jupyter notebook with all code |
| week1_day3_summary.pdf | 2‑page summary of engineered features, CV results, statistical tests, and model selection |
| preprocessor_day3.pkl | Saved preprocessing pipeline for reuse |
| cv_boxplots.png | Boxplots of cross‑validation scores for all models |
| README.md | This file |

## Tech stack
| Component | Tool |
|---|---|
| Language | Python 3 |
| Data processing | pandas, NumPy |
| Preprocessing | scikit‑learn (ColumnTransformer, Pipeline, FunctionTransformer) |
| Models | Logistic Regression, Random Forest, Gradient Boosting |
| Evaluation | 5‑fold cross‑validation, Accuracy, F1, ROC AUC |
| Statistical tests | Paired t‑test, Wilcoxon test |
| Feature selection | SelectKBest, Mutual Information |

## Engineered features (summary)
| Feature | Type | Creation rule | Predictive signal (MI) |
|---|---:|---|---:|
| age_bucket | Categorical | Binned age into 5 groups | 0.0628 |
| hours_bucket | Categorical | Binned hours into 4 groups | 0.0302 |
| has_capital_gain | Binary | Flag if capital_gain > 0 | 0.0095 |
| log_capital_gain | Numeric | log(capital_gain + 1) | 0.0775 |
| higher_education | Binary | education‑num >= 13 | 0.0495 |
| edu_hours_interaction | Numeric | education‑num × hours‑per‑week | 0.0810 |

Key insight: log_capital_gain and edu_hours_interaction show the highest mutual information with the target.

## Cross‑validated model comparison (5‑fold)
| Model | Accuracy | F1 | ROC AUC |
|---|---:|---:|---:|
| Logistic Regression | 0.8557 ± 0.0022 | 0.6683 ± 0.0067 | 0.9120 ± 0.0024 |
| Random Forest | 0.8515 ± 0.0011 | 0.6646 ± 0.0038 | 0.9020 ± 0.0028 |
| Gradient Boosting | 0.8638 ± 0.0032 | 0.6790 ± 0.0071 | 0.9200 ± 0.0024 |

Observations:
- Gradient Boosting performs best across accuracy, F1, and ROC AUC.
- Logistic Regression remains strong and interpretable.
- All models show low variance across folds.

## Statistical comparison
| Comparison | Test | p‑value | Significant? |
|---|---|---:|:---|
| Logistic vs Random Forest | Paired t‑test | 0.0002 | ✅ Yes |
| Logistic vs Gradient Boosting | Paired t‑test | 0.0048 | ✅ Yes |
| Random Forest vs Gradient Boosting | Paired t‑test | 0.0002 | ✅ Yes |

Conclusion: Gradient Boosting is statistically significantly better than both Logistic Regression and Random Forest at p < 0.05.

## Feature importance (Random Forest)
Top features (example importance scores):
- num__fnlwgt (0.1428) — Demographic weight
- num__age (0.1088) — Age
- num__edu_hours_interaction (0.0711) — Engineered interaction
- cat__marital-status_Married-civ-spouse (0.0643) — Marital status
- num__capital-gain (0.0528) — Capital gain

Engineered features of note:
- log_capital_gain (0.0421) — helps with skewness
- edu_hours_interaction (0.0711) — captures combined effect of education and hours
- higher_education (0.0221) — useful binary signal

## Feature selection impact
| Model | ROC AUC (All features) | ROC AUC (Selected, k=20) | Change |
|---|---:|---:|---:|
| Random Forest | 0.9020 | 0.9018 | ~ -0.02% |

Decision for Day 4: Keep all engineered features — the small performance change doesn't justify removing informative transformations.

## Deliverables
- Push the notebook (week1_day3.ipynb), the brief PDF summary, and any artifacts (preprocessor, plots) into Week-1/Day-3/.
- Update this README with a short 2–3 sentence summary of what you did and links to important outputs (notebook, deployed models, screenshots).

## Notes / tips
- Always keep a reproducible preprocessing pipeline (ColumnTransformer + Pipeline).
- Report cross‑validation means and standard deviations, not only single split results.
- When comparing models, use paired tests on fold scores to assess statistical significance.

