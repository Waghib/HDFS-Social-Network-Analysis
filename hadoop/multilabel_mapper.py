#!/usr/bin/env python3
"""
Mapper for processing multi-label columns (hobbies and languages)
Input: Tab-separated lines from Pokec profiles
Output: Key-value pairs for word frequency counting
Format: category_name|word\t1
"""

import sys
import re
from typing import List, Tuple

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text or text == 'null':
        return ''
    
    # Convert to lowercase and remove special characters
    text = str(text).lower()
    text = re.sub(r'[^\w\s,;-]', ' ', text)
    return text

def split_text(text: str) -> List[str]:
    """Split text into individual words/terms"""
    # Split on common separators
    items = []
    for item in re.split(r'[,;]', text):
        # Clean and validate each item
        item = item.strip()
        if len(item) > 1:  # Ignore single characters
            items.extend(item.split())
    return items

def process_hobbies(text: str) -> List[Tuple[str, str]]:
    """Process hobbies text into category-word pairs"""
    hobby_words = split_text(clean_text(text))
    return [('hobby', word) for word in hobby_words if word]

def process_languages(text: str) -> List[Tuple[str, str]]:
    """Process languages text into category-word pairs"""
    language_words = split_text(clean_text(text))
    return [('language', word) for word in language_words if word]

def main():
    # Process input lines from stdin
    for line in sys.stdin:
        try:
            # Split line into fields
            fields = line.strip().split('\t')
            
            if len(fields) >= 17:  # Ensure we have enough fields
                # Extract hobbies (field 11) and languages (field 10)
                hobbies = fields[11]
                languages = fields[10]
                
                # Process hobbies
                for category, word in process_hobbies(hobbies):
                    print(f"{category}|{word}\t1")
                
                # Process languages
                for category, word in process_languages(languages):
                    print(f"{category}|{word}\t1")
                    
        except Exception as e:
            sys.stderr.write(f"Error processing line: {str(e)}\n")
            continue

if __name__ == "__main__":
    main()
