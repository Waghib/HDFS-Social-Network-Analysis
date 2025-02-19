import pandas as pd
import numpy as np
from collections import defaultdict
from mapreduce_framework import Mapper, Reducer, MapReduceFramework
from typing import Dict, List, Any

class DemographicMapper(Mapper):
    def map(self, chunk: pd.DataFrame) -> Dict[str, List]:
        results = {
            'age_stats': [],
            'gender_counts': [],
            'region_counts': [],
            'completion_rates': []
        }
        
        # Age analysis
        age_data = chunk.iloc[:, 2].dropna()
        results['age_stats'].extend(age_data.values)
        
        # Gender analysis (column 1)
        gender_counts = chunk.iloc[:, 1].value_counts()
        for gender, count in gender_counts.items():
            results['gender_counts'].append((gender, count))
        
        # Region analysis (column 4)
        region_counts = chunk.iloc[:, 4].value_counts()
        for region, count in region_counts.items():
            results['region_counts'].append((region, count))
        
        # Calculate completion rates
        chunk['completion_rate'] = chunk.apply(lambda row: (row.notna().sum() / len(row)) * 100, axis=1)
        results['completion_rates'].extend(chunk['completion_rate'].values)
        
        return results

class DemographicReducer(Reducer):
    def reduce(self, key: str, values: List) -> Dict:
        if key == 'age_stats':
            return {
                'mean': np.mean(values),
                'median': np.median(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values)
            }
        elif key in ['gender_counts', 'region_counts']:
            counts = defaultdict(int)
            for val, count in values:
                counts[val] += count
            return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
        elif key == 'completion_rates':
            return {
                'mean': np.mean(values),
                'median': np.median(values),
                'std': np.std(values)
            }
        return {}
