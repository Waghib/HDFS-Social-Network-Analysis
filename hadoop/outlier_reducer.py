#!/usr/bin/env python3
"""
Reducer for outlier analysis and handling sparsity in the dataset
Input format: Key-value pairs from mapper with statistics
"""
import sys
import json
import numpy as np
from collections import defaultdict

class NumericStatsAggregator:
    def __init__(self):
        self.values = []
        
    def add(self, value):
        self.values.append(value)
    
    def compute_stats(self):
        if not self.values:
            return None
            
        values = np.array(self.values)
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1
        
        return {
            'count': len(values),
            'mean': np.mean(values),
            'std': np.std(values),
            'min': np.min(values),
            'max': np.max(values),
            'q1': q1,
            'q3': q3,
            'iqr': iqr,
            'lower_bound': q1 - 1.5 * iqr,
            'upper_bound': q3 + 1.5 * iqr
        }

class FeatureStatsAggregator:
    def __init__(self):
        self.total_count = 0
        self.missing_count = 0
        
    def add(self, is_missing):
        self.total_count += 1
        if is_missing:
            self.missing_count += 1
    
    def compute_stats(self):
        if self.total_count == 0:
            return None
            
        return {
            'total_count': self.total_count,
            'missing_count': self.missing_count,
            'missing_percentage': (self.missing_count / self.total_count) * 100,
            'completeness': ((self.total_count - self.missing_count) / self.total_count) * 100
        }

def main():
    # Initialize aggregators
    numeric_stats = defaultdict(NumericStatsAggregator)
    feature_stats = defaultdict(FeatureStatsAggregator)
    
    # Process input from mapper
    for line in sys.stdin:
        try:
            key, value = line.strip().split('\t')
            data = json.loads(value)
            
            if key == 'NUMERIC':
                field = data['field']
                numeric_stats[field].add(data['value'])
            elif key == 'FEATURE':
                field = data['field']
                feature_stats[field].add(data['is_missing'])
                
        except Exception as e:
            continue
    
    # Generate report
    report = {
        'numeric_fields': {},
        'feature_quality': {
            'high_quality': [],
            'medium_quality': [],
            'low_quality': []
        },
        'outlier_summary': {}
    }
    
    # Process numeric statistics
    for field, aggregator in numeric_stats.items():
        stats = aggregator.compute_stats()
        if stats:
            report['numeric_fields'][field] = stats
            
            # Calculate outliers
            values = np.array(aggregator.values)
            outliers = values[(values < stats['lower_bound']) | (values > stats['upper_bound'])]
            report['outlier_summary'][field] = {
                'total_outliers': len(outliers),
                'outlier_percentage': (len(outliers) / len(values)) * 100
            }
    
    # Process feature quality
    for field, aggregator in feature_stats.items():
        stats = aggregator.compute_stats()
        if stats:
            completeness = stats['completeness']
            if completeness >= 80:
                report['feature_quality']['high_quality'].append({
                    'field': field,
                    'completeness': completeness
                })
            elif completeness >= 50:
                report['feature_quality']['medium_quality'].append({
                    'field': field,
                    'completeness': completeness
                })
            else:
                report['feature_quality']['low_quality'].append({
                    'field': field,
                    'completeness': completeness
                })
    
    # Output report
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
