#!/usr/bin/env python3
import sys
import os
import traceback
from collections import defaultdict

def reduce_demographics():
    try:
        # Debug information
        sys.stderr.write(f"Starting reducer with Python: {sys.executable}\n")
        sys.stderr.write(f"Current directory: {os.getcwd()}\n")
        sys.stderr.write(f"Files in current directory: {os.listdir('.')}\n")
        
        # Initialize counters for each category
        age_groups = defaultdict(int)
        genders = defaultdict(int)
        regions = defaultdict(int)
        visibilities = defaultdict(int)
        
        # Process input from mapper
        for line in sys.stdin:
            try:
                category, value, count = line.strip().split('\t')
                count = int(count)
                
                if category == 'age_group':
                    age_groups[value] += count
                elif category == 'gender':
                    genders[value] += count
                elif category == 'region':
                    regions[value] += count
                elif category == 'visibility':
                    visibilities[value] += count
                    
            except Exception as e:
                sys.stderr.write(f"Error processing line: {line.strip()} - {str(e)}\n")
                continue
        
        # Output age group statistics
        sys.stdout.write("\nAge Group Distribution:\n")
        total_age = sum(age_groups.values())
        for age_group in ['<18', '18-24', '25-34', '35-49', '50+']:
            count = age_groups[age_group]
            percentage = (count / total_age * 100) if total_age > 0 else 0
            sys.stdout.write(f"{age_group}: {count} ({percentage:.2f}%)\n")
        sys.stdout.flush()
        
        # Output gender statistics
        sys.stdout.write("\nGender Distribution:\n")
        total_gender = sum(genders.values())
        for gender in sorted(genders):
            count = genders[gender]
            percentage = (count / total_gender * 100) if total_gender > 0 else 0
            sys.stdout.write(f"{gender}: {count} ({percentage:.2f}%)\n")
        sys.stdout.flush()
        
        # Output profile visibility statistics
        sys.stdout.write("\nProfile Visibility:\n")
        total_visibility = sum(visibilities.values())
        for visibility in sorted(visibilities):
            count = visibilities[visibility]
            percentage = (count / total_visibility * 100) if total_visibility > 0 else 0
            sys.stdout.write(f"{visibility}: {count} ({percentage:.2f}%)\n")
        sys.stdout.flush()
        
        # Output top 10 regions
        sys.stdout.write("\nTop 10 Regions:\n")
        sorted_regions = sorted(regions.items(), key=lambda x: x[1], reverse=True)[:10]
        total_regions = sum(regions.values())
        for region, count in sorted_regions:
            percentage = (count / total_regions * 100) if total_regions > 0 else 0
            sys.stdout.write(f"{region}: {count} ({percentage:.2f}%)\n")
        sys.stdout.flush()
        
    except Exception as e:
        sys.stderr.write(f"Fatal error in reducer: {str(e)}\n")
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    reduce_demographics()
