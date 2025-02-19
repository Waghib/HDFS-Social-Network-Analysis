import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Read the TSV file in chunks to handle large file size
chunk_size = 100000
chunks = pd.read_csv('soc-pokec-profiles.txt', 
                    sep='\t',
                    header=None,
                    chunksize=chunk_size)

# Convert chunks to parquet
for i, chunk in enumerate(chunks):
    if i == 0:
        # Write first chunk
        chunk.to_parquet('profiles.parquet', engine='pyarrow')
    else:
        # Append subsequent chunks
        chunk.to_parquet('profiles.parquet', engine='pyarrow', append=True)

print("Conversion completed. Check the new file size.")
