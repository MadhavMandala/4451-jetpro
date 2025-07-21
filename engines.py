import numpy as np

from boxes import *


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


def turbofan_afterburner_separate(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma):
    s01 = diffuser(ta, pa, M, n.get("d"), cp_R.get("d"))
    s02 = compressor(s01[0], s01[1], n.get("f"), 1, cp_R.get("f"), Prf)
    s03 = compressor(s02[0], s02[1], n.get("c"), 1, cp_R.get("c"), Prc)
    s04 = burner(s03[0], s03[1], n.get("b"), cp_R.get("b"), f, delta_h_R, Prb)
    s05_1 = turbine(s04[0], s04[1], f, b, n.get("t"), cp_R.get("t"), s03[2])
    s05_m = turbineMixer(s05_1[0], s05_1[1], s03[0], s05_1[1], (1+f-b), b, cp_R.get("tmh"), cp_R.get("tmc"))
    s05_2 = turbine(s05_m[0], s05_m[1], f, 0, n.get("ft"), cp_R.get("ft"), s02[2]*(beta+1))
    s06 = afterburner(s05_2[0], s05_2[1], n.get("ab"), cp_R.get("ab"), fab, 1+f, delta_h_R, Prab)
    s0e = nozzle(s06[0], s06[1], pa, n.get("n"), cp_R.get("n"))
    s0ef = nozzle(s02[0], s02[1], pa, n.get("fn"), cp_R.get("fn"))
    pm = performanceMetrics(s0e[0], s0ef[0], M, ta, f, fab, beta, 1, cp_R.get("d"), delta_h_R)
    return pm

def turbofan_separate(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma):
    s01 = diffuser(ta, pa, M, n.get("d"), cp_R.get("d"))
    s02 = compressor(s01[0], s01[1], n.get("f"), 1, cp_R.get("f"), Prf)
    s03 = compressor(s02[0], s02[1], n.get("c"), 1, cp_R.get("c"), Prc)
    s04 = burner(s03[0], s03[1], n.get("b"), cp_R.get("b"), f, delta_h_R, Prb)
    s05_1 = turbine(s04[0], s04[1], f, b, n.get("t"), cp_R.get("t"), s03[2])
    s05_m = turbineMixer(s05_1[0], s05_1[1], s03[0], s05_1[1], (1+f-b), b, cp_R.get("tmh"), cp_R.get("tmc"))
    s05_2 = turbine(s05_m[0], s05_m[1], f, 0, n.get("ft"), cp_R.get("ft"), s02[2]*(beta+1))
    s0e = nozzle(s05_2[0], s05_2[1], pa, n.get("n"), cp_R.get("n"))
    s0ef = nozzle(s02[0], s02[1], pa, n.get("fn"), cp_R.get("fn"))
    pm = performanceMetrics(s0e[0], s0ef[0], M, ta, f, fab, beta, 1, cp_R.get("d"), delta_h_R)
    return pm

def turbofan_afterburner_combined(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma):
    s01 = diffuser(ta, pa, M, n.get("d"), cp_R.get("d"))
    s02 = compressor(s01[0], s01[1], n.get("f"), 1, cp_R.get("f"), Prf)
    s03 = compressor(s02[0], s02[1], n.get("c"), 1, cp_R.get("c"), Prc)
    s04 = burner(s03[0], s03[1], n.get("b"), cp_R.get("b"), f, delta_h_R, Prb)
    s05_1 = turbine(s04[0], s04[1], f, b, n.get("t"), cp_R.get("t"), s03[2])
    s05_m = turbineMixer(s05_1[0], s05_1[1], s03[0], s05_1[1], (1+f-b), b, cp_R.get("tmh"), cp_R.get("tmc"))
    s05_2 = turbine(s05_m[0], s05_m[1], f, 0, n.get("ft"), cp_R.get("ft"), s02[2]*(beta+1))
    s06 = afterburner(s05_2[0], s05_2[1], n.get("ab"), cp_R.get("ab"), fab, 1+f, delta_h_R, Prab)
    s06_5 = nozzleMixer(s06[0], s06[1], s02[0], s02[1], 1+f+fab, (beta*(1-sigma)), cp_R.get("nm1"), cp_R.get("nm2"))
    s07 = nozzle(s06_5[0], s06_5[1], pa, n.get("cn"), cp_R.get("cn"))
    pm = performanceMetrics(s07[0], s0ef[0], M, ta, f, fab, beta, sigma, cp_R.get("d"), delta_h_R)
    return pm

