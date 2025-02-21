#!/usr/bin/env python3
"""
MapReduce implementation - Mapper
Calculate days_since_registration from registration and last_login dates
Input: Tab-separated lines from Pokec profiles
Output: Key-value pairs for duration analysis
"""

import sys
from datetime import datetime

def parse_date(date_str):
    """Parse date string to datetime object"""
    try:
        if not date_str or date_str == 'null':
            return None
        # Try parsing with milliseconds
        try:
            return datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            # Try without milliseconds
            return datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S')
    except Exception:
        return None

def get_duration_category(days):
    """Get duration category for given days"""
    if days <= 30:
        return '1_month'
    elif days <= 90:
        return '3_months'
    elif days <= 180:
        return '6_months'
    elif days <= 365:
        return '1_year'
    elif days <= 730:
        return '2_years'
    else:
        return '2+_years'

def main():
    # Process input lines from stdin
    for line in sys.stdin:
        try:
            # Split line into fields
            fields = line.strip().split('\t')
            
            if len(fields) >= 7:  # Ensure we have enough fields
                # Extract registration (field 6) and last_login (field 5)
                last_login_str = fields[5]
                reg_str = fields[6]
                
                # Parse dates
                last_login = parse_date(last_login_str)
                reg_date = parse_date(reg_str)
                
                if last_login and reg_date:
                    # Calculate days
                    days = (last_login - reg_date).days
                    
                    if days >= 0:  # Valid only if registration is before last login
                        # Get duration category
                        category = get_duration_category(days)
                        
                        # Emit multiple key-value pairs for different analyses
                        # Format: key\tvalue
                        
                        # For category counts
                        print(f"category\t{category}")
                        
                        # For general statistics
                        print(f"stats\t{days}")
                        
                        # For detailed day counts (for percentiles)
                        print(f"days\t{days}")
                        
        except Exception as e:
            sys.stderr.write(f"Error processing line: {str(e)}\n")
            continue

if __name__ == "__main__":
    main()
