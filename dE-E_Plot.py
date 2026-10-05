import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

Rb77_path = r"PATH"
Rb79_path = r"PATH"
Sr79_path = r"PATH"
Sr80_path = r"PATH"
Y80_path  = r"PATH"
Zr80_path = r"PATH"

#---------- Detector Settings -----------

x_start =  #Point where the delta E region starts
x_split_point =  #Point when delta E stops and E starts
x_detector   =  #Point where all ions stop

#---------------------------------------


#---------------------------------------77Rb Calculation------------------------------------------

# Sets the columns of the EXYZ file that python will look at
Rb77_ION_NUMBER = slice(0,7)
Rb77_ION_ENERGY = slice(8,18)
Rb77_ION_DEPTH = slice(20,30)

# Sets up dictionaries
Rb77_energies = defaultdict(list)
Rb77_depths   = defaultdict(list)


# The old A1 special

Rb77_bad = 0 # Sets value of bad lines / ions to 0

# Opens the EXYZ file and does magic to get it into dictionaries of ions, depths and energies
with open(Rb77_path, "r", errors="ignore") as f:
    for line in f:
        # bad = 0, why?
        if len(line) < 32:
            continue

        try:
            Rb77_ion_str = line[Rb77_ION_NUMBER].strip()
            Rb77_e_str   = line[Rb77_ION_ENERGY].strip()
            Rb77_x_str   = line[Rb77_ION_DEPTH].strip()

            # Skips blank lines
            if not Rb77_ion_str or not Rb77_e_str or not Rb77_x_str:
                continue

            Rb77_ion = int(Rb77_ion_str)
            Rb77_E   = float(Rb77_e_str)
            Rb77_x   = float(Rb77_x_str)

        except ValueError:
            Rb77_bad += 1
            continue

        Rb77_energies[Rb77_ion].append(Rb77_E)
        Rb77_depths[Rb77_ion].append(Rb77_x)

#print(f"Parsed ions: {len(energies)}")
#print(f"Lines skipped: {bad}")

# Convert each ion’s lists to arrays, as the machine god demands
for Rb77_ion in list(Rb77_energies.keys()):
    Rb77_energies[Rb77_ion] = np.asarray(Rb77_energies[Rb77_ion], dtype=np.float64)
    Rb77_depths[Rb77_ion]   = np.asarray(Rb77_depths[Rb77_ion], dtype=np.float64)



# print 4000000000000 lines of text, must punish the RAM

with open("Rb77_EXYZ_PARSED.txt", "w") as f:
    f.write("Ion    Depth    Energy\n")  # header data
    for Rb77_ion in Rb77_energies:
        for Rb77_x, Rb77_E in zip(Rb77_depths[Rb77_ion], Rb77_energies[Rb77_ion]):
            f.write(f"{Rb77_ion:4d}  {Rb77_x:10.4f}  {Rb77_E:10.4f}\n")


# Sets up arrays for ΔE (dE_First) & E (dE_rest)
Rb77_dE_first = []
Rb77_dE_rest  = []
Rb77_skipped = {"no_split": 0, "no_end": 0, "bad": 0}

# Defines variables for the energy and depth points for each ion
for Rb77_ion in Rb77_energies.keys():
    Rb77_x = Rb77_depths[Rb77_ion]
    Rb77_E = Rb77_energies[Rb77_ion]

    # Ensure monotonic depth for interpolation
    Rb79_idx = np.argsort(Rb77_x)
    Rb77_x = Rb77_x[Rb79_idx]
    Rb77_E = Rb77_E[Rb79_idx]


    # Need ion to reach 5 cm
    if x_split_point < Rb77_x.min() or x_split_point > Rb77_x.max():
        Rb77_skipped["no_split"] += 1
        continue

    # Need ion to reach detector end
    if x_detector < Rb77_x.min() or x_detector > Rb77_x.max():
        Rb77_skipped["no_end"] += 1
        continue

    Rb77_E0 = np.interp(x_start, Rb77_x, Rb77_E)  # Ion energy at set ΔE distance
    Rb77_E5   = np.interp(x_split_point, Rb77_x, Rb77_E)  # Ion energy at set ΔE distance
    Rb77_Eend = np.interp(x_detector,   Rb77_x, Rb77_E)  # Ion energy at the end of the detector

    # Quick maths
    Rb77_dE1 = Rb77_E0 - Rb77_E5 # Works out ΔE
    Rb77_dE2 = Rb77_E5 - Rb77_Eend # Works out E

    # Gets rid of negative values and labels them as bad
    if Rb77_dE1 < 0 or Rb77_dE2 < 0:
        Rb77_skipped["bad"] += 1
        continue

    # Append this, bitch
    Rb77_dE_first.append(Rb77_dE1)
    Rb77_dE_rest.append(Rb77_dE2)

