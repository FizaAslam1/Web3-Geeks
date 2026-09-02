
📌 Overview
Day 3 focuses on feature engineering, cross-validation, and model comparison on the UCI Adult (Census Income) dataset. The goal is to expand the feature set with principled engineering, and use cross-validation to compare models reliably before hyperparameter tuning.

📂 Files
File	Description
week1_day3.ipynb	Jupyter notebook with all code
week1_day3_summary.pdf	2-page summary of engineered features, CV results, statistical tests, and model selection
preprocessor_day3.pkl	Saved preprocessing pipeline for reuse
cv_boxplots.png	Boxplots of cross-validation scores for all models
README.md	This file
🛠️ Tech Stack
Component	Tool
Language	Python 3
Data Processing	Pandas, NumPy
Preprocessing	Scikit-learn (ColumnTransformer, Pipeline, FunctionTransformer)
Models	Logistic Regression, Random Forest, Gradient Boosting
Evaluation	Cross-validation (5-fold), Accuracy, F1, ROC AUC
Statistical Tests	Paired t-test, Wilcoxon test
Feature Selection	SelectKBest, Mutual Information
📊 Engineered Features
Feature	Type	Creation Rule	Predictive Signal (MI)
age_bucket	Categorical	Binned age into 5 groups	0.0628
hours_bucket	Categorical	Binned hours into 4 groups	0.0302
has_capital_gain	Binary	Flag if capital_gain > 0	0.0095
log_capital_gain	Numeric	log(capital_gain + 1)	0.0775
higher_education	Binary	education-num >= 13	0.0495
edu_hours_interaction	Numeric	education-num × hours-per-week	0.0810
Key Insight: log_capital_gain and edu_hours_interaction have the highest predictive signal.

📈 Cross-Validated Model Comparison (5-fold)
Model	Accuracy	F1	ROC AUC
Logistic Regression	0.8557 ± 0.0022	0.6683 ± 0.0067	0.9120 ± 0.0024
Random Forest	0.8515 ± 0.0011	0.6646 ± 0.0038	0.9020 ± 0.0028
Gradient Boosting	0.8638 ± 0.0032	0.6790 ± 0.0071	0.9200 ± 0.0024
Key Observations:

Gradient Boosting performs best across all metrics.

Logistic Regression is strong and highly interpretable.

All models are stable (low standard deviations).

🔍 Statistical Comparison
Comparison	Test	p-value	Significant?
Logistic vs Random Forest	Paired t-test	0.0002	✅ Yes
Logistic vs Gradient Boosting	Paired t-test	0.0048	✅ Yes
Random Forest vs Gradient Boosting	Paired t-test	0.0002	✅ Yes
Conclusion: Gradient Boosting is statistically significantly better than both Logistic Regression and Random Forest (p < 0.05).

📌 Feature Importance (Random Forest)
Top 5 Features:

num__fnlwgt (0.1428) — Demographic weight

num__age (0.1088) — Age

num__edu_hours_interaction (0.0711) — Engineered interaction

cat__marital-status_Married-civ-spouse (0.0643) — Marital status

num__capital-gain (0.0528) — Capital gain

Engineered Features that Mattered Most:

log_capital_gain (0.0421) — Handles skewness

edu_hours_interaction (0.0711) — Captures combined effect

higher_education (0.0221) — Strong predictor

📊 Feature Selection Impact
Model	ROC AUC (All)	ROC AUC (Selected, k=20)	Change
Random Forest	0.9020	0.9018	~ -0.02%
Decision for Day 4: Keep all features. Performance drop is minimal, and engineered features provide valuable information for hyperparameter tuning.

