
# Week 1 — Day 1: ML Foundations

## Dataset
UCI Adult (Census Income) dataset — predict whether income >50K/year.

## Tasks Completed

### Task 1: Problem Framing & Metric Selection
- **Business Objective:** Identify individuals earning >50K to target for a premium financial product. Precision is prioritized to avoid wasting marketing budget on false positives.
- **Target:** income >50K = positive class (1), income ≤50K = negative class (0)
- **Base Rate:** 23.93% of individuals earn >50K.
- **Chosen Metric:** Precision (minimize false positives).

### Task 2: Data Loading & EDA
- **Data Shape:** 48,842 rows, 15 columns
- **Key Findings:**
  - Class imbalance: 76% earn ≤50K, 24% earn >50K.
  - Average age: ~38.6 years.
  - Most common education: HS-grad, Some-college, Bachelors.
  - Capital gain is highly skewed (75% of values are 0).
- **Missing Values:** ' ?' replaced with NaN.
- **Visualizations:** Histograms and bar plots created.

### Task 3: Reproducible Splits
- **Stratified split** used to maintain class distribution.
- **Train:** 35,166
- **Dev:** 3,908
- **Test:** 9,768

### Task 4: Baselines
| Baseline | Accuracy | Precision | Recall | F1 | ROC AUC |
|----------|----------|-----------|--------|----|---------|
| Majority Class | 76.07% | 0.00% | 0.00% | 0.00% | 0.5000 |
| Rule-Based (education-num >= 13) | 75.30% | 48.44% | 49.70% | 49.06% | 0.6653 |

**Interpretation:** Rule-based baseline outperforms majority-class because it actually catches high earners (recall 49.70%).

### Task 5: Error Analysis
- **False Positives:** 477
- **False Negatives:** 949

**Patterns:**
- False Positives: Older (45+), slightly educated, work more hours.
- False Negatives: Middle-aged (42), less educated, work moderate hours.

**Feature Issues to Fix:**
1. Missing values in workclass, occupation, native-country
2. Skewed features: capital-gain, capital-loss
3. High-cardinality categorical: occupation, native-country
4. Outliers in hours-per-week

## Primary Metric for Week 2
**F1 Score** — balance between precision and recall. Baseline F1 = 0.49. Target: >0.55.

## Author
**Fiza Aslam**
