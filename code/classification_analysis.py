#!/usr/bin/env python3
"""
Classification analysis using Random Forest and Gradient Boosting
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class PokecClassifier:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.rf_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.gb_classifier = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        
    def load_data(self, file_path, nrows=10000):
        """Load and prepare the dataset"""
        # Read data
        df = pd.read_csv(file_path, 
                        sep='\t',
                        names=range(60),
                        nrows=nrows)
        
        # Select relevant features
        features = {
            3: 'public',          # Target variable
            7: 'age',            
            8: 'body_type',
            9: 'completion_percentage',
            10: 'spoken_languages',
            11: 'hobbies',
            12: 'music',
            13: 'movies',
            14: 'books',
            15: 'sports'
        }
        
        # Rename columns
        df = df[features.keys()]
        df.columns = features.values()
        
        return df
    
    def preprocess_data(self, df):
        """Preprocess the dataset"""
        # Handle missing values
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        df['completion_percentage'] = pd.to_numeric(df['completion_percentage'], errors='coerce')
        
        # Fill missing values
        df['age'] = df['age'].fillna(df['age'].median())
        df['completion_percentage'] = df['completion_percentage'].fillna(0)
        
        # Create binary features for text columns
        text_columns = ['spoken_languages', 'hobbies', 'music', 'movies', 'books', 'sports']
        for col in text_columns:
            df[f'has_{col}'] = df[col].notna().astype(int)
        
        # Encode categorical variables
        categorical_columns = ['body_type']
        for col in categorical_columns:
            self.label_encoders[col] = LabelEncoder()
            df[col] = self.label_encoders[col].fit_transform(df[col].fillna('unknown'))
        
        # Select final features
        feature_columns = ['age', 'body_type', 'completion_percentage'] + \
                         [f'has_{col}' for col in text_columns]
        
        X = df[feature_columns]
        y = df['public']
        
        return X, y
    
    def train_and_evaluate(self, X, y):
        """Train and evaluate the models"""
        # Split data
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest
        print("\nTraining Random Forest...")
        self.rf_classifier.fit(X_train_scaled, y_train)
        rf_predictions = self.rf_classifier.predict(X_test_scaled)
        
        # Train Gradient Boosting
        print("\nTraining Gradient Boosting...")
        self.gb_classifier.fit(X_train_scaled, y_train)
        gb_predictions = self.gb_classifier.predict(X_test_scaled)
        
        return {
            'rf_predictions': rf_predictions,
            'gb_predictions': gb_predictions,
            'y_test': y_test,
            'feature_names': X.columns
        }
    
    def plot_feature_importance(self, feature_names, output_dir):
        """Plot feature importance for both models"""
        # Random Forest feature importance
        rf_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': self.rf_classifier.feature_importances_
        }).sort_values('importance', ascending=False)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=rf_importance, x='importance', y='feature')
        plt.title('Random Forest Feature Importance')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/rf_feature_importance.png')
        plt.close()
        
        # Gradient Boosting feature importance
        gb_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': self.gb_classifier.feature_importances_
        }).sort_values('importance', ascending=False)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=gb_importance, x='importance', y='feature')
        plt.title('Gradient Boosting Feature Importance')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/gb_feature_importance.png')
        plt.close()
        
        return rf_importance, gb_importance
    
    def plot_confusion_matrices(self, results, output_dir):
        """Plot confusion matrices for both models"""
        # Random Forest confusion matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            confusion_matrix(results['y_test'], results['rf_predictions']),
            annot=True,
            fmt='d',
            cmap='Blues'
        )
        plt.title('Random Forest Confusion Matrix')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/rf_confusion_matrix.png')
        plt.close()
        
        # Gradient Boosting confusion matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            confusion_matrix(results['y_test'], results['gb_predictions']),
            annot=True,
            fmt='d',
            cmap='Blues'
        )
        plt.title('Gradient Boosting Confusion Matrix')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/gb_confusion_matrix.png')
        plt.close()

def main():
    # Create necessary directories
    Path("data").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    Path("plots").mkdir(exist_ok=True)
    
    print("Starting classification analysis...")
    
    # Initialize classifier
    classifier = PokecClassifier()
    
    # Load and preprocess data
    print("\nLoading data...")
    df = classifier.load_data('data/soc-pokec-profiles.txt')
    
    print("\nPreprocessing data...")
    X, y = classifier.preprocess_data(df)
    
    # Train and evaluate models
    results = classifier.train_and_evaluate(X, y)
    
    # Generate feature importance plots
    print("\nGenerating feature importance plots...")
    rf_importance, gb_importance = classifier.plot_feature_importance(
        results['feature_names'],
        'plots'
    )
    
    # Generate confusion matrix plots
    print("\nGenerating confusion matrix plots...")
    classifier.plot_confusion_matrices(results, 'plots')
    
    # Generate classification reports
    rf_report = classification_report(results['y_test'], results['rf_predictions'])
    gb_report = classification_report(results['y_test'], results['gb_predictions'])
    
    # Create analysis report
    report = [
        "Classification Analysis Report",
        "===========================",
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Dataset Size: {len(df):,} profiles",
        "\nFeatures Used:",
        "-------------",
        "\n".join(f"- {feature}" for feature in results['feature_names']),
        "\nRandom Forest Results:",
        "--------------------",
        rf_report,
        "\nGradient Boosting Results:",
        "------------------------",
        gb_report,
        "\nFeature Importance:",
        "-----------------",
        "\nRandom Forest Top Features:",
        rf_importance.to_string(),
        "\nGradient Boosting Top Features:",
        gb_importance.to_string(),
        "\nVisualization Files:",
        "------------------",
        "- plots/rf_feature_importance.png",
        "- plots/gb_feature_importance.png",
        "- plots/rf_confusion_matrix.png",
        "- plots/gb_confusion_matrix.png"
    ]
    
    # Save report
    with open('reports/classification_analysis.txt', 'w') as f:
        f.write('\n'.join(report))
    
    print("\nAnalysis complete! Results saved to:")
    print("- reports/classification_analysis.txt")
    print("- plots/rf_feature_importance.png")
    print("- plots/gb_feature_importance.png")
    print("- plots/rf_confusion_matrix.png")
    print("- plots/gb_confusion_matrix.png")

if __name__ == "__main__":
    main()
