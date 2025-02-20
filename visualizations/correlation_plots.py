#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Create output directory for plots
output_dir = Path(__file__).parent / 'plots'
output_dir.mkdir(parents=True, exist_ok=True)

def read_pokec_data(sample_size=10000):
    """Read the Pokec dataset and return as DataFrame with specified sample size"""
    print(f"Reading data (sample size: {sample_size})...")
    """Read the Pokec dataset and return as DataFrame"""
    data = []
    line_count = 0
    sample_interval = None
    
    # First count total lines to determine sampling interval
    with open('/home/waghib/Desktop/HDFS-Social-Network-Analysis/data/soc-pokec-profiles.txt', 'r') as f:
        total_lines = sum(1 for _ in f)
        sample_interval = max(1, total_lines // sample_size)
    
    print(f"Total records: {total_lines}, sampling every {sample_interval}th record")
    
    # Now read the sampled data
    with open('/home/waghib/Desktop/HDFS-Social-Network-Analysis/data/soc-pokec-profiles.txt', 'r') as f:
        for line_num, line in enumerate(f):
            if line_num % sample_interval != 0:
                continue
            
            line_count += 1
            if line_count > sample_size:
                break
            fields = line.strip().split('\t')
            if len(fields) >= 5:
                # Calculate completion percentage
                total_fields = len(fields[5:])
                non_null_fields = sum(1 for field in fields[5:] if field and field.lower() != 'null')
                completion_percentage = (non_null_fields / total_fields * 100) if total_fields > 0 else 0
                
                # Extract basic fields
                record = {
                    'user_id': fields[0],
                    'gender': 'woman' if fields[1] == '1' else 'man',
                    'age': float(fields[2]) if fields[2] and fields[2].lower() != 'null' else None,
                    'public': fields[3] == '1',
                    'region': fields[4],
                    'completion_percentage': completion_percentage
                }
                
                # Add any additional fields if available
                if len(fields) > 5:
                    record['favorite_color'] = fields[5] if fields[5] and fields[5].lower() != 'null' else None
                
                data.append(record)
    
    return pd.DataFrame(data)

def plot_completion_vs_categorical(df, column, title):
    """Create boxplot for completion percentage vs categorical variable"""
    plt.clf()  # Clear the current figure
    """Create boxplot for completion percentage vs categorical variable"""
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=column, y='completion_percentage', data=df)
    plt.title(f'Profile Completion vs {title}')
    plt.xlabel(title)
    plt.ylabel('Completion Percentage')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / f'completion_vs_{column}.png')
    plt.close()

def plot_completion_vs_age(df):
    """Create scatter plot for completion percentage vs age"""
    plt.clf()  # Clear the current figure
    """Create scatter plot for completion percentage vs age"""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='age', y='completion_percentage', data=df)
    plt.title('Profile Completion vs Age')
    plt.xlabel('Age')
    plt.ylabel('Completion Percentage')
    
    # Add trend line
    z = np.polyfit(df['age'].dropna(), df['completion_percentage'].dropna(), 1)
    p = np.poly1d(z)
    plt.plot(df['age'].dropna(), p(df['age'].dropna()), "r--", alpha=0.8)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'completion_vs_age.png')
    plt.close()

def plot_correlation_heatmap(df):
    """Create correlation heatmap for numerical variables"""
    plt.clf()  # Clear the current figure
    """Create correlation heatmap for numerical variables"""
    # Select numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[numerical_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(output_dir / 'correlation_heatmap.png')
    plt.close()

def plot_completion_distribution(df):
    """Plot distribution of completion percentages"""
    plt.clf()  # Clear the current figure
    """Plot distribution of completion percentages"""
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='completion_percentage', bins=30)
    plt.title('Distribution of Profile Completion Percentages')
    plt.xlabel('Completion Percentage')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(output_dir / 'completion_distribution.png')
    plt.close()

def cleanup_memory():
    """Clean up memory after plotting"""
    plt.close('all')
    import gc
    gc.collect()

def main():
    try:
        # Set style
        print("Setting up visualization environment...")
        sns.set_theme(style="whitegrid")
        
        # Read data
        print("Reading data...")
        df = read_pokec_data()
        print(f"Successfully read {len(df)} records")
        
        print("\nGenerating plots...")
        
        # Create various plots
        print("1. Creating gender completion boxplot...")
        plot_completion_vs_categorical(df, 'gender', 'Gender')
        cleanup_memory()
        
        print("2. Creating profile visibility boxplot...")
        plot_completion_vs_categorical(df, 'public', 'Profile Visibility')
        cleanup_memory()
        
        if 'favorite_color' in df.columns:
            print("3. Creating favorite color boxplot...")
            plot_completion_vs_categorical(df, 'favorite_color', 'Favorite Color')
            cleanup_memory()
        
        print("4. Creating age vs completion scatter plot...")
        plot_completion_vs_age(df)
        cleanup_memory()
        
        print("5. Creating correlation heatmap...")
        plot_correlation_heatmap(df)
        cleanup_memory()
        
        print("6. Creating completion distribution histogram...")
        plot_completion_distribution(df)
        cleanup_memory()
        
        print(f"\nAll plots have been successfully saved to: {output_dir}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