def turbofan_combined(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma):
    s01 = diffuser(ta, pa, M, n.get("d"), cp_R.get("d"))
    s02 = compressor(s01[0], s01[1], n.get("f"), 1, cp_R.get("f"), Prf)
    s03 = compressor(s02[0], s02[1], n.get("c"), 1, cp_R.get("c"), Prc)
    s04 = burner(s03[0], s03[1], n.get("b"), cp_R.get("b"), f, delta_h_R, Prb)
    s05_1 = turbine(s04[0], s04[1], f, b, n.get("t"), cp_R.get("t"), s03[2])
    s05_m = turbineMixer(s05_1[0], s05_1[1], s03[0], s05_1[1], (1+f-b), b, cp_R.get("tmh"), cp_R.get("tmc"))
    s05_2 = turbine(s05_m[0], s05_m[1], f, 0, n.get("ft"), cp_R.get("ft"), s02[2]*(beta+1))
    s06_5 = nozzleMixer(s05_m[0], s05_m[1], s02[0], s02[1], 1+f+fab, (beta*(1-sigma)), cp_R.get("nm1"), cp_R.get("nm2"))
    s07 = nozzle(s06_5[0], s06_5[1], pa, n.get("cn"), cp_R.get("cn"))
    pm = performanceMetrics(s07[0], s0ef[0], M, ta, f, fab, beta, sigma, cp_R.get("d"), delta_h_R)
    return pm


def turbojet_afterburner(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma):
    s01 = diffuser(ta, pa, M, n.get("d"), cp_R.get("d"))
    s02 = compressor(s01[0], s01[1], n.get("f"), 1, cp_R.get("f"), Prf)
    s03 = burner(s02[0], s02[1], n.get("b"), cp_R.get("b"), f, delta_h_R, Prb)
    s05 = turbine(s03[0], s03[1], f, b, n.get("t"), cp_R.get("t"), s02[2])
    s05_m = turbineMixer(s05[0], s05[1], s02[0], s05[1], (1+f-b), b, cp_R.get("tmh"), cp_R.get("tmc"))
    s06 = afterburner(s05_m[0], s05_m[1], n.get("ab"), cp_R.get("ab"), fab, 1+f, delta_h_R, Prab)
    s0e = nozzle(s06[0], s06[1], pa, n.get("n"), cp_R.get("n"))
    pm = performanceMetrics(s0e[0], 0, M, ta, f, fab, beta, 1, cp_R.get("d"), delta_h_R)
    return pm

def turbojet(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma):
    s01 = diffuser(ta, pa, M, n.get("d"), cp_R.get("d"))
    s02 = compressor(s01[0], s01[1], n.get("f"), 1, cp_R.get("f"), Prf)
    s03 = burner(s02[0], s02[1], n.get("b"), cp_R.get("b"), f, delta_h_R, Prb)
    s05 = turbine(s03[0], s03[1], f, b, n.get("t"), cp_R.get("t"), s02[2])
    s05_m = turbineMixer(s05[0], s05[1], s02[0], s05[1], (1+f-b), b, cp_R.get("tmh"), cp_R.get("tmc"))
    s0e = nozzle(s05_m[0], s05_m[1], pa, n.get("n"), cp_R.get("n"))
    pm = performanceMetrics(s0e[0], 0, M, ta, f, fab, beta, 1, cp_R.get("d"), delta_h_R)
    return pm

def ramjet(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma):
    s01 = diffuser(ta, pa, M, n.get("d"), cp_R.get("d"))
    s03 = burner(s01[0], s01[1], n.get("b"), cp_R.get("b"), f, delta_h_R, Prb)
    s0e = nozzle(s03[0], s03[1], pa, n.get("n"), cp_R.get("n"))
    pm = performanceMetrics(s0e[0], 0, M, ta, f, fab, beta, 1, cp_R.get("d"), delta_h_R)
    return pm

