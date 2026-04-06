import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("--- PHASE 4: EDA & PHASE 5: FEATURE ENGINEERING ---")
    os.makedirs(os.path.join(BASE_DIR, 'reports', 'figures'), exist_ok=True)
    
    print("Loading preprocessed training data...")
    # Load preprocessed data
    train_df = pd.read_csv(os.path.join(BASE_DIR, 'dataset', 'processed', 'train.csv'))
    test_df = pd.read_csv(os.path.join(BASE_DIR, 'dataset', 'processed', 'test.csv'))
    
    X_train = train_df.drop('attack_category', axis=1)
    y_train = train_df['attack_category']
    X_test = test_df.drop('attack_category', axis=1)
    y_test = test_df['attack_category']
    
    print("1. Plotting Attack Distribution...")
    # 1. Attack Distribution Bar Chart
    plt.figure(figsize=(10, 6))
    sns.countplot(x='attack_category', data=train_df)
    plt.title('Attack Category Distribution')
    plt.savefig(os.path.join(BASE_DIR, 'reports', 'figures', 'attack_distribution.png'))
    plt.close()
    
    print("2. Plotting Correlation Heatmap...")
    # 2. Correlation Heatmap
    plt.figure(figsize=(12, 10))
    corr = X_train.iloc[:, :15].corr()
    sns.heatmap(corr, annot=False, cmap='coolwarm')
    plt.title('Correlation Heatmap (First 15 Features)')
    plt.savefig(os.path.join(BASE_DIR, 'reports', 'figures', 'correlation_heatmap.png'))
    plt.close()
    
    print("3. Calculating Feature Importance using Random Forest...")
    # 3. Feature Importance
    rf = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    
    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(12, 6))
    plt.title("Feature Importances (Top 20)")
    plt.bar(range(20), importances[indices][:20], align="center")
    plt.xticks(range(20), [X_train.columns[i] for i in indices[:20]], rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, 'reports', 'figures', 'feature_importance.png'))
    plt.close()
    
    print("4. Selecting Features...")
    # Select important features
    top_features = [X_train.columns[i] for i in indices[:20]]
    print("Top 20 Selected Features:", top_features)
    
    os.makedirs(os.path.join(BASE_DIR, 'models'), exist_ok=True)
    joblib.dump(top_features, os.path.join(BASE_DIR, 'models', 'selected_features.pkl'))
    
    print("5. Optional: Dimensionality Reduction (PCA)")
    pca = PCA(n_components=20)
    pca.fit(X_train[top_features])
    joblib.dump(pca, os.path.join(BASE_DIR, 'models', 'pca_model.pkl'))
    
    # Save transformed data? If we just use top features, we can do it in training.
    # For now, let's keep the pipeline simple and rely on top_features filter.
    
    print("EDA and Feature Engineering complete. Figures saved to reports/figures/.")

if __name__ == '__main__':
    main()
