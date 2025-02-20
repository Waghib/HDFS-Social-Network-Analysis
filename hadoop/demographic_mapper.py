#!/usr/bin/env python3
import sys
import os
import traceback

def map_demographics():
    try:
        # Debug information
        sys.stderr.write(f"Starting demographic mapper. Python version: {sys.version}\n")
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
                except IndexError:
                    sys.stderr.write(f"Missing required fields in line {line_count}\n")
                    error_count += 1
                    continue
                
                # Emit age groups
                if age and age.lower() != 'null':
                    try:
                        age_val = float(age)
                        if 0 <= age_val <= 100:
                            age_group = None
                            if age_val < 18:
                                age_group = '<18'
                            elif age_val < 25:
                                age_group = '18-24'
                            elif age_val < 35:
                                age_group = '25-34'
                            elif age_val < 50:
                                age_group = '35-49'
                            else:
                                age_group = '50+'
                            
                            if age_group:
                                sys.stdout.write(f'age_group\t{age_group}\t1\n')
                                sys.stdout.flush()
                    except ValueError:
                        sys.stderr.write(f"Invalid age value on line {line_count}: {age}\n")
                        error_count += 1
                
                # Emit gender counts (1 for woman, 0 for man)
                if gender in ['0', '1']:
                    gender_str = 'woman' if gender == '1' else 'man'
                    sys.stdout.write(f'gender\t{gender_str}\t1\n')
                    sys.stdout.flush()
                
                # Emit region counts
                if region and region.lower() != 'null':
                    sys.stdout.write(f'region\t{region}\t1\n')
                    sys.stdout.flush()
                
                # Emit profile visibility counts
                if public in ['0', '1']:
                    visibility = 'public' if public == '1' else 'private'
                    sys.stdout.write(f'visibility\t{visibility}\t1\n')
                    sys.stdout.flush()
                    
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
    map_demographics()
