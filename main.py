from diffuser import diffuser
from compressor import fan, compressor
from burner import burner, afterburner
from turbine import turbine, fan_turbine
from pump import pump
from nozzles import turbineMixer, nozzleMixer, nozzle
import numpy as np

def simulate_jet_engine(T_a, p_a, M, Pr_c, Pr_f, Beta, b, sigma, f, f_ab):

    p_01, T_01 = diffuser(p_a, T_a, M)
    # print("Diffuser: P_01 = {:.4f} Pa, T_01 = {:.4f} K".format(p_01, T_01))

    p_02, T_02, w_f = fan(p_01, T_01, Pr_f, Beta)
    # print("Fan: p_02 = {:.4f} Pa, T_02 = {:.4f} K, w_f = {:.4f} kg/s".format(p_02, T_02, w_f))

    p_03, T_03, w_c = compressor(p_02, T_02, Pr_c)
    # print("Compressor: p_03 = {:.4f} Pa, T_03 = {:.4f} K".format(p_03, T_03))

    p_04, T_04, f = burner(p_03, T_03, f, b)
    # print("Burner: p_04 = {:.4f} Pa, T_04 = {:.4f} K".format(p_04, T_04))

    p_f1, p_f2, w_p = pump(p_a / 1000, p_03 / 1000, f, f_ab)
    # print("Pump: p_f1 = {:.4f} KPa, p_f2 = {:.4f} KPa, w_p = {:.4f} kg/s".format(p_f1, p_f2, w_p))

    p_051, T_051 = turbine(p_04, T_04, b, (w_c + w_p) * 1000, f)
    # print("Turbine: p_05 = {:.4f} Pa, T_05 = {:.4f} K".format(p_051, T_051))

    T_051m, p_051m = turbineMixer(T_051, p_051 / 1000, T_03, b, f)
    # print("Turbine Mixer: T_051m = {:.4f} K, p_051m = {:.4f} Pa".format(T_051m, p_051m * 1000))

    p_052, T_052 = fan_turbine(p_051m * 1000, T_051m, w_f * 1000, f)
    # print("Fan Turbine: p_052 = {:.4f} Pa, T_052 = {:.4f} K".format(p_052, T_052))

    p_06, T_06, f_ab = afterburner(p_052, T_052, f, f_ab)
    # print("Afterburner: p_06 = {:.4f} Pa, T_06 = {:.4f} K, f_ab = {:.4f}".format(p_06, T_06, f_ab))

    T_07, p_07 = nozzleMixer(T_06, p_06 / 1000, T_02, p_02 / 1000, p_a, sigma, Beta, f, f_ab)
    # print("Nozzle Mixer: p_07 = {:.4f} Pa, T_07 = {:.4f} K".format(p_07 * 1000, T_07))

    T_e, u_e, M_e, T_ef, u_ef, M_ef = nozzle(T_07, p_07, T_02, p_02 / 1000, p_a / 1000, sigma)
    # print("Nozzle: T_e = {:.4f} K, u_e = {:.4f} m/s, M_e = {:.4f}, T_ef = {:.4f} K, u_ef = {:.4f} m/s, M_ef = {:.4f}".format(
        # T_e, u_e, M_e, T_ef, u_ef, M_ef))
    
    return {
        "T_01": T_01,
        "p_01": p_01,
        "T_02": T_02,
        "p_02": p_02,
        "T_03": T_03,
        "p_03": p_03,
        "T_04": T_04,
        "p_04": p_04,
        "p_f1": p_f1,
        "p_f2": p_f2,
        "T_051": T_051,
        "p_051": p_051,
        "T_051m": T_051m,
        "p_051m": p_051m,
        "T_052": T_052,
        "p_052": p_052,
        "T_06": T_06,
        "p_06": p_06,
        "T_07": T_07,
        "p_07": p_07,
        "T_e": T_e,
        "u_e": u_e,
        "M_e": M_e,
        "T_ef": T_ef,
        "u_ef": u_ef,
        "M_ef": M_ef,
        "f_ab": f_ab,
        "f": f,
        "w_f": w_f,
        "w_c": w_c,
        "w_p": w_p,
        "p_a": p_a,
        "T_a": T_a,
        "M": M,
        "Pr_c": Pr_c,
        "Pr_f": Pr_f,
        "Beta": Beta,
        "b": b,
        "sigma": sigma
    }

outputs = simulate_jet_engine(220.0, 11000.0, 1.10, 15, 1.2, 1.5, 0.06, 0.72, 0.025, 0.005)
# print(outputs)

def performance_metrics(outputs):
    u = outputs["M"] * np.sqrt(outputs["T_a"] * 8314.5 / 28.9644 * 1.4)
    delta_drag = 263 * outputs["M"]**2 * outputs["p_a"] / 100000 * outputs["Beta"]**1.5
    ST = (1 + outputs["f"] + outputs["f_ab"] + outputs["Beta"]*(1-outputs["sigma"])) * outputs["u_e"] + (outputs["Beta"]*outputs["sigma"]) * outputs["u_ef"] - (1+outputs["Beta"]) * u - delta_drag
    TSFC = (outputs["f"] + outputs["f_ab"]) / ST
    outputs["u"] = u
    outputs["delta_drag"] = delta_drag
    outputs["ST"] = ST
    outputs["TSFC"] = TSFC
    outputs["delta_H_r"] = 43.52 * 1000000
    outputs["eta_o"] = u / TSFC / outputs["delta_H_r"]
    dKEoverma = 0.5 * ((1 + outputs["f"] + outputs["f_ab"] + outputs["Beta"]*(1-outputs["sigma"])) * outputs["u_e"]**2 + (outputs["Beta"]*outputs["sigma"]) * outputs["u_ef"]**2 - (1+outputs["Beta"]) * u**2)
    outputs["eta_th"] = dKEoverma / (outputs["delta_H_r"] * (outputs["f"] + outputs["f_ab"]))
    outputs["eta_p"] = outputs["eta_o"] / outputs["eta_th"]
    return outputs

outputs = performance_metrics(outputs)
print("Performance Metrics:")
print("Overall Efficiency (eta_o): {:.4f}".format(outputs["eta_o"]))    
print("Thermal Efficiency (eta_th): {:.4f}".format(outputs["eta_th"]))
print("Propulsive Efficiency (eta_p): {:.4f}".format(outputs["eta_p"]))
print("Thrust Specific Fuel Consumption (TSFC): {:.4f} kg/(kN*s)".format(outputs["TSFC"]*1000*3600))
print("Specific Thrust (ST): {:.4f} N*s/kg".format(outputs["ST"]))
