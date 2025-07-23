import numpy as np

from boxes import *


#EXAMPLE CASE WE WERE GIVEN IN TERMS OF SETUP
def turbofan_afterburner_separate(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma):
    s01 = diffuser(ta, pa, M)
    s02 = fan(s01[0], s01[1], 0, Prf)
    s03 = compressor(s02[0], s02[1], b, Prc)
    s04 = burner(s03[0], s03[1], f, 1-b)
    s05_1 = turbine(s04[0], s04[1], f, b, s03[2])
    s05_m = turbineMixer(s05_1[0], s05_1[1], s03[0], s05_1[1], (1+f-b), b)
    s05_2 = fanturbine(s05_m[0], s05_m[1], f, 0, s02[2]*(beta+1))
    s06 = afterburner(s05_2[0], s05_2[1], fab, 1+f)
    s0e = corenozzle(s06[0], s06[1], pa)
    s0ef = fannozzle(s02[0], s02[1], pa)
    pm = performanceMetrics(s0e[0], s0ef[0], M, ta, f, fab, beta, 1, s04[0], s06[0])
    return pm

def turbofan_separate(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma):
    s01 = diffuser(ta, pa, M)
    s02 = fan(s01[0], s01[1], Prf)
    s03 = compressor(s02[0], s02[1], Prc)
    s04 = burner(s03[0], s03[1], f)
    s05_1 = turbine(s04[0], s04[1], f, b, s03[2])
    s05_m = turbineMixer(s05_1[0], s05_1[1], s03[0], s05_1[1], (1+f-b), b)
    s05_2 = turbine(s05_m[0], s05_m[1], f, 0, s02[2]*(beta+1))
    s0e = corenozzle(s05_2[0], s05_2[1], pa)
    s0ef = fannozzle(s02[0], s02[1], pa)
    pm = performanceMetrics(s0e[0], s0ef[0], M, ta, f, fab, beta, 1)
    return pm

def turbofan_afterburner_combined(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma):
    s01 = diffuser(ta, pa, M)
    s02 = compressor(s01[0], s01[1], Prf)
    s03 = compressor(s02[0], s02[1], Prc)
    s04 = burner(s03[0], s03[1], f)
    s05_1 = turbine(s04[0], s04[1], f, b, s03[2])
    s05_m = turbineMixer(s05_1[0], s05_1[1], s03[0], s05_1[1], (1+f-b), b)
    s05_2 = turbine(s05_m[0], s05_m[1], f, 0, s02[2]*(beta+1))
    s06 = afterburner(s05_2[0], s05_2[1], fab, 1+f)
    s06_5 = nozzleMixer(s06[0], s06[1], s02[0], s02[1], 1+f+fab, (beta*(1-sigma)))
    s07 = combinednozzle(s06_5[0], s06_5[1], pa)
    pm = performanceMetrics(s07[0], 0, M, ta, f, fab, beta, sigma)
    return pm

def turbofan_combined(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma):
    s01 = diffuser(ta, pa, M)
    s02 = compressor(s01[0], s01[1], Prf)
    s03 = compressor(s02[0], s02[1], Prc)
    s04 = burner(s03[0], s03[1], f)
    s05_1 = turbine(s04[0], s04[1], f, b, s03[2])
    s05_m = turbineMixer(s05_1[0], s05_1[1], s03[0], s05_1[1], (1+f-b), b)
    s05_2 = turbine(s05_m[0], s05_m[1], f, 0, s02[2]*(beta+1))
    s06_5 = nozzleMixer(s05_m[0], s05_m[1], s02[0], s02[1], 1+f+fab, (beta*(1-sigma)))
    s07 = combinednozzle(s06_5[0], s06_5[1], pa)
    pm = performanceMetrics(s07[0], 0, M, ta, f, fab, beta, sigma)
    return pm


def turbojet_afterburner(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma):
    s01 = diffuser(ta, pa, M)
    s02 = compressor(s01[0], s01[1], Prf)
    s03 = burner(s02[0], s02[1], f)
    s05 = turbine(s03[0], s03[1], f, b, s02[2])
    s05_m = turbineMixer(s05[0], s05[1], s02[0], s05[1], (1+f-b), b)
    s06 = afterburner(s05_m[0], s05_m[1], fab, 1+f)
    s0e = corenozzle(s06[0], s06[1], pa)
    pm = performanceMetrics(s0e[0], 0, M, ta, f, fab, beta, 1)
    return pm

def turbojet(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma):
    s01 = diffuser(ta, pa, M)
    s02 = compressor(s01[0], s01[1], Prc)
    s03 = burner(s02[0], s02[1], f)
    s05 = turbine(s03[0], s03[1], f, b, s02[2])
    s05_m = turbineMixer(s05[0], s05[1], s02[0], s05[1], (1+f-b), b)
    s0e = corenozzle(s05_m[0], s05_m[1], pa)
    pm = performanceMetrics(s0e[0], 0, M, ta, f, fab, beta, 1)
    return pm, s0e

def ramjet(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma):
    s01 = diffuser(ta, pa, M)
    s03 = burner(s01[0], s01[1], f)
    s0e = corenozzle(s03[0], s03[1], pa)
    pm = performanceMetrics(s0e[0], 0, M, ta, f, fab, beta, 1)
    return pm


