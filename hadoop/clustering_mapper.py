#!/usr/bin/env python3
"""
Mapper for clustering analysis of user age and completion percentage
Input format: tab-separated values with user profile data
"""
import sys
import json

# Pre-defined cluster centers (based on previous analysis)
AGE_CLUSTERS = {
    0: 20.1,  # Young adults (17-23)
    1: 35.9,  # Middle-aged (32-42)
    2: 13.9,  # Teenagers (10-16)
    3: 49.6,  # Older adults (43+)
    4: 27.0   # Adults (24-31)
}

def clean_numeric(value):
    """Clean and validate numeric values"""
    try:
        value = float(value)
        if value != value:  # Check for NaN
            return None
        return value
    except:
        return None

def assign_cluster(age):
    """Assign a user to the nearest cluster based on age"""
    if age is None:
        return None
        
    min_dist = float('inf')
    nearest_cluster = None
    
    for cluster_id, center in AGE_CLUSTERS.items():
        dist = abs(age - center)
        if dist < min_dist:
            min_dist = dist
            nearest_cluster = cluster_id
            
    return nearest_cluster

def process_line(line):
    """Process a single line of input data"""
    try:
        fields = line.strip().split('\t')
        
        # Extract and clean age and completion percentage
        age = clean_numeric(fields[7])  # AGE column
        completion = clean_numeric(fields[2])  # completion_percentage column
        
        if age is not None and completion is not None:
            # Validate age range
            if 10 <= age <= 100:
                cluster = assign_cluster(age)
                if cluster is not None:
                    # Emit cluster statistics
                    print(f"CLUSTER\t{json.dumps({
                        'cluster': cluster,
                        'age': age,
                        'completion': completion
                    })}")
                    
                # Emit overall age statistics for verification
                print(f"AGE_STATS\t{json.dumps({
                    'age': age,
                    'completion': completion
                })}")
                
    except Exception as e:
        return  # Skip malformed lines

def main():
    for line in sys.stdin:
        process_line(line)

if __name__ == "__main__":
    main()
