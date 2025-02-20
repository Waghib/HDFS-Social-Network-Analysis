# User Clustering Analysis Report

## Executive Summary
This report presents the findings from our MapReduce-based clustering analysis of the Pokec social network dataset. We analyzed over 1.6 million user profiles, focusing on the relationship between user age and profile completion rates. The analysis revealed five distinct user segments, each with unique characteristics and engagement patterns.

## Methodology
- Implemented a distributed clustering algorithm using MapReduce
- Features analyzed: User age and profile completion percentage
- Total profiles analyzed: 1,632,803
- Clustering approach: Distance-based clustering with 5 clusters

## User Segments Analysis

### 1. Young Users (Cluster 0)
- **Size**: 487,178 members (29.8% of users)
- **Age Range**: 0-43 years (mean: 17.42 ± 9.31)
- **Completion Rate**: 11.35% ± 10.01%
- **Key Characteristics**:
  * Largest youth segment
  * Lowest profile completion rates
  * High variability in engagement

### 2. Middle-Aged Active Users (Cluster 1)
- **Size**: 56,754 members (3.5% of users)
- **Age Range**: 45-52 years (mean: 48.51 ± 2.40)
- **Completion Rate**: 44.56% ± 2.60%
- **Key Characteristics**:
  * Most consistent engagement levels
  * Moderate profile completion
  * Narrow age range

### 3. Mixed Age Group (Cluster 2)
- **Size**: 771,789 members (47.3% of users)
- **Age Range**: 0-100 years (mean: 41.29 ± 22.51)
- **Completion Rate**: 36.93% ± 24.15%
- **Key Characteristics**:
  * Largest cluster
  * Highly diverse age range
  * Variable completion rates

### 4. Senior Active Users (Cluster 3)
- **Size**: 280,158 members (17.2% of users)
- **Age Range**: 60-76 years (mean: 67.14 ± 4.29)
- **Completion Rate**: 64.67% ± 4.57%
- **Key Characteristics**:
  * High engagement levels
  * Consistent profile maintenance
  * Significant segment size

### 5. Senior Power Users (Cluster 4)
- **Size**: 36,924 members (2.2% of users)
- **Age Range**: 78-100 years (mean: 82.57 ± 4.70)
- **Completion Rate**: 81.27% ± 5.11%
- **Key Characteristics**:
  * Highest completion rates
  * Most engaged user segment
  * Smallest but most dedicated group

## Key Findings

1. **Age-Completion Correlation**
   - Strong positive correlation between age and profile completion
   - Older users consistently maintain more complete profiles
   - Younger users show lower engagement with profile completion

2. **Engagement Patterns**
   - Clear segmentation by age and engagement level
   - Most users fall into either young low-engagement or mixed middle-age groups
   - Senior users show highest engagement despite smaller population

3. **User Distribution**
   - Mixed age group dominates (47.3%)
   - Young users form second-largest segment (29.8%)
   - Senior segments combined represent significant portion (19.4%)

## Recommendations

1. **Youth Engagement**
   - Develop targeted features for users under 43
   - Implement engagement strategies to increase profile completion
   - Consider gamification elements for younger users

2. **Middle-Age Retention**
   - Focus on converting moderate users to high-engagement
   - Provide tools for professional networking
   - Enhance features valued by this consistent user base

3. **Senior User Support**
   - Maintain and enhance features used by senior users
   - Consider accessibility improvements
   - Leverage high-engagement users for community building

4. **Platform Development**
   - Design age-appropriate interfaces for each segment
   - Implement features that encourage profile completion
   - Consider segment-specific content and interactions

## Conclusion
The clustering analysis reveals clear patterns in user engagement based on age. This segmentation provides valuable insights for targeted feature development and marketing strategies. The platform should focus on increasing engagement among younger users while maintaining the high engagement levels of senior users.

## Overview
This report presents the results of K-means clustering analysis performed on user profiles from the Pokec dataset. The clustering was based on two key features:
1. User Age
2. Profile Completion Percentage

## Methodology
- Used K-means clustering algorithm with 5 clusters
- Features were standardized before clustering
- Analysis performed on a representative sample of users

## Cluster Characteristics


### Cluster 0
- **Size**: 2660 users
- **Age Range**: 60.0 - 72.0 years
- **Average Age**: 66.5 ± 3.8 years
- **Completion Rate**: 63.9% ± 4.0%

### Cluster 1
- **Size**: 3840 users
- **Age Range**: 0.0 - 22.0 years
- **Average Age**: 13.1 ± 2.5 years
- **Completion Rate**: 6.7% ± 2.6%

### Cluster 2
- **Size**: 1312 users
- **Age Range**: 24.0 - 43.0 years
- **Average Age**: 33.9 ± 5.9 years
- **Completion Rate**: 29.0% ± 6.4%

### Cluster 3
- **Size**: 538 users
- **Age Range**: 74.0 - 100.0 years
- **Average Age**: 79.8 ± 5.2 years
- **Completion Rate**: 78.3% ± 5.6%

### Cluster 4
- **Size**: 1650 users
- **Age Range**: 45.0 - 59.0 years
- **Average Age**: 52.8 ± 4.5 years
- **Completion Rate**: 49.2% ± 4.8%

## Visualizations
The following visualizations have been generated:

1. **User Clusters** (`user_clusters.png`):
   - Scatter plot showing the distribution of users across clusters
   - Red X marks indicate cluster centers
   - Different colors represent different clusters

2. **Age Distribution** (`cluster_age_distribution.png`):
   - Box plots showing the age distribution within each cluster
   - Helps identify age-based patterns across clusters

3. **Completion Distribution** (`cluster_completion_distribution.png`):
   - Box plots showing the profile completion distribution within each cluster
   - Helps identify completion rate patterns across clusters

## Key Findings
1. Age and profile completion show distinct clustering patterns
2. Different age groups exhibit varying levels of profile completion
3. Clusters reveal natural user segments based on these characteristics

## Implications
1. User segmentation can be used for targeted feature development
2. Different engagement strategies might be needed for different clusters
3. Age-specific UI/UX considerations could be valuable
