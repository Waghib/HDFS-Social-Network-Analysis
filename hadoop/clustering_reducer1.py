#!/usr/bin/env python3
import sys
import os

def reduce_features():
    """Identity reducer - just pass through the features"""
    try:
        sys.stderr.write(f"Starting feature extraction reducer\n")
        
        for line in sys.stdin:
            # Simply pass through the data
            sys.stdout.write(line)
            sys.stdout.flush()
                
    except Exception as e:
        sys.stderr.write(f"Fatal error in reducer: {str(e)}\n")
        sys.exit(1)

if __name__ == '__main__':
    reduce_features()
