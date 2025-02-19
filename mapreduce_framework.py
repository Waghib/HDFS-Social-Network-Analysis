from abc import ABC, abstractmethod
from collections import defaultdict
import multiprocessing as mp
from typing import Iterator, List, Tuple, Any, Dict
import pandas as pd
import numpy as np
from datetime import datetime

class MapReduceFramework:
    def __init__(self, n_workers: int = None):
        self.n_workers = n_workers or mp.cpu_count()

    def run(self, mapper_class, reducer_class, input_data: pd.DataFrame) -> Dict:
        # Initialize mapper and reducer
        mapper = mapper_class()
        reducer = reducer_class()
        
        # Partition data for parallel processing
        chunks = np.array_split(input_data, self.n_workers)
        
        # Run map phase in parallel
        with mp.Pool(self.n_workers) as pool:
            mapped_results = pool.map(mapper.map, chunks)
        
        # Combine mapped results
        combined_results = defaultdict(list)
        for result in mapped_results:
            for key, values in result.items():
                combined_results[key].extend(values)
        
        # Run reduce phase
        final_results = {}
        for key, values in combined_results.items():
            final_results[key] = reducer.reduce(key, values)
            
        return final_results

class Mapper(ABC):
    @abstractmethod
    def map(self, chunk: pd.DataFrame) -> Dict[Any, List]:
        pass

class Reducer(ABC):
    @abstractmethod
    def reduce(self, key: Any, values: List) -> Any:
        pass

# Utility functions
def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime object."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
    except (ValueError, TypeError):
        return None

def calculate_completion_percentage(row: pd.Series) -> float:
    """Calculate profile completion percentage."""
    non_null_count = row.notna().sum()
    total_fields = len(row)
    return (non_null_count / total_fields) * 100

def process_multi_label_field(field: str) -> List[str]:
    """Process multi-label fields like hobbies and languages."""
    if pd.isna(field):
        return []
    return [item.strip() for item in field.split(',')]
