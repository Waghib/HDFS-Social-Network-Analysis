import pandas as pd
import pyarrow.parquet as pq

def display_profile_stats():
    # Read the parquet file
    print('Reading Parquet file...')
    df = pd.read_parquet('profiles.parquet')
    
    # Display basic information about the dataset
    print('\nDataset Info:')
    print(f'Number of profiles: {len(df)}')
    print(f'Number of columns: {len(df.columns)}')
    
    # Display first few rows with better formatting
    print('\nFirst 5 profiles (selected columns):')
    # Select specific columns and give them meaningful names
    sample_df = df.iloc[:5, :10]  # First 5 rows, first 10 columns
    print(sample_df)
    
    # Display some basic statistics
    print('\nAge distribution (column 2):')
    age_data = df.iloc[:, 2]  # Get the third column (age)
    print(age_data.describe())
    
    # Count number of users by region
    print('\nTop 5 regions by number of users (column 4):')
    regions = df.iloc[:, 4]  # Get the fifth column (region)
    print(regions.value_counts().head())

if __name__ == '__main__':
    display_profile_stats()