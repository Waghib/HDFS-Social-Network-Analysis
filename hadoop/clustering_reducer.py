#!/usr/bin/env python3
"""
Reducer for clustering analysis of user age and completion percentage
"""
import sys
import json
from collections import defaultdict
import math

class ClusterStats:
    """Calculate statistics for a cluster"""
    def __init__(self):
        self.ages = []
        self.completions = []
        self.count = 0
        self.age_sum = 0
        self.completion_sum = 0
        self.completion_sum_sq = 0
        
    def add_point(self, age, completion):
        self.ages.append(age)
        self.completions.append(completion)
        self.count += 1
        self.age_sum += age
        self.completion_sum += completion
        self.completion_sum_sq += completion * completion
        
    def get_stats(self):
        if self.count == 0:
            return None
            
        # Calculate basic statistics
        mean_age = self.age_sum / self.count
        mean_completion = self.completion_sum / self.count
        
        # Calculate completion percentage statistics
        variance = (self.completion_sum_sq / self.count) - (mean_completion * mean_completion)
        std_dev = math.sqrt(variance) if variance > 0 else 0
        
        # Calculate median completion
        self.completions.sort()
        if self.count % 2 == 0:
            median = (self.completions[self.count//2-1] + self.completions[self.count//2]) / 2
        else:
            median = self.completions[self.count//2]
            
        # Calculate age range
        self.ages.sort()
        age_min = self.ages[0]
        age_max = self.ages[-1]
        
        return {
            'count': self.count,
            'age_range': {'min': age_min, 'max': age_max},
            'mean_age': round(mean_age, 1),
            'completion': {
                'mean': round(mean_completion, 2),
                'median': round(median, 2),
                'std_dev': round(std_dev, 2)
            }
        }

class OverallStats:
    """Calculate overall statistics"""
    def __init__(self):
        self.ages = []
        self.completions = []
        
    def add_point(self, age, completion):
        self.ages.append(age)
        self.completions.append(completion)
        
    def get_stats(self):
        if not self.ages:
            return None
            
        return {
            'total_users': len(self.ages),
            'age_range': {
                'min': min(self.ages),
                'max': max(self.ages)
            },
            'completion_range': {
                'min': min(self.completions),
                'max': max(self.completions)
            }
        }

def generate_report(cluster_stats, overall_stats):
    """Generate the analysis report"""
    report = """# User Age Clustering Analysis Report (MapReduce Implementation)

## Cluster Characteristics

The users have been segmented into clusters based on their age. Here are the characteristics of each cluster:

"""
    # Sort clusters by mean age
    sorted_clusters = sorted(
        cluster_stats.items(),
        key=lambda x: x[1]['mean_age']
    )
    
    for cluster_id, stats in sorted_clusters:
        report += f"### Cluster {cluster_id}\n"
        report += f"- Age Range: {stats['age_range']['min']:.0f} - {stats['age_range']['max']:.0f} years\n"
        report += f"- Mean Age: {stats['mean_age']} years\n"
        report += f"- Number of Users: {stats['count']:,}\n"
        report += f"- Completion Rate Statistics:\n"
        report += f"  - Mean: {stats['completion']['mean']}%\n"
        report += f"  - Median: {stats['completion']['median']}%\n"
        report += f"  - Standard Deviation: {stats['completion']['std_dev']}%\n\n"
    
    report += """## Key Findings

1. Age-Based Segmentation:
   - Users have been divided into distinct age groups
   - Each cluster represents a different age segment of the user base

2. Completion Rate Patterns:
   - Different age clusters show varying patterns in profile completion
   - The analysis reveals how age groups differ in their engagement

3. Overall Statistics:\n"""
    
    report += f"   - Total Users Analyzed: {overall_stats['total_users']:,}\n"
    report += f"   - Age Range: {overall_stats['age_range']['min']:.0f} - {overall_stats['age_range']['max']:.0f} years\n"
    report += f"   - Completion Range: {overall_stats['completion_range']['min']:.1f}% - {overall_stats['completion_range']['max']:.1f}%\n"
    
    return report

def main():
    # Initialize statistics collectors
    cluster_stats = defaultdict(ClusterStats)
    overall_stats = OverallStats()
    
    # Process input from mapper
    for line in sys.stdin:
        try:
            key, value = line.strip().split('\t')
            data = json.loads(value)
            
            if key == 'CLUSTER':
                # Add data to cluster statistics
                cluster_stats[data['cluster']].add_point(data['age'], data['completion'])
                
            elif key == 'AGE_STATS':
                # Add data to overall statistics
                overall_stats.add_point(data['age'], data['completion'])
                
        except Exception as e:
            continue
    
    # Calculate final statistics
    final_cluster_stats = {
        cluster_id: stats.get_stats()
        for cluster_id, stats in cluster_stats.items()
    }
    
    final_overall_stats = overall_stats.get_stats()
    
    # Generate and print report
    if final_cluster_stats and final_overall_stats:
        report = generate_report(final_cluster_stats, final_overall_stats)
        print("###START_REPORT###")
        print(report)
        print("###END_REPORT###")
    else:
        print("Error: No valid data to analyze")

if __name__ == "__main__":
    main()