Rb77_dE_first = np.array(Rb77_dE_first)
Rb77_dE_rest  = np.array(Rb77_dE_rest)

#---------------------------------------79Rb Calculation------------------------------------------

# Sets the columns of the EXYZ file that python will look at
Rb79_ION_NUMBER = slice(0,7)
Rb79_ION_ENERGY = slice(8,18)
Rb79_ION_DEPTH = slice(20,30)

# Sets up dictionaries
Rb79_energies = defaultdict(list)
Rb79_depths   = defaultdict(list)


# The old A1 special

Rb79_bad = 0 # Sets value of bad lines / ions to 0

# Opens the EXYZ file and does magic to get it into dictionaries of ions, depths and energies
with open(Rb79_path, "r", errors="ignore") as f:
    for line in f:
        # bad = 0, why?
        if len(line) < 32:
            continue

        try:
            Rb79_ion_str = line[Rb79_ION_NUMBER].strip()
            Rb79_e_str   = line[Rb79_ION_ENERGY].strip()
            Rb79_x_str   = line[Rb79_ION_DEPTH].strip()

            # Skips blank lines
            if not Rb79_ion_str or not Rb79_e_str or not Rb79_x_str:
                continue

            Rb79_ion = int(Rb79_ion_str)
            Rb79_E   = float(Rb79_e_str)
            Rb79_x   = float(Rb79_x_str)

        except ValueError:
            Rb79_bad += 1
            continue

        Rb79_energies[Rb79_ion].append(Rb79_E)
        Rb79_depths[Rb79_ion].append(Rb79_x)

# Convert each ion’s lists to arrays, as the machine god demands
for Rb79_ion in list(Rb79_energies.keys()):
    Rb79_energies[Rb79_ion] = np.asarray(Rb79_energies[Rb79_ion], dtype=np.float64)
    Rb79_depths[Rb79_ion]   = np.asarray(Rb79_depths[Rb79_ion], dtype=np.float64)



# print 4000000000000 lines of text, must punish the RAM

with open("Rb79_EXYZ_PARSED.txt", "w") as f:
    f.write("Ion    Depth    Energy\n")  # header data
    for Rb79_ion in Rb79_energies:
        for Rb79_x, Rb79_E in zip(Rb79_depths[Rb79_ion], Rb79_energies[Rb79_ion]):
            f.write(f"{Rb79_ion:4d}  {Rb79_x:10.4f}  {Rb79_E:10.4f}\n")


# Sets up arrays for ΔE (dE_First) & E (dE_rest)
Rb79_dE_first = []
Rb79_dE_rest  = []
Rb79_skipped = {"no_split": 0, "no_end": 0, "bad": 0}

