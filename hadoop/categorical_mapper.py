#!/usr/bin/env python3
"""
Mapper for categorical encoding.
Input: Tab-separated lines from Pokec profiles
Output: Key-value pairs for one-hot encoding
Format: category_name\tvalue\t1
"""

import sys

def clean_gender(value):
    """Clean and standardize gender values"""
    if not value or value == 'null':
        return 'unknown'
    value = str(value).lower().strip()
    return 'male' if value == '1' else 'female'

def clean_region(value):
    """Clean and standardize region values"""
    if not value or value == 'null':
        return 'unknown'
    return value.lower().strip()

def clean_eye_color(value):
    """Clean and standardize eye color values"""
    if not value or value == 'null':
        return 'unknown'
    
    value = str(value).lower().strip()
    color_map = {
        'zelene': 'green',
        'modre': 'blue',
        'hnede': 'brown',
        'cierne': 'black',
        'sive': 'grey'
    }
    
    for slovak, english in color_map.items():
        if slovak in value:
            return english
    return value

def main():
    # Read input lines from stdin
    for line in sys.stdin:
        try:
            # Split line into fields
            fields = line.strip().split('\t')
            
            # Extract relevant fields (gender, region, eye_color)
            # Fields are at positions 3, 4, and 16 respectively
            if len(fields) >= 17:
                gender = clean_gender(fields[3])
                region = clean_region(fields[4])
                eye_color = clean_eye_color(fields[16])
                
                # Emit key-value pairs for each category
                print(f"gender\t{gender}\t1")
                print(f"region\t{region}\t1")
                print(f"eye_color\t{eye_color}\t1")
        except Exception as e:
            sys.stderr.write(f"Error processing line: {str(e)}\n")
            continue

if __name__ == "__main__":
    main()
