#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Create directories for outputs
Path("reports/figures").mkdir(parents=True, exist_ok=True)

def load_data():
    """Load and preprocess the data"""
    print("Loading data...")
    # Read relevant columns for correlation analysis
    columns = [
        'user_id', 'public', 'completion_percentage', 'gender', 
        'AGE', 'last_login', 'registration'
    ]
    
    # Read the first few lines to get column positions
    df = pd.read_csv('data/soc-pokec-profiles.txt', 
                     sep='\t',
                     usecols=[0, 1, 2, 3, 7],  # Adjust indices based on actual positions
                     names=['user_id', 'public', 'completion_percentage', 'gender', 'AGE'])
    
    # Convert data types
    df['completion_percentage'] = pd.to_numeric(df['completion_percentage'], errors='coerce')
    df['AGE'] = pd.to_numeric(df['AGE'], errors='coerce')
    df['public'] = pd.to_numeric(df['public'], errors='coerce')
    df['gender'] = pd.to_numeric(df['gender'], errors='coerce')
    
    return df

def analyze_completion_percentage(df):
    """Basic analysis of completion percentage"""
    stats = {
        'mean': df['completion_percentage'].mean(),
        'median': df['completion_percentage'].median(),
        'std': df['completion_percentage'].std(),
        'min': df['completion_percentage'].min(),
        'max': df['completion_percentage'].max()
    }
    
    # Create distribution plot
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='completion_percentage', bins=50)
    plt.title('Distribution of Profile Completion Percentage')
    plt.xlabel('Completion Percentage')
    plt.ylabel('Count')
    plt.savefig('reports/figures/completion_percentage_distribution.png')
    plt.close()
    
    return stats

def analyze_correlations(df):
    """Analyze correlations between completion_percentage and other features"""
    # Calculate correlations
    correlations = df.corr()['completion_percentage'].sort_values(ascending=False)
    
    # Create correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig('reports/figures/correlation_heatmap.png')
    plt.close()
    
    return correlations

def analyze_completion_by_gender(df):
    """Analyze completion percentage by gender"""
    gender_stats = df.groupby('gender')['completion_percentage'].agg(['mean', 'median', 'count']).round(2)
    
    # Create box plot
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x='gender', y='completion_percentage')
    plt.title('Profile Completion Percentage by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Completion Percentage')
    plt.savefig('reports/figures/completion_by_gender.png')
    plt.close()
    
    return gender_stats

def analyze_completion_by_age(df):
    """Analyze completion percentage by age groups"""
    # Create age groups
    df['age_group'] = pd.cut(df['AGE'], 
                            bins=[0, 20, 30, 40, 50, 100],
                            labels=['<20', '20-30', '30-40', '40-50', '>50'])
    
    age_stats = df.groupby('age_group')['completion_percentage'].agg(['mean', 'median', 'count']).round(2)
    
    # Create box plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='age_group', y='completion_percentage')
    plt.title('Profile Completion Percentage by Age Group')
    plt.xlabel('Age Group')
    plt.ylabel('Completion Percentage')
    plt.savefig('reports/figures/completion_by_age.png')
    plt.close()
    
    return age_stats

def generate_report(completion_stats, correlations, gender_stats, age_stats):
    """Generate a report with the analysis results"""
    report = """# Profile Completion Correlation Analysis Report

## Overall Completion Percentage Statistics
"""
    report += f"- Mean: {completion_stats['mean']:.2f}%\n"
    report += f"- Median: {completion_stats['median']:.2f}%\n"
    report += f"- Standard Deviation: {completion_stats['std']:.2f}%\n"
    report += f"- Range: {completion_stats['min']:.2f}% - {completion_stats['max']:.2f}%\n"

    report += "\n## Correlations with Completion Percentage\n"
    for feature, corr in correlations.items():
        if feature != 'completion_percentage':
            report += f"- {feature}: {corr:.3f}\n"

    report += "\n## Completion Percentage by Gender\n"
    for gender, stats in gender_stats.iterrows():
        report += f"- Gender {gender}:\n"
        report += f"  - Mean: {stats['mean']:.2f}%\n"
        report += f"  - Median: {stats['median']:.2f}%\n"
        report += f"  - Count: {stats['count']:,}\n"

    report += "\n## Completion Percentage by Age Group\n"
    for age_group, stats in age_stats.iterrows():
        report += f"- Age {age_group}:\n"
        report += f"  - Mean: {stats['mean']:.2f}%\n"
        report += f"  - Median: {stats['median']:.2f}%\n"
        report += f"  - Count: {stats['count']:,}\n"

    report += "\n## Visualizations\n"
    report += "The following visualizations have been generated in the reports/figures directory:\n"
    report += "1. Completion Percentage Distribution (completion_percentage_distribution.png)\n"
    report += "2. Correlation Heatmap (correlation_heatmap.png)\n"
    report += "3. Completion Percentage by Gender (completion_by_gender.png)\n"
    report += "4. Completion Percentage by Age Group (completion_by_age.png)\n"

    # Save report
    # Ensure reports directory exists
    Path('reports').mkdir(exist_ok=True)
    
    # Save report as txt file in reports directory
    with open('reports/correlation_analysis_report.txt', 'w') as f:
        f.write(report)

def main():
    print("Starting correlation analysis...")
    
    # Load and preprocess data
    df = load_data()
    
    # Perform analyses
    completion_stats = analyze_completion_percentage(df)
    correlations = analyze_correlations(df)
    gender_stats = analyze_completion_by_gender(df)
    age_stats = analyze_completion_by_age(df)
    
    # Generate report
    generate_report(completion_stats, correlations, gender_stats, age_stats)
    
    print("Analysis complete! Check reports/correlation_analysis_report.txt for results.")

if __name__ == "__main__":
    main()