# Defines variables for the energy and depth points for each ion
for Rb79_ion in Rb79_energies.keys():
    Rb79_x = Rb79_depths[Rb79_ion]
    Rb79_E = Rb79_energies[Rb79_ion]

    # Ensure monotonic depth for interpolation
    Rb79_idx = np.argsort(Rb79_x)
    Rb79_x = Rb79_x[Rb79_idx]
    Rb79_E = Rb79_E[Rb79_idx]

    # Need ion to reach 5 cm
    if x_split_point < Rb79_x.min() or x_split_point > Rb79_x.max():
        Rb79_skipped["no_split"] += 1
        continue

    # Need ion to reach detector end
    if x_detector < Rb79_x.min() or x_detector > Rb79_x.max():
        Rb79_skipped["no_end"] += 1
        continue

    Rb79_E0 = np.interp(x_start, Rb79_x, Rb79_E)  # Ion energy at set ΔE distance
    Rb79_E5   = np.interp(x_split_point, Rb79_x, Rb79_E)  # Ion energy at set ΔE distance
    Rb79_Eend = np.interp(x_detector,   Rb79_x, Rb79_E)  # Ion energy at the end of the detector

    # Quick maths
    Rb79_dE1 = Rb79_E0 - Rb79_E5 # Works out ΔE
    Rb79_dE2 = Rb79_E5 - Rb79_Eend # Works out E

    # Gets rid of negative values and labels them as bad
    if Rb79_dE1 < 0 or Rb79_dE2 < 0:
        Rb79_skipped["bad"] += 1
        continue

    # Append this, bitch
    Rb79_dE_first.append(Rb79_dE1)
    Rb79_dE_rest.append(Rb79_dE2)

Rb79_dE_first = np.array(Rb79_dE_first)
Rb79_dE_rest  = np.array(Rb79_dE_rest)

#---------------------------------------79Sr Calculation------------------------------------------

# Sets the columns of the EXYZ file that python will look at
Sr79_ION_NUMBER = slice(0,7)
Sr79_ION_ENERGY = slice(8,18)
Sr79_ION_DEPTH = slice(20,30)

# Sets up dictionaries
Sr79_energies = defaultdict(list)
Sr79_depths   = defaultdict(list)


# The old A1 special

Sr79_bad = 0 # Sets value of bad lines / ions to 0

# Opens the EXYZ file and does magic to get it into dictionaries of ions, depths and energies
with open(Sr79_path, "r", errors="ignore") as f:
    for line in f:
        # bad = 0, why?
        if len(line) < 32:
            continue

        try:
            Sr79_ion_str = line[Sr79_ION_NUMBER].strip()
            Sr79_e_str   = line[Sr79_ION_ENERGY].strip()
            Sr79_x_str   = line[Sr79_ION_DEPTH].strip()

            # Skips blank lines
            if not Sr79_ion_str or not Sr79_e_str or not Sr79_x_str:
                continue

            Sr79_ion = int(Sr79_ion_str)
            Sr79_E   = float(Sr79_e_str)
            Sr79_x   = float(Sr79_x_str)

        except ValueError:
            Sr79_bad += 1
            continue

        Sr79_energies[Sr79_ion].append(Sr79_E)
        Sr79_depths[Sr79_ion].append(Sr79_x)

# Convert each ion’s lists to arrays, as the machine god demands
for Sr79_ion in list(Sr79_energies.keys()):
    Sr79_energies[Sr79_ion] = np.asarray(Sr79_energies[Sr79_ion], dtype=np.float64)
    Sr79_depths[Sr79_ion]   = np.asarray(Sr79_depths[Sr79_ion], dtype=np.float64)



# print 4000000000000 lines of text, must punish the RAM

with open("Sr79_EXYZ_PARSED.txt", "w") as f:
    f.write("Ion    Depth    Energy\n")  # header data
    for Sr79_ion in Sr79_energies:
        for Sr79_x, Sr79_E in zip(Sr79_depths[Sr79_ion], Sr79_energies[Sr79_ion]):
            f.write(f"{Sr79_ion:4d}  {Sr79_x:10.4f}  {Sr79_E:10.4f}\n")


# Sets up arrays for ΔE (dE_First) & E (dE_rest)
Sr79_dE_first = []
Sr79_dE_rest  = []
Sr79_skipped = {"no_split": 0, "no_end": 0, "bad": 0}

