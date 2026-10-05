import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

fig = plt.figure(figsize=(12, 8))

#PANDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Data_Read = pd.read_csv(r"FILE.csv", header=None)
depths = Data_Read.iloc[:,1].values

plt.hist(depths, bins=50, color='orange', edgecolor='black', label="Mean Range = 907.743mm")
plt.xlabel("Projected Range (mm)")
plt.ylabel("Ion Count")
plt.title("Ion Range Distribution")
plt.tight_layout()
plt.legend()
#plt.show()

plt.savefig("Range Histogram.png", dpi = fig.dpi)

mean_range = sum(depths) / len(depths)

print(mean_range)