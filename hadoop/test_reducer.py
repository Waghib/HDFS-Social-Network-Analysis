#!/usr/bin/env python3
import sys

total = 0
for line in sys.stdin:
    key, value = line.strip().split('\t')
    if key == 'count':
        total += int(value)

print(f'Total lines: {total}')
