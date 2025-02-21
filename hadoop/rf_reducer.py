#!/usr/bin/env python3
"""
Random Forest Analysis - Reducer
Process features and train Random Forest model
Input: Key-value pairs from mapper
Output: Model results and statistics in JSON format
"""

import sys
import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from collections import defaultdict

class RFReducer:
    def __init__(self):
        self.feature_stats = defaultdict(lambda: {
            'sum': 0,
            'sum_squared': 0,
            'count': 0,
            'min': float('inf'),
            'max': float('-inf')
        })
        self.data = []
        
    def update_stats(self, features):
        """Update running statistics for numeric features"""
        numeric_features = ['age', 'completion_percentage']
        
        for feature in numeric_features:
            value = features[feature]
            stats = self.feature_stats[feature]
            stats['sum'] += value
            stats['sum_squared'] += value * value
            stats['count'] += 1
            stats['min'] = min(stats['min'], value)
            stats['max'] = max(stats['max'], value)
    
    def normalize_features(self, features):
        """Normalize numeric features"""
        normalized = features.copy()
        
        for feature in ['age', 'completion_percentage']:
            stats = self.feature_stats[feature]
            if stats['count'] > 0:
                # Z-score normalization
                mean = stats['sum'] / stats['count']
                variance = (stats['sum_squared'] / stats['count']) - (mean * mean)
                std = np.sqrt(variance) if variance > 0 else 1
                
                normalized[feature] = (features[feature] - mean) / std
        
        return normalized
    
    def prepare_data(self):
        """Prepare data for model training"""
        X = []
        y = []
        
        for features in self.data:
            normalized = self.normalize_features(features)
            
            X.append([
                normalized['age'],
                normalized['completion_percentage'],
                features['has_languages'],
                features['has_hobbies']
            ])
            
            y.append(1 if features['public'] == '1' else 0)
        
        return np.array(X), np.array(y)
    
    def train_model(self, X, y):
        """Train Random Forest model"""
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42
        )
        
        # Split data (70-30)
        split_idx = int(0.7 * len(X))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Train model
        model.fit(X_train, y_train)
        
        # Make predictions
        predictions = model.predict(X_test)
        
        return {
            'model': model,
            'predictions': predictions.tolist(),
            'y_test': y_test.tolist(),
            'feature_importance': model.feature_importances_.tolist()
        }
    
    def process_input(self):
        """Process input from mapper"""
        for line in sys.stdin:
            try:
                key, value = line.strip().split('\t')
                features = json.loads(value)
                
                if key == 'stats':
                    self.update_stats(features)
                
                if key == 'data':
                    self.data.append(features)
                    
            except Exception as e:
                sys.stderr.write(f"Error processing line: {str(e)}\n")
                continue
    
    def output_results(self):
        """Output analysis results"""
        # Prepare and train
        X, y = self.prepare_data()
        results = self.train_model(X, y)
        
        # Generate report
        report = classification_report(
            results['y_test'],
            results['predictions'],
            output_dict=True
        )
        
        # Prepare feature importance
        feature_importance = [
            {'feature': 'age', 'importance': results['feature_importance'][0]},
            {'feature': 'completion_percentage', 'importance': results['feature_importance'][1]},
            {'feature': 'has_languages', 'importance': results['feature_importance'][2]},
            {'feature': 'has_hobbies', 'importance': results['feature_importance'][3]}
        ]
        
        # Final output
        output = {
            'statistics': {
                name: {k: v for k, v in stats.items() if k != 'sum_squared'}
                for name, stats in self.feature_stats.items()
            },
            'model_performance': report,
            'feature_importance': feature_importance,
            'data_size': len(self.data)
        }
        
        print(json.dumps(output, indent=2))

def main():
    reducer = RFReducer()
    reducer.process_input()
    reducer.output_results()

if __name__ == "__main__":
    main()
