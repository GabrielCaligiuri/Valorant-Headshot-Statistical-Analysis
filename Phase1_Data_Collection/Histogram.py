import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load clean data
df = pd.read_csv("cleanData.csv")

# Split populations
weekday = df[df["Time"] == "Weekday"]
weekend = df[df["Time"] == "Weekend"]



# Extract arrays
wd = weekday["unweighted_hs"].values
we = weekend["unweighted_hs"].values

# Weekday stats
wd_mean = np.mean(wd)
wd_var = np.var(wd, ddof=1)   # sample variance
wd_std = np.std(wd, ddof=1)   # sample std
wd_range = np.max(wd) - np.min(wd)

# Weekend stats
we_mean = np.mean(we)
we_var = np.var(we, ddof=1)   #sample variance
we_std = np.std(we, ddof=1)   #sample std
we_range = np.max(we) - np.min(we)

xmin = min(wd.min(), we.min())  #graph limits
xmax = max(wd.max(), we.max()) + 0.05  #graph limits, with 0.05 added for extra space

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))

# Weekday
ax1.set_xlim(xmin, xmax)
ax1.hist(wd, bins=30, density=True)
ax1.set_title("Weekday HS% Distribution")

ax1.text(0.02, 0.95,
         f"Mean = {wd_mean:.4f}\nVar = {wd_var:.6f}\nStd = {wd_std:.4f}\nRange = {wd_range:.4f}",
         transform=ax1.transAxes,
         verticalalignment='top')

# Weekend
ax2.set_xlim(xmin, xmax)
ax2.hist(we, bins=30, density=True)
ax2.set_title("Weekend HS% Distribution")

ax2.text(0.02, 0.95,
         f"Mean = {we_mean:.4f}\nVar = {we_var:.6f}\nStd = {we_std:.4f}\nRange = {we_range:.4f}",
         transform=ax2.transAxes,
         verticalalignment='top')

plt.tight_layout()
plt.show()