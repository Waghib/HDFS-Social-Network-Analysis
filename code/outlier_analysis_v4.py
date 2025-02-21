#!/usr/bin/env python3
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Create directories for outputs
Path("reports/figures").mkdir(parents=True, exist_ok=True)

def load_data():
    """Load and perform initial data cleaning"""
    print("Loading data...")
    
    # Read all potentially relevant columns
    df = pd.read_csv('data/soc-pokec-profiles.txt', 
                     sep='\t',
                     names=['user_id', 'public', 'completion_percentage', 'gender',
                           'region', 'last_login', 'registration', 'AGE', 'body',
                           'I_am_working_in_field', 'spoken_languages', 'hobbies',
                           'I_most_enjoy_good_food', 'pets', 'body_type', 'my_eyesight',
                           'eye_color', 'hair_color', 'hair_type', 'completed_level_of_education',
                           'favourite_color', 'relation_to_smoking', 'relation_to_alcohol',
                           'sign_in_zodiac', 'on_pokec_for', 'love_is_for_me', 'relation_to_casual_sex',
                           'my_partner_should_be', 'marital_status', 'children', 'relation_to_children',
                           'I_like_movies', 'I_like_watching_movie', 'I_like_music', 'I_mostly_like',
                           'the_idea_of_good_evening', 'I_like_specialties_from_kitchen',
                           'fun', 'I_am_going_to_concerts', 'my_active_sports',
                           'my_passive_sports', 'profession', 'I_like_books', 'life_style',
                           'music', 'cars', 'politics', 'relationships', 'art_culture',
                           'hobbies_interests', 'science_technologies', 'computers_internet',
                           'education', 'sport', 'movies', 'travelling', 'health',
                           'companies_brands', 'more'])
    
    # Convert and clean numeric columns with reasonable bounds
    df['AGE'] = pd.to_numeric(df['AGE'], errors='coerce')
    df.loc[(df['AGE'] < 10) | (df['AGE'] > 100), 'AGE'] = np.nan
    
    df['completion_percentage'] = pd.to_numeric(df['completion_percentage'], errors='coerce')
    df.loc[(df['completion_percentage'] < 0) | (df['completion_percentage'] > 100), 'completion_percentage'] = np.nan
    
    df['user_id'] = pd.to_numeric(df['user_id'], errors='coerce')
    
    print("Initial data shape:", df.shape)
    return df

def calculate_zscore_outliers(series):
    """Calculate number of outliers using z-score method"""
    clean_series = series.dropna()
    z_scores = np.abs(stats.zscore(clean_series))
    return len(clean_series[z_scores > 3])

def identify_outliers(df):
    """Identify outliers using multiple methods and provide justification"""
    print("Identifying outliers...")
    
    # 1. Age Outliers
    age_stats = {
        'mean': df['AGE'].mean(),
        'std': df['AGE'].std(),
        'q1': df['AGE'].quantile(0.25),
        'q3': df['AGE'].quantile(0.75),
        'iqr': df['AGE'].quantile(0.75) - df['AGE'].quantile(0.25)
    }
    
    age_outliers = {
        'zscore': calculate_zscore_outliers(df['AGE']),
        'iqr': len(df[
            (df['AGE'] < age_stats['q1'] - 1.5 * age_stats['iqr']) |
            (df['AGE'] > age_stats['q3'] + 1.5 * age_stats['iqr'])
        ].dropna())
    }
    
    # 2. Completion Percentage Outliers
    comp_stats = {
        'mean': df['completion_percentage'].mean(),
        'std': df['completion_percentage'].std(),
        'q1': df['completion_percentage'].quantile(0.25),
        'q3': df['completion_percentage'].quantile(0.75),
        'iqr': df['completion_percentage'].quantile(0.75) - df['completion_percentage'].quantile(0.25)
    }
    
    completion_outliers = {
        'zscore': calculate_zscore_outliers(df['completion_percentage']),
        'iqr': len(df[
            (df['completion_percentage'] < comp_stats['q1'] - 1.5 * comp_stats['iqr']) |
            (df['completion_percentage'] > comp_stats['q3'] + 1.5 * comp_stats['iqr'])
        ].dropna())
    }
    
    # 3. Identify sparse columns
    sparsity = (df.isnull().sum() / len(df) * 100).round(1)
    sparse_columns = sparsity[sparsity > 50].index.tolist()
    
    # 4. Analyze feature completeness
    feature_completeness = (1 - df.isnull().mean()) * 100
    
    return {
        'age_stats': age_stats,
        'age_outliers': age_outliers,
        'comp_stats': comp_stats,
        'completion_outliers': completion_outliers,
        'sparse_columns': sparse_columns,
        'sparsity': sparsity,
        'feature_completeness': feature_completeness
    }

