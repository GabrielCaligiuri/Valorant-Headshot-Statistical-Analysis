# Valorant-Headshot-Statistical-Analysis
Statistical analysis of 20,000 Valorant matches comparing weekday vs weekend headshot percentages across 4 phases using Python, pandas, numpy, and scipy.

This project investigates whether a meaningful difference exists between weekday and weekend headshot percentages among high ranked Valorant players. Match data was collected from 20,000 matches via the Riot Games API and Henrik's API and analyzed across 4 phases covering distribution analysis, confidence interval estimation, and hypothesis testing with power analysis. 

To recreate these tests I've provided the cleaned dataset. Raw data including leaderboard info and player identifiers has been excluded to preserve player privacy.

All statistical analysis was conducted using unweighted match data. A weighted approach was considered as an earlier approach but excluded as it did not provide any additional value for comparing distributions of the populations.

# Findings
No statistically significant difference was found between weekday and weekend headshot percentages, even after increasing sample size to achieve 80% statistical power.