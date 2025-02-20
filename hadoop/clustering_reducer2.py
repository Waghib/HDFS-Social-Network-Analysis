#!/usr/bin/env python3
import sys
import os
from collections import defaultdict
import math

def calculate_stats(values):
    """Calculate basic statistics for a list of values"""
    n = len(values)
    if n == 0:
        return 0, 0, 0, 0
    
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / n
    std = math.sqrt(variance)
    return mean, std, min(values), max(values)

def analyze_clusters():
    """Analyze and summarize clustering results"""
    try:
        sys.stderr.write("Starting clustering analysis...\n")
        
        # Store cluster information
        clusters = defaultdict(list)
        
        # Process input
        for line in sys.stdin:
            try:
                cluster_id, value = line.strip().split('\t')
                user_id, age, completion = value.split(',')
                clusters[int(cluster_id)].append((float(age), float(completion)))
            except Exception as e:
                sys.stderr.write(f"Error processing line: {str(e)}\n")
                continue
        
        # Analyze each cluster
        sys.stdout.write("\nCluster Analysis Results:\n\n")
        
        for cluster_id in sorted(clusters.keys()):
            members = clusters[cluster_id]
            ages = [age for age, _ in members]
            completions = [comp for _, comp in members]
            
            # Calculate statistics
            age_mean, age_std, age_min, age_max = calculate_stats(ages)
            comp_mean, comp_std, comp_min, comp_max = calculate_stats(completions)
            
            # Output cluster statistics
            sys.stdout.write(f"Cluster {cluster_id}:\n")
            sys.stdout.write(f"Size: {len(members)} members\n")
            sys.stdout.write(f"Age: {age_mean:.2f} ± {age_std:.2f} years (range: {age_min:.2f} - {age_max:.2f})\n")
            sys.stdout.write(f"Completion: {comp_mean:.2f}% ± {comp_std:.2f}% (range: {comp_min:.2f}% - {comp_max:.2f}%)\n")
            sys.stdout.write("\n")
            
            sys.stdout.flush()
                
    except Exception as e:
        sys.stderr.write(f"Fatal error in reducer: {str(e)}\n")
        sys.exit(1)

if __name__ == '__main__':
    analyze_clusters()
