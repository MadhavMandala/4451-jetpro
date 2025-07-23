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

s01 = diffuser(ta, pa, M)
print(s01)

s02 = fan(s01[0], s01[1], 0, Prf)
print(s02)

s03 = compressor(s02[0], s02[1], b, Prc)
print(s03)

s0p = pump(pa, s02[1], f, fab)
print(s0p)

s04 = burner(s03[0], s03[1], f, 1-b)
print(s04)

s051 = turbine(s04[0], s04[1], f, b, (s03[2] + s0p[2]))
print(s051)

s05m = turbineMixer(s051[0], s051[1], s03[0], s051[1], (1+f-b), b)
print(s05m)

s05m = np.array([1275.45, 147900])
s052 = fanturbine(s05m[0], s05m[1], f, b, (beta+1)*s02[2])
print(s052)

s06 = afterburner(s052[0], s052[1], fab, 1+f)
print(s06)

s0e = corenozzle(s06[0], s06[1], pa)
print(s0e)

s0ef = fannozzle(s02[0], s02[1], pa)
print(s0ef)

print(s0p)

pm = performanceMetrics(s0e[1], s0ef[1], M, ta, f, fab, beta, 1, s04[0], s06[0])
print(pm)

s0nm = nozzleMixer(s06[0], s06[1], s02[0], s02[1], 1+f+fab, beta)
print(s0nm)

s0ec = combinednozzle(s0nm[0], s0nm[1], pa)
print(s0ec)

pm2 = performanceMetrics(s0ec[1], s0ef[1], M, ta, f, fab, beta, sigma, s04[0], s06[0])
print(pm2)


print('.....................................................')

print(performanceMetrics(1196, 357.2, 1.1, 220, 0.025, 0.005, 1.5, 1, 1, 1))