def handle_outliers(df, outlier_info):
    """Handle outliers using appropriate methods"""
    print("Handling outliers...")
    
    df_cleaned = df.copy()
    
    # 1. Age Handling
    age_lower = max(10, outlier_info['age_stats']['q1'] - 1.5 * outlier_info['age_stats']['iqr'])
    age_upper = min(100, outlier_info['age_stats']['q3'] + 1.5 * outlier_info['age_stats']['iqr'])
    
    df_cleaned.loc[df_cleaned['AGE'] < age_lower, 'AGE'] = age_lower
    df_cleaned.loc[df_cleaned['AGE'] > age_upper, 'AGE'] = age_upper
    
    # 2. Completion Percentage Handling
    df_cleaned['low_completion_flag'] = df_cleaned['completion_percentage'] < 10
    
    # 3. Handle Sparse Features
    for col in outlier_info['sparse_columns']:
        df_cleaned[f'{col}_missing'] = df_cleaned[col].isnull()
    
    # 4. Create feature groups based on completeness
    completeness_groups = {
        'high_quality': [],
        'medium_quality': [],
        'low_quality': []
    }
    
    for col, completeness in outlier_info['feature_completeness'].items():
        if completeness >= 80:
            completeness_groups['high_quality'].append(col)
        elif completeness >= 50:
            completeness_groups['medium_quality'].append(col)
        else:
            completeness_groups['low_quality'].append(col)
    
    return df_cleaned, completeness_groups

def generate_visualizations(df, df_cleaned, outlier_info):
    """Generate visualizations for outlier analysis"""
    print("Generating visualizations...")
    
    # 1. Age Distribution Before and After
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    sns.boxplot(x=df['AGE'].dropna(), ax=ax1)
    ax1.set_title('Age Distribution (Before)')
    sns.boxplot(x=df_cleaned['AGE'].dropna(), ax=ax2)
    ax2.set_title('Age Distribution (After)')
    plt.tight_layout()
    plt.savefig('reports/figures/age_outliers.png')
    plt.close()
    
    # 2. Completion Percentage Distribution
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df['completion_percentage'].dropna())
    plt.title('Completion Percentage Distribution')
    plt.savefig('reports/figures/completion_distribution.png')
    plt.close()
    
    # 3. Feature Completeness Distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(data=outlier_info['feature_completeness'], bins=20)
    plt.title('Feature Completeness Distribution')
    plt.xlabel('Completeness (%)')
    plt.ylabel('Number of Features')
    plt.savefig('reports/figures/feature_completeness.png')
    plt.close()

