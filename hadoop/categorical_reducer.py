#!/usr/bin/env python3
"""
Reducer for categorical encoding.
Input: Key-value pairs from mapper (category_name\tvalue\t1)
Output: One-hot encoded counts for each category
"""

import sys
from collections import defaultdict
import json

def main():
    current_category = None
    category_counts = defaultdict(int)
    category_values = defaultdict(set)
    
    # Read input key-value pairs from stdin
    for line in sys.stdin:
        try:
            # Parse input
            category, value, count = line.strip().split('\t')
            count = int(count)
            
            # If we encounter a new category, output the previous category's counts
            if current_category and current_category != category:
                # Output one-hot encoded counts for the previous category
                output = {
                    'category': current_category,
                    'total_records': sum(category_counts.values()),
                    'unique_values': len(category_counts),
                    'value_counts': dict(category_counts)
                }
                print(json.dumps(output))
                
                # Reset counts for new category
                category_counts = defaultdict(int)
            
            # Update current category and counts
            current_category = category
            category_counts[value] += count
            category_values[category].add(value)
            
        except Exception as e:
            sys.stderr.write(f"Error processing line: {str(e)}\n")
            continue
    
    # Output the last category
    if current_category:
        output = {
            'category': current_category,
            'total_records': sum(category_counts.values()),
            'unique_values': len(category_counts),
            'value_counts': dict(category_counts)
        }
        print(json.dumps(output))
    
    # Output summary statistics
    summary = {
        'categories': list(category_values.keys()),
        'unique_values_per_category': {
            cat: len(values) for cat, values in category_values.items()
        }
    }
    print("SUMMARY: " + json.dumps(summary))
