#!/usr/bin/env python3
"""
Mapper for outlier analysis and handling sparsity in the dataset
Input format: tab-separated values with user profile data
"""
import sys
import json

def clean_numeric(value):
    """Clean and validate numeric values"""
    try:
        value = float(value)
        if value != value:  # Check for NaN
            return None
        return value
    except:
        return None

def emit_numeric_stats(key, value):
    """Emit statistics for numeric fields"""
    if value is not None:
        print(f"NUMERIC\t{json.dumps({'field': key, 'value': value})}")

def emit_feature_stats(field_name, value):
    """Emit statistics for feature completeness"""
    print(f"FEATURE\t{json.dumps({'field': field_name, 'is_missing': value is None})}")

def process_age(age):
    """Process and validate age value"""
    age = clean_numeric(age)
    if age is not None and (age < 10 or age > 100):
        age = None
    return age

# Define column indices and names
COLUMNS = {
    'user_id': 0,
    'public': 1,
    'completion_percentage': 2,
    'gender': 3,
    'region': 4,
    'last_login': 5,
    'registration': 6,
    'AGE': 7,
    'body': 8,
    'I_am_working_in_field': 9,
    'spoken_languages': 10,
    'hobbies': 11,
    'I_most_enjoy_good_food': 12,
    'pets': 13,
    'body_type': 14,
    'my_eyesight': 15,
    'eye_color': 16,
    'hair_color': 17,
    'hair_type': 18,
    'completed_level_of_education': 19,
    'favourite_color': 20,
    'relation_to_smoking': 21,
    'relation_to_alcohol': 22,
    'sign_in_zodiac': 23,
    'on_pokec_for': 24,
    'love_is_for_me': 25,
    'relation_to_casual_sex': 26,
    'my_partner_should_be': 27,
    'marital_status': 28,
    'children': 29,
    'relation_to_children': 30
}

def main():
    for line in sys.stdin:
        try:
            fields = line.strip().split('\t')
            
            if len(fields) < max(COLUMNS.values()) + 1:
                continue
                
            # Process numeric fields
            age = process_age(fields[COLUMNS['AGE']])
            completion = clean_numeric(fields[COLUMNS['completion_percentage']])
            
            # Emit numeric statistics
            emit_numeric_stats('AGE', age)
            emit_numeric_stats('completion_percentage', completion)
            
            # Emit feature completeness statistics
            for field_name, index in COLUMNS.items():
                value = fields[index] if index < len(fields) else None
                emit_feature_stats(field_name, value)
                
        except Exception as e:
            continue

if __name__ == "__main__":
    main()
