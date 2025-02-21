#!/usr/bin/env python3
"""
More flexible version of multi-label processing that better handles Slovak text variations.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re
from collections import defaultdict

def clean_text(text):
    """Clean text but preserve more potential matches"""
    if pd.isna(text) or text == 'null':
        return []
    
    # Convert to lowercase
    text = str(text).lower()
    
    # Remove special characters but keep letters with diacritics
    text = re.sub(r'[^a-záäéíóôúýčďĺľňŕšťž\s,;-]', ' ', text)
    
    # Split on common separators and clean
    items = []
    for item in re.split(r'[,;]', text):
        item = item.strip()
        if len(item) > 1:  # Keep items longer than 1 character
            items.append(item)
    
    return items

def get_hobby_keywords():
    """Define hobby categories with more Slovak variations"""
    return {
        'sport': ['sport', 'futbal', 'basketbal', 'volejbal', 'tenis', 'hokej', 'fitness', 
                 'behanie', 'plavanie', 'sportovanie', 'futbalovy', 'basketbalovy', 'hokejovy'],
        'music': ['hudba', 'spev', 'gitara', 'klavir', 'spievanie', 'koncerty', 'hudby', 
                 'spievam', 'hudobny', 'gitare', 'klaviri', 'koncertoch'],
        'reading': ['citanie', 'knihy', 'literatura', 'citat', 'knih', 'literarny'],
        'movies': ['filmy', 'kino', 'serial', 'filmov', 'serialy', 'filmare', 'kinach'],
        'travel': ['cestovanie', 'turistika', 'cestovat', 'cestuje', 'turista', 'cestovatel'],
        'art': ['umenie', 'malovanie', 'kresba', 'fotenie', 'fotografovanie', 'malovat', 
               'kreslit', 'fotit', 'umeni', 'umelecky'],
        'computers': ['pocitace', 'programovanie', 'hry', 'gaming', 'internet', 'pc', 
                    'notebook', 'programator', 'herne', 'online'],
        'food': ['varenie', 'jedlo', 'gastonomia', 'pecenie', 'varit', 'kuchyna', 
                'gastronomie', 'kucharske', 'peciem'],
        'nature': ['priroda', 'zahrada', 'zvierata', 'turistika', 'prirode', 'zahradka', 
                 'zvieratka', 'prirodny'],
        'social': ['priatelia', 'party', 'zabava', 'tanec', 'disco', 'zabavat', 
                 'kamarati', 'parties', 'diskoteky', 'tanecny'],
        'sports_extreme': ['skateboard', 'snowboard', 'bike', 'adrenalin', 'extreme', 
                         'skating', 'biking', 'adrenalinu'],
        'education': ['studium', 'ucenie', 'skola', 'vzdelavanie', 'student', 'ucit', 
                    'skolsky', 'vzdelavaci'],
        'cars': ['auta', 'motocykle', 'mechanika', 'auto', 'moto', 'automobily', 
               'motorkarske', 'mechanik'],
        'shopping': ['nakupovanie', 'moda', 'oblecenie', 'nakupovat', 'nakupy', 
                   'modne', 'obliekanie']
    }

def get_language_keywords():
    """Define language mappings with more variations"""
    return {
        'slovak': ['slovensky', 'slovencina', 'slovensky jazyk', 'slovensky hovorim', 
                 'slovenska rec', 'slovensky perfektne'],
        'english': ['anglicky', 'anglictina', 'english', 'aj', 'eng', 'anglicky jazyk'],
        'german': ['nemecky', 'nemcina', 'deutsch', 'nj', 'nemecky jazyk', 'po nemecky'],
        'czech': ['cesky', 'cestina', 'cj', 'cesky jazyk', 'po cesky'],
        'hungarian': ['madarsky', 'madarcina', 'madarsky jazyk', 'po madarsky'],
        'french': ['francuzsky', 'francuzstina', 'fj', 'francuzsky jazyk'],
        'russian': ['rusky', 'rustina', 'rj', 'rusky jazyk', 'po rusky'],
        'spanish': ['spanielsky', 'spanielcina', 'sj', 'spanielsky jazyk'],
        'italian': ['taliansky', 'taliancina', 'tj', 'taliansky jazyk'],
        'polish': ['polsky', 'polstina', 'pj', 'polsky jazyk']
    }

def find_matches(text_list, category_keywords):
    """Find matches using more flexible matching"""
    matches = set()
    
    for text in text_list:
        text = ' ' + text + ' '  # Add spaces to help with word boundaries
        for category, keywords in category_keywords.items():
            if any(f' {keyword} ' in text for keyword in keywords):
                matches.add(category)
            # Try partial matches for longer strings
            elif len(text) > 10 and any(keyword in text for keyword in keywords):
                matches.add(category)
    
    return list(matches)

def main():
    print("Loading data...")
    
    # Create necessary directories
    Path("data").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    
    # Read data
    df = pd.read_csv('data/soc-pokec-profiles.txt', 
                     sep='\t',
                     names=range(60),
                     usecols=[11, 10],  # hobbies and languages columns
                     nrows=10000)
    
    # Rename columns
    df.columns = ['hobbies', 'languages']
    
    print("\nProcessing hobbies...")
    df['hobbies_clean'] = df['hobbies'].apply(clean_text)
    df['hobby_categories'] = df['hobbies_clean'].apply(
        lambda x: find_matches(x, get_hobby_keywords())
    )
    
    print("Processing languages...")
    df['languages_clean'] = df['languages'].apply(clean_text)
    df['language_categories'] = df['languages_clean'].apply(
        lambda x: find_matches(x, get_language_keywords())
    )
    
    # Create binary columns
    print("\nCreating binary columns...")
    
    # For hobbies
    hobby_cols = pd.DataFrame()
    all_hobbies = set().union(*df['hobby_categories'])
    for hobby in sorted(all_hobbies):
        hobby_cols[f'hobby_{hobby}'] = df['hobby_categories'].apply(lambda x: hobby in x)
    
    # For languages
    lang_cols = pd.DataFrame()
    all_languages = set().union(*df['language_categories'])
    for lang in sorted(all_languages):
        lang_cols[f'language_{lang}'] = df['language_categories'].apply(lambda x: lang in x)
    
    # Combine all columns
    df_encoded = pd.concat([df, hobby_cols, lang_cols], axis=1)
    
    # Generate report
    print("\nGenerating report...")
    report = []
    report.append("# Multi-label Column Processing Report\n")
    
    # Hobby statistics
    report.append("## Hobbies Analysis")
    report.append(f"Total unique hobby categories: {len(all_hobbies)}")
    report.append("Categories:")
    
    for hobby in sorted(all_hobbies):
        count = df_encoded[f'hobby_{hobby}'].sum()
        percentage = (count / len(df)) * 100
        report.append(f"- {hobby}: {int(count):,} profiles ({percentage:.1f}%)")
    
    # Language statistics
    report.append("\n## Languages Analysis")
    report.append(f"Total unique languages: {len(all_languages)}")
    report.append("Languages:")
    
    for lang in sorted(all_languages):
        count = df_encoded[f'language_{lang}'].sum()
        percentage = (count / len(df)) * 100
        report.append(f"- {lang}: {int(count):,} profiles ({percentage:.1f}%)")
    
    # Additional statistics
    report.append("\n## Additional Statistics")
    report.append(f"Total profiles analyzed: {len(df):,}")
    report.append(f"Profiles with hobbies: {len(df[df['hobby_categories'].str.len() > 0]):,}")
    report.append(f"Profiles with languages: {len(df[df['language_categories'].str.len() > 0]):,}")
    
    # Save results
    print("\nSaving results...")
    df_encoded.to_parquet('data/multilabel_encoded_flexible.parquet')
    with open('reports/multilabel_report_flexible.md', 'w') as f:
        f.write('\n'.join(report))
    
    print("\nResults saved to:")
    print("- data/multilabel_encoded_flexible.parquet")
    print("- reports/multilabel_report_flexible.md")
    
    # Print sample
    print("\nSample of encoded data (first 5 rows):")
    print("\nHobby columns:")
    print(df_encoded[[col for col in df_encoded.columns if col.startswith('hobby_')]].head())
    print("\nLanguage columns:")
    print(df_encoded[[col for col in df_encoded.columns if col.startswith('language_')]].head())

if __name__ == "__main__":
    main()
