#!/usr/bin/env python3
"""
MapReduce implementation - Reducer
Process age statistics and perform clustering
Input: Key-value pairs from mapper
Output: JSON format with normalized/standardized ages and clusters
"""

import sys
import json
import numpy as np
from collections import defaultdict

class AgeAnalysisReducer:
    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters
        self.ages = []
        self.sum_age = 0
        self.sum_squared = 0
        self.count = 0
        self.cluster_centers = None
        self.stats = {
            'min_age': float('inf'),
            'max_age': float('-inf'),
            'mean_age': 0,
            'std_age': 0
        }
    
    def update_statistics(self, age):
        """Update running statistics"""
        self.stats['min_age'] = min(self.stats['min_age'], age)
        self.stats['max_age'] = max(self.stats['max_age'], age)
        self.sum_age += age
        self.sum_squared += age * age
        self.count += 1
        self.ages.append(age)
    
    def calculate_final_statistics(self):
        """Calculate final statistics"""
        if self.count > 0:
            self.stats['mean_age'] = self.sum_age / self.count
            variance = (self.sum_squared / self.count) - (self.stats['mean_age'] ** 2)
            self.stats['std_age'] = np.sqrt(variance)
    
    def normalize_age(self, age):
        """Min-max normalization"""
        if self.stats['max_age'] == self.stats['min_age']:
            return 0.5  # Default for constant values
        return (age - self.stats['min_age']) / (self.stats['max_age'] - self.stats['min_age'])
    
    def standardize_age(self, age):
        """Z-score standardization"""
        if self.stats['std_age'] == 0:
            return 0  # Default for constant values
        return (age - self.stats['mean_age']) / self.stats['std_age']
    
    def initialize_clusters(self):
        """Initialize cluster centers using quantiles"""
        if self.ages:
            ages_array = np.array(self.ages)
            quantiles = np.linspace(0, 100, self.n_clusters + 1)[1:-1]
            self.cluster_centers = np.percentile(ages_array, quantiles)
    
    def assign_cluster(self, age):
        """Assign age to nearest cluster"""
        if self.cluster_centers is None:
            return 0
        distances = np.abs(self.cluster_centers - age)
        return int(np.argmin(distances))
    
    def process_input(self):
        """Process input from mapper"""
        for line in sys.stdin:
            try:
                key, value = line.strip().split('\t')
                
                if key == 'stats':
                    # Process statistics
                    data = json.loads(value)
                    age = data['age']
                    self.update_statistics(age)
                    
            except Exception as e:
                sys.stderr.write(f"Error processing line: {str(e)}\n")
                continue
        
        # Calculate final statistics
        self.calculate_final_statistics()
        
        # Initialize clusters
        self.initialize_clusters()
    
    def output_results(self):
        """Output results in JSON format"""
        # Process all ages
        processed_ages = []
        for age in self.ages:
            processed_ages.append({
                'original': age,
                'normalized': self.normalize_age(age),
                'standardized': self.standardize_age(age),
                'cluster': self.assign_cluster(age)
            })
        
        # Calculate cluster statistics
        cluster_stats = defaultdict(lambda: {'count': 0, 'sum_age': 0, 'sum_squared': 0})
        for age_data in processed_ages:
            cluster = age_data['cluster']
            age = age_data['original']
            cluster_stats[cluster]['count'] += 1
            cluster_stats[cluster]['sum_age'] += age
            cluster_stats[cluster]['sum_squared'] += age * age
        
        # Finalize cluster statistics
        for cluster_id, stats in cluster_stats.items():
            count = stats['count']
            if count > 0:
                mean = stats['sum_age'] / count
                variance = (stats['sum_squared'] / count) - (mean ** 2)
                cluster_stats[cluster_id] = {
                    'count': count,
                    'mean': mean,
                    'std': np.sqrt(variance)
                }
        
        # Prepare final report
        report = {
            'statistics': self.stats,
            'clusters': {
                'centers': self.cluster_centers.tolist(),
                'stats': cluster_stats
            },
            'processed_ages': processed_ages[:5]  # Sample of first 5 processed ages
        }
        
        # Output JSON results
        print(json.dumps(report, indent=2))

def main():
    reducer = AgeAnalysisReducer()
    reducer.process_input()
    reducer.output_results()

if __name__ == "__main__":
    main()
