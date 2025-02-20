#!/usr/bin/env python3
import sys
import os
import traceback
from collections import defaultdict

def calculate_correlation(values_x, values_y):
    """Calculate Pearson correlation coefficient between two lists of values"""
    n = len(values_x)
    if n < 2:
        return None
    
    mean_x = sum(values_x) / n
    mean_y = sum(values_y) / n
    
    covariance = sum((x - mean_x) * (y - mean_y) for x, y in zip(values_x, values_y))
    variance_x = sum((x - mean_x) ** 2 for x in values_x)
    variance_y = sum((y - mean_y) ** 2 for y in values_y)
    
    if variance_x == 0 or variance_y == 0:
        return None
    
    correlation = covariance / (variance_x ** 0.5 * variance_y ** 0.5)
    return correlation

def reduce_correlations():
    try:
        # Debug information
        sys.stderr.write(f"Starting reducer with Python: {sys.executable}\n")
        sys.stderr.write(f"Current directory: {os.getcwd()}\n")
        sys.stderr.write(f"Files in current directory: {os.listdir('.')}\n")
        
        # Store values for each category
        age_values = []
        age_completions = []
        gender_data = defaultdict(list)  # gender -> [completion percentages]
        visibility_data = defaultdict(list)  # visibility -> [completion percentages]
        
        # Process input from mapper
        for line in sys.stdin:
            try:
                category, value, completion = line.strip().split('\t')
                completion = float(completion)
                
                if category == 'age':
                    age = float(value)
                    age_values.append(age)
                    age_completions.append(completion)
                elif category == 'gender':
                    gender_data[value].append(completion)
                elif category == 'visibility':
                    visibility_data[value].append(completion)
                    
            except Exception as e:
                sys.stderr.write(f"Error processing line: {line.strip()} - {str(e)}\n")
                continue
        
        # Calculate and output age correlation
        age_correlation = calculate_correlation(age_values, age_completions)
        sys.stdout.write("\nAge vs Profile Completion Correlation:\n")
        if age_correlation is not None:
            sys.stdout.write(f"Pearson correlation coefficient: {age_correlation:.4f}\n")
        else:
            sys.stdout.write("Insufficient data for correlation calculation\n")
        sys.stdout.flush()
        
        # Calculate and output gender statistics
        sys.stdout.write("\nGender vs Profile Completion:\n")
        for gender in sorted(gender_data):
            completions = gender_data[gender]
            avg_completion = sum(completions) / len(completions) if completions else 0
            sys.stdout.write(f"{gender}: Average completion = {avg_completion:.2f}% (n={len(completions)})\n")
        sys.stdout.flush()
        
        # Calculate and output visibility statistics
        sys.stdout.write("\nProfile Visibility vs Completion:\n")
        for visibility in sorted(visibility_data):
            completions = visibility_data[visibility]
            avg_completion = sum(completions) / len(completions) if completions else 0
            sys.stdout.write(f"{visibility}: Average completion = {avg_completion:.2f}% (n={len(completions)})\n")
        sys.stdout.flush()
        
    except Exception as e:
        sys.stderr.write(f"Fatal error in reducer: {str(e)}\n")
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    reduce_correlations()
