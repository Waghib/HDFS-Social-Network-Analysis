#!/usr/bin/env python3
"""
MapReduce implementation - Reducer
Calculate days_since_registration statistics and distribution
Input: Key-value pairs from mapper
Output: JSON format with statistics and distribution
"""

import sys
import json
from collections import defaultdict

class RegistrationDurationReducer:
    def __init__(self):
        self.category_counts = defaultdict(int)
        self.days_list = []
        self.total_days = 0
        self.count = 0
        
        # Initialize statistics
        self.stats = {
            'total_profiles': 0,
            'valid_profiles': 0,
            'min_days': float('inf'),
            'max_days': 0,
            'avg_days': 0,
            'median_days': 0,
            'percentiles': {},
            'distribution': {},
            'duration_percentages': {}
        }
    
    def calculate_percentiles(self):
        """Calculate percentiles from days list"""
        if self.days_list:
            sorted_days = sorted(self.days_list)
            n = len(sorted_days)
            
            # Calculate key percentiles
            self.stats['percentiles'] = {
                'p25': sorted_days[n // 4],
                'p50': sorted_days[n // 2],
                'p75': sorted_days[3 * n // 4],
                'p90': sorted_days[9 * n // 10],
                'p95': sorted_days[95 * n // 100],
                'p99': sorted_days[99 * n // 100]
            }
    
    def calculate_statistics(self):
        """Calculate final statistics"""
        if self.count > 0:
            self.stats.update({
                'valid_profiles': self.count,
                'min_days': min(self.days_list),
                'max_days': max(self.days_list),
                'avg_days': self.total_days / self.count,
                'distribution': dict(self.category_counts)
            })
            
            # Calculate percentages
            total = sum(self.category_counts.values())
            self.stats['duration_percentages'] = {
                category: (count / total) * 100
                for category, count in self.category_counts.items()
            }
            
            # Calculate percentiles
            self.calculate_percentiles()
    
    def process_input(self):
        """Process input from mapper"""
        for line in sys.stdin:
            try:
                # Parse input
                key, value = line.strip().split('\t')
                
                if key == 'category':
                    # Update category counts
                    self.category_counts[value] += 1
                    
                elif key == 'stats':
                    # Update general statistics
                    days = int(value)
                    self.total_days += days
                    self.count += 1
                    
                elif key == 'days':
                    # Store days for percentile calculation
                    self.days_list.append(int(value))
                    
            except Exception as e:
                sys.stderr.write(f"Error processing line: {str(e)}\n")
                continue
    
    def output_results(self):
        """Output results in JSON format"""
        # Calculate final statistics
        self.calculate_statistics()
        
        # Generate detailed report
        report = {
            'summary': {
                'title': 'Registration Duration Analysis',
                'timestamp': '2025-02-21T18:48:21+05:00',
                'dataset': 'Pokec Social Network Profiles'
            },
            'statistics': self.stats,
            'analysis': {
                'user_retention': {
                    'long_term_users': self.stats['duration_percentages'].get('2+_years', 0),
                    'new_users': self.stats['duration_percentages'].get('1_month', 0)
                },
                'platform_health': {
                    'avg_account_age_days': self.stats['avg_days'],
                    'median_account_age_days': self.stats['percentiles']['p50']
                }
            }
        }
        
        # Output JSON results
        print(json.dumps(report, indent=2))

def main():
    reducer = RegistrationDurationReducer()
    reducer.process_input()
    reducer.output_results()

if __name__ == "__main__":
    main()
