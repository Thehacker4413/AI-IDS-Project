# AI-Based Intrusion Detection System: Model Comparison Report

This report provides a comparative analysis of the various machine learning models evaluated for the active AI-Based Intrusion Detection System, trained on the NSL-KDD dataset. 

## Models Evaluated

Four distinct classification algorithms were implemented and trained to identify network anomalies:

1. **Decision Tree**: A foundational tree-based model useful for its interpretability.
2. **Support Vector Machine (SVM)**: A robust classifier focusing on hyperplane optimization (using LinearSVC).
3. **Random Forest**: An ensemble method using multiple decision trees to improve generalization and reduce overfitting.
4. **XGBoost**: An advanced gradient boosting framework known for high performance and execution speed in structured data.

## Evaluation Metrics

The models were evaluated against the following primary classification metrics based on the test set predictions:
- **Accuracy**: The overall percentage of correctly classified instances (both normal and attacks).
- **Precision**: The proportion of true positive attack predictions out of all positive predictions.
- **Recall**: The proportion of actual attacks that were correctly identified.
- **F1-Score**: The harmonic mean of precision and recall, serving as a critical measure for imbalanced datasets in intrusion detection.

## Performance Comparison Data

Based on the quantitative results derived from our testing pipeline, the following performance metrics were secured across the four models:

| Model | Accuracy | Precision | Recall | F1-Score |
| :--- | :--- | :--- | :--- | :--- |
| **XGBoost** | 76.77% | 82.65% | 76.77% | 72.74% |
| **Random Forest** | 75.28% | 79.22% | 75.28% | 70.51% |
| **Decision Tree** | 73.78% | 68.42% | 73.78% | 69.47% |
| **SVM** | 72.11% | 65.33% | 72.11% | 67.19% |

*(Note: Data derived from system-generated evaluation exports)*

## Analysis and Conclusion

1. **Best Performing Model**: **XGBoost** emerged as the top-performing model across all metrics. It safely secures the highest Accuracy (76.77%), Precision (82.65%), and F1-Score (72.74%). Its capability to continually optimize model errors via gradient boosting demonstrates strong applicability for detecting complex network attack signatures.
2. **Ensemble Advantages**: **Random Forest** closely followed XGBoost, highlighting that ensemble tree-based models generally perform better than individual models (Decision Tree) on our high-dimensional dataset features.
3. **Linear Models Limitations**: The linear implementation of **SVM** yielded the lowest metrics within this comparison, largely due to the highly non-linear relationships present in the NSL-KDD dataset features representing various cyber attacks.
4. **System Selection**: Based on this empirical evidence, **XGBoost** is the recommended default predictive engine for the real-time AI-IDS pipeline and web dashboard inference due to its superior precision, thereby significantly minimizing false positives in an operational network context.
