#!/usr/bin/env python3
"""
Reducer for analyzing relationships between completion_percentage and categorical variables
"""
import sys
import json
from collections import defaultdict
import math

class StatisticsCalculator:
    """Calculate statistics for a group of values"""
    def __init__(self):
        self.count = 0
        self.sum = 0
        self.sum_squares = 0
        self.values = []
    
    def add_value(self, value):
        self.count += 1
        self.sum += value
        self.sum_squares += value * value
        self.values.append(value)
    
    def get_stats(self):
        if self.count == 0:
            return None
            
        mean = self.sum / self.count
        variance = (self.sum_squares / self.count) - (mean * mean)
        std_dev = math.sqrt(variance) if variance > 0 else 0
        
        # Calculate median
        self.values.sort()
        if self.count % 2 == 0:
            median = (self.values[self.count//2-1] + self.values[self.count//2]) / 2
        else:
            median = self.values[self.count//2]
            
        return {
            'count': self.count,
            'mean': round(mean, 2),
            'median': round(median, 2),
            'std_dev': round(std_dev, 2)
        }

class CorrelationCalculator:
    """Calculate correlation between two variables"""
    def __init__(self):
        self.sum_x = 0
        self.sum_y = 0
        self.sum_xy = 0
        self.sum_x2 = 0
        self.sum_y2 = 0
        self.n = 0
    
    def add_pair(self, x, y):
        self.sum_x += x
        self.sum_y += y
        self.sum_xy += x * y
        self.sum_x2 += x * x
        self.sum_y2 += y * y
        self.n += 1
    
    def get_correlation(self):
        if self.n == 0:
            return 0
        
        numerator = (self.n * self.sum_xy) - (self.sum_x * self.sum_y)
        denominator = math.sqrt(
            ((self.n * self.sum_x2) - (self.sum_x * self.sum_x)) *
            ((self.n * self.sum_y2) - (self.sum_y * self.sum_y))
        )
        
        if denominator == 0:
            return 0
            
        return round(numerator / denominator, 3)

# Initialize data structures
feature_stats = defaultdict(lambda: defaultdict(StatisticsCalculator))
correlation_calc = CorrelationCalculator()

# Process input from mapper
for line in sys.stdin:
    try:
        key, value = line.strip().split('\t')
        data = json.loads(value)
        
        if key == 'FEATURE':
            # Add completion percentage to feature statistics
            feature_stats[data['name']][data['value']].add_value(data['completion'])
            
        elif key == 'CORRELATION':
            # Add values to correlation calculator
            correlation_calc.add_pair(data['x'], data['y'])
            
    except Exception as e:
        continue

# Generate report
report = """# Feature Relationships Analysis Report

## Categorical Variable Relationships\n"""

# Process each feature's statistics
for feature_name, value_stats in feature_stats.items():
    report += f"\n### Profile Completion by {feature_name.replace('_', ' ').title()}\n\n"
    report += "| Category | Count | Mean | Median | Std Dev |\n"
    report += "|----------|-------|------|---------|----------|\n"
    
    # Get top 10 categories by count
    top_categories = sorted(
        [(value, calc.count) for value, calc in value_stats.items()],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    for value, _ in top_categories:
        stats = value_stats[value].get_stats()
        if stats:
            report += f"| {value} | {stats['count']:,} | {stats['mean']:.2f}% | "
            report += f"{stats['median']:.2f}% | {stats['std_dev']:.2f}% |\n"

# Add correlation results
correlation = correlation_calc.get_correlation()
report += "\n## Numerical Correlations\n\n"
report += f"Correlation between user_id and completion_percentage: {correlation}\n"

report += "\n## Visualizations\n"
report += "Note: In the MapReduce implementation, visualizations need to be generated separately\n"
report += "using the data from this analysis.\n"

# Print report
print("###START_REPORT###")
print(report)
print("###END_REPORT###")