# Defines variables for the energy and depth points for each ion
for Sr79_ion in Sr79_energies.keys():
    Sr79_x = Sr79_depths[Sr79_ion]
    Sr79_E = Sr79_energies[Sr79_ion]

    # Ensure monotonic depth for interpolation
    Sr79_idx = np.argsort(Sr79_x)
    Sr79_x = Sr79_x[Sr79_idx]
    Sr79_E = Sr79_E[Sr79_idx]

    # Need ion to reach 5 cm
    if x_split_point < Sr79_x.min() or x_split_point > Sr79_x.max():
        Sr79_skipped["no_split"] += 1
        continue

    # Need ion to reach detector end
    if x_detector < Sr79_x.min() or x_detector > Sr79_x.max():
        Sr79_skipped["no_end"] += 1
        continue

    Sr79_E0 = np.interp(x_start, Sr79_x, Sr79_E)  # Ion energy at set ΔE distance
    Sr79_E5   = np.interp(x_split_point, Sr79_x, Sr79_E)  # Ion energy at set ΔE distance
    Sr79_Eend = np.interp(x_detector,   Sr79_x, Sr79_E)  # Ion energy at the end of the detector

    # Quick maths
    Sr79_dE1 = Sr79_E0 - Sr79_E5 # Works out ΔE
    Sr79_dE2 = Sr79_E5 - Sr79_Eend # Works out E

    # Gets rid of negative values and labels them as bad
    if Sr79_dE1 < 0 or Sr79_dE2 < 0:
        Sr79_skipped["bad"] += 1
        continue

    # Append this, bitch
    Sr79_dE_first.append(Sr79_dE1)
    Sr79_dE_rest.append(Sr79_dE2)

x = np.array(Sr79_dE_rest)
y = np.array(Sr79_dE_first)

# distance from the median point (robust center)
#cx, cy = np.median(x), np.median(y)
#dist2 = (x - cx)**2 + (y - cy)**2

#i = np.argmax(dist2)
#print("Removing index:", i, "x=", x[i], "y=", y[i])

#mask = np.ones_like(x, dtype=bool)
#mask[i] = False

#xf = x[mask]
#yf = y[mask]

Sr79_dE_first_A = np.array(x)
Sr79_dE_rest_A  = np.array(y)


#---------------------------------------80Sr Calculation------------------------------------------

# Sets the columns of the EXYZ file that python will look at
Sr80_ION_NUMBER = slice(0,7)
Sr80_ION_ENERGY = slice(8,18)
Sr80_ION_DEPTH = slice(20,30)

# Sets up dictionaries
Sr80_energies = defaultdict(list)
Sr80_depths   = defaultdict(list)


# The old A1 special

Sr80_bad = 0 # Sets value of bad lines / ions to 0

# Opens the EXYZ file and does magic to get it into dictionaries of ions, depths and energies
with open(Sr80_path, "r", errors="ignore") as f:
    for line in f:
        # bad = 0, why?
        if len(line) < 32:
            continue

        try:
            Sr80_ion_str = line[Sr80_ION_NUMBER].strip()
            Sr80_e_str   = line[Sr80_ION_ENERGY].strip()
            Sr80_x_str   = line[Sr80_ION_DEPTH].strip()

            # Skips blank lines
            if not Sr80_ion_str or not Sr80_e_str or not Sr80_x_str:
                continue

            Sr80_ion = int(Sr80_ion_str)
            Sr80_E   = float(Sr80_e_str)
            Sr80_x   = float(Sr80_x_str)

        except ValueError:
            Sr80_bad += 1
            continue

        Sr80_energies[Sr80_ion].append(Sr80_E)
        Sr80_depths[Sr80_ion].append(Sr80_x)

# Convert each ion’s lists to arrays, as the machine god demands
for Sr80_ion in list(Sr80_energies.keys()):
    Sr80_energies[Sr80_ion] = np.asarray(Sr80_energies[Sr80_ion], dtype=np.float64)
    Sr80_depths[Sr80_ion]   = np.asarray(Sr80_depths[Sr80_ion], dtype=np.float64)



# print 4000000000000 lines of text, must punish the RAM

