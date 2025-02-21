#!/usr/bin/env python3
"""
Normalize and standardize age feature, with clustering analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_clean_age(df):
    """Clean and validate age data"""
    # Convert age to numeric, handling errors
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    
    # Filter out invalid ages (e.g., negative or unreasonably high)
    df = df[df['age'].between(1, 100)]
    
    return df

def normalize_age(age_series):
    """Apply min-max normalization"""
    min_max_scaler = MinMaxScaler()
    age_normalized = min_max_scaler.fit_transform(age_series.values.reshape(-1, 1))
    return pd.Series(age_normalized.flatten(), index=age_series.index)

def standardize_age(age_series):
    """Apply z-score standardization"""
    standard_scaler = StandardScaler()
    age_standardized = standard_scaler.fit_transform(age_series.values.reshape(-1, 1))
    return pd.Series(age_standardized.flatten(), index=age_series.index)

def analyze_age_distribution(df, normalized_age, standardized_age):
    """Analyze age distribution and create visualizations"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Original age distribution
    sns.histplot(data=df['age'], bins=30, ax=axes[0])
    axes[0].set_title('Original Age Distribution')
    axes[0].set_xlabel('Age')
    
    # Normalized age distribution
    sns.histplot(data=normalized_age, bins=30, ax=axes[1])
    axes[1].set_title('Normalized Age Distribution')
    axes[1].set_xlabel('Normalized Age')
    
    # Standardized age distribution
    sns.histplot(data=standardized_age, bins=30, ax=axes[2])
    axes[2].set_title('Standardized Age Distribution')
    axes[2].set_xlabel('Standardized Age')
    
    plt.tight_layout()
    return fig

def perform_clustering(age_standardized, n_clusters=5):
    """Perform K-means clustering on standardized age"""
    # Reshape for clustering
    X = age_standardized.values.reshape(-1, 1)
    
    # Fit KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)
    
    return clusters, kmeans.cluster_centers_

def plot_clusters(age_standardized, clusters, centers):
    """Plot clustering results"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot distribution for each cluster
    for i in range(len(centers)):
        cluster_data = age_standardized[clusters == i]
        sns.kdeplot(data=cluster_data, ax=ax, label=f'Cluster {i+1}')
    
    # Plot cluster centers
    for i, center in enumerate(centers):
        ax.axvline(x=center, color=f'C{i}', linestyle='--', alpha=0.5)
    
    ax.set_title('Age Clusters Distribution')
    ax.set_xlabel('Standardized Age')
    ax.legend()
    
    return fig

def main():
    print("Loading data...")
    
    # Create necessary directories
    Path("data").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    Path("plots").mkdir(exist_ok=True)
    
    # Read data
    df = pd.read_csv('data/soc-pokec-profiles.txt', 
                     sep='\t',
                     names=range(60),
                     usecols=[7],  # age column
                     nrows=10000)
    
    # Rename column
    df.columns = ['age']
    
    print("\nCleaning age data...")
    df = load_and_clean_age(df)
    
    print("\nNormalizing and standardizing age...")
    # Apply normalizations
    df['age_normalized'] = normalize_age(df['age'])
    df['age_standardized'] = standardize_age(df['age'])
    
    print("\nPerforming clustering analysis...")
    clusters, centers = perform_clustering(df['age_standardized'])
    df['age_cluster'] = clusters
    
    # Generate statistics
    stats = {
        'original': {
            'mean': df['age'].mean(),
            'std': df['age'].std(),
            'min': df['age'].min(),
            'max': df['age'].max(),
            'median': df['age'].median()
        },
        'normalized': {
            'mean': df['age_normalized'].mean(),
            'std': df['age_normalized'].std(),
            'min': df['age_normalized'].min(),
            'max': df['age_normalized'].max(),
            'median': df['age_normalized'].median()
        },
        'standardized': {
            'mean': df['age_standardized'].mean(),
            'std': df['age_standardized'].std(),
            'min': df['age_standardized'].min(),
            'max': df['age_standardized'].max(),
            'median': df['age_standardized'].median()
        }
    }
    
    # Generate cluster statistics
    cluster_stats = df.groupby('age_cluster')['age'].agg(['count', 'mean', 'std']).round(2)
    
    # Create visualizations
    print("\nGenerating visualizations...")
    dist_fig = analyze_age_distribution(df, df['age_normalized'], df['age_standardized'])
    cluster_fig = plot_clusters(df['age_standardized'], clusters, centers.flatten())
    
    # Save visualizations
    dist_fig.savefig('plots/age_distributions.png')
    cluster_fig.savefig('plots/age_clusters.png')
    plt.close('all')
    
    # Save processed data
    df.to_parquet('data/age_processed.parquet')
    
    # Generate report
    report = ["Age Feature Analysis Report",
             "=======================\n",
             "1. Data Summary",
             "--------------",
             f"Total profiles analyzed: {len(df):,}",
             f"Valid age entries: {len(df):,}\n",
             "2. Original Age Statistics",
             "----------------------",
             f"Mean: {stats['original']['mean']:.2f}",
             f"Std: {stats['original']['std']:.2f}",
             f"Min: {stats['original']['min']:.2f}",
             f"Max: {stats['original']['max']:.2f}",
             f"Median: {stats['original']['median']:.2f}\n",
             "3. Normalized Age Statistics [0-1]",
             "------------------------------",
             f"Mean: {stats['normalized']['mean']:.2f}",
             f"Std: {stats['normalized']['std']:.2f}",
             f"Min: {stats['normalized']['min']:.2f}",
             f"Max: {stats['normalized']['max']:.2f}",
             f"Median: {stats['normalized']['median']:.2f}\n",
             "4. Standardized Age Statistics (z-score)",
             "------------------------------------",
             f"Mean: {stats['standardized']['mean']:.2f}",
             f"Std: {stats['standardized']['std']:.2f}",
             f"Min: {stats['standardized']['min']:.2f}",
             f"Max: {stats['standardized']['max']:.2f}",
             f"Median: {stats['standardized']['median']:.2f}\n",
             "5. Cluster Analysis",
             "-----------------",
             "Cluster Statistics:",
             cluster_stats.to_string(),
             "\nVisualizations saved:",
             "- plots/age_distributions.png",
             "- plots/age_clusters.png",
             "\nProcessed data saved to: data/age_processed.parquet"]
    
    # Save report
    with open('reports/age_analysis.txt', 'w') as f:
        f.write('\n'.join(report))
    
    print("\nResults saved to:")
    print("- data/age_processed.parquet")
    print("- reports/age_analysis.txt")
    print("- plots/age_distributions.png")
    print("- plots/age_clusters.png")
    
    # Print sample
    print("\nSample of processed data (first 5 rows):")
    print(df.head().to_string())
    
    print("\nCluster Statistics:")
    print(cluster_stats.to_string())

if __name__ == "__main__":
    main()
