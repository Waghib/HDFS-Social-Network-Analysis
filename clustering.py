import pandas as pd
import numpy as np
from collections import defaultdict
from mapreduce_framework import Mapper, Reducer, MapReduceFramework
from typing import Dict, List, Any
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import MiniBatchKMeans

class ClusteringMapper(Mapper):
    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters
        self.kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()
    
    def map(self, chunk: pd.DataFrame) -> Dict[str, List]:
        results = defaultdict(list)
        
        # Extract age and calculate completion rate
        age_data = chunk.iloc[:, 2].fillna(chunk.iloc[:, 2].mean())
        completion_rates = chunk.apply(lambda row: (row.notna().sum() / len(row)) * 100, axis=1)
        
        # Scale features
        X = self.scaler.fit_transform(np.column_stack([age_data, completion_rates]))
        
        # Perform clustering
        cluster_labels = self.kmeans.fit_predict(X)
        
        # Collect statistics for each cluster
        for cluster_id in range(self.n_clusters):
            mask = cluster_labels == cluster_id
            cluster_data = {
                'age_mean': age_data[mask].mean(),
                'age_std': age_data[mask].std(),
                'completion_mean': completion_rates[mask].mean(),
                'completion_std': completion_rates[mask].std(),
                'size': mask.sum()
            }
            results['cluster_stats'].append((cluster_id, cluster_data))
        
        return results

class ClusteringReducer(Reducer):
    def reduce(self, key: str, values: List) -> Dict:
        if key == 'cluster_stats':
            # Combine cluster statistics
            cluster_stats = defaultdict(lambda: {
                'age_sum': 0,
                'age_sq_sum': 0,
                'completion_sum': 0,
                'completion_sq_sum': 0,
                'count': 0
            })
            
            # Aggregate statistics
            for cluster_id, stats in values:
                cluster_stats[cluster_id]['age_sum'] += stats['age_mean'] * stats['size']
                cluster_stats[cluster_id]['age_sq_sum'] += (stats['age_std']**2 + stats['age_mean']**2) * stats['size']
                cluster_stats[cluster_id]['completion_sum'] += stats['completion_mean'] * stats['size']
                cluster_stats[cluster_id]['completion_sq_sum'] += (stats['completion_std']**2 + stats['completion_mean']**2) * stats['size']
                cluster_stats[cluster_id]['count'] += stats['size']
            
            # Calculate final statistics
            final_stats = {}
            for cluster_id, stats in cluster_stats.items():
                n = stats['count']
                final_stats[cluster_id] = {
                    'age_mean': stats['age_sum'] / n,
                    'age_std': np.sqrt(stats['age_sq_sum']/n - (stats['age_sum']/n)**2),
                    'completion_mean': stats['completion_sum'] / n,
                    'completion_std': np.sqrt(stats['completion_sq_sum']/n - (stats['completion_sum']/n)**2),
                    'size': n
                }
            
            return final_stats
        
        return {}
