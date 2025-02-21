#!/usr/bin/env python3
"""
Reducer for analyzing user features (age, gender, region)
Input format: key\tvalue where key is one of [AGE, GENDER, REGION]
"""
import sys
from collections import defaultdict
import json

# Initialize counters
age_data = {
    'count': 0,
    'sum': 0,
    'min': float('inf'),
    'max': float('-inf'),
    'values': []  # For calculating median
}

gender_counts = defaultdict(int)
region_counts = defaultdict(int)

# Process input from mapper
for line in sys.stdin:
    try:
        # Remove leading/trailing whitespace and split by tab
        key, value = line.strip().split('\t')
        
        if key == 'AGE':
            age = int(value)
            age_data['count'] += 1
            age_data['sum'] += age
            age_data['min'] = min(age_data['min'], age)
            age_data['max'] = max(age_data['max'], age)
            age_data['values'].append(age)
            
        elif key == 'GENDER':
            gender_counts[value] += 1
            
        elif key == 'REGION':
            region_counts[value] += 1
            
    except Exception as e:
        continue

# Calculate statistics
results = {
    'age_analysis': {
        'total_users': age_data['count'],
        'mean_age': round(age_data['sum'] / age_data['count'], 2) if age_data['count'] > 0 else 0,
        'min_age': age_data['min'] if age_data['min'] != float('inf') else 0,
        'max_age': age_data['max'] if age_data['max'] != float('-inf') else 0,
        'median_age': sorted(age_data['values'])[len(age_data['values'])//2] if age_data['values'] else 0
    },
    'gender_analysis': {
        'counts': dict(gender_counts),
        'percentages': {
            gender: round(count / sum(gender_counts.values()) * 100, 2)
            for gender, count in gender_counts.items()
        }
    },
    'region_analysis': {
        'top_5_regions': dict(sorted(region_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
        'percentages': {
            region: round(count / sum(region_counts.values()) * 100, 2)
            for region, count in sorted(region_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    }
}

# Generate report
report = f"""# User Features Analysis Report

## Dataset Overview
Total number of users with valid age data: {results['age_analysis']['total_users']:,}

## Age Analysis
- Mean Age: {results['age_analysis']['mean_age']} years
- Median Age: {results['age_analysis']['median_age']:.2f} years
- Age Range: {results['age_analysis']['min_age']} - {results['age_analysis']['max_age']} years

## Gender Distribution"""

for gender, count in results['gender_analysis']['counts'].items():
    percentage = results['gender_analysis']['percentages'][gender]
    report += f"\n- Gender {gender}: {count:,} users ({percentage:.2f}%)"

report += "\n\n## Top 5 Regions by User Count"
for region, count in results['region_analysis']['top_5_regions'].items():
    percentage = results['region_analysis']['percentages'][region]
    report += f"\n- {region}: {count:,} users ({percentage:.2f}%)"

# Print both JSON results and formatted report
print("### JSON RESULTS ###")
print(json.dumps(results, indent=2))
print("\n### FORMATTED REPORT ###")
print(report)