with open("Sr80_EXYZ_PARSED.txt", "w") as f:
    f.write("Ion    Depth    Energy\n")  # header data
    for Sr80_ion in Sr80_energies:
        for Sr80_x, Sr80_E in zip(Sr80_depths[Sr80_ion], Sr80_energies[Sr80_ion]):
            f.write(f"{Sr80_ion:4d}  {Sr80_x:10.4f}  {Sr80_E:10.4f}\n")


# Sets up arrays for ΔE (dE_First) & E (dE_rest)
Sr80_dE_first = []
Sr80_dE_rest  = []
Sr80_skipped = {"no_split": 0, "no_end": 0, "bad": 0}

# Defines variables for the energy and depth points for each ion
for Sr80_ion in Sr80_energies.keys():
    Sr80_x = Sr80_depths[Sr80_ion]
    Sr80_E = Sr80_energies[Sr80_ion]

    # Ensure monotonic depth for interpolation
    Sr80_idx = np.argsort(Sr80_x)
    Sr80_x = Sr80_x[Sr80_idx]
    Sr80_E = Sr80_E[Sr80_idx]

    # Need ion to reach 5 cm
    if x_split_point < Sr80_x.min() or x_split_point > Sr80_x.max():
        Sr80_skipped["no_split"] += 1
        continue

    # Need ion to reach detector end
    if x_detector < Sr80_x.min() or x_detector > Sr80_x.max():
        Sr80_skipped["no_end"] += 1
        continue

    Sr80_E0 = np.interp(x_start, Sr80_x, Sr80_E)  # Ion energy at set ΔE distance
    Sr80_E5   = np.interp(x_split_point, Sr80_x, Sr80_E)  # Ion energy at set ΔE distance
    Sr80_Eend = np.interp(x_detector,   Sr80_x, Sr80_E)  # Ion energy at the end of the detector

    # Quick maths
    Sr80_dE1 = Sr80_E0 - Sr80_E5 # Works out ΔE
    Sr80_dE2 = Sr80_E5 - Sr80_Eend # Works out E

    # Gets rid of negative values and labels them as bad
    if Sr80_dE1 < 0 or Sr80_dE2 < 0:
        Sr80_skipped["bad"] += 1
        continue

    # Append this, bitch
    Sr80_dE_first.append(Sr80_dE1)
    Sr80_dE_rest.append(Sr80_dE2)

Sr80_dE_first = np.array(Sr80_dE_first)
Sr80_dE_rest  = np.array(Sr80_dE_rest)


#----------------------------------------80Y Calculation------------------------------------------

# Sets the columns of the EXYZ file that python will look at
Y80_ION_NUMBER = slice(0,7)
Y80_ION_ENERGY = slice(8,18)
Y80_ION_DEPTH = slice(20,30)

# Sets up dictionaries
Y80_energies = defaultdict(list)
Y80_depths   = defaultdict(list)


# The old A1 special

Y80_bad = 0 # Sets value of bad lines / ions to 0

# Opens the EXYZ file and does magic to get it into dictionaries of ions, depths and energies
with open(Y80_path, "r", errors="ignore") as f:
    for line in f:
        # bad = 0, why?
        if len(line) < 32:
            continue

        try:
            Y80_ion_str = line[Y80_ION_NUMBER].strip()
            Y80_e_str   = line[Y80_ION_ENERGY].strip()
            Y80_x_str   = line[Y80_ION_DEPTH].strip()

            # Skips blank lines
            if not Y80_ion_str or not Y80_e_str or not Y80_x_str:
                continue

            Y80_ion = int(Y80_ion_str)
            Y80_E   = float(Y80_e_str)
            Y80_x   = float(Y80_x_str)

        except ValueError:
            Y80_bad += 1
            continue

        Y80_energies[Y80_ion].append(Y80_E)
        Y80_depths[Y80_ion].append(Y80_x)

# Convert each ion’s lists to arrays, as the machine god demands
for Y80_ion in list(Y80_energies.keys()):
    Y80_energies[Y80_ion] = np.asarray(Y80_energies[Y80_ion], dtype=np.float64)
    Y80_depths[Y80_ion]   = np.asarray(Y80_depths[Y80_ion], dtype=np.float64)



