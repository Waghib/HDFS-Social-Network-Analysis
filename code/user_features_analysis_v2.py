import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Set style for better visualizations
sns.set_style("whitegrid")
sns.set_palette("husl")

# Create directories for outputs
Path("reports/figures").mkdir(parents=True, exist_ok=True)

def load_data():
    """Load and preprocess the data"""
    print("Loading data...")
    # Read only the columns we need (columns 0, 3, 4, 7 contain user_id, gender, region, age)
    df = pd.read_csv('data/soc-pokec-profiles.txt', 
                     sep='\t', 
                     usecols=[0, 3, 4, 7], 
                     names=['user_id', 'gender', 'region', 'AGE'])
    
    # Basic data cleaning
    df['AGE'] = pd.to_numeric(df['AGE'], errors='coerce')
    
    return df

def analyze_age(df):
    """Analyze age distribution"""
    print("Analyzing age distribution...")
    plt.figure(figsize=(12, 6))
    
    # Filter valid ages (e.g., between 10 and 100)
    valid_age = df[(df['AGE'] >= 10) & (df['AGE'] <= 100)]['AGE']
    
    sns.histplot(data=valid_age, bins=30)
    plt.title('Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Count')
    plt.savefig('reports/figures/age_distribution.png')
    plt.close()
    
    # Calculate age statistics
    age_stats = {
        'mean_age': valid_age.mean(),
        'median_age': valid_age.median(),
        'min_age': valid_age.min(),
        'max_age': valid_age.max(),
        'total_valid_users': len(valid_age)
    }
    return age_stats

def analyze_gender(df):
    """Analyze gender distribution"""
    print("Analyzing gender distribution...")
    plt.figure(figsize=(8, 6))
    
    gender_counts = df['gender'].value_counts()
    gender_counts.plot(kind='bar')
    plt.title('Gender Distribution')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.savefig('reports/figures/gender_distribution.png')
    plt.close()
    
    # Calculate percentages
    gender_percentages = (gender_counts / len(df) * 100).round(2)
    return dict(gender_counts), dict(gender_percentages)

def analyze_region(df):
    """Analyze regional distribution"""
    print("Analyzing regional distribution...")
    plt.figure(figsize=(15, 6))
    
    # Get top 20 regions
    region_counts = df['region'].value_counts().head(20)
    region_counts.plot(kind='bar')
    plt.title('Top 20 Regions Distribution')
    plt.xlabel('Region')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('reports/figures/region_distribution.png')
    plt.close()
    
    # Calculate percentages for top 5 regions
    top_5_regions = df['region'].value_counts().head()
    top_5_percentages = (top_5_regions / len(df) * 100).round(2)
    return dict(top_5_regions), dict(top_5_percentages)

def generate_report(age_stats, gender_counts, gender_percentages, region_counts, region_percentages):
    """Generate a markdown report with the analysis results"""
    print("Generating report...")
    report = f"""# User Features Analysis Report

## Dataset Overview
Total number of users with valid age data: {age_stats['total_valid_users']:,}

## Age Analysis
- Mean Age: {age_stats['mean_age']:.2f} years
- Median Age: {age_stats['median_age']:.2f} years
- Age Range: {age_stats['min_age']:.0f} - {age_stats['max_age']:.0f} years

## Gender Distribution
"""
    for gender, count in gender_counts.items():
        percentage = gender_percentages[gender]
        report += f"- Gender {gender}: {count:,} users ({percentage:.2f}%)\n"
    
    report += "\n## Top 5 Regions by User Count\n"
    for region, count in region_counts.items():
        percentage = region_percentages[region]
        report += f"- {region}: {count:,} users ({percentage:.2f}%)\n"
    
    report += "\n## Visualizations\n"
    report += "The following visualizations have been generated in the reports/figures directory:\n"
    report += "1. Age Distribution (age_distribution.png)\n"
    report += "2. Gender Distribution (gender_distribution.png)\n"
    report += "3. Region Distribution (region_distribution.png)\n"
    
    with open('reports/user_features_analysis.md', 'w') as f:
        f.write(report)

def main():
    print("Starting user features analysis...")
    
    # Load and preprocess data
    df = load_data()
    
    # Perform analysis
    age_stats = analyze_age(df)
    gender_counts, gender_percentages = analyze_gender(df)
    region_counts, region_percentages = analyze_region(df)
    
    # Generate report
    generate_report(age_stats, gender_counts, gender_percentages, region_counts, region_percentages)
    
    print("Analysis complete! Check reports/user_features_analysis.md for results.")

if __name__ == "__main__":
    main()
