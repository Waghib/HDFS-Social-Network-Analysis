#!/usr/bin/env python3
import sys
import os

sys.stderr.write(f"Starting mapper with Python: {sys.executable}\n")
sys.stderr.write(f"Current directory: {os.getcwd()}\n")
sys.stderr.write(f"Directory contents: {os.listdir('.')}\n")

for line in sys.stdin:
    sys.stdout.write('count\t1\n')
    sys.stdout.flush()
