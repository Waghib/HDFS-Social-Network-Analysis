#!/usr/bin/env python3
"""
Complete pipeline for processing and encoding the social network profiles data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re
from sklearn.preprocessing import LabelEncoder
from category_encoders import TargetEncoder
import warnings
warnings.filterwarnings('ignore')

def load_raw_data():
    """Load the raw data from soc-pokec-profiles.txt"""
    print("Loading raw data...")
    
    # Define column names based on the dataset description
    columns = [
        'user_id', 'public', 'completion_percentage', 'gender', 'region',
        'last_login', 'registration', 'AGE', 'body', 'I_am_working_in_field',
        'spoken_languages', 'hobbies', 'I_most_enjoy_good_food', 'pets',
        'body_type', 'my_eyesight', 'eye_color', 'hair_color', 'hair_type',
        'completed_level_of_education', 'favourite_color', 'relation_to_smoking',
        'relation_to_alcohol', 'sign_in_zodiac', 'on_pokec_for', 'love_is_for_me',
        'relation_to_casual_sex', 'my_partner_should_be', 'marital_status',
        'children', 'relation_to_children', 'I_like_movies', 'I_like_watching_movie',
        'I_like_music', 'I_mostly_like_listening_to_music', 'the_idea_of_good_evening',
        'I_like_specialties_from_kitchen', 'fun', 'I_am_going_to_concerts',
        'my_active_sports', 'my_passive_sports', 'profession', 'I_like_books',
        'life_style', 'music', 'cars', 'politics', 'relationships', 'art_culture',
        'hobbies_interests', 'science_technologies', 'computers_internet',
        'education', 'sport', 'movies', 'travelling', 'health', 'companies_brands',
        'more'
    ]
    
    # Read the data
    df = pd.read_csv('data/soc-pokec-profiles.txt', sep='\t', names=columns)
    return df

def clean_text(text):
    """Clean text data by removing special characters and normalizing"""
    if pd.isna(text) or not isinstance(text, str):
        return 'MISSING'
    
    # Remove special characters and normalize whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Handle empty or meaningless values
    if not text or text.lower() in ['none', 'nan', 'null', 'missing', '']:
        return 'MISSING'
    
    return text.lower()

def standardize_categories(df, column):
    """Standardize categories by grouping similar values"""
    if column not in df.columns:
        return df
    
    # Common mappings for each column
    mappings = {
        'gender': {
            r'.*\b(male|man|boy|m)\b.*': 'male',
            r'.*\b(female|woman|girl|f)\b.*': 'female',
            r'.*\b(other|diverse|non-binary)\b.*': 'other'
        },
        'region': {
            r'.*\b(bratislava)\b.*': 'bratislava',
            r'.*\b(kosice)\b.*': 'kosice',
            r'.*\b(prague)\b.*': 'prague',
            r'.*\b(brno)\b.*': 'brno',
            r'.*\b(nitra)\b.*': 'nitra',
            r'.*\b(zilina)\b.*': 'zilina'
        },
        'eye_color': {
            r'.*\b(blue|modre)\b.*': 'blue',
            r'.*\b(brown|hnede)\b.*': 'brown',
            r'.*\b(green|zelene)\b.*': 'green',
            r'.*\b(hazel|grey|sive)\b.*': 'hazel',
            r'.*\b(black|cierne)\b.*': 'black'
        }
    }
    
    if column in mappings:
        # Create a copy of the column
        df[column] = df[column].astype(str).str.lower()
        
        # Apply mappings
        for pattern, replacement in mappings[column].items():
            df.loc[df[column].str.contains(pattern, regex=True, na=False), column] = replacement
        
        # Set remaining values to 'other'
        known_categories = set(mappings[column].values())
        df.loc[~df[column].isin(known_categories), column] = 'other'
    
    return df

def encode_categorical_variables(df):
    """Encode categorical variables using appropriate methods"""
    # Columns to encode
    categorical_cols = ['gender', 'region', 'eye_color']
    
    # Initialize encoders dictionary
    encoders = {}
    
    # Clean and standardize categories
    print("Cleaning and standardizing categories...")
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
            df = standardize_categories(df, col)
    
    # Create encoded dataframe
    df_encoded = df.copy()
    
    # One-hot encoding for gender (low cardinality)
    print("Applying one-hot encoding to gender...")
    if 'gender' in df.columns:
        gender_dummies = pd.get_dummies(df['gender'], prefix='gender')
        df_encoded = pd.concat([df_encoded, gender_dummies], axis=1)
        encoders['gender'] = {'type': 'onehot', 'categories': list(gender_dummies.columns)}
    
    # Target encoding for region (high cardinality)
    print("Applying target encoding to region...")
    if 'region' in df.columns and 'completion_percentage' in df.columns:
        # Convert completion_percentage to numeric
        df_encoded['completion_percentage'] = pd.to_numeric(df_encoded['completion_percentage'], errors='coerce')
        df_encoded['completion_percentage'] = df_encoded['completion_percentage'].fillna(df_encoded['completion_percentage'].mean())
        
        target_encoder = TargetEncoder(cols=['region'], handle_missing='value')
        df_encoded['region_encoded'] = target_encoder.fit_transform(df[['region']], df_encoded['completion_percentage'])
        encoders['region'] = {'type': 'target', 'encoder': target_encoder}
    
    # Label encoding for eye_color (medium cardinality)
    print("Applying label encoding to eye_color...")
    if 'eye_color' in df.columns:
        label_encoder = LabelEncoder()
        df_encoded['eye_color_encoded'] = label_encoder.fit_transform(df['eye_color'])
        encoders['eye_color'] = {'type': 'label', 'encoder': label_encoder}
    
    return df_encoded, encoders

def generate_encoding_report(df_original, df_encoded, encoders):
    """Generate a detailed report of the encoding process"""
    report = "# Categorical Encoding Report\n\n"
    
    # Original data statistics
    report += "## Original Data Statistics\n\n"
    for col in ['gender', 'region', 'eye_color']:
        if col in df_original.columns:
            value_counts = df_original[col].value_counts()
            report += f"\n### {col.title()} Distribution:\n"
            report += f"- Total unique values: {len(value_counts)}\n"
            report += "- Top 5 most common values:\n"
            for val, count in value_counts.head().items():
                report += f"  - {val}: {count} ({count/len(df_original)*100:.1f}%)\n"
    
    # Encoded data statistics
    report += "\n## Encoded Data Statistics\n\n"
    
    # Gender (one-hot)
    if 'gender' in encoders:
        report += "### Gender (One-hot Encoding)\n"
        gender_cols = [col for col in df_encoded.columns if col.startswith('gender_')]
        for col in gender_cols:
            count = df_encoded[col].sum()
            report += f"- {col}: {count} records ({count/len(df_encoded)*100:.1f}%)\n"
    
    # Region (target)
    if 'region' in encoders:
        report += "\n### Region (Target Encoding)\n"
        region_stats = df_encoded['region_encoded'].describe()
        report += f"- Mean encoded value: {region_stats['mean']:.3f}\n"
        report += f"- Std encoded value: {region_stats['std']:.3f}\n"
        report += f"- Min encoded value: {region_stats['min']:.3f}\n"
        report += f"- Max encoded value: {region_stats['max']:.3f}\n"
    
    # Eye color (label)
    if 'eye_color' in encoders:
        report += "\n### Eye Color (Label Encoding)\n"
        eye_color_stats = df_encoded['eye_color_encoded'].describe()
        report += f"- Number of unique categories: {len(encoders['eye_color']['encoder'].classes_)}\n"
        report += f"- Categories: {', '.join(encoders['eye_color']['encoder'].classes_)}\n"
    
    # Memory usage comparison
    original_memory = df_original.memory_usage(deep=True).sum() / 1024 / 1024  # MB
    encoded_memory = df_encoded.memory_usage(deep=True).sum() / 1024 / 1024  # MB
    
    report += f"\n## Memory Usage\n"
    report += f"- Original data: {original_memory:.2f} MB\n"
    report += f"- Encoded data: {encoded_memory:.2f} MB\n"
    report += f"- Memory increase: {((encoded_memory/original_memory - 1) * 100):.1f}%\n"
    
    return report

def main():
    # Create necessary directories
    Path("data").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    
    # Load raw data
    df = load_raw_data()
    print(f"Loaded raw dataset with shape: {df.shape}")
    
    # Encode categorical variables
    print("Encoding categorical variables...")
    df_encoded, encoders = encode_categorical_variables(df)
    
    # Generate report
    print("Generating encoding report...")
    report = generate_encoding_report(df, df_encoded, encoders)
    
    # Save results
    print("Saving results...")
    df_encoded.to_parquet('data/profiles_encoded_final.parquet')
    with open('reports/categorical_encoding_report_final.md', 'w') as f:
        f.write(report)
    
    print("\nEncoding complete!")
    print("- Encoded data saved as data/profiles_encoded_final.parquet")
    print("- Report saved as reports/categorical_encoding_report_final.md")

if __name__ == "__main__":
    main()
