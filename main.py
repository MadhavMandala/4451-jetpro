from diffuser import diffuser
from compressor import fan, compressor
from burner import burner, afterburner
from turbine import turbine, fan_turbine
from pump import pump
from nozzles import turbineMixer, nozzleMixer, nozzle

def simulate_jet_engine(T_a, p_a, M, Pr_c, Pr_f, Beta, b, sigma, f, f_ab):

    p_01, T_01 = diffuser(p_a, T_a, M)
    print("Diffuser: P_01 = {:.4f} Pa, T_01 = {:.4f} K".format(p_01, T_01))

    p_02, T_02, w_f = fan(p_01, T_01, Pr_f, Beta)
    print("Fan: p_02 = {:.4f} Pa, T_02 = {:.4f} K, w_f = {:.4f} kg/s".format(p_02, T_02, w_f))

    p_03, T_03, w_c = compressor(p_02, T_02, Pr_c)
    print("Compressor: p_03 = {:.4f} Pa, T_03 = {:.4f} K".format(p_03, T_03))

    p_04, T_04, f = burner(p_03, T_03, f, b)
    print("Burner: p_04 = {:.4f} Pa, T_04 = {:.4f} K".format(p_04, T_04))

    p_f1, p_f2, w_p = pump(p_a / 1000, p_03 / 1000, f, f_ab)
    print("Pump: p_f1 = {:.4f} KPa, p_f2 = {:.4f} KPa, w_p = {:.4f} kg/s".format(p_f1, p_f2, w_p))

    p_051, T_051 = turbine(p_04, T_04, b, (w_c + w_p) * 1000, f)
    print("Turbine: p_05 = {:.4f} Pa, T_05 = {:.4f} K".format(p_051, T_051))

    T_051m, p_051m = turbineMixer(T_051, p_051 / 1000, T_03, b, f)
    print("Turbine Mixer: T_051m = {:.4f} K, p_051m = {:.4f} Pa".format(T_051m, p_051m * 1000))

    p_052, T_052 = fan_turbine(p_051m * 1000, T_051m, w_f * 1000, f)
    print("Fan Turbine: p_052 = {:.4f} Pa, T_052 = {:.4f} K".format(p_052, T_052))

    p_06, T_06, f_ab = afterburner(p_052, T_052, f, f_ab)
    print("Afterburner: p_06 = {:.4f} Pa, T_06 = {:.4f} K, f_ab = {:.4f}".format(p_06, T_06, f_ab))

    T_07, p_07 = nozzleMixer(T_06, p_06 / 1000, T_02, p_02 / 1000, p_a, sigma, Beta, f, f_ab)
    print("Nozzle Mixer: p_07 = {:.4f} Pa, T_07 = {:.4f} K".format(p_07 * 1000, T_07))

    T_e, u_e, M_e, T_ef, u_ef, M_ef = nozzle(T_07, p_07, T_02, p_02 / 1000, p_a / 1000, sigma)
    print("Nozzle: T_e = {:.4f} K, u_e = {:.4f} m/s, M_e = {:.4f}, T_ef = {:.4f} K, u_ef = {:.4f} m/s, M_ef = {:.4f}".format(
        T_e, u_e, M_e, T_ef, u_ef, M_ef))

simulate_jet_engine(220.0, 11000.0, 1.10, 15, 1.2, 1.5, 0.06, 1, 0.025, 0.005)

# import numpy as np

# from boxes import *

# # Flight conditions
# ta   = 220.0   # ambient temperature (K)
# pa   = 11000.0   # ambient pressure (Pa)
# pf   = 0.0   # fuel storage pressure (Pa)
# M    = 1.10   # flight Mach number

# # Design parameters
# Prc       = 15   # compressor (stagnation) pressure ratio
# Prf       = 1.2   # fan (stagnation) pressure ratio
# f         = 0.025   # main burner fuel–air ratio (f_ma)
# fab       = 0.050   # afterburner fuel–air ratio (f_ab)
# beta      = 1.5   # bypass ratio (β = ṁ_s / ṁ_a)
# b         = 0.0   # bleed ratio (b = ṁ_b / ṁ_a)
# sigma     = 0.0   # split ratio (fraction of bypass air to fan nozzle)

# # Component / flow properties (arrays or dicts keyed by component index/name as needed)
# T = sp.symbols('T')
# cp_R = {
#     "d" : 3.5,
#     "f" : 3.5,
#     "c" : 3.62,
#     "b" : 3.7 + .66*(T/1000)**2 - 0.2*(T/1000)**3,
#     "t" : 3.38 + 0.7*(T/1000)**2 - 0.2*(T/1000)**3,
#     "tm" : 0,
#     "ft" : 0,
#     "ab" : 0,
#     "n" : 0,
#     "fn" : 3.5,
#     "nm" : 0,
#     "cn" : 0,
#     "p" : 0
# } 

# W = 28.9   # molecular weights Wi for each component


# # Efficiencies
# n = {
#     "d" : .94,
#     "f" : .92,
#     "c" : .91,
#     "b" : .99,
#     "t" : .94,
#     "tm" : 0,
#     "ft" : .94,
#     "ab" : .96,
#     "n" : .96,
#     "fn" : .97,
#     "nm" : 0,
#     "cn" : .96,
#     "p" : .48
# } 

# # Fuel properties
# delta_h_R = 43520000   # fuel heating value (J/kg)
# Prb = .95
# rho_f     = 0.0   # fuel density (kg/m³)

# # Loss functions
# delta_d   = 0.0   # specific drag loss associated with bypass fan
# Pr_nm     = 0.0   # pressure loss function for virtual nozzle mixer

# # Temperature limits
# Tmax      = 0.0   # maximum turbine inlet temperature in main burner (K)
# Tmax_ab   = 0.0   # maximum turbine inlet temperature in afterburner (K)

# # Constraint limits
# b_max      = 0.0   # maximum bleed fraction
# beta_max   = 0.0   # maximum bypass ratio
# Prf_min    = 0.0   # minimum fan pressure ratio
# Prf_max    = 0.0   # maximum fan pressure ratio
# Prc_max    = 0.0   # maximum overall compressor (stagnation) pressure ratio


# s01 = diffuser(ta, pa, M, n.get("d"), cp_R.get("d"))
# print("diffuser: ", s01)

# s02 = compressor(s01[0], s01[1], n.get("f"), 1, cp_R.get("f"), Prf)
# print("fan: ", s02)

# s03 = compressor(s02[0], s02[1], n.get("c"), 1, cp_R.get("c"), Prc)
# print("compressor: ", s03)

# s04 = burner(s03[0], s03[1], n.get("b"), cp_R.get("b"), f, delta_h_R, Prb)
# print("burner: ", s04)

# s05 = turbine(s04[0], s04[1], n.get("t"), cp_R.get("t"), s03[2])
# print("turbine: ", s05)