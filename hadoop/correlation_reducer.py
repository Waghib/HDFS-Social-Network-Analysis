#!/usr/bin/env python3
"""
Reducer for analyzing correlations between completion_percentage and other features
"""
import sys
import json
from collections import defaultdict
import math

class StatisticsCalculator:
    def __init__(self):
        self.count = 0
        self.sum = 0
        self.sum_squares = 0
        self.values = []
        self.min_val = float('inf')
        self.max_val = float('-inf')
    
    def add_value(self, value):
        self.count += 1
        self.sum += value
        self.sum_squares += value * value
        self.values.append(value)
        self.min_val = min(self.min_val, value)
        self.max_val = max(self.max_val, value)
    
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
            'std_dev': round(std_dev, 2),
            'min': round(self.min_val, 2),
            'max': round(self.max_val, 2)
        }

class CorrelationCalculator:
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
completion_stats = StatisticsCalculator()
correlations = defaultdict(CorrelationCalculator)
gender_stats = defaultdict(StatisticsCalculator)
age_group_stats = defaultdict(StatisticsCalculator)

# Process input from mapper
for line in sys.stdin:
    try:
        key, *values = line.strip().split('\t')
        
        if key == 'COMPLETION_STATS':
            completion_stats.add_value(float(values[0]))
            
        elif key == 'CORRELATION':
            feature, value, completion = values
            correlations[feature].add_pair(float(value), float(completion))
            
        elif key == 'GENDER_COMPLETION':
            gender, completion = values
            gender_stats[gender].add_value(float(completion))
            
        elif key == 'AGE_GROUP':
            age_group, completion = values
            age_group_stats[age_group].add_value(float(completion))
            
    except Exception as e:
        continue

# Generate report
report = """# Profile Completion Correlation Analysis Report

## Overall Completion Percentage Statistics"""

stats = completion_stats.get_stats()
if stats:
    report += f"""
- Mean: {stats['mean']}%
- Median: {stats['median']}%
- Standard Deviation: {stats['std_dev']}%
- Range: {stats['min']}% - {stats['max']}%

## Correlations with Completion Percentage"""

    for feature, calc in correlations.items():
        correlation = calc.get_correlation()
        report += f"\n- {feature}: {correlation}"

    report += "\n\n## Completion Percentage by Gender"
    for gender, calc in gender_stats.items():
        stats = calc.get_stats()
        if stats:
            report += f"""
- Gender {gender}:
  - Mean: {stats['mean']}%
  - Median: {stats['median']}%
  - Count: {stats['count']:,}"""

    report += "\n\n## Completion Percentage by Age Group"
    for age_group in ['<20', '20-30', '30-40', '40-50', '>50']:
        stats = age_group_stats[age_group].get_stats()
        if stats:
            report += f"""
- Age {age_group}:
  - Mean: {stats['mean']}%
  - Median: {stats['median']}%
  - Count: {stats['count']:,}"""

# Print report in a format that can be easily parsed
print("###START_REPORT###")
print(report)
print("###END_REPORT###")
