#!/usr/bin/env python3
import sys

def map_demographics():
    line_count = 0
    for line in sys.stdin:
        try:
            line_count += 1
            # Print debug info
            if line_count <= 5:
                print(f'Processing line {line_count}: {line[:50]}...', file=sys.stderr)
            
            # Split the line by tabs
            fields = line.strip().split('\t')
            
            # Print field count for first few lines
            if line_count <= 5:
                print(f'Found {len(fields)} fields', file=sys.stderr)
            
            if len(fields) < 3:  # We need at least user_id, gender, and age
                print(f'Skipping line {line_count}: insufficient fields', file=sys.stderr)
                continue
                
            # Extract key demographics
            user_id = fields[0]
            gender = fields[1]
            age = fields[2]
            region = fields[4] if len(fields) > 4 else None
            
            # Calculate completion percentage
            non_null_count = sum(1 for f in fields if f and f.lower() != 'null')
            completion_percentage = (non_null_count / len(fields)) * 100
            
            # Age analysis
            if age and age.lower() != 'null':
                print(f'age\t{age}\t1')
                if line_count <= 5:
                    print(f'Emitted age: {age}', file=sys.stderr)
            
            # Gender analysis
            if gender and gender.lower() != 'null':
                print(f'gender\t{gender}\t1')
                if line_count <= 5:
                    print(f'Emitted gender: {gender}', file=sys.stderr)
            
            # Region analysis
            if region and region.lower() != 'null':
                print(f'region\t{region}\t1')
                if line_count <= 5:
                    print(f'Emitted region: {region}', file=sys.stderr)
            
            # Completion rate analysis
            print(f'completion\t{int(completion_percentage)}\t1')
            if line_count <= 5:
                print(f'Emitted completion: {int(completion_percentage)}', file=sys.stderr)
            
        except Exception as e:
            print(f'Error processing line {line_count}: {str(e)}', file=sys.stderr)
            continue

if __name__ == '__main__':
    map_demographics()
