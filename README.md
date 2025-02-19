# HDFS Social Network Analysis

This project implements MapReduce-based analysis of the Pokec social network profiles dataset using Apache Hadoop.

## Prerequisites

- Apache Hadoop 3.4.1
- Python 3.x
- Required Python packages: `numpy`, `pandas`, `matplotlib`, `seaborn`, `scikit-learn`

## Project Structure

```
.
├── hadoop/
│   ├── demographic_mapper.py    # Mapper for demographic analysis
│   ├── demographic_reducer.py   # Reducer for demographic analysis
│   ├── correlation_mapper.py    # Mapper for correlation analysis
│   └── correlation_reducer.py   # Reducer for correlation analysis
├── results/                    # Directory containing analysis results
│   └── demographic_analysis.json # Demographic analysis results
├── run_hadoop_analysis.sh       # Script to run Hadoop jobs
├── soc-pokec-profiles.txt      # Input data file
└── README.md
```

## Features

1. **Demographic Analysis**
   - Age distribution statistics
   - Gender distribution
   - Regional distribution
   - Profile completion rates

2. **Correlation Analysis**
   - Correlation between age and profile completion
   - Average completion rates by gender
   - Average completion rates by region

## Running the Analysis

1. Ensure Hadoop services are running:
   ```bash
   start-dfs.sh
   start-yarn.sh
   ```

2. Make the scripts executable:
   ```bash
   chmod +x run_hadoop_analysis.sh
   chmod +x hadoop/*.py
   ```

3. Run the analysis:
   ```bash
   ./run_hadoop_analysis.sh
   ```

## Viewing Results

The analysis results are stored in two locations:

1. HDFS (Hadoop Distributed File System):
   ```bash
   # View demographic analysis results
   hadoop fs -cat /user/pokec/output/demographics/part-00000
   ```

2. Local filesystem:
   ```bash
   # View demographic analysis results
   cat results/demographic_analysis.json
   ```

The results are stored in JSON format and contain detailed statistics about:
- User demographics (age, gender, region)
- Profile completion rates
- Regional distribution
- Overall summary statistics

3. Run the analysis:
   ```bash
   ./run_hadoop_analysis.sh
   ```

## Output

The analysis results will be stored in HDFS under `/user/pokec/output/` with two subdirectories:
- `demographics/`: Contains demographic analysis results
- `correlations/`: Contains correlation analysis results

## Implementation Details

### MapReduce Jobs

1. **Demographic Analysis**
   - Mapper: Processes each profile and emits key-value pairs for age, gender, and region statistics
   - Reducer: Aggregates statistics and calculates distributions

2. **Correlation Analysis**
   - Mapper: Emits profile completion percentages paired with various attributes
   - Reducer: Calculates correlations and category-wise averages

### Data Processing

- Handles missing values and data cleaning
- Calculates profile completion percentages
- Performs statistical analysis using MapReduce paradigm
- Supports large-scale data processing through Hadoop's distributed computing
