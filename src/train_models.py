import pandas as pd
import numpy as np
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def evaluate_model(name, model, X_test, y_test):
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"\n--- {name} Performance ---")
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    # Save confusion matrix plot
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix: {name}')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig(os.path.join(BASE_DIR, 'reports', 'figures', f'cm_{name.replace(" ", "_")}.png'))
    plt.close()
    
    return {'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1}

def train_and_evaluate():
    print("--- PHASE 6: MODEL TRAINING ---")
    print("Loading preprocessed data...")
    train_df = pd.read_csv(os.path.join(BASE_DIR, 'dataset', 'processed', 'train.csv'))
    test_df = pd.read_csv(os.path.join(BASE_DIR, 'dataset', 'processed', 'test.csv'))
    
    # Load selected features to reduce dimensionality and training time
    print("Loading selected features...")
    selected_features = joblib.load(os.path.join(BASE_DIR, 'models', 'selected_features.pkl'))
    
    X_train = train_df[selected_features]
    y_train = train_df['attack_category']
    X_test = test_df[selected_features]
    y_test = test_df['attack_category']
    
    results = {}
    best_model = None
    best_f1 = 0
    best_name = ""
    
    # 1. Decision Tree
    print("\nTraining Decision Tree...")
    dt = DecisionTreeClassifier(random_state=42)
    dt.fit(X_train, y_train)
    results['Decision Tree'] = evaluate_model('Decision Tree', dt, X_test, y_test)
    if results['Decision Tree']['f1'] > best_f1:
        best_f1 = results['Decision Tree']['f1']
        best_model = dt
        best_name = 'Decision Tree'
    
    # 2. Random Forest
    print("\nTraining Random Forest with GridSearchCV...")
    rf = RandomForestClassifier(random_state=42)
    rf_params = {'n_estimators': [50, 100], 'max_depth': [None, 20]}
    rf_grid = GridSearchCV(rf, rf_params, cv=3, scoring='f1_weighted', n_jobs=-1)
    rf_grid.fit(X_train, y_train)
    print(f"Best RF Params: {rf_grid.best_params_}")
    results['Random Forest'] = evaluate_model('Random Forest', rf_grid.best_estimator_, X_test, y_test)
    if results['Random Forest']['f1'] > best_f1:
        best_f1 = results['Random Forest']['f1']
        best_model = rf_grid.best_estimator_
        best_name = 'Random Forest'

    # 3. XGBoost
    print("\nTraining XGBoost...")
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
    xgb.fit(X_train, y_train)
    results['XGBoost'] = evaluate_model('XGBoost', xgb, X_test, y_test)
    if results['XGBoost']['f1'] > best_f1:
        best_f1 = results['XGBoost']['f1']
        best_model = xgb
        best_name = 'XGBoost'
        
    # 4. SVM
    print("\nTraining Linear SVM...")
    svm = LinearSVC(random_state=42, dual=False)
    svm.fit(X_train, y_train)
    results['SVM'] = evaluate_model('SVM', svm, X_test, y_test)
    if results['SVM']['f1'] > best_f1:
        best_f1 = results['SVM']['f1']
        best_model = svm
        best_name = 'SVM'

    print("\n--- PHASE 7: MODEL EVALUATION & PHASE 8: MODEL SAVING ---")
    print(f"Best Model Selected: {best_name} with F1-Score: {best_f1:.4f}")
    
    # Save Best Model
    joblib.dump(best_model, os.path.join(BASE_DIR, 'models', 'best_model.pkl'))
    print("Best model explicitly saved to models/best_model.pkl")
    
    # Save results to report
    results_df = pd.DataFrame(results).T
    results_df.to_csv(os.path.join(BASE_DIR, 'reports', 'model_comparison.csv'))
    print("Model comparison saved to reports/model_comparison.csv")
    print("\n--- Summary of Model Performances ---")
    print(results_df)

if __name__ == '__main__':
    train_and_evaluate()
