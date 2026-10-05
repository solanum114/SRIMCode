import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import axvline
from scipy.interpolate import interp1d
import pandas as pd

#PANDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Data_Read = pd.read_csv(r"FILE.csv", header=None)
depths = Data_Read.iloc[:,2].values
ion_path = Data_Read.iloc[:,3].values

f_interp = interp1d(depths, ion_path, kind='linear', fill_value=0, bounds_error=False)

#Integral over whole setup
xxa = np.linspace(0, 100000000, 5000)
yya = f_interp(xxa)
area_trapza = np.trapezoid(yya, xxa)

#Integral over Layer A
xxb = np.linspace(0, 0, 5000)
yyb = f_interp(xxb)
area_trapzb = np.trapezoid(yyb, xxb)

#Integral over Layer B
xxc = np.linspace(0, 0, 5000)
yyc = f_interp(xxc)
area_trapzc = np.trapezoid(yyc, xxc)

#Integral over Layer C
xxd = np.linspace(0, 0, 5000)
yyd = f_interp(xxd)
area_trapzd = np.trapezoid(yyd, xxd)

#Integral over Layer D
xxe = np.linspace(0, 0, 5000)
yye = f_interp(xxe)
area_trapze = np.trapezoid(yye, xxe)

#Integral over Layer E
xxf = np.linspace(0, 0, 5000)
yyf = f_interp(xxf)
area_trapzf = np.trapezoid(yyf, xxf)

#Integral over Layer F
xxg = np.linspace(0, 0, 5000)
yyg = f_interp(xxg)
area_trapzg = np.trapezoid(yyg, xxg)

#Integral over Layer G
xxh = np.linspace(0, 0, 5000)
yyh = f_interp(xxh)
area_trapzh = np.trapezoid(yyh, xxh)

axvline(20)
axvline(98)
axvline(109)
axvline(197)
axvline(207)
axvline(307)
axvline(407)
axvline(596)
axvline(615)
axvline(715)
axvline(815)
axvline(915)

plt.plot(xxa, yya, color='red', lw=1, )
plt.show()



#Just run this and it will print out the energy loss values in each region of the detector

print(f"Energy loss through entire detector= {area_trapza:.2e} eV")

print(f"Energy loss through Layer A = {area_trapzb:.2e} eV")

print(f"Energy loss through Layer B = {area_trapzc:.2e} eV")

print(f"Energy loss through Layer C = {area_trapzd:.2e} eV")

print(f"Energy loss through Layer D = {area_trapze:.2e} eV")

print(f"Energy loss through Layer E = {area_trapzf:.2e} eV")

print(f"Energy loss through Layer F = {area_trapzg:.2e} eV")

print(f"Energy loss through Layer G = {area_trapzh:.2e} eV")
