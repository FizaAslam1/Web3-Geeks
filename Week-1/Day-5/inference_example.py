"""
Working Inference Example — UCI Adult (Census Income) Final Pipeline
Week 1, Day 5 — Production-Ready Inference

This script loads the saved, calibrated Gradient Boosting pipeline (final_pipeline.pkl)
and runs it on unseen data to produce final income predictions.
"""

import joblib
import pandas as pd
import numpy as np

SELECTED_THRESHOLD = 0.40  # F1-optimal threshold selected in Day 4


# REQUIRED before loading the pipeline: `final_pipeline.pkl` contains a
# FunctionTransformer(add_engineered_features) step. joblib/pickle only stores a
# reference to the function's NAME, not its code, so this function must be defined
# here (identically to Day 3/4) before joblib.load() runs.
def add_engineered_features(X):
    """
    Add 6 engineered features to the dataframe.
    All features use only current-row data — no data leakage.
    """
    X = X.copy()

    # 1. Age buckets
    X['age_bucket'] = pd.cut(X['age'], bins=[0, 25, 35, 45, 55, 100],
                             labels=['<25', '25-34', '35-44', '45-54', '55+'])

    # 2. Hours-per-week buckets
    X['hours_bucket'] = pd.cut(X['hours-per-week'], bins=[0, 20, 40, 60, 100],
                               labels=['part-time', 'full-time', 'overtime', 'heavy'])

    # 3. Flag: capital_gain > 0
    X['has_capital_gain'] = (X['capital-gain'] > 0).astype(int)

    # 4. log(capital_gain + 1)
    X['log_capital_gain'] = np.log1p(X['capital-gain'])

    # 5. Higher-education boolean
    X['higher_education'] = (X['education-num'] >= 13).astype(int)

    # 6. Interaction: education_num x hours_per_week
    X['edu_hours_interaction'] = X['education-num'] * X['hours-per-week']

    return X


def predict_income(new_data: pd.DataFrame) -> pd.DataFrame:
    """
    Takes raw new/unseen data (same raw columns as training data) and returns
    predicted probability + final class label using the Day 4 tuned threshold.

    WHY: predict_proba + a manual threshold is used instead of .predict(), because
    .predict() defaults to 0.5, which does not match the F1-optimal threshold (0.40)
    selected during Day 4 tuning. Preprocessing is NOT repeated manually here — the
    pipeline already includes it, per the task requirement.
    """
    probs = model.predict_proba(new_data)[:, 1]
    preds = (probs >= SELECTED_THRESHOLD).astype(int)

    result = new_data.copy()
    result["predicted_probability"] = probs
    result["predicted_income"] = preds
    result["predicted_income_label"] = result["predicted_income"].map({0: "<=50K", 1: ">50K"})
    return result


if __name__ == "__main__":
    model = joblib.load("final_pipeline.pkl")

    # Example: run on 10 unseen test examples
    # (replace X_test with any new raw DataFrame with the same original columns)
    from sklearn.datasets import fetch_openml
    from sklearn.model_selection import train_test_split

    data = fetch_openml(name="adult", version=2, as_frame=True)
    df = data.frame.copy()
    df["income"] = df["class"].astype(str).str.contains(">50K").astype(int)
    X = df.drop(columns=["class", "income"])
    y = df["income"]
    _, X_test, _, _ = train_test_split(X, y, test_size=0.20, stratify=y, random_state=42)

    sample_new_data = X_test.sample(10, random_state=42)
    predictions = predict_income(sample_new_data)
    print(predictions[["predicted_probability", "predicted_income_label"]])


# ============================================================
# ACTUAL OUTPUT (from the executed Day 5 notebook, 10 unseen test examples)
# ============================================================
#        predicted_probability predicted_income_label
# 39062               0.045067                  <=50K
# 22272               0.026835                  <=50K
# 32903               0.075708                  <=50K
# 20948               0.004926                  <=50K
# 39688               0.008861                  <=50K
# 363                 0.319275                  <=50K
# 11897               0.007394                  <=50K
# 14076               0.971179                   >50K
# 18176               0.319221                  <=50K
# 8435                0.224359                  <=50K
