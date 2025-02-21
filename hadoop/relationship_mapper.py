#!/usr/bin/env python3
"""
Mapper for analyzing relationships between completion_percentage and categorical variables
Input format: tab-separated values where columns contain user profile data
"""
import sys
import json

def clean_value(value):
    """Clean and validate a value"""
    if not value or value == 'null' or value.strip() == '':
        return None
    return value.strip()

def emit_feature(feature_name, feature_value, completion_percentage):
    """Emit a feature-value pair with completion percentage"""
    if feature_value is not None:
        print(f"FEATURE\t{json.dumps({'name': feature_name, 'value': feature_value, 'completion': float(completion_percentage)})}")

def emit_correlation(value1, value2):
    """Emit values for correlation calculation"""
    try:
        v1, v2 = float(value1), float(value2)
        print(f"CORRELATION\t{json.dumps({'x': v1, 'y': v2})}")
    except:
        pass

# Define feature columns and their indices
FEATURES = {
    'eye_color': 20,
    'hair_color': 21,
    'hair_type': 22,
    'body_type': 23,
    'relation_to_smoking': 26,
    'relation_to_alcohol': 27,
    'sign_in_zodiac': 28,
    'marital_status': 33
}

for line in sys.stdin:
    try:
        # Remove leading/trailing whitespace and split by tab
        fields = line.strip().split('\t')
        
        if len(fields) < max(FEATURES.values()) + 1:
            continue
            
        # Get completion percentage
        completion_percentage = clean_value(fields[2])
        if completion_percentage is None:
            continue
            
        # Emit user_id correlation data
        emit_correlation(fields[0], completion_percentage)
        
        # Process each categorical feature
        for feature_name, index in FEATURES.items():
            feature_value = clean_value(fields[index])
            emit_feature(feature_name, feature_value, completion_percentage)
            
    except Exception as e:
        continue  # Skip malformed lines
