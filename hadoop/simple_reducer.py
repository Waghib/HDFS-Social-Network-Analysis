#!/usr/bin/env python3
import sys
import os

sys.stderr.write(f"Starting reducer with Python: {sys.executable}\n")
sys.stderr.write(f"Current directory: {os.getcwd()}\n")
sys.stderr.write(f"Directory contents: {os.listdir('.')}\n")

total = 0
for line in sys.stdin:
    key, value = line.strip().split('\t')
    if key == 'count':
        total += int(value)

sys.stdout.write(f'Total lines: {total}\n')
sys.stdout.flush()
