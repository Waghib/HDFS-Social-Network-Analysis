#!/usr/bin/env python3
import sys
import os
import math
from random import uniform

def euclidean_distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def initialize_centroids(data_points, k):
    # Find min and max for each dimension
    min_age = min(p[0] for p in data_points)
    max_age = max(p[0] for p in data_points)
    min_comp = min(p[1] for p in data_points)
    max_comp = max(p[1] for p in data_points)
    
    # Initialize k centroids randomly within the data bounds
    centroids = []
    for _ in range(k):
        age = uniform(min_age, max_age)
        comp = uniform(min_comp, max_comp)
        centroids.append([age, comp])
    return centroids

def assign_clusters(data_points, centroids):
    clusters = []
    for point in data_points:
        # Find nearest centroid
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
        cluster_id = distances.index(min(distances))
        clusters.append(cluster_id)
    return clusters

def process_data():
    """Process data points and perform clustering"""
    try:
        # Collect data points
        data_points = []
        user_ids = []
        
        sys.stderr.write("Reading data points...\n")
        for line in sys.stdin:
            try:
                user_id, features = line.strip().split('\t')
                age, completion = map(float, features.split(','))
                data_points.append([age, completion])
                user_ids.append(user_id)
            except Exception as e:
                sys.stderr.write(f"Error processing line: {str(e)}\n")
                continue
        
        if not data_points:
            sys.stderr.write("No valid data points found\n")
            return
        
        # Initialize centroids
        k = 5  # number of clusters
        centroids = initialize_centroids(data_points, k)
        
        # Assign clusters
        clusters = assign_clusters(data_points, centroids)
        
        # Emit results
        for user_id, point, cluster in zip(user_ids, data_points, clusters):
            age, completion = point
            # Key: cluster_id, Value: user_id,age,completion
            sys.stdout.write(f"{cluster}\t{user_id},{age:.2f},{completion:.2f}\n")
            sys.stdout.flush()
            
    except Exception as e:
        sys.stderr.write(f"Fatal error: {str(e)}\n")
        sys.exit(1)

if __name__ == '__main__':
    process_data()
