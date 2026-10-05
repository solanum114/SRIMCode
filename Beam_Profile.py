import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

fig = plt.figure(figsize=(12, 8))

#PANDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Data_Read = pd.read_csv(r"FILE.csv", header=None)
y_vals= Data_Read.iloc[:,1].values
z_vals= Data_Read.iloc[:,3].values

y_vals = np.array(y_vals)
z_vals = np.array(z_vals)

# Plot data
# s-value is the size of each dot, alpha is colour intensity of each dot
plt.scatter(y_vals, z_vals, s=3, alpha=1, color='black')
plt.xlabel("Lateral Straggling (mm)")
plt.ylabel("Vertical Straggling (mm)")
plt.title("Beam Profile")
plt.axis("equal")
plt.tight_layout()
#plt.show()

plt.savefig("Beam Profile.png", dpi=fig.dpi)