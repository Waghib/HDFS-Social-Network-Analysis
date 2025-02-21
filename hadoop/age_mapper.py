#!/usr/bin/env python3
"""
MapReduce implementation - Mapper
Normalize and standardize age feature, with clustering
Input: Tab-separated lines from Pokec profiles
Output: Key-value pairs for age statistics and clustering
"""

import sys
import json

def validate_age(age_str):
    """Validate and clean age value"""
    try:
        age = float(age_str)
        if 1 <= age <= 100:  # Valid age range
            return age
    except (ValueError, TypeError):
        pass
    return None

def main():
    # Process input lines from stdin
    for line in sys.stdin:
        try:
            # Split line into fields
            fields = line.strip().split('\t')
            
            if len(fields) >= 8:  # Ensure we have enough fields
                # Extract age (field 7)
                age = validate_age(fields[7])
                
                if age is not None:
                    # Emit for different computations
                    
                    # For basic statistics
                    print(f"stats\t{json.dumps({'age': age, 'count': 1})}")
                    
                    # For age value (used in normalization)
                    print(f"age_value\t{age}")
                    
                    # For squared differences (used in standardization)
                    print(f"age_squared\t{age * age}")
                    
                    # For clustering initialization
                    print(f"cluster_point\t{age}")
                    
        except Exception as e:
            sys.stderr.write(f"Error processing line: {str(e)}\n")
            continue

if __name__ == "__main__":
    main()
