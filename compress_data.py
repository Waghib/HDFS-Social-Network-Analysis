import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os

def convert_to_parquet(input_file, output_file):
    print("Reading data...")
    # Read data in chunks
    df = pd.read_csv(input_file, 
                     sep='\t',
                     header=None,
                     na_values=['null'],  # Convert 'null' strings to NaN
                     dtype_backend='pyarrow')  # Use PyArrow backend for better memory efficiency
    
    print("Converting to Parquet...")
    # Write to parquet with snappy compression
    df.to_parquet(output_file, 
                  engine='pyarrow',
                  compression='snappy',
                  index=False)
    
    # Print size comparison
    original_size = os.path.getsize(input_file) / (1024 * 1024)  # Size in MB
    compressed_size = os.path.getsize(output_file) / (1024 * 1024)  # Size in MB
    
    print(f"\nOriginal file size: {original_size:.2f} MB")
    print(f"Compressed file size: {compressed_size:.2f} MB")
    print(f"Compression ratio: {compressed_size/original_size:.2%}")

if __name__ == "__main__":
    input_file = "soc-pokec-profiles.txt"
    output_file = "profiles.parquet"
    convert_to_parquet(input_file, output_file)
