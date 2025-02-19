import pandas as pd
import numpy as np
from collections import defaultdict
from mapreduce_framework import Mapper, Reducer, MapReduceFramework
from typing import Dict, List, Any

class CorrelationMapper(Mapper):
    def map(self, chunk: pd.DataFrame) -> Dict[str, List]:
        results = defaultdict(list)
        
        # Calculate completion percentage for each profile
        chunk['completion_rate'] = chunk.apply(lambda row: (row.notna().sum() / len(row)) * 100, axis=1)
        
        # Analyze correlations with numerical features
        numerical_cols = [2]  # Age column
        for col in numerical_cols:
            valid_data = chunk[chunk.iloc[:, col].notna()]
            results['numerical_corr'].append((col, 
                np.corrcoef(valid_data.iloc[:, col], valid_data['completion_rate'])[0, 1]))
        
        # Analyze categorical features
        categorical_cols = [1, 4]  # Gender and region columns
        for col in categorical_cols:
            group_stats = chunk.groupby(chunk.iloc[:, col])['completion_rate'].agg(['mean', 'count'])
            for category, stats in group_stats.iterrows():
                results['categorical_stats'].append((col, category, stats['mean'], stats['count']))
        
        return results

class CorrelationReducer(Reducer):
    def reduce(self, key: str, values: List) -> Dict:
        if key == 'numerical_corr':
            # Average correlation coefficients
            corr_dict = defaultdict(list)
            for col, corr in values:
                corr_dict[col].append(corr)
            return {col: np.mean(corrs) for col, corrs in corr_dict.items()}
        
        elif key == 'categorical_stats':
            # Combine category statistics
            stats_dict = defaultdict(lambda: defaultdict(lambda: {'sum': 0, 'count': 0}))
            for col, category, mean, count in values:
                stats_dict[col][category]['sum'] += mean * count
                stats_dict[col][category]['count'] += count
            
            # Calculate final averages
            result = {}
            for col, categories in stats_dict.items():
                result[col] = {
                    cat: stats['sum'] / stats['count']
                    for cat, stats in categories.items()
                }
            return result
        
        return {}
