from typing import Dict, List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from mapreduce_framework import MapReduceFramework
from demographic_analysis import DemographicMapper, DemographicReducer
from correlation_analysis import CorrelationMapper, CorrelationReducer
from clustering import ClusteringMapper, ClusteringReducer

def load_data(file_path: str) -> pd.DataFrame:
    """Load the profile data from parquet file."""
    return pd.read_parquet(file_path)

def run_demographic_analysis(data: pd.DataFrame) -> Dict:
    """Run demographic analysis using MapReduce."""
    framework = MapReduceFramework()
    results = framework.run(DemographicMapper, DemographicReducer, data)
    
    # Visualize results
    plt.figure(figsize=(15, 5))
    
    # Age distribution
    plt.subplot(131)
    plt.hist(results['age_stats'], bins=50)
    plt.title('Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Count')
    
    # Gender distribution
    plt.subplot(132)
    gender_data = results['gender_counts']
    plt.bar(range(len(gender_data)), list(gender_data.values()))
    plt.xticks(range(len(gender_data)), list(gender_data.keys()))
    plt.title('Gender Distribution')
    
    # Top 10 regions
    plt.subplot(133)
    top_regions = dict(list(results['region_counts'].items())[:10])
    plt.bar(range(len(top_regions)), list(top_regions.values()))
    plt.xticks(range(len(top_regions)), list(top_regions.keys()), rotation=45)
    plt.title('Top 10 Regions')
    
    plt.tight_layout()
    plt.savefig('demographic_analysis.png')
    return results

def run_correlation_analysis(data: pd.DataFrame) -> Dict:
    """Run correlation analysis using MapReduce."""
    framework = MapReduceFramework()
    results = framework.run(CorrelationMapper, CorrelationReducer, data)
    
    # Visualize correlations
    plt.figure(figsize=(10, 6))
    
    # Numerical correlations
    corr_data = results['numerical_corr']
    plt.bar(range(len(corr_data)), list(corr_data.values()))
    plt.xticks(range(len(corr_data)), [f'Column {k}' for k in corr_data.keys()])
    plt.title('Feature Correlations with Completion Rate')
    plt.ylabel('Correlation Coefficient')
    
    plt.tight_layout()
    plt.savefig('correlation_analysis.png')
    return results

def run_clustering_analysis(data: pd.DataFrame, n_clusters: int = 5) -> Dict:
    """Run clustering analysis using MapReduce."""
    framework = MapReduceFramework()
    mapper = ClusteringMapper(n_clusters=n_clusters)
    results = framework.run(mapper, ClusteringReducer, data)
    
    # Visualize clusters
    plt.figure(figsize=(10, 6))
    
    # Plot cluster statistics
    cluster_stats = results['cluster_stats']
    x = np.arange(len(cluster_stats))
    width = 0.35
    
    plt.bar(x - width/2, [stats['age_mean'] for stats in cluster_stats.values()], width, label='Age')
    plt.bar(x + width/2, [stats['completion_mean'] for stats in cluster_stats.values()], width, label='Completion Rate')
    
    plt.xlabel('Cluster')
    plt.ylabel('Value')
    plt.title('Cluster Statistics')
    plt.xticks(x, [f'Cluster {i}' for i in range(len(cluster_stats))])
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('clustering_analysis.png')
    return results

def main():
    # Load data
    data = load_data('profiles.parquet')
    
    # Run analyses
    demographic_results = run_demographic_analysis(data)
    correlation_results = run_correlation_analysis(data)
    clustering_results = run_clustering_analysis(data)
    
    # Print summary results
    print("\nDemographic Analysis Results:")
    print(f"Total profiles: {len(data)}")
    print(f"Age statistics: {demographic_results['age_stats']}")
    print(f"Gender distribution: {demographic_results['gender_counts']}")
    
    print("\nCorrelation Analysis Results:")
    print(f"Feature correlations: {correlation_results['numerical_corr']}")
    
    print("\nClustering Analysis Results:")
    for cluster_id, stats in clustering_results['cluster_stats'].items():
        print(f"\nCluster {cluster_id}:")
        print(f"Size: {stats['size']}")
        print(f"Average age: {stats['age_mean']:.2f} ± {stats['age_std']:.2f}")
        print(f"Average completion rate: {stats['completion_mean']:.2f}% ± {stats['completion_std']:.2f}%")

if __name__ == "__main__":
    main()