# print 4000000000000 lines of text, must punish the RAM

with open("Y80_EXYZ_PARSED.txt", "w") as f:
    f.write("Ion    Depth    Energy\n")  # header data
    for Y80_ion in Y80_energies:
        for Y80_x, Y80_E in zip(Y80_depths[Y80_ion], Y80_energies[Y80_ion]):
            f.write(f"{Y80_ion:4d}  {Y80_x:10.4f}  {Y80_E:10.4f}\n")


# Sets up arrays for ΔE (dE_First) & E (dE_rest)
Y80_dE_first = []
Y80_dE_rest  = []
Y80_skipped = {"no_split": 0, "no_end": 0, "bad": 0}

# Defines variables for the energy and depth points for each ion
for Y80_ion in Y80_energies.keys():
    Y80_x = Y80_depths[Y80_ion]
    Y80_E = Y80_energies[Y80_ion]

    # Ensure monotonic depth for interpolation
    Y80_idx = np.argsort(Y80_x)
    Y80_x = Y80_x[Y80_idx]
    Y80_E = Y80_E[Y80_idx]

    # Need ion to reach 5 cm
    if x_split_point < Y80_x.min() or x_split_point > Y80_x.max():
        Y80_skipped["no_split"] += 1
        continue

    # Need ion to reach detector end
    if x_detector < Y80_x.min() or x_detector > Y80_x.max():
        Y80_skipped["no_end"] += 1
        continue

    Y80_E0 = np.interp(x_start, Y80_x, Y80_E)  # Ion energy at set ΔE distance
    Y80_E5   = np.interp(x_split_point, Y80_x, Y80_E)  # Ion energy at set ΔE distance
    Y80_Eend = np.interp(x_detector,   Y80_x, Y80_E)  # Ion energy at the end of the detector

    # Quick maths
    Y80_dE1 = Y80_E0 - Y80_E5 # Works out ΔE
    Y80_dE2 = Rb79_E5 - Y80_Eend # Works out E

    # Gets rid of negative values and labels them as bad
    if Y80_dE1 < 0 or Y80_dE2 < 0:
        Y80_skipped["bad"] += 1
        continue

    # Append this, bitch
    Y80_dE_first.append(Y80_dE1)
    Y80_dE_rest.append(Y80_dE2)

Y80_dE_first = np.array(Y80_dE_first)
Y80_dE_rest  = np.array(Y80_dE_rest)

#----------------------------------------80Zr Calculation------------------------------------------

# Sets the columns of the EXYZ file that python will look at
Zr80_ION_NUMBER = slice(0,7)
Zr80_ION_ENERGY = slice(8,18)
Zr80_ION_DEPTH = slice(20,30)

# Sets up dictionaries
Zr80_energies = defaultdict(list)
Zr80_depths   = defaultdict(list)


# The old A1 special

Zr80_bad = 0 # Sets value of bad lines / ions to 0

# Opens the EXYZ file and does magic to get it into dictionaries of ions, depths and energies
with open(Zr80_path, "r", errors="ignore") as f:
    for line in f:
        # bad = 0, why?
        if len(line) < 32:
            continue

        try:
            Zr80_ion_str = line[Zr80_ION_NUMBER].strip()
            Zr80_e_str   = line[Zr80_ION_ENERGY].strip()
            Zr80_x_str   = line[Zr80_ION_DEPTH].strip()

            # Skips blank lines
            if not Zr80_ion_str or not Zr80_e_str or not Zr80_x_str:
                continue

            Zr80_ion = int(Zr80_ion_str)
            Zr80_E   = float(Zr80_e_str)
            Zr80_x   = float(Zr80_x_str)

        except ValueError:
            Zr80_bad += 1
            continue

        Zr80_energies[Zr80_ion].append(Zr80_E)
        Zr80_depths[Zr80_ion].append(Zr80_x)

