#!/usr/bin/env python3
import sys
from collections import defaultdict
import json

def reduce_demographics():
    # Counters for categorical values
    gender_counts = defaultdict(int)
    region_counts = defaultdict(int)
    
    # Statistics for numerical values
    age_values = []
    completion_values = []
    
    # Process input
    for line in sys.stdin:
        try:
            # Parse input
            analysis_type, key, value = line.strip().split('\t')
            
            if analysis_type == 'gender':
                # Convert gender codes to readable format
                gender_key = 'Male' if key == '1' else 'Female' if key == '2' else f'Other ({key})'
                gender_counts[gender_key] += 1
            elif analysis_type == 'region':
                region_counts[key] += 1
            elif analysis_type == 'age':
                age_values.append(int(key))
            elif analysis_type == 'completion':
                completion_values.append(int(key))
        
        except Exception as e:
            print(f'Error processing line: {str(e)}', file=sys.stderr)
            continue
    
    # Calculate and output statistics
    results = {
        'gender_distribution': dict(gender_counts),
        'region_distribution': dict(sorted(region_counts.items(), key=lambda x: x[1], reverse=True)[:20]),  # Top 20 regions
        'age_statistics': calculate_stats(age_values),
        'completion_statistics': calculate_stats(completion_values)
    }
    
    # Add total counts
    results['summary'] = {
        'total_users': len(age_values),
        'total_regions': len(region_counts),
        'gender_ratio': {
            'male_percentage': (gender_counts['Male'] / sum(gender_counts.values()) * 100) if gender_counts else 0,
            'female_percentage': (gender_counts['Female'] / sum(gender_counts.values()) * 100) if gender_counts else 0
        }
    }
    
    # Output results as JSON
    print(json.dumps(results, indent=2))

def calculate_stats(values):
    if not values:
        return None
    
    n = len(values)
    mean = sum(values) / n
    sorted_values = sorted(values)
    
    return {
        'count': n,
        'mean': round(mean, 2),
        'median': sorted_values[n//2],
        'min': min(values),
        'max': max(values),
        'quartiles': {
            'q1': sorted_values[n//4],
            'q2': sorted_values[n//2],
            'q3': sorted_values[3*n//4]
        }
    }

if __name__ == '__main__':
    reduce_demographics()
