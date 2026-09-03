# Week 1, Day 4: ML Pipeline Development & Model Evaluation

## 📋 Overview

This notebook demonstrates a **production-ready machine learning pipeline** for binary classification on the Adult Census Income dataset. It covers the complete workflow from data loading through model deployment, with emphasis on reproducibility, hyperparameter tuning, and probability calibration.

**Dataset:** Adult Census Income (OpenML)  
**Target:** Predict if income > $50K  
**Train/Test Split:** 80/20 (39,073 training samples, 9,769 test samples)

---

## 🎯 Learning Objectives

By completing this notebook, you will understand:

1. ✅ Building fully reproducible ML pipelines with sklearn
2. ✅ Feature engineering for non-linear relationships
3. ✅ Hyperparameter search with RandomizedSearchCV
4. ✅ Diagnosing overfitting vs underfitting
5. ✅ Probability calibration and threshold tuning
6. ✅ Deploying models for production use

---

## 📚 Key Concepts Covered

### **TASK 1: Fully Reproducible Pipelines**

**Why reproducibility matters:**
- Ensures consistent results across runs
- Makes models deployable and maintainable
- Enables collaboration and peer review

**Components:**

1. **Feature Engineering** (6 engineered features):
   - `age_bucket`: Age groups (non-linear relationship with income)
   - `hours_bucket`: Work hour categories (part-time vs full-time vs overtime)
   - `has_capital_gain`: Binary flag for presence of capital gains
   - `log_capital_gain`: Log-transformed capital gains (handles skewed distribution)
   - `higher_education`: Boolean indicator for college degree or higher
   - `edu_hours_interaction`: Education × Hours interaction term

2. **Preprocessing Pipeline**:
   - **Numeric features**: Median imputation + StandardScaler
     - Median handles outliers better than mean
     - Scaling is required for logistic regression
   - **Categorical features**: Most-frequent imputation + OneHotEncoder
     - OneHotEncoder preserves nominal relationships without assuming order

3. **Reproducibility Settings**:
   - `random_state=42` for all models
   - OpenML version=2 for consistent column names
   - Stratified split maintains class distribution

---

### **TASK 2: Hyperparameter Search**

**Three candidate models tested:**

#### 1. Logistic Regression
- **Best CV ROC AUC:** 0.9124 ± 0.0030
- **Best Hyperparameters:**
  - `C=1` (regularization strength)
  - `penalty='l1'` (L1 regularization for feature selection)
  - `solver='saga'` (supports L1 and L2)

**Why Logistic Regression?**
- Interpretable coefficients
- Strong baseline for classification
- Fast training

#### 2. Random Forest
- **Best CV ROC AUC:** 0.9163 ± 0.0030
- **Best Hyperparameters:**
  - `n_estimators=200` (number of trees)
  - `max_depth=20` (tree depth)
  - `min_samples_leaf=4` (regularization)
  - `max_features='sqrt'` (feature subsampling)

**Why Random Forest?**
- Captures non-linear relationships
- Handles interactions automatically
- Robust to outliers

#### 3. Gradient Boosting ⭐ **Winner**
- **Best CV ROC AUC:** 0.9277 ± 0.0026
- **Best Hyperparameters:**
  - `n_estimators=200` (boosting stages)
  - `learning_rate=0.05` (step size)
  - `max_depth=7` (tree complexity)
  - `subsample=0.8` (row sampling for regularization)

**Why Gradient Boosting?**
- Sequential error correction
- Highest cross-validation score
- Excellent generalization

---

### **TASK 3: Diagnosing Overfitting / Underfitting**

**Learning curves analysis:**

1. **Logistic Regression (C parameter effect)**:
   - `C=0.001` (heavy regularization) → Underfitting
   - `C=1` → Best balance
   - `C=100` (weak regularization) → Overfitting

2. **Gradient Boosting (max_depth effect)**:
   - `max_depth=1-3` → Underfitting (too simple)
   - `max_depth=5` → Optimal
   - `max_depth=7+` → Overfitting (captures noise)

**Key Insights:**
- Regularization strength must be tuned to the data
- Too simple models underfit; too complex models overfit
- Cross-validation helps find the sweet spot

---

### **TASK 4: Probability Calibration & Threshold Selection**

#### Calibration
- **Brier Score:** 0.0714 (lower is better)
- **Method:** Sigmoid calibration with 5-fold cross-validation
- **Why calibrate?** Raw model probabilities are often not well-calibrated
  - Predicted probability should match actual probability of positive class
  - Essential for business decisions based on confidence

#### Threshold Tuning
Different thresholds optimize different metrics:

| Threshold | Precision | Recall | F1 |
|-----------|-----------|--------|-----|
| 0.10 | 0.520 | 0.978 | 0.679 |
| 0.20 | 0.616 | 0.937 | 0.744 |
| 0.30 | 0.692 | 0.877 | 0.774 |
| **0.40** | **0.767** | **0.794** | **0.781** |
| 0.50 | 0.833 | 0.713 | 0.768 |
| 0.60 | 0.888 | 0.623 | 0.732 |