# Convert each ion’s lists to arrays, as the machine god demands
for Zr80_ion in list(Zr80_energies.keys()):
    Zr80_energies[Zr80_ion] = np.asarray(Zr80_energies[Zr80_ion], dtype=np.float64)
    Zr80_depths[Zr80_ion]   = np.asarray(Zr80_depths[Zr80_ion], dtype=np.float64)



# print 4000000000000 lines of text, must punish the RAM

with open("Zr80_EXYZ_PARSED.txt", "w") as f:
    f.write("Ion    Depth    Energy\n")  # header data
    for Zr80_ion in Zr80_energies:
        for Zr80_x, Zr80_E in zip(Zr80_depths[Zr80_ion], Zr80_energies[Zr80_ion]):
            f.write(f"{Zr80_ion:4d}  {Zr80_x:10.4f}  {Zr80_E:10.4f}\n")


# Sets up arrays for ΔE (dE_First) & E (dE_rest)
Zr80_dE_first = []
Zr80_dE_rest  = []
Zr80_skipped = {"no_split": 0, "no_end": 0, "bad": 0}

# Defines variables for the energy and depth points for each ion
for Zr80_ion in Zr80_energies.keys():
    Zr80_x = Zr80_depths[Zr80_ion]
    Zr80_E = Zr80_energies[Zr80_ion]

    # Ensure monotonic depth for interpolation
    Zr80_idx = np.argsort(Zr80_x)
    Zr80_x = Zr80_x[Zr80_idx]
    Zr80_E = Zr80_E[Zr80_idx]

    # Need ion to reach 5 cm
    if x_split_point < Zr80_x.min() or x_split_point > Zr80_x.max():
        Zr80_skipped["no_split"] += 1
        continue

    # Need ion to reach detector end
    if x_detector < Zr80_x.min() or x_detector > Zr80_x.max():
        Zr80_skipped["no_end"] += 1
        continue

    Zr80_E0 = np.interp(x_start, Zr80_x, Zr80_E)  # Ion energy at set ΔE distance
    Zr80_E5   = np.interp(x_split_point, Zr80_x, Zr80_E)  # Ion energy at set ΔE distance
    Zr80_Eend = np.interp(x_detector,   Zr80_x, Zr80_E)  # Ion energy at the end of the detector

    # Quick maths
    Zr80_dE1 = Zr80_E0 - Zr80_E5 # Works out ΔE
    Zr80_dE2 = Rb79_E5 - Zr80_Eend # Works out E

    # Gets rid of negative values and labels them as bad
    if Zr80_dE1 < 0 or Zr80_dE2 < 0:
        Zr80_skipped["bad"] += 1
        continue

    # Append this, bitch
    Zr80_dE_first.append(Zr80_dE1)
    Zr80_dE_rest.append(Zr80_dE2)

Zr80_dE_first = np.array(Zr80_dE_first)
Zr80_dE_rest  = np.array(Zr80_dE_rest)

#---------------------------------------Plot All The Data-----------------------------------------

plt.scatter(Rb77_dE_rest, Rb77_dE_first, s=0.5**2, color = "blue", label="Rb77")
plt.scatter(Rb79_dE_rest, Rb79_dE_first, s=0.5**2, color = "red", label="Rb79")
plt.scatter(Sr79_dE_rest_A, Sr79_dE_first_A, s=0.5**2, color = "green", label="Sr79")
plt.scatter(Sr80_dE_rest, Sr80_dE_first, s=0.5**2, color = "orange", label="Sr80")
plt.scatter(Y80_dE_rest, Y80_dE_first, s=0.5**2, color = "purple", label="Y80")
plt.scatter(Zr80_dE_rest, Zr80_dE_first, s=0.5**2, color = "brown", label="Zr80")
plt.grid()
plt.legend()
#plt.xlim(37000, 40500)
#plt.ylim(2000, 5000)
plt.xlabel("Energy loss from 2.5 cm to 22.5 cm (KeV)")
plt.ylabel("Energy loss in first 2.5 cm (KeV)")
plt.title("ΔE–E Plot")
#plt.show()

