import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

fig = plt.figure(figsize=(12, 8))

#PANDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Data_Read = pd.read_csv(r"FILE.csv", header=None)
depths = Data_Read.iloc[:,2].values
ion_eloss = Data_Read.iloc[:,3].values

plt.plot(depths, ion_eloss, color='red', lw=1)
plt.xlabel("Depth (mm)")
plt.ylabel("Ion Energy Loss (MeV / mm)")
plt.title("Ion Energy Loss by Depth")
#plt.legend()
plt.tight_layout()
#plt.show()

plt.savefig("Ion Energy Loss by Depth.png", dpi=fig.dpi)

print(depths)