def generate_report(df, df_cleaned, outlier_info, completeness_groups):
    """Generate a comprehensive report on outlier handling"""
    print("Generating report...")
    
    report = """# Outlier Analysis and Handling Report

## 1. Dataset Overview

Initial Analysis:
- Total Records: {total_records:,}
- Total Features: {total_features:,}
- Missing Value Percentage Range: {min_missing:.1f}% to {max_missing:.1f}%

## 2. Data Quality Assessment

### 2.1 Feature Quality Groups
High Quality Features (>80% complete):
{high_quality_features}

Medium Quality Features (50-80% complete):
{medium_quality_features}

Low Quality Features (<50% complete):
{low_quality_features}

### 2.2 Age Data
- Mean Age: {age_mean:.2f}
- Standard Deviation: {age_std:.2f}
- IQR Range: {age_q1:.1f} - {age_q3:.1f}
- Z-score Outliers: {age_zscore_outliers:,} records
- IQR Outliers: {age_iqr_outliers:,} records

### 2.3 Completion Percentage
- Mean Completion: {comp_mean:.2f}%
- Standard Deviation: {comp_std:.2f}%
- IQR Range: {comp_q1:.1f}% - {comp_q3:.1f}%
- Z-score Outliers: {comp_zscore_outliers:,} records
- IQR Outliers: {comp_iqr_outliers:,} records

## 3. Outlier Handling Strategy

### 3.1 Age Outliers
- Method: Capping at IQR boundaries (constrained to 10-100 years)
- Justification: 
  * Preserves data distribution while handling extreme values
  * More robust than z-score method for non-normal distributions
  * Maintains reasonable age ranges for analysis
  * Biological constraints applied (10-100 years)

### 3.2 Completion Percentage
- Method: Flagging extremely low values (<10%)
- Justification:
  * Low completion rates are valid data points
  * Flagging allows for separate analysis of low-engagement users
  * Preserves original data while enabling filtered analysis

### 3.3 Sparse Features
- Method: Feature flagging and quality grouping
- Justification:
  * Creates binary indicators for missing data
  * Groups features by quality for appropriate handling
  * Enables targeted analysis based on data quality

## 4. Impact Analysis

### 4.1 Age Distribution
- Before: Range {orig_age_min:.1f} - {orig_age_max:.1f}
- After: Range {clean_age_min:.1f} - {clean_age_max:.1f}
- Impact: More concentrated age distribution within biologically reasonable bounds

### 4.2 Data Quality Improvements
- Removed impossible age values
- Created {new_feature_count:,} new feature quality indicators
- Grouped features by completeness for targeted analysis

## 5. Recommendations

1. Feature Selection:
   - Primary analysis should focus on high-quality features
   - Medium-quality features should be used with appropriate missing data handling
   - Low-quality features should be excluded or used only for supplementary analysis

2. Age Analysis:
   - Use cleaned age values for demographic analysis
   - Consider age groups rather than exact ages
   - Pay special attention to boundary cases

3. Completion Rate Analysis:
   - Use low_completion_flag for segmentation
   - Investigate patterns in low-completion profiles
   - Consider completion rate in feature importance

4. Missing Data Strategy:
   - For high-quality features: imputation may be appropriate
   - For medium-quality features: use missing indicators
   - For low-quality features: consider excluding from primary analysis

## 6. Visualizations

The following visualizations have been generated in the reports/figures directory:
1. age_outliers.png - Age distribution before and after cleaning
2. completion_distribution.png - Completion percentage distribution
3. feature_completeness.png - Distribution of feature completeness

""".format(
        total_records=len(df),
        total_features=len(df.columns),
        min_missing=outlier_info['sparsity'].min(),
        max_missing=outlier_info['sparsity'].max(),
        high_quality_features='\n'.join(f'- {col}' for col in completeness_groups['high_quality']),
        medium_quality_features='\n'.join(f'- {col}' for col in completeness_groups['medium_quality']),
        low_quality_features='\n'.join(f'- {col}' for col in completeness_groups['low_quality']),
        age_mean=outlier_info['age_stats']['mean'],
        age_std=outlier_info['age_stats']['std'],
        age_q1=outlier_info['age_stats']['q1'],
        age_q3=outlier_info['age_stats']['q3'],
        age_zscore_outliers=outlier_info['age_outliers']['zscore'],
        age_iqr_outliers=outlier_info['age_outliers']['iqr'],
        comp_mean=outlier_info['comp_stats']['mean'],
        comp_std=outlier_info['comp_stats']['std'],
        comp_q1=outlier_info['comp_stats']['q1'],
        comp_q3=outlier_info['comp_stats']['q3'],
        comp_zscore_outliers=outlier_info['completion_outliers']['zscore'],
        comp_iqr_outliers=outlier_info['completion_outliers']['iqr'],
        orig_age_min=df['AGE'].min(),
        orig_age_max=df['AGE'].max(),
        clean_age_min=df_cleaned['AGE'].min(),
        clean_age_max=df_cleaned['AGE'].max(),
        new_feature_count=len(outlier_info['sparse_columns'])
    )
    
    # Save report
    with open('reports/outlier_analysis_report.txt', 'w') as f:
        f.write(report)

def main():
    print("Starting outlier analysis...")
    
    # Load data
    df = load_data()
    
    # Identify outliers
    outlier_info = identify_outliers(df)
    
    # Handle outliers
    df_cleaned, completeness_groups = handle_outliers(df, outlier_info)
    
    # Generate visualizations
    generate_visualizations(df, df_cleaned, outlier_info)
    
    # Generate report
    generate_report(df, df_cleaned, outlier_info, completeness_groups)
    
    print("Analysis complete! Check reports/outlier_analysis_report.txt for results.")

if __name__ == "__main__":
    main()
