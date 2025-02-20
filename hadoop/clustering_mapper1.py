#!/usr/bin/env python3
import sys
import os

def map_features():
    """Extract age and completion percentage features for clustering"""
    try:
        sys.stderr.write(f"Starting feature extraction mapper\n")
        
        for line in sys.stdin:
            try:
                fields = line.strip().split('\t')
                
                if len(fields) >= 5:
                    # Get age
                    try:
                        age = float(fields[2]) if fields[2] and fields[2].lower() != 'null' else None
                        
                        # Only process if age is valid
                        if age is not None and 0 <= age <= 100:
                            # Calculate completion percentage
                            total_fields = len(fields[5:])
                            non_null_fields = sum(1 for field in fields[5:] if field and field.lower() != 'null')
                            completion_percentage = (non_null_fields / total_fields * 100) if total_fields > 0 else 0
                            
                            # Emit user_id as key, age and completion as value
                            sys.stdout.write(f"{fields[0]}\t{age:.2f},{completion_percentage:.2f}\n")
                            sys.stdout.flush()
                            
                    except (ValueError, TypeError) as e:
                        sys.stderr.write(f"Error processing age: {e}\n")
                        continue
                        
            except Exception as e:
                sys.stderr.write(f"Error processing line: {str(e)}\n")
                continue
                
    except Exception as e:
        sys.stderr.write(f"Fatal error in mapper: {str(e)}\n")
        sys.exit(1)

if __name__ == '__main__':
    map_features()
