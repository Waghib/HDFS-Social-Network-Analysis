#!/usr/bin/env python3
"""
Calculate days_since_registration from registration and last_login dates.
Final version with correct column indices and datetime parsing.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

def parse_date(date_str):
    """Parse date string to datetime object"""
    try:
        if pd.isna(date_str) or date_str == 'null':
            return None
        # Parse datetime string
        return datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S.%f')
    except Exception:
        try:
            # Try without milliseconds
            return datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S')
        except Exception:
            return None

def calculate_days_between(row):
    """Calculate days between registration and last login"""
    try:
        reg_date = parse_date(row['registration'])
        login_date = parse_date(row['last_login'])
        
        if reg_date is None or login_date is None:
            return np.nan
            
        # Calculate difference in days
        days = (login_date - reg_date).days
        
        # Validate the difference makes sense
        if days < 0:
            return np.nan  # Invalid if registration is after last login
        return days
        
    except Exception as e:
        print(f"Error calculating days: {e}")
        return np.nan

def get_duration_category(days):
    """Get duration category for given days"""
    if pd.isna(days):
        return 'Invalid/Missing'
    elif days <= 30:
        return '1 month'
    elif days <= 90:
        return '3 months'
    elif days <= 180:
        return '6 months'
    elif days <= 365:
        return '1 year'
    elif days <= 730:
        return '2 years'
    else:
        return '2+ years'

def main():
    print("Loading data...")
    
    # Create necessary directories
    Path("data").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    
    # Read only required columns (5=last_login, 6=registration)
    df = pd.read_csv('data/soc-pokec-profiles.txt', 
                     sep='\t',
                     names=range(60),
                     usecols=[5, 6],
                     nrows=10000)
    
    # Rename columns
    df.columns = ['last_login', 'registration']
    
    print("\nSample of raw data:")
    print(df.head().to_string())
    
    print("\nCalculating days since registration...")
    
    # Calculate days between registration and last login
    df['days_since_registration'] = df.apply(calculate_days_between, axis=1)
    
    # Add duration category
    df['duration_category'] = df['days_since_registration'].apply(get_duration_category)
    
    # Generate statistics
    valid_days = df['days_since_registration'].dropna()
    stats = {
        'total_profiles': len(df),
        'profiles_with_valid_dates': len(valid_days),
        'min_days': valid_days.min() if len(valid_days) > 0 else None,
        'max_days': valid_days.max() if len(valid_days) > 0 else None,
        'avg_days': valid_days.mean() if len(valid_days) > 0 else None,
        'median_days': valid_days.median() if len(valid_days) > 0 else None
    }
    
    # Calculate distribution
    duration_dist = df['duration_category'].value_counts().sort_index()
    
    # Generate report
    report = ["Registration Duration Analysis",
             "============================\n",
             "Summary Statistics:",
             f"Total profiles analyzed: {stats['total_profiles']:,}",
             f"Profiles with valid dates: {stats['profiles_with_valid_dates']:,}",
             f"Invalid/missing dates: {stats['total_profiles'] - stats['profiles_with_valid_dates']:,}\n"]
    
    if stats['profiles_with_valid_dates'] > 0:
        report.extend([
            "Duration Metrics:",
            f"Minimum days: {stats['min_days']:.0f}",
            f"Maximum days: {stats['max_days']:.0f}",
            f"Average days: {stats['avg_days']:.0f}",
            f"Median days: {stats['median_days']:.0f}\n",
            "Distribution:",
            "-------------"
        ])
        
        # Add distribution data
        for category, count in duration_dist.items():
            percentage = (count / stats['total_profiles']) * 100
            report.append(f"{category}: {count:,} profiles ({percentage:.1f}%)")
    else:
        report.append("\nNo valid registration durations found in the data.")
    
    # Save results
    print("\nSaving results...")
    
    # Save processed data
    df.to_parquet('data/registration_duration.parquet')
    
    # Save report
    with open('reports/registration_analysis.txt', 'w') as f:
        f.write('\n'.join(report))
    
    print("\nResults saved to:")
    print("- data/registration_duration.parquet")
    print("- reports/registration_analysis.txt")
    
    # Print sample
    print("\nSample of processed data (first 5 rows):")
    print(df.head().to_string())
    
    # Print distribution summary
    print("\nDuration Distribution:")
    print(duration_dist.to_string())

if __name__ == "__main__":
    main()
