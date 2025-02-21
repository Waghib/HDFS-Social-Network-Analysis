#!/usr/bin/env python3
"""
Random Forest Analysis - Mapper
Input: Tab-separated lines from Pokec profiles
Output: Key-value pairs for feature extraction and analysis
"""

import sys
import json

def validate_numeric(value):
    """Validate and convert numeric values"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def process_line(line):
    """Process a single line of input"""
    try:
        fields = line.strip().split('\t')
        
        if len(fields) < 12:  # Ensure minimum required fields
            return None
            
        # Extract features
        features = {
            'public': fields[3],  # Target variable
            'age': validate_numeric(fields[7]),
            'completion_percentage': validate_numeric(fields[9]),
            'has_languages': 1 if fields[10].strip() else 0,
            'has_hobbies': 1 if fields[11].strip() else 0
        }
        
        # Basic validation
        if features['age'] is None or features['completion_percentage'] is None:
            return None
            
        if not (1 <= features['age'] <= 100):  # Valid age range
            return None
            
        return features
        
    except Exception as e:
        sys.stderr.write(f"Error processing line: {str(e)}\n")
        return None

def main():
    # Process input lines from stdin
    for line in sys.stdin:
        features = process_line(line)
        
        if features:
            # Emit for feature statistics (used in normalization)
            print(f"stats\t{json.dumps(features)}")
            
            # Emit for model training
            print(f"data\t{json.dumps(features)}")

if __name__ == "__main__":
    main()
