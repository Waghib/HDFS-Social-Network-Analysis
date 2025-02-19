#!/usr/bin/env python3
import sys

def map_correlations():
    for line in sys.stdin:
        try:
            # Split the line by tabs
            fields = line.strip().split('\t')
            if len(fields) < 60:
                continue
            
            # Calculate completion percentage
            non_null_count = sum(1 for f in fields if f and f.lower() != 'null')
            completion_percentage = (non_null_count / len(fields)) * 100
            
            # Extract features
            age = fields[2]
            gender = fields[1]
            region = fields[4]
            
            # Emit age correlation data
            if age and age.lower() != 'null':
                try:
                    age_val = float(age)
                    print(f'age_corr\t{age_val}\t{completion_percentage}')
                except ValueError:
                    pass
            
            # Emit categorical correlations
            if gender and gender.lower() != 'null':
                print(f'gender_comp\t{gender}\t{completion_percentage}')
            
            if region and region.lower() != 'null':
                print(f'region_comp\t{region}\t{completion_percentage}')
            
        except Exception as e:
            continue

if __name__ == '__main__':
    map_correlations()