plt.savefig("Setup A dE-E Huge.png")


# ***************************************************************

# This writes an output file that summarises all info / parameters from above

split_dist = x_split_point / 1e8
total_dist = x_detector / 1e8

stats_path = "ΔE-E_Stats.txt"

with open(stats_path, "w") as f:
    f.write("SRIM dE–E Analysis Summary\n")
    f.write("==========================\n\n")

    f.write(f"dE Boundary: {split_dist} cm\n")

    f.write(f"Total E Length: {total_dist} cm\n")

    f.write("\n")

    f.write("**************************\n\n")

    f.write(f"Ion : Rb77\n\n")

    f.write(f"Total ions simulated:              {len(Rb77_energies)}\n")
    f.write(f"Ions plotted:                      {len(Rb77_dE_first)}\n")

    f.write("\n")

    f.write(f"Did not reach dE Boundary:         {Rb77_skipped['no_split']}\n")
    f.write(f"Did not reach detector end:        {Rb77_skipped['no_end']}\n")
    f.write(f"Unphysical Ions:                   {Rb77_skipped['bad']}\n\n")

    f.write("**************************\n\n")

    f.write(f"Ion : Rb79\n\n")

    f.write(f"Total ions simulated:              {len(Rb79_energies)}\n")
    f.write(f"Ions plotted:                      {len(Rb79_dE_first)}\n")

    f.write("\n")

    f.write(f"Did not reach dE Boundary:         {Rb79_skipped['no_split']}\n")
    f.write(f"Did not reach detector end:        {Rb79_skipped['no_end']}\n")
    f.write(f"Unphysical Ions:                   {Rb79_skipped['bad']}\n\n")

    f.write("**************************\n\n")

    f.write(f"Ion : Sr79\n\n")

    #f.write("Sr79 Ions Omitted Due To Plotting Error\n\n")

    f.write(f"Total ions simulated:              {len(Sr79_energies)}\n")
    f.write(f"Ions plotted:                      {len(Sr79_dE_first)}\n")

    f.write("\n")

    f.write(f"Did not reach dE Boundary:         {Sr79_skipped['no_split']}\n")
    f.write(f"Did not reach detector end:        {Sr79_skipped['no_end']}\n")
    f.write(f"Unphysical Ions:                   {Sr79_skipped['bad']}\n")

    f.write("**************************\n\n")

    f.write(f"Ion : Sr80\n\n")

    f.write(f"Total ions simulated:              {len(Sr80_energies)}\n")
    f.write(f"Ions plotted:                      {len(Sr80_dE_first)}\n")

    f.write("\n")

    f.write(f"Did not reach dE Boundary:         {Sr80_skipped['no_split']}\n")
    f.write(f"Did not reach detector end:        {Sr80_skipped['no_end']}\n")
    f.write(f"Unphysical Ions:                   {Sr80_skipped['bad']}\n\n")

    f.write("**************************\n\n")

    f.write(f"Ion : Y80\n\n")

    f.write(f"Total ions simulated:              {len(Y80_energies)}\n")
    f.write(f"Ions plotted:                      {len(Y80_dE_first)}\n")

    f.write("\n")

    f.write(f"Did not reach dE Boundary:         {Y80_skipped['no_split']}\n")
    f.write(f"Did not reach detector end:        {Y80_skipped['no_end']}\n")
    f.write(f"Unphysical Ions:                   {Y80_skipped['bad']}\n\n")

    f.write("**************************\n\n")

    f.write(f"Ion : Zr80\n\n")

    f.write(f"Total ions simulated:              {len(Zr80_energies)}\n")
    f.write(f"Ions plotted:                      {len(Zr80_dE_first)}\n")

    f.write("\n")

    f.write(f"Did not reach dE Boundary:         {Zr80_skipped['no_split']}\n")
    f.write(f"Did not reach detector end:        {Zr80_skipped['no_end']}\n")
    f.write(f"Unphysical Ions:                   {Zr80_skipped['bad']}\n\n")

print(f"Stats written to: {stats_path}")