#!/usr/bin/env python3
import sys
from collections import defaultdict
import math

def calculate_correlation(x_values, y_values):
    n = len(x_values)
    if n < 2:
        return 0
    
    # Calculate means
    x_mean = sum(x_values) / n
    y_mean = sum(y_values) / n
    
    # Calculate correlation coefficient
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
    denominator = math.sqrt(sum((x - x_mean) ** 2 for x in x_values) * 
                          sum((y - y_mean) ** 2 for y in y_values))
    
    if denominator == 0:
        return 0
    return numerator / denominator

def reduce_correlations():
    current_type = None
    current_key = None
    
    # Store values for correlation calculation
    x_values = []
    y_values = []
    
    # Store category statistics
    category_stats = defaultdict(lambda: {'sum': 0, 'count': 0})
    
    for line in sys.stdin:
        try:
            # Parse input
            analysis_type, key, value = line.strip().split('\t')
            value = float(value)
            
            # If we're starting a new type or key
            if current_type != analysis_type or (current_type == analysis_type and current_key != key):
                if current_type == 'age_corr' and x_values:
                    # Calculate and output correlation for age
                    correlation = calculate_correlation(x_values, y_values)
                    print(f'correlation\tage\t{correlation}')
                    x_values = []
                    y_values = []
                elif current_type in ['gender_comp', 'region_comp'] and current_key:
                    # Output average completion rate for category
                    stats = category_stats[current_key]
                    if stats['count'] > 0:
                        avg_completion = stats['sum'] / stats['count']
                        print(f'{current_type}_avg\t{current_key}\t{avg_completion}')
                
                current_type = analysis_type
                current_key = key
                category_stats.clear()
            
            # Update statistics
            if analysis_type == 'age_corr':
                x_values.append(float(key))
                y_values.append(value)
            elif analysis_type in ['gender_comp', 'region_comp']:
                category_stats[key]['sum'] += value
                category_stats[key]['count'] += 1
                
        except Exception as e:
            continue
    
    # Output final results
    if current_type == 'age_corr' and x_values:
        correlation = calculate_correlation(x_values, y_values)
        print(f'correlation\tage\t{correlation}')
    elif current_type in ['gender_comp', 'region_comp'] and current_key:
        stats = category_stats[current_key]
        if stats['count'] > 0:
            avg_completion = stats['sum'] / stats['count']
            print(f'{current_type}_avg\t{current_key}\t{avg_completion}')

if __name__ == '__main__':
    reduce_correlations()
