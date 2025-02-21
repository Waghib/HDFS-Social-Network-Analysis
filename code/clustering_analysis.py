#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Create directories for outputs
Path("reports/figures").mkdir(parents=True, exist_ok=True)

def load_data():
    """Load and preprocess the data"""
    print("Loading data...")
    
    # Read relevant columns
    df = pd.read_csv('data/soc-pokec-profiles.txt', 
                     sep='\t',
                     usecols=[0, 2, 7],  # user_id, completion_percentage, age
                     names=['user_id', 'completion_percentage', 'AGE'])
    
    # Clean and preprocess data
    df['completion_percentage'] = pd.to_numeric(df['completion_percentage'], errors='coerce')
    df['AGE'] = pd.to_numeric(df['AGE'], errors='coerce')
    
    # Filter valid ages and completion percentages
    df = df[
        (df['AGE'] >= 10) & 
        (df['AGE'] <= 100) & 
        (df['completion_percentage'].notna())
    ]
    
    return df

def perform_clustering(df, n_clusters=5):
    """Perform K-means clustering on age"""
    print("Performing clustering analysis...")
    
    # Prepare data for clustering
    X = df[['AGE']].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X_scaled)
    
    # Get cluster centers
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    
    return df, cluster_centers

def analyze_clusters(df, cluster_centers):
    """Analyze completion rates across clusters"""
    print("Analyzing clusters...")
    
    # Calculate cluster statistics
    cluster_stats = df.groupby('Cluster').agg({
        'AGE': ['mean', 'min', 'max', 'count'],
        'completion_percentage': ['mean', 'median', 'std']
    }).round(2)
    
    # Sort clusters by age mean
    cluster_stats = cluster_stats.sort_values(('AGE', 'mean'))
    
    # Create visualizations
    
    # 1. Box plot of completion percentage by cluster
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='Cluster', y='completion_percentage')
    plt.title('Profile Completion Percentage by Age Cluster')
    plt.xlabel('Age Cluster')
    plt.ylabel('Completion Percentage')
    plt.savefig('reports/figures/completion_by_cluster_boxplot.png')
    plt.close()
    
    # 2. Scatter plot of age vs completion percentage, colored by cluster
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df.sample(n=min(10000, len(df))), 
                    x='AGE', y='completion_percentage', 
                    hue='Cluster', alpha=0.5)
    plt.title('Age vs Completion Percentage by Cluster')
    plt.xlabel('Age')
    plt.ylabel('Completion Percentage')
    plt.savefig('reports/figures/age_completion_scatter.png')
    plt.close()
    
    # 3. Distribution of ages within each cluster
    plt.figure(figsize=(12, 6))
    for cluster in range(len(cluster_centers)):
        sns.kdeplot(data=df[df['Cluster'] == cluster], x='AGE', 
                    label=f'Cluster {cluster}')
    plt.title('Age Distribution by Cluster')
    plt.xlabel('Age')
    plt.ylabel('Density')
    plt.legend()
    plt.savefig('reports/figures/age_distribution_by_cluster.png')
    plt.close()
    
    return cluster_stats

def generate_report(cluster_stats, cluster_centers):
    """Generate a report with the analysis results"""
    print("Generating report...")
    
    report = """# User Age Clustering Analysis Report

## Cluster Characteristics

The users have been segmented into clusters based on their age using K-means clustering. Here are the characteristics of each cluster:

"""
    
    # Add cluster statistics
    for cluster in range(len(cluster_centers)):
        stats = cluster_stats.xs(cluster)
        report += f"### Cluster {cluster}\n"
        report += f"- Age Range: {stats[('AGE', 'min')]:.0f} - {stats[('AGE', 'max')]:.0f} years\n"
        report += f"- Mean Age: {stats[('AGE', 'mean')]:.1f} years\n"
        report += f"- Number of Users: {stats[('AGE', 'count')]:,}\n"
        report += f"- Completion Rate Statistics:\n"
        report += f"  - Mean: {stats[('completion_percentage', 'mean')]:.2f}%\n"
        report += f"  - Median: {stats[('completion_percentage', 'median')]:.2f}%\n"
        report += f"  - Standard Deviation: {stats[('completion_percentage', 'std')]:.2f}%\n\n"

    report += """## Key Findings

1. Age-Based Segmentation:
   - The users have been divided into distinct age groups using K-means clustering
   - Each cluster represents a different age segment of the user base

2. Completion Rate Patterns:
   - Different age clusters show varying patterns in profile completion
   - The analysis reveals how age groups differ in their engagement with the platform

3. Cluster Sizes:
   - The distribution of users across clusters shows the age composition of the user base
   - Some age groups are more represented than others

## Visualizations

The following visualizations have been generated in the reports/figures directory:
1. Completion by Cluster (completion_by_cluster_boxplot.png)
   - Shows the distribution of completion percentages within each cluster
2. Age vs Completion Scatter Plot (age_completion_scatter.png)
   - Visualizes the relationship between age and completion percentage
3. Age Distribution by Cluster (age_distribution_by_cluster.png)
   - Shows how ages are distributed within each cluster
"""

    # Save report
    with open('reports/clustering_analysis_report.txt', 'w') as f:
        f.write(report)

def main():
    print("Starting clustering analysis...")
    
    # Load and preprocess data
    df = load_data()
    
    # Perform clustering
    df, cluster_centers = perform_clustering(df)
    
    # Analyze clusters
    cluster_stats = analyze_clusters(df, cluster_centers)
    
    # Generate report
    generate_report(cluster_stats, cluster_centers)
    
    print("Analysis complete! Check reports/clustering_analysis_report.txt for results.")

if __name__ == "__main__":
    main()
