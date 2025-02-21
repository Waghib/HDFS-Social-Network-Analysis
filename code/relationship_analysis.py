#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Set style for better visualizations
sns.set_style('whitegrid')
sns.set_palette("husl")

# Create directories for outputs
Path("reports/figures").mkdir(parents=True, exist_ok=True)

def load_data():
    """Load and preprocess the data"""
    print("Loading data...")
    # Read relevant columns
    columns = [
        'user_id', 'completion_percentage', 'favourite_color',
        'eye_color', 'hair_color', 'body_type', 'relation_to_smoking',
        'relation_to_alcohol', 'sign_in_zodiac', 'marital_status'
    ]
    
    # Map column indices to their positions in the file
    col_indices = [0, 2, 20, 21, 22, 23, 26, 27, 28, 33]  # Indices for relevant columns
    col_names = ['user_id', 'completion_percentage', 'eye_color', 'hair_color',
                'hair_type', 'body_type', 'relation_to_smoking', 'relation_to_alcohol',
                'sign_in_zodiac', 'marital_status']
    
    df = pd.read_csv('data/soc-pokec-profiles.txt', 
                     sep='\t',
                     usecols=col_indices,
                     names=col_names)
    
    # Clean and preprocess data
    df['completion_percentage'] = pd.to_numeric(df['completion_percentage'], errors='coerce')
    
    return df

def analyze_categorical_relationships(df):
    """Analyze relationships between completion_percentage and categorical variables"""
    print("Analyzing categorical relationships...")
    categorical_vars = ['eye_color', 'hair_color', 'hair_type', 'body_type',
                      'relation_to_smoking', 'relation_to_alcohol',
                      'sign_in_zodiac', 'marital_status']
    
    results = {}
    for var in categorical_vars:
        # Remove null values and get top 10 categories
        valid_data = df[df[var].notna() & (df[var] != 'null')]
        top_categories = valid_data[var].value_counts().head(10).index
        
        # Filter for top categories
        plot_data = valid_data[valid_data[var].isin(top_categories)]
        
        # Create boxplot
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=plot_data, x=var, y='completion_percentage')
        plt.xticks(rotation=45, ha='right')
        plt.title(f'Profile Completion Percentage by {var.replace("_", " ").title()}')
        plt.tight_layout()
        plt.savefig(f'reports/figures/completion_by_{var}.png')
        plt.close()
        
        # Calculate statistics
        stats = plot_data.groupby(var)['completion_percentage'].agg([
            'count', 'mean', 'median', 'std'
        ]).round(2)
        
        results[var] = stats.to_dict('index')
    
    return results

def analyze_numerical_correlations(df):
    """Analyze correlations between numerical variables"""
    print("Analyzing numerical correlations...")
    
    # Select numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    # Calculate correlation matrix
    corr_matrix = df[numerical_cols].corr()
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Heatmap of Numerical Variables')
    plt.tight_layout()
    plt.savefig('reports/figures/numerical_correlations_heatmap.png')
    plt.close()
    
    return corr_matrix.to_dict()

def generate_report(categorical_results, numerical_correlations):
    """Generate a report with the analysis results"""
    print("Generating report...")
    report = """# Feature Relationships Analysis Report

## Categorical Variable Relationships

"""
    # Add categorical analysis results
    for var, stats in categorical_results.items():
        report += f"### Profile Completion by {var.replace('_', ' ').title()}\n\n"
        report += "| Category | Count | Mean | Median | Std Dev |\n"
        report += "|----------|-------|------|---------|----------|\n"
        
        for category, values in stats.items():
            report += f"| {category} | {values['count']:,} | {values['mean']:.2f}% | "
            report += f"{values['median']:.2f}% | {values['std']:.2f}% |\n"
        
        report += "\n"

    # Add numerical correlations
    report += "\n## Numerical Correlations\n\n"
    report += "The correlation heatmap shows relationships between numerical variables:\n\n"
    
    for var1, correlations in numerical_correlations.items():
        for var2, corr in correlations.items():
            if var1 != var2:
                report += f"- {var1} vs {var2}: {corr:.3f}\n"

    report += "\n## Visualizations\n"
    report += "The following visualizations have been generated in the reports/figures directory:\n"
    report += "1. Boxplots showing completion percentage distribution by categorical variables\n"
    report += "2. Correlation heatmap for numerical variables\n"

    # Save report
    # Print report to console and save to file
    print(report)
    
    # Save report
    with open('relationship_analysis_report.txt', 'w') as f:
        f.write(report)

def main():
    print("Starting relationship analysis...")
    
    # Load and preprocess data
    df = load_data()
    
    # Perform analyses
    categorical_results = analyze_categorical_relationships(df)
    numerical_correlations = analyze_numerical_correlations(df)
    
    # Generate report
    generate_report(categorical_results, numerical_correlations)
    
    print("Analysis complete! Check reports/relationship_analysis_report.txt for results.")

if __name__ == "__main__":
    main()
