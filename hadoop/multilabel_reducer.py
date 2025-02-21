#!/usr/bin/env python3
"""
Reducer for processing multi-label columns (hobbies and languages)
Input: Key-value pairs from mapper (category_name|word\t1)
Output: JSON format with word frequencies and binary flags
"""

import sys
import json
from collections import defaultdict
from typing import Dict, Set, List

class MultiLabelReducer:
    def __init__(self):
        # Store word frequencies
        self.hobby_counts: Dict[str, int] = defaultdict(int)
        self.language_counts: Dict[str, int] = defaultdict(int)
        
        # Store unique words for binary encoding
        self.hobby_words: Set[str] = set()
        self.language_words: Set[str] = set()
        
        # Track total records
        self.total_records = 0
    
    def process_input(self):
        """Process input from mapper"""
        current_key = None
        current_count = 0
        
        # Read input key-value pairs
        for line in sys.stdin:
            try:
                # Parse input
                key, count = line.strip().split('\t')
                category, word = key.split('|')
                count = int(count)
                
                # Update counts based on category
                if category == 'hobby':
                    self.hobby_counts[word] += count
                    self.hobby_words.add(word)
                elif category == 'language':
                    self.language_counts[word] += count
                    self.language_words.add(word)
                
            except Exception as e:
                sys.stderr.write(f"Error processing line: {str(e)}\n")
                continue
    
    def get_top_items(self, counts: Dict[str, int], n: int = 10) -> List[Dict]:
        """Get top N items by frequency"""
        sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        return [
            {'word': word, 'count': count, 'percentage': (count/self.total_records)*100}
            for word, count in sorted_items[:n]
        ]
    
    def output_results(self):
        """Output results in JSON format"""
        # Calculate total records (use max of hobby/language counts)
        self.total_records = max(
            sum(self.hobby_counts.values()),
            sum(self.language_counts.values())
        )
        
        results = {
            'summary': {
                'total_records': self.total_records,
                'unique_hobbies': len(self.hobby_words),
                'unique_languages': len(self.language_words)
            },
            'hobbies': {
                'top_frequencies': self.get_top_items(self.hobby_counts),
                'binary_columns': sorted(list(self.hobby_words)),
                'total_mentions': sum(self.hobby_counts.values())
            },
            'languages': {
                'top_frequencies': self.get_top_items(self.language_counts),
                'binary_columns': sorted(list(self.language_words)),
                'total_mentions': sum(self.language_counts.values())
            }
        }
        
        # Output JSON results
        print(json.dumps(results, indent=2))
        
        # Output binary encoding instructions
        print("\nBINARY ENCODING INSTRUCTIONS:")
        print("1. Hobbies: Create these binary columns:")
        for hobby in sorted(self.hobby_words):
            print(f"   - hobby_{hobby}")
        
        print("\n2. Languages: Create these binary columns:")
        for lang in sorted(self.language_words):
            print(f"   - language_{lang}")

def main():
    reducer = MultiLabelReducer()
    reducer.process_input()
    reducer.output_results()

if __name__ == "__main__":
    main()
