import pandas as pd
import numpy as np

# Read the original and encoded data
print("Loading data...")
df_encoded = pd.read_parquet('data/encoded_categorical_simple.parquet')

# Show examples for each category
print("\n1. GENDER ENCODING EXAMPLE (First 5 rows)")
print("-" * 50)
gender_cols = [col for col in df_encoded.columns if col.startswith('gender_')]
print(df_encoded[gender_cols].head())

print("\n2. REGION ENCODING EXAMPLE (First 5 rows, top 5 regions)")
print("-" * 50)
region_cols = [col for col in df_encoded.columns if col.startswith('region_')][:5]
print(df_encoded[region_cols].head())

print("\n3. EYE COLOR ENCODING EXAMPLE (First 5 rows, top 5 colors)")
print("-" * 50)
eye_cols = [col for col in df_encoded.columns if col.startswith('eye_color_')][:5]
print(df_encoded[eye_cols].head())

# Show summary statistics
print("\nSUMMARY STATISTICS")
print("-" * 50)
print(f"Total number of encoded columns: {len(df_encoded.columns)}")
print(f"- Gender columns: {len(gender_cols)}")
print(f"- Region columns: {len(region_cols)}")
print(f"- Eye color columns: {len(eye_cols)}")

# Show memory usage
print("\nMEMORY USAGE")
print("-" * 50)
memory_mb = df_encoded.memory_usage(deep=True).sum() / 1024 / 1024
print(f"Total memory usage: {memory_mb:.2f} MB")