**Best threshold: 0.40** (maximizes F1 score)

**Business trade-off:**
- Lower threshold → Higher recall (catch more high earners)
- Higher threshold → Higher precision (confident predictions)

---

### **TASK 5: Final Evaluation & Save Artifact**

#### Final Test Metrics (Gradient Boosting + Calibration + Threshold=0.40)

| Metric | Score |
|--------|-------|
| **Accuracy** | 0.8783 |
| **Precision** | 0.7951 |
| **Recall** | 0.6621 |
| **F1 Score** | 0.7225 |
| **ROC AUC** | 0.9292 |
| **PR AUC** | 0.8336 |
| **Brier Score** | 0.0868 |

#### Model Deployment

**Save the pipeline:**
```python
joblib.dump(calibrated_model, 'final_pipeline.pkl')
```

**Load and use for inference:**
```python
import joblib
import pandas as pd

# Load model
model = joblib.load('final_pipeline.pkl')

# Make predictions
X_new = pd.read_csv('new_data.csv')  # Same columns as training
predictions = model.predict(X_new)  # Binary: 0 or 1
probabilities = model.predict_proba(X_new)[:, 1]  # Probability of >50K

# Use custom threshold
custom_predictions = (probabilities >= 0.40).astype(int)
```

---

## 🔧 Technical Stack

```python
# Core libraries
numpy          # Numerical computing
pandas         # Data manipulation
scikit-learn   # ML pipeline & models

# Models tested
LogisticRegression
RandomForestClassifier
GradientBoostingClassifier

# Utilities
joblib         # Model serialization
matplotlib     # Visualization
seaborn        # Statistical plots
```

---

## 📊 Key Takeaways

### 1. **Reproducibility is Critical**
- Use `random_state` everywhere
- Version your data sources (OpenML version=2)
- Document preprocessing steps in the pipeline

### 2. **Feature Engineering Matters**
- 6 engineered features capture domain knowledge
- Non-linear transformations help tree-based models
- Interaction terms can reveal hidden patterns

### 3. **Hyperparameter Tuning is an Art**
- RandomizedSearchCV is efficient for large search spaces
- Cross-validation prevents overfitting to the validation set
- Balance between exploration and computation time

### 4. **Calibration ≠ Performance**
- Calibration improves probability estimates, not ranking
- Useful when probabilities are used for business decisions
- Sigmoid calibration works well for tree-based models

### 5. **Threshold Selection is Business-Driven**
- Default threshold (0.5) is not always optimal
- F1 score balances precision and recall
- Business context determines optimal threshold

---

## 🚀 How to Run

1. **Install dependencies:**
   ```bash
   pip install numpy pandas scikit-learn matplotlib seaborn joblib
   ```

2. **Run the notebook:**
   ```bash
   jupyter notebook "week1 day4.ipynb"
   ```

3. **Execute cells in order** (top to bottom) for reproducible results

4. **Output files generated:**
   - `final_pipeline.pkl` — Deployable model
   - `logreg_C_effect.png` — Regularization effect
   - `gb_depth_effect.png` — Tree depth effect
   - `calibration_plot.png` — Probability calibration
   - `confusion_matrix_threshold.png` — Classification errors

---

## 📝 Production Checklist

Before deploying this model to production:

- ✅ **Data Validation**: Ensure new data has same columns and types
- ✅ **Missing Values**: Pipeline handles via imputation
- ✅ **Categorical Encoding**: Pipeline handles via OneHotEncoder
- ✅ **Scaling**: Numeric features are standardized
- ✅ **Probability Calibration**: Sigmoid calibration applied
- ✅ **Threshold**: Set to 0.40 for F1 optimization
- ⚠️ **Non-Causal Features**: `fnlwgt` (final weight) should not be used for causal inference
- ⚠️ **Data Drift**: Monitor input distributions in production

---

## 🎓 Further Reading

**Concepts to explore:**
- [ROC-AUC vs Precision-Recall curves](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [Probability Calibration](https://scikit-learn.org/stable/modules/calibration.html)
- [Hyperparameter Tuning Strategies](https://scikit-learn.org/stable/modules/grid_search.html)
- [Feature Engineering Best Practices](https://en.wikipedia.org/wiki/Feature_engineering)

---

## 📞 Questions?

This notebook is designed for learning. If you have questions about any section:
1. Read the inline comments in the code
2. Check the "WHY" explanations in each task
3. Refer to scikit-learn documentation
4. Run experiments by modifying hyperparameters

---

**Last Updated:** Week 1, Day 4  
**Dataset:** Adult Census Income (OpenML v2)  
**Best Model:** Gradient Boosting Classifier  
**Final Test ROC AUC:** 0.9292
