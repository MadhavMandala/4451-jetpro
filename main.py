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
fab       = 0.050   # afterburner fuel–air ratio (f_ab)
beta      = 1.5   # bypass ratio (β = ṁ_s / ṁ_a)
b         = 0.0   # bleed ratio (b = ṁ_b / ṁ_a)
sigma     = 0.0   # split ratio (fraction of bypass air to fan nozzle)

# Component / flow properties (arrays or dicts keyed by component index/name as needed)
T = sp.symbols('T')
cp_R = {
    "d" : 3.5,
    "f" : 3.5,
    "c" : 3.62,
    "b" : 3.7 + .66*(T/1000)**2 - 0.2*(T/1000)**3,
    "t" : 3.38 + 0.7*(T/1000)**2 - 0.2*(T/1000)**3,
    "tm" : 0,
    "ft" : 0,
    "ab" : 0,
    "n" : 0,
    "fn" : 3.5,
    "nm" : 0,
    "cn" : 0,
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
Prb = .95
rho_f     = 0.0   # fuel density (kg/m³)

# Loss functions
delta_d   = 0.0   # specific drag loss associated with bypass fan
Pr_nm     = 0.0   # pressure loss function for virtual nozzle mixer

# Temperature limits
Tmax      = 0.0   # maximum turbine inlet temperature in main burner (K)
Tmax_ab   = 0.0   # maximum turbine inlet temperature in afterburner (K)

# Constraint limits
b_max      = 0.0   # maximum bleed fraction
beta_max   = 0.0   # maximum bypass ratio
Prf_min    = 0.0   # minimum fan pressure ratio
Prf_max    = 0.0   # maximum fan pressure ratio
Prc_max    = 0.0   # maximum overall compressor (stagnation) pressure ratio


s01 = diffuser(ta, pa, M, n.get("d"), cp_R.get("d"))
print("diffuser: ", s01)

s02 = compressor(s01[0], s01[1], n.get("f"), 1, cp_R.get("f"), Prf)
print("fan: ", s02)

s03 = compressor(s02[0], s02[1], n.get("c"), 1, cp_R.get("c"), Prc)
print("compressor: ", s03)

s04 = burner(s03[0], s03[1], n.get("b"), cp_R.get("b"), f, delta_h_R, Prb)
print("burner: ", s04)

s05 = turbine(s04[0], s04[1], n.get("t"), cp_R.get("t"), s03[2])
print("turbine: ", s05)