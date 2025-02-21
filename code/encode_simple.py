#!/usr/bin/env python3
"""
Simple script to encode categorical variables from the Pokec dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def main():
    # Create output directories
    Path("data").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    
    print("Loading data...")
    # Read only the columns we need
    df = pd.read_csv('data/soc-pokec-profiles.txt', 
                     sep='\t',
                     usecols=[3, 4, 16],  # gender, region, eye_color columns
                     nrows=10000,  # Sample size
                     names=range(60))  # Just number the columns 0-59
    
    # Rename columns to meaningful names
    df.columns = ['gender', 'region', 'eye_color']
    
    print("\nOriginal data sample:")
    print(df.head())
    print("\nValue counts:")
    for col in df.columns:
        print(f"\n{col}:")
        print(df[col].value_counts().head())
    
    # One-hot encode each column
    print("\nApplying one-hot encoding...")
    df_encoded = pd.get_dummies(df, columns=['gender', 'region', 'eye_color'])
    
    print("\nEncoded data shape:", df_encoded.shape)
    print("\nEncoded columns:", df_encoded.columns.tolist())
    
    # Save results
    print("\nSaving results...")
    df_encoded.to_parquet('data/encoded_categorical_simple.parquet')
    
    # Generate simple report
    report = f"""# One-Hot Encoding Results

## Original Data
- Number of rows: {len(df)}
- Columns: {', '.join(df.columns)}

## Encoded Data
- Number of rows: {len(df_encoded)}
- Number of columns: {len(df_encoded.columns)}
- Memory usage: {df_encoded.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB

## Unique Values Per Column
"""
    for col in df.columns:
        unique_vals = df[col].nunique()
        report += f"\n### {col}\n"
        report += f"- Unique values: {unique_vals}\n"
        report += "- Top 5 values:\n"
        for val, count in df[col].value_counts().head().items():
            report += f"  - {val}: {count:,} ({count/len(df)*100:.1f}%)\n"
    
    with open('reports/encoding_report_simple.md', 'w') as f:
        f.write(report)
    
    print("\nDone! Check reports/encoding_report_simple.md for details")

if __name__ == "__main__":
    main()
