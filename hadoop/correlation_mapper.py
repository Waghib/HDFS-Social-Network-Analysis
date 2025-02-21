#!/usr/bin/env python3
"""
Mapper for analyzing correlations between completion_percentage and other features
Input format: tab-separated values where:
- column 0: user_id
- column 1: public
- column 2: completion_percentage
- column 3: gender
- column 7: age
"""
import sys
import json

def is_valid_age(age):
    """Validate age is within reasonable range"""
    try:
        age = int(age)
        return 10 <= age <= 100
    except:
        return False

def get_age_group(age):
    """Convert age to age group"""
    try:
        age = int(age)
        if age <= 20:
            return '<20'
        elif age <= 30:
            return '20-30'
        elif age <= 40:
            return '30-40'
        elif age <= 50:
            return '40-50'
        else:
            return '>50'
    except:
        return None

for line in sys.stdin:
    try:
        # Remove leading/trailing whitespace and split by tab
        fields = line.strip().split('\t')
        
        if len(fields) < 8:  # Ensure we have enough fields
            continue
            
        user_id = fields[0]
        public = fields[1]
        completion_percentage = fields[2]
        gender = fields[3]
        age = fields[7]
        
        # Convert to numeric values
        try:
            completion_percentage = float(completion_percentage)
            public = int(public)
            gender = float(gender)
        except:
            continue
            
        # Emit data for overall completion percentage statistics
        print(f"COMPLETION_STATS\t{completion_percentage}")
        
        # Emit data for correlation analysis
        if public in [0, 1]:
            print(f"CORRELATION\tpublic\t{public}\t{completion_percentage}")
            
        if gender in [0, 1]:
            print(f"CORRELATION\tgender\t{gender}\t{completion_percentage}")
            
        if is_valid_age(age):
            age_val = int(age)
            print(f"CORRELATION\tage\t{age_val}\t{completion_percentage}")
            
            # Emit data for age group analysis
            age_group = get_age_group(age_val)
            if age_group:
                print(f"AGE_GROUP\t{age_group}\t{completion_percentage}")
        
        # Emit data for gender-specific analysis
        if gender in [0, 1]:
            print(f"GENDER_COMPLETION\t{gender}\t{completion_percentage}")
            
    except Exception as e:
        continue  # Skip malformed lines
