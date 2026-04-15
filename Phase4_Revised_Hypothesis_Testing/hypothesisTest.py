from scipy import stats
import pandas as pd
import numpy as np

#Written to not have to manually compute 2 sample t-test for 2700 samples.

df = pd.read_csv('Phase4_Samples.csv')
weekday = df[df['Time'] == 'Weekday']['unweighted_hs'].sample(n=2700, random_state=42)
weekend = df[df['Time'] == 'Weekend']['unweighted_hs'].sample(n=2700, random_state=42)

result = stats.ttest_ind(weekday, weekend, equal_var=False)
print(f"t = {result.statistic:.4f}, p = {result.pvalue:.4f}, df = {result.df:.4f}, x1 = {np.mean(weekday):.4f}, x2 = {np.mean(weekend):.4f}, Sx1 = {np.std(weekday):.4f}, Sx2 = {np.std(weekend):.4f}")