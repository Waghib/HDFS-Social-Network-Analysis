#!/usr/bin/env python3
"""
Mapper for analyzing user features (age, gender, region)
Input format: tab-separated values where:
- column 0: user_id
- column 3: gender
- column 4: region
- column 7: age
"""
import sys

def is_valid_age(age):
    try:
        age = int(age)
        return 10 <= age <= 100
    except:
        return False

for line in sys.stdin:
    try:
        # Remove leading/trailing whitespace and split by tab
        fields = line.strip().split('\t')
        
        if len(fields) < 8:  # Ensure we have enough fields
            continue
            
        user_id = fields[0]
        gender = fields[3]
        region = fields[4]
        age = fields[7]
        
        # Emit for age analysis (if valid age)
        if is_valid_age(age):
            print(f"AGE\t{age}")
        
        # Emit for gender analysis
        if gender in ['0', '1']:
            print(f"GENDER\t{gender}")
        
        # Emit for region analysis (if region is not empty)
        if region and region != 'null':
            print(f"REGION\t{region}")
            
    except Exception as e:
        continue  # Skip malformed lines
