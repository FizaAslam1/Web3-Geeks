# UCI Adult (Census Income) — Final ML Project

## Project Objective
Predict whether an individual's annual income exceeds $50K based on U.S. Census demographic and
employment attributes. This is a binary classification problem where the model must balance
precision and recall based on the relative cost of false positives vs. false negatives.

## Dataset Description
- **Source:** UCI Adult / Census Income (OpenML, version=2)
- **Rows:** 48,842 (Train: 39,073 / Test: 9,769 — 80/20 stratified split, random_state=42)
- **Target variable:** `income` (binary — 1 if >50K, else 0)
- **Test set positive rate:** 23.93%

## Feature Engineering
Six engineered features were added (based on Day 3's mutual information analysis):
1. `age_bucket` — binned age into 5 groups (<25, 25-34, 35-44, 45-54, 55+)
2. `hours_bucket` — binned hours-per-week into 4 groups (part-time, full-time, overtime, heavy)
3. `has_capital_gain` — binary flag for capital_gain > 0
4. `log_capital_gain` — log(capital_gain + 1), to handle the highly skewed distribution
5. `higher_education` — binary flag for education-num >= 13 (college degree indicator)
6. `edu_hours_interaction` — education-num × hours-per-week interaction term

## Preprocessing Steps
- **Numeric features:** median imputation + StandardScaler
- **Categorical features:** most-frequent imputation + OneHotEncoder (handle_unknown='ignore')
- Applied via a `ColumnTransformer`, fit only on training data — confirmed leak-free (0 overlapping
  indices between train and test sets)

## Models Tested
| Model | Best CV ROC AUC (Day 4) |
|---|---|
| Logistic Regression | 0.9124 |
| Random Forest | 0.9163 |
| **Gradient Boosting (SELECTED)** | **0.9277** |

## Hyperparameter Tuning Approach
`RandomizedSearchCV` with 5-fold `StratifiedKFold` across all three model families.

## Best Parameters (Gradient Boosting)
`learning_rate=0.05, n_estimators=200, max_depth=7, subsample=0.8`

## Selected Classification Threshold
**0.40** — chosen to maximize F1 score on the Day 4 threshold sweep (0.10 to 0.90), rather than
using the default 0.5. Applied via `predict_proba()` + manual threshold comparison, not `.predict()`.

## Final Test Performance (Day 5, on the untouched hold-out test set)
| Metric | Value |
|---|---|
| Accuracy | 0.8711 |
| Precision | 0.7299 |
| Recall | 0.7327 |
| F1 | 0.7313 |
| ROC AUC | 0.9292 |
| PR AUC | 0.8336 |
| Brier Score | 0.0868 |

**Confusion Matrix (Test, threshold=0.40):**
| | Predicted ≤50K | Predicted >50K |
|---|---|---|
| **Actual ≤50K** | 6,797 | 634 (FP) |
| **Actual >50K** | 625 (FN) | 1,713 |

## Important Features
Top predictors by Gradient Boosting feature importance:
1. `marital-status_Married-civ-spouse` (0.321) — by far the strongest predictor
2. `education-num` (0.102)
3. `edu_hours_interaction` (0.088) — engineered feature
4. `log_capital_gain` (0.085) — engineered feature
5. `capital-gain` (0.082)
6. `capital-loss` (0.064)
7. `age` (0.060)
8. `fnlwgt` (0.042) — ⚠️ see limitations below

## Known Limitations
- **`fnlwgt` is a Census sampling weight, not a causal income driver.** It reflects how many people
  in the population a row represents, not anything about that individual's earning potential. Its
  non-trivial importance score (0.042) is likely picking up incidental correlations with demographic
  sampling strata and should not be interpreted as a genuine income signal.
- **Elevated error rates in specific occupations:** Protective-serv (21.5% error rate), Exec-managerial
  (19.2%), and Craft-repair (18.1%) show the highest misclassification rates, likely because income in
  these roles varies widely with seniority and overtime — factors not fully captured by the available
  features.
- **Calibration trade-off:** sigmoid calibration slightly increased the Brier score on training data
  (0.0714 → 0.0868 pre/post calibration in Day 4), reflecting the standard accuracy/calibration
  trade-off — probabilities are better calibrated but marginally less sharp.
- Dataset reflects U.S. Census data and may not generalize to other populations or time periods.

## How to Reproduce Training
1. Load data via `fetch_openml("adult", version=2)`
2. Split 80/20 stratified, `random_state=42`
3. Apply `add_engineered_features()` (6 features, see above)
4. Fit `ColumnTransformer` (median/scale numeric, most-frequent/one-hot categorical) on training
   data only
5. Tune Gradient Boosting via `RandomizedSearchCV` (5-fold `StratifiedKFold`)
6. Wrap the fitted pipeline in `CalibratedClassifierCV(method='sigmoid', cv=5)`
7. Select threshold (0.40) via F1-maximizing sweep on training probabilities
8. Save via `joblib.dump(calibrated_model, 'final_pipeline.pkl')`

## How to Run Inference
```python
import joblib

# NOTE: add_engineered_features() must be defined in this session before loading,
# since it's referenced inside the pickled FunctionTransformer step.
model = joblib.load('final_pipeline.pkl')

probs = model.predict_proba(new_data)[:, 1]
preds = (probs >= 0.40).astype(int)  # use the selected threshold, not .predict()'s default 0.5
```

## Environment / Library Versions
- scikit-learn: 1.8.0
- pandas, numpy, joblib (standard versions — run `pip freeze` for exact pins)
