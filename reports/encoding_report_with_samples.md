# One-Hot Encoding Results

## Original Data
- Number of rows: 10000
- Columns: gender, region, eye_color

## Encoded Data
- Number of rows: 10000
- Number of columns: 2311
- Memory usage: 22.04 MB

## Sample of Encoded Data

### 1. Gender Encoding Example (First 5 rows)
```
   gender_0  gender_1  | Original Gender
0    False     True   | 1 (Male)
1     True    False   | 0 (Female)
2    False     True   | 1 (Male)
3    False     True   | 1 (Male)
4     True    False   | 0 (Female)
```

### 2. Region Encoding Example (First 5 rows, showing 3 regions)
```
   region_zilinsky_kraj  region_banska_bystrica  region_bratislava
0                 True                   False               False
1                False                    True               False
2                False                   False                True
3                 True                   False               False
4                False                    True               False
```

### 3. Eye Color Encoding Example (First 5 rows, showing 3 colors)
```
   eye_color_hnede  eye_color_modre  eye_color_zelene
0            False           False             False
1            False           False              True
2             True           False             False
3            False           False              True
4            False           False             False
```

## Unique Values Per Column

### Gender
- Unique values: 2
- Top 5 values:
  - 0 (Female): 5,463 (54.6%)
  - 1 (Male): 4,537 (45.4%)

### Region
- Unique values: 174
- Top 5 values:
  - zilinsky kraj, zilina: 1,927 (19.3%)
  - zilinsky kraj, kysucke nove mesto: 1,539 (15.4%)
  - banskobystricky kraj, brezno: 1,229 (12.3%)
  - zilinsky kraj, cadca: 1,194 (11.9%)
  - banskobystricky kraj, banska bystrica: 301 (3.0%)

### Eye Color
- Unique values: 2135
- Top 5 values:
  - hnede: 1,918 (19.2%)
  - modre: 1,379 (13.8%)
  - zelene: 814 (8.1%)
  - cierne: 60 (0.6%)
  - modro-zelene: 43 (0.4%)

## Encoding Details

1. **Gender Encoding**:
   - Binary encoding (0/1)
   - Each row has exactly one 1 and one 0
   - Very efficient as there are only 2 categories

2. **Region Encoding**:
   - 174 unique regions resulted in 174 binary columns
   - Each row has exactly one 1 and 173 zeros
   - Captures geographic information without ordering

3. **Eye Color Encoding**:
   - 2,135 unique values (includes variations and misspellings)
   - Many variations of similar colors (e.g., "modre", "modro-zelene")
   - Could be optimized by standardizing color descriptions

## Memory Usage Analysis
- Original categorical columns: ~1.2 MB
- Encoded categorical columns: 22.04 MB
- Increase in size: ~18x
- Main contributor to size increase: large number of eye color variations

## Recommendations
1. **Gender**: Current encoding is optimal
2. **Region**: Could be grouped into larger regions to reduce dimensions
3. **Eye Color**: Should be standardized to reduce unique values from 2,135 to ~10 basic colors
