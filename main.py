import numpy as np

from boxes import *

# Flight conditions
ta   = 220.0   # ambient temperature (K)
pa   = 11000.0   # ambient pressure (Pa)
pf   = 0.0   # fuel storage pressure (Pa)
M    = 1.10   # flight Mach number

# Design parameters
Prc       = 15   # compressor (stagnation) pressure ratio
Prf       = 1.2   # fan (stagnation) pressure ratio
f         = 0.025   # main burner fuel–air ratio (f_ma)
fab       = 0.0050   # afterburner fuel–air ratio (f_ab)
beta      = 1.5   # bypass ratio (β = ṁ_s / ṁ_a)
b         = 0.06   # bleed ratio (b = ṁ_b / ṁ_a)
sigma     = 0.72   # split ratio (fraction of bypass air to fan nozzle)

# Component / flow properties (arrays or dicts keyed by component index/name as needed)
T = sp.symbols('T')
cp_R = {
    "d" : 3.5,
    "f" : 3.5,
    "c" : 3.62,
    "b" : 3.7 + .66*(T/1000)**2 - 0.2*(T/1000)**3,
    "t" : 3.38 + 0.7*(T/1000)**2 - 0.2*(T/1000)**3,
    "tmh" : 3.70 + 0.78*(T/1000)**2 - 0.36*(T/1000)**3,
    "tmc" : 3.43 + 0.78*(T/1000)**2 - 0.27*(T/1000)**3,
    "ft" : 3.4 + 0.63*(T/1000)**2 - 0.2*(T/1000)**3,
    "ab" : 3.5 + 0.72*(T/1000)**2 - 0.210*(T/1000)**3,
    "n" : 3.45 + 0.55*(T/1000)**2 - 0.15*(T/1000)**3,
    "fn" : 3.5 * T/T,
    "nm1" : 3.44 + 0.79*(T/1000)**2 - 0.27*(T/1000)**3,
    "nm2" : 3.43 + 0.79*(T/1000)**2 - 0.28*(T/1000)**3,
    "cn" : 3.45 + 0.550*(T/1000.0)**2 - 0.150*(T/1000.0)**3,
    "p" : 0
} 

W = 28.9   # molecular weights Wi for each component


# Efficiencies
n = {
    "d" : .94,
    "f" : .92,
    "c" : .91,
    "b" : .99,
    "t" : .94,
    "tm" : 0,
    "ft" : .94,
    "ab" : .96,
    "n" : .96,
    "fn" : .97,
    "nm" : 0,
    "cn" : .96,
    "p" : .48
} 

# Fuel properties
delta_h_R = 43520000   # fuel heating value (J/kg)
Prb = 0.95
Prab = 0.97
rho_f     = 0.0   # fuel density (kg/m³)

# Loss functions
delta_d   = 0.0   # specific drag loss associated with bypass fan
Pr_nm     = 0.0   # pressure loss function for virtual nozzle mixer



s01 = diffuser(ta, pa, M, n.get("d"), cp_R.get("d"))
print("diffuser: ", s01)

s02 = compressor(s01[0], s01[1], n.get("f"), 1, cp_R.get("f"), Prf)
print("fan: ", s02)

s03 = compressor(s02[0], s02[1], n.get("c"), 1, cp_R.get("c"), Prc)
print("compressor: ", s03)

s04 = burner(s03[0], s03[1], n.get("b"), cp_R.get("b"), f, delta_h_R, Prb)
print("burner: ", s04)

s05_1 = turbine(s04[0], s04[1], f, b, n.get("t"), cp_R.get("t"), s03[2])
print("turbine: ", s05_1)

s05_m = turbineMixer(s05_1[0], s05_1[1], s03[0], s05_1[1], (1+f-b), b, cp_R.get("tmh"), cp_R.get("tmc"))
print("turbine mixer: ", s05_m)

s05_2 = turbine(s05_m[0], s05_m[1], f, 0, n.get("ft"), cp_R.get("ft"), s02[2]*(beta+1))
print("fan turbine: ", s05_2)

s06 = afterburner(s05_2[0], s05_2[1], n.get("ab"), cp_R.get("ab"), fab, 1+f, delta_h_R, Prab)
print("afterburner: ", s06)

s0e = nozzle(s06[0], s06[1], pa, n.get("n"), cp_R.get("n"))
print("core nozzle: ", s0e)

s0ef = nozzle(s02[0], s02[1], pa, n.get("fn"), cp_R.get("fn"))
print("fan nozzle: ", s0ef)

pm1 = performanceMetrics(s0e[0], s0ef[0], M, ta, f, fab, beta, 1, cp_R.get("d"), delta_h_R)
print(pm1)


s06_5 = nozzleMixer(s06[0], s06[1], s02[0], s02[1], 1+f+fab, (beta*(1-sigma)), cp_R.get("nm1"), cp_R.get("nm2"))
print("combined nozzle: ", s06_5)

s07 = nozzle(s06_5[0], s06_5[1], pa, n.get("cn"), cp_R.get("cn"))
print("combined exit: ", s07)

pm2 = performanceMetrics(s07[0], s0ef[0], M, ta, f, fab, beta, sigma, cp_R.get("d"), delta_h_R)
print(pm2)


