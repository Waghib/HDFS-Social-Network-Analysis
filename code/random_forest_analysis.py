#!/usr/bin/env python3
"""
Simple Random Forest Classification Analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_prepare_data(file_path, nrows=10000):
    """Load and prepare the dataset"""
    # Read data
    df = pd.read_csv(file_path, 
                    sep='\t',
                    names=range(60),
                    nrows=nrows)
    
    # Select only essential features
    features = {
        3: 'public',          # Target variable
        7: 'age',            
        9: 'completion_percentage',
        10: 'spoken_languages',
        11: 'hobbies'
    }
    
    # Rename columns
    df = df[features.keys()]
    df.columns = features.values()
    
    return df

def preprocess_data(df):
    """Basic preprocessing"""
    # Handle numeric features
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df['completion_percentage'] = pd.to_numeric(df['completion_percentage'], errors='coerce')
    
    # Fill missing values
    df['age'] = df['age'].fillna(df['age'].median())
    df['completion_percentage'] = df['completion_percentage'].fillna(0)
    
    # Create binary features for text columns
    df['has_languages'] = df['spoken_languages'].notna().astype(int)
    df['has_hobbies'] = df['hobbies'].notna().astype(int)
    
    # Select final features
    X = df[['age', 'completion_percentage', 'has_languages', 'has_hobbies']]
    y = df['public']
    
    return X, y

def train_and_evaluate(X, y):
    """Train and evaluate Random Forest"""
    # Split data - 70% train, 30% test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    rf = RandomForestClassifier(
        n_estimators=100,  # Reduced number of trees
        max_depth=5,       # Limited depth
        random_state=42
    )
    
    print("\nTraining Random Forest...")
    rf.fit(X_train_scaled, y_train)
    
    # Make predictions
    predictions = rf.predict(X_test_scaled)
    
    return {
        'model': rf,
        'predictions': predictions,
        'y_test': y_test,
        'feature_names': X.columns
    }

def generate_report(results, output_dir):
    """Generate analysis report and visualizations"""
    # Feature importance plot
    importance = pd.DataFrame({
        'feature': results['feature_names'],
        'importance': results['model'].feature_importances_
    }).sort_values('importance', ascending=False)
    
    plt.figure(figsize=(8, 4))
    sns.barplot(data=importance, x='importance', y='feature')
    plt.title('Feature Importance')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/feature_importance.png')
    plt.close()
    
    # Generate classification report
    report = [
        "Random Forest Classification Analysis",
        "==================================",
        "\nModel Configuration:",
        "- n_estimators: 100",
        "- max_depth: 5",
        "\nFeatures Used:",
        "-------------",
        "\n".join(f"- {feature}" for feature in results['feature_names']),
        "\nClassification Report:",
        "--------------------",
        classification_report(results['y_test'], results['predictions']),
        "\nFeature Importance:",
        "-----------------",
        importance.to_string(),
        "\nVisualization saved to: plots/feature_importance.png"
    ]
    
    # Save report
    with open('reports/rf_classification_analysis.txt', 'w') as f:
        f.write('\n'.join(report))

def main():
    # Create directories
    Path("data").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    Path("plots").mkdir(exist_ok=True)
    
    print("Starting Random Forest analysis...")
    
    # Load and process data
    print("\nLoading data...")
    df = load_and_prepare_data('data/soc-pokec-profiles.txt')
    
    print("\nPreprocessing data...")
    X, y = preprocess_data(df)
    
    # Train and evaluate
    results = train_and_evaluate(X, y)
    
    # Generate report
    print("\nGenerating report...")
    generate_report(results, 'plots')
    
    print("\nAnalysis complete! Results saved to:")
    print("- reports/rf_classification_analysis.txt")
    print("- plots/feature_importance.png")

if __name__ == "__main__":
    main()
