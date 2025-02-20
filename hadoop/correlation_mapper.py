#!/usr/bin/env python3
import sys
import os
import traceback

def calculate_completion_percentage(fields):
    """Calculate the profile completion percentage based on non-null fields"""
    total_fields = len(fields[5:])  # Exclude the first 5 fields (id, gender, age, public, region)
    if total_fields == 0:
        return 0
    
    non_null_fields = sum(1 for field in fields[5:] if field and field.lower() != 'null')
    return (non_null_fields / total_fields) * 100

def map_correlations():
    try:
        # Debug information
        sys.stderr.write(f"Starting correlation mapper. Python version: {sys.version}\n")
        sys.stderr.write(f"Current directory: {os.getcwd()}\n")
        sys.stderr.write(f"Files in current directory: {os.listdir('.')}\n")
        
        line_count = 0
        error_count = 0
        
        for line in sys.stdin:
            try:
                line_count += 1
                if line_count % 1000 == 0:
                    sys.stderr.write(f"Processed {line_count} lines, {error_count} errors\n")
                    sys.stderr.flush()
                
                # Split the line by tabs
                fields = line.strip().split('\t')
                
                # Debug first few lines
                if line_count <= 5:
                    sys.stderr.write(f"Line {line_count} fields: {fields[:5]}\n")
                
                if len(fields) < 5:  # We need at least user_id, gender, age, public, and region
                    sys.stderr.write(f"Line {line_count} has insufficient fields: {len(fields)}\n")
                    error_count += 1
                    continue
                
                try:
                    user_id = fields[0]
                    gender = fields[1]  # 1 for woman, 0 for man
                    age = fields[2]
                    public = fields[3]  # 1 for public profile
                    region = fields[4]
                    
                    completion_percentage = calculate_completion_percentage(fields)
                    
                    # Emit age vs completion percentage
                    if age and age.lower() != 'null':
                        try:
                            age_val = float(age)
                            sys.stdout.write(f'age\t{age_val}\t{completion_percentage}\n')
                            sys.stdout.flush()
                        except ValueError:
                            sys.stderr.write(f"Invalid age value on line {line_count}: {age}\n")
                    
                    # Emit gender vs completion percentage
                    if gender in ['0', '1']:
                        gender_str = 'woman' if gender == '1' else 'man'
                        sys.stdout.write(f'gender\t{gender_str}\t{completion_percentage}\n')
                        sys.stdout.flush()
                    
                    # Emit profile visibility vs completion percentage
                    if public in ['0', '1']:
                        visibility = 'public' if public == '1' else 'private'
                        sys.stdout.write(f'visibility\t{visibility}\t{completion_percentage}\n')
                        sys.stdout.flush()
                        
                except IndexError:
                    sys.stderr.write(f"Missing required fields in line {line_count}\n")
                    error_count += 1
                    continue
                    
            except Exception as e:
                error_count += 1
                sys.stderr.write(f"Error processing line {line_count}: {str(e)}\n")
                traceback.print_exc(file=sys.stderr)
                continue
                
        sys.stderr.write(f"Finished processing {line_count} lines with {error_count} errors\n")
        
    except Exception as e:
        sys.stderr.write(f"Fatal error in mapper: {str(e)}\n")
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    map_correlations()
