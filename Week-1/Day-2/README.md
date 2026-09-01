# Week 1 Day 2: Data Preprocessing & Supervised Learning Models

## Overview
This notebook demonstrates end-to-end machine learning workflow including data preprocessing, exploratory data analysis, and training two supervised learning models on the Adult dataset.

## Learning Objectives
- Understand data preprocessing pipelines
- Handle missing values in numerical and categorical features
- Implement feature scaling and encoding
- Train and evaluate supervised learning models
- Use scikit-learn's Pipeline and ColumnTransformer

## Dataset
**Adult Dataset** (OpenML)
- **Total Samples**: ~48,842
- **Target Variable**: Income (Binary: ≤50K or >50K)
- **Train/Dev/Test Split**: 80/10/10 with stratification

### Dataset Composition
- **Numeric Features** (6): age, fnlwgt, education-num, capital-gain, capital-loss, hours-per-week
- **Categorical Features** (8): workclass, education, marital-status, occupation, relationship, race, sex, native-country

## Key Findings

### Missing Values
| Feature | Missing Count | Missing % |
|---------|---------------|-----------|
| occupation | 2,809 | 5.75% |
| workclass | 2,799 | 5.73% |
| native-country | 857 | 1.75% |

## Tasks

### Task 1: Preprocessing Plan & Implementation

#### Data Cleaning
- Loaded Adult dataset using scikit-learn's `fetch_openml()`
- Mapped income classes to binary labels (0: ≤50K, 1: >50K)
- Replaced missing value placeholder (' ?') with NaN

#### Feature Analysis
- Identified numeric and categorical features
- Generated missing values summary
- Created bar plots for all categorical features to understand distributions

#### Preprocessing Pipelines

**Numeric Pipeline:**
```python
Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
```
- **Median Imputation**: Robust to outliers
- **Standardization**: Suitable for logistic regression

**Categorical Pipeline:**
```python
Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])
```
- **Most Frequent Imputation**: Safe strategy for categorical data
- **One-Hot Encoding**: Converts categorical variables to numeric format

#### Data Splitting
```
Train: 35,165 samples (70%)
Dev: 3,908 samples (10%)
Test: 9,769 samples (20%)
```
- Used stratified splitting to maintain class distribution

### Task 2: Train Two Supervised Models

Two classification models are trained and compared:

1. **Logistic Regression**
   - Linear model suitable for binary classification
   - Provides probability estimates
   - Interpretable coefficients

2. **Decision Tree Classifier**
   - Non-linear model with max_depth=10
   - Handles feature interactions naturally
   - Interpretable tree structure

#### Model Pipeline
Both models are integrated into scikit-learn pipelines:
```python
Pipeline([
    ('preprocessor', ColumnTransformer),
    ('classifier', Model)
])
```

This ensures preprocessing is applied consistently to all data.

## Libraries Used
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **matplotlib & seaborn**: Data visualization
- **scikit-learn**: Machine learning pipeline and models
  - `fetch_openml`: Dataset loading
  - `train_test_split`: Data splitting with stratification
  - `ColumnTransformer`: Feature preprocessing
  - `Pipeline`: Model pipelines
  - `SimpleImputer`: Missing value handling
  - `StandardScaler`: Feature normalization
  - `OneHotEncoder`: Categorical encoding
  - `LogisticRegression`: Linear classifier
  - `DecisionTreeClassifier`: Tree-based classifier

## Key Concepts

### Why Median for Numeric Features?
Median imputation is more robust to outliers compared to mean imputation, preserving data distribution better.

### Why StandardScaler for Logistic Regression?
Logistic regression is sensitive to feature scaling. Standardization (z-score normalization) ensures all features contribute equally to the model.

### Why One-Hot Encoding?
Converts categorical variables into a format suitable for machine learning algorithms that require numerical input.

### Stratified Splitting?
Maintains the same class distribution in train, dev, and test sets, preventing skewed evaluations.

## Files Generated
- `categorical_bar_plots.png`: Visualization of categorical feature distributions

## Next Steps
- Evaluate model performance on dev and test sets
- Compare metrics (accuracy, precision, recall, F1-score)
- Fine-tune hyperparameters
- Analyze feature importance
- Cross-validation for robust evaluation

## References
- [scikit-learn Pipeline Documentation](https://scikit-learn.org/stable/modules/pipeline.html)
- [scikit-learn ColumnTransformer](https://scikit-learn.org/stable/modules/compose.html#columntransformer)
- [OpenML Adult Dataset](https://www.openml.org/d/1590)

---

**Created for**: Web3-Geeks Learning Program  
**Week**: 1 | **Day**: 2
