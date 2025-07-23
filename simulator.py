
import numpy as np

def turbine(p_0, T_0, b, w, f):
    # Accepts the compressor exit pressure (Pa) and temperature (K), 
    # the bypass ratio, the turbine work (J/kg), and the fuel-to-air ratio.
    if w == 0:
        return p_0, T_0
    
    C_p_over_R = lambda T_0:  3.38 + 0.700 * (T_0/1000) ** 2 - 0.200 * (T_0/1000) ** 3
    mw = 28.9
    R = 8314.46 / mw
    C_p = C_p_over_R(T_0) * R
    eta_p = 0.94

    mass_ratio = 1 + f - b
    T_0_exit = T_0 -  w/C_p/mass_ratio
    Tr = T_0_exit / T_0
    eta = (Tr - 1) / (Tr ** (1/eta_p) - 1)
    p_0_exit = p_0 * (1 - (1 - Tr) / eta) ** (C_p_over_R(T_0))

    return p_0_exit, T_0_exit
    # Returns the exit stagnation pressure (Pa) and temperature (K) of the turbine.

# print(turbine(384100, 1628, .06, 384100, 0.025))

def fan_turbine(p_0, T_0, w, f):
    # Accepts the fan exit pressure (Pa) and temperature (K), 
    # the fan work (J/kg), and the fuel-to-air ratio.
    if w == 0:
        return p_0, T_0
    
    C_p_over_R = lambda T_0: 3.40 + 0.630 * (T_0/1000) ** 2 - 0.200 * (T_0/1000) ** 3
    mw = 28.9
    R = 8314.5 / mw
    C_p = C_p_over_R(T_0) * R
    gamma = C_p / (C_p - R)
    eta_p = 0.94

    mass_ratio = 1 + f
    T_0_exit = T_0 -  w/C_p/mass_ratio
    Tr = T_0_exit / T_0
    eta = (Tr - 1) / (Tr ** (1/eta_p) - 1)
    p_0_exit = p_0 * (1 - (1 - Tr) / eta) ** (gamma / (gamma - 1))

    return p_0_exit, T_0_exit
    # Returns the exit stagnation pressure (Pa) and temperature (K) of the turbine.

# print(fan_turbine(146700, 1276, 40070, 0.025))


def pump(pa, pc, f, f_ab):
    # Accepts values for ambient pressure (pa), compressor exit pressure (pc)
    # in KPa, fuel-to-air ratio (f), and afterburner fuel-to-air ratio (f_ab).
    rho = 780
    dpf = 20.7
    dpinj = 572
    eta = 0.48
    p_in = pa + dpf
    p_out = pc + dpinj
    dp = p_out - p_in
    w = dp * (f + f_ab) / eta / rho
    return p_in, p_out, w
    # Returns specific work in kJ/kg.

# print(pump(11, 404.4, 0.025, 0.005))


def turbineMixer(T051,P051,T03,b,f):

    MW = 28.9
    P051 = P051 * 1000

    # Finds Cp/R for the turbine exhaust air
    CpoRt = 3.43 + 0.780 * (T051 / 1000) ** 2 - 0.270 * (T051 / 1000) ** 3

    # Finds Cp/R for the compressor exhaust air
    CpoRc = 3.70 + 0.780 * (T03 / 1000) ** 2 - 0.360 * (T03 / 1000) ** 3

    # Finds R
    R = 8314.462618 / MW

    # Finds Cp for the turbine exhaust air
    Cpt = CpoRt * R

    # Finds Cp for the compressor exhaust air
    Cpc = CpoRc * R

    # Finds stagnation temp coming out of mixer
    T051m = ( (b * Cpc * T03 + (1-b+f) * Cpt * T051) / (b * Cpc + (1-b+f) * Cpt) )

    # Finds reversible stagnation pressure coming out of the mixer
    exp1 = b / ( 1 + f )
    exp2 = ( 1 + f - b ) / ( 1 + f )
    P051m = (P051 ** exp1) * (P051 ** exp2) * ((T051m/T051) ** (exp2 * CpoRt)) * ((T051m/T03) ** (exp1 * CpoRc))

    P051m = P051m / 1000

    return T051m, P051m

# Nozzle Mixer: Feeds into the core nozzle
def nozzleMixer(T06,P06,T02,P02,Pa,sigma,beta,f,fab):

    MW = 28.9
    P06 = P06 * 1000
    P02 = P02 * 1000
    Pa = Pa * 1000

    # Finds estimated nozzle mixer output temp if both flows had the same Cp/R
    T07p = ( ( (1-sigma) * beta * T02 ) + ( (1+f+fab) * T06 ) ) / ( ((1-sigma) * beta) + (1+f+fab))

    # Finds T0 bar for the core and bypass
    T0bc = (T06 + T07p) / 2
    T0bby = (T02 + T07p) / 2

    # Finds the Cp/R for the core
    CpoRc = 3.44 + 0.79 * (T0bc / 1000) ** 2 - 0.27 * (T0bc / 1000) ** 3

    # Finds Cp/R for the bypass
    CpoRs = 3.43 + 0.79 * (T0bby / 1000) ** 2 - 0.28 * (T0bby / 1000) ** 3

    # Finds R
    R = 8314.462618 / MW

    # Finds Cp for the core air
    Cpc = CpoRc * R

    # Finds Cp for the bypass air
    Cps = CpoRs * R

    # Finds stagnation temp coming out of mixer
    T07 = ( ((1-sigma) * beta * Cps * T02) + ((1+f+fab) * Cpc * T06) ) / ( ((1-sigma) * beta * Cps) + ((1+f+fab) * Cpc) )

    # Finds adjusted stagnation pressure coming out of mixer
    Cnm = 2
    mdot1 = (1-sigma) * beta
    mdot2 = 1 + f + fab

    # Finds reversible stagnation pressure coming out of the mixer
    P07rev = P02 ** (mdot1/(mdot1+mdot2)) * P06 ** (mdot2/(mdot1+mdot2)) * (T07/T02) ** (CpoRs*(mdot1/(mdot1+mdot2))) * (T07/T06) ** (CpoRc*(mdot2/(mdot1+mdot2)))

    if ((mdot1 < mdot2) & (mdot1 > 0)):
        mr = mdot2 / mdot1
        Prnm = np.exp(-Cnm / (1 + mr ** 0.5))
        P07 = P07rev * Prnm
    else:
        mr = mdot1 / mdot2
        Prnm = np.exp(-Cnm / (1 + mr ** 0.5))
        P07 = P07rev * Prnm


    P07 = P07 / 1000

    return T07, P07




#   Nozzle method. Input T06, P06, T02, P02, sigma, and Pa to find Te, ue, Me, Tef, uef, Mef
def nozzle(T07, P07, T02, P02, Pa, sigma):

    P07 = P07 * 1000
    P02 = P02 * 1000
    Pa = Pa * 1000

    # Core Values
    MWc = 28.9
    CpoRc = 3.45 + 0.55*(T07/1000)**2 - 0.15*(T07/1000)**3
    Rc = 8314.462618 / MWc
    etanc = 0.96
    Cpc = CpoRc * Rc

    # Bypass Values
    MWs = 28.9
    CpoRs = 3.5
    Rs = 8314.462618 / MWs
    etans = 0.97
    Cps = CpoRs * Rs

    # See if Core and Bypass are completely mixed
    if (sigma == 0):
        Tef = 0
        uef = 0
        Mef = 0


    # CORE Finds static exit temperature using isentropic relations
    Te = T07 * (1 - etanc * (1 - (Pa/P07)**(1/CpoRc))) 

    # CORE Find exit velocity
    ue = np.sqrt((2*Cpc*(T07-Te)))

    # CORE Find R and gamma using CPG relations
    R = Cpc / CpoRc
    gamma = Cpc / (Cpc - R)

    # CORE Finds exit Mach number using above info
    Me = ue / (gamma * R * Te)**0.5

    # BYPASS Finds static exit temperature using isentropic relations
    Tef = T02 * (1 - etans * (1 - (Pa/P02)**(1/CpoRs))) 

    # BYPASS Find exit velocity
    uef = (2*Cps*(T02-Tef))**0.5

    # BYPASS Find R and gamma using CPG relations
    R = Cps / CpoRs
    gammas = Cps / (Cps - Rs)

    # BYPASS Finds exit Mach number using above info
    Mef = uef / (gammas * Rs * Tef)**0.5



    return Te, ue, Me, Tef, uef, Mef


def diffuser(p_a, T_a, M):
    if 1 < M < 5:
        r_d = 1 - 0.075 * (M - 1) ** 1.35
    else:
        r_d = 1
        
    eta = 0.94
    mw = 28.9
    R = 8314.5 / mw
    C_p = 3.5 * R
    gamma = C_p / (C_p - R)

    T_0_exit = T_a * (1 + ((gamma - 1) / 2) * M ** 2)
    p_0_exit = p_a * r_d * (1 + eta * ((gamma - 1) / 2) * M ** 2) ** (gamma / (gamma - 1))

    return p_0_exit, T_0_exit

# print(diffuser(11000, 220, 1.1))

def fan(p_0, T_0, Pr, Beta):
    # Accepts diffuser exit stagnation quantities in KPa and K,
    # as well as the fan pressure ratio and bypass ratio.
    if Beta == 0:
        return p_0, T_0, 0
    
    eta_p = 0.92
    mw = 28.9
    R = 8314.5 / mw
    C_p = 3.5 * R

    p_0_exit = p_0 * Pr
    Tr = Pr ** (R / C_p / eta_p)
    T_0_exit = T_0 * Tr

    w = C_p * (T_0_exit - T_0) * (1 + Beta) / 1000
    return p_0_exit, T_0_exit, w
    # Returns the fan exit stagnation pressure and temperature in KPa and K, 
    # and the fan specific work in kJ/kg.

# print(fan(22.4639, 273.24, 1.2, 1.5))

def compressor(p_0, T_0, Pr):
    if Pr == 1:
        return p_0, T_0, 0
    
    eta_p = 0.91
    mw = 28.9
    R = 8314.5 / mw
    C_p = 3.62 * R

    p_0_exit = p_0 * Pr
    Tr = Pr ** (R / C_p / eta_p)
    T_0_exit = T_0 * Tr

    w = C_p * (T_0_exit - T_0) * (1) / 1000
    return p_0_exit, T_0_exit, w

# print(compressor(26956.68, 289.15767609413706, 15))


def afterburner(p_0, T_0, f, f_ab):
    # Accepts the fan turbine exit stagnation pressure (Pa) and temperature (K),
    # the fuel-to-air ratio, and the afterburner fuel-to-air ratio.
    if f_ab == 0:
        return p_0, T_0, f_ab, 2300
 
    Pr = 0.97
    mw = 28.9
    R = 8314.5 / mw
    dhr = 43.52 * 1000000
    # T_max = 2300
    C_p = (3.50 + 0.720*(T_0/1000)**2 - 0.210*(T_0/1000)**3) * R
    eta = 0.96

    mass_ratio = 1 + f + f_ab
    p_0_exit = p_0 * Pr
    T_0_exit = (eta*f_ab*dhr/C_p + (1+f)*T_0) / mass_ratio

    # if T_0_exit > T_max:
    #     T_0_exit = T_max
    #     f_ab = (T_0_exit/T_0 - 1) / ((eta*dhr/C_p/T_0) - T_0_exit/T_0)

    return p_0_exit, T_0_exit, f_ab, 2300
    # Returns the stagnation pressure (Pa), stagnation temperature (K), 
    # and afterburner fuel-to-air ratio.

# print(afterburner(130800, 1242, 0.025, 0.005))

def burner(p_0, T_0, f, b):
    if f == 0:
        C_b = 700
        b_max = 0.15
        n = 0.6
        T_max = 1400
        T_max = T_max + C_b * (b / b_max) ** n
        return p_0, T_0, f, T_max
 
    Pr = 0.95
    mw = 28.9
    R = 8314.5 / mw
    dhr = 43.52 * 1000000

    C_b = 700
    b_max = 0.15
    n = 0.6
    T_max = 1400
    T_max = T_max + C_b * (b / b_max) ** n
    C_p = (3.70 + 0.660 * (T_0/1000) ** 2 - 0.200 * (T_0/1000) ** 3) * R
    eta = 0.99

    mass_ratio = 1 + f - b
    p_0_exit = p_0 * Pr
    T_0_exit = (eta*f*dhr/C_p + (1-b)*T_0) / mass_ratio

    # if T_0_exit > T_max:
    #     T_0_exit = T_max
    #     f = (T_0_exit/T_0 - 1) / ((eta*dhr/C_p/T_0) - T_0_exit/T_0)

    return p_0_exit, T_0_exit, f, T_max

# print(burner(404350, 657.9, 0.025, 0.06))


def simulate_jet_engine(T_a, p_a, M, Pr_c, Pr_f, Beta, b, sigma, f, f_ab):

    p_01, T_01 = diffuser(p_a, T_a, M)
    # print("Diffuser: P_01 = {:.4f} Pa, T_01 = {:.4f} K".format(p_01, T_01))

    p_02, T_02, w_f = fan(p_01, T_01, Pr_f, Beta)
    # print("Fan: p_02 = {:.4f} Pa, T_02 = {:.4f} K, w_f = {:.4f} kg/s".format(p_02, T_02, w_f))

    p_03, T_03, w_c = compressor(p_02, T_02, Pr_c)
    # print("Compressor: p_03 = {:.4f} Pa, T_03 = {:.4f} K".format(p_03, T_03))

    p_04, T_04, f, T_max = burner(p_03, T_03, f, b)
    # print("Burner: p_04 = {:.4f} Pa, T_04 = {:.4f} K".format(p_04, T_04))

    p_f1, p_f2, w_p = pump(p_a / 1000, p_03 / 1000, f, f_ab)
    # print("Pump: p_f1 = {:.4f} KPa, p_f2 = {:.4f} KPa, w_p = {:.4f} kg/s".format(p_f1, p_f2, w_p))

    p_051, T_051 = turbine(p_04, T_04, b, (w_c + w_p) * 1000, f)
    # print("Turbine: p_05 = {:.4f} Pa, T_05 = {:.4f} K".format(p_051, T_051))

    T_051m, p_051m = turbineMixer(T_051, p_051 / 1000, T_03, b, f)
    # print("Turbine Mixer: T_051m = {:.4f} K, p_051m = {:.4f} Pa".format(T_051m, p_051m * 1000))

    p_052, T_052 = fan_turbine(p_051m * 1000, T_051m, w_f * 1000, f)
    # print("Fan Turbine: p_052 = {:.4f} Pa, T_052 = {:.4f} K".format(p_052, T_052))

    p_06, T_06, f_ab, T_max_ab = afterburner(p_052, T_052, f, f_ab)
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
        "sigma": sigma,
        "T_max": T_max,
        "T_max_ab": T_max_ab
    }

outputs = simulate_jet_engine(220.0, 11000.0, 1.10, 15, 1.2, 1.5, 0.06, 0.72, 0.025, 0.005)
# print(outputs)


def simulate_turbojet_engine(T_a, p_a, M, Pr_c, Pr_f, Beta, b, sigma, f, f_ab):

    p_01, T_01 = diffuser(p_a, T_a, M)
    # print("Diffuser: P_01 = {:.4f} Pa, T_01 = {:.4f} K".format(p_01, T_01))

    p_03, T_03, w_c = compressor(p_01, T_01, Pr_c)
    # print("Compressor: p_03 = {:.4f} Pa, T_03 = {:.4f} K".format(p_03, T_03))

    p_04, T_04, f, T_max = burner(p_03, T_03, f, b)
    # print("Burner: p_04 = {:.4f} Pa, T_04 = {:.4f} K".format(p_04, T_04))

    p_f1, p_f2, w_p = pump(p_a / 1000, p_03 / 1000, f, f_ab)
    # print("Pump: p_f1 = {:.4f} KPa, p_f2 = {:.4f} KPa, w_p = {:.4f} kg/s".format(p_f1, p_f2, w_p))

    p_051, T_051 = turbine(p_04, T_04, b, (w_c + w_p) * 1000, f)
    # print("Turbine: p_05 = {:.4f} Pa, T_05 = {:.4f} K".format(p_051, T_051))

    p_06, T_06, f_ab, T_max_ab = afterburner(p_051, T_051, f, f_ab)
    # print("Afterburner: p_06 = {:.4f} Pa, T_06 = {:.4f} K, f_ab = {:.4f}".format(p_06, T_06, f_ab))

    T_e, u_e, M_e, T_ef, u_ef, M_ef = nozzle(T_06, p_06, 0, 0, p_a / 1000, sigma)
    # print("Nozzle: T_e = {:.4f} K, u_e = {:.4f} m/s, M_e = {:.4f}, T_ef = {:.4f} K, u_ef = {:.4f} m/s, M_ef = {:.4f}".format(
        # T_e, u_e, M_e, T_ef, u_ef, M_ef))
    
    return {
        "T_01": T_01,
        "p_01": p_01,
        "T_02": 0,
        "p_02": 0,
        "T_03": T_03,
        "p_03": p_03,
        "T_04": T_04,
        "p_04": p_04,
        "p_f1": p_f1,
        "p_f2": p_f2,
        "T_051": T_051,
        "p_051": p_051,
        "T_051m": 0,
        "p_051m": 0,
        "T_052": 0,
        "p_052": 0,
        "T_06": T_06,
        "p_06": p_06,
        "T_07": 0,
        "p_07": 0,
        "T_e": T_e,
        "u_e": u_e,
        "M_e": M_e,
        "T_ef": T_ef,
        "u_ef": u_ef,
        "M_ef": M_ef,
        "f_ab": f_ab,
        "f": f,
        "w_f": 0,
        "w_c": w_c,
        "w_p": w_p,
        "p_a": p_a,
        "T_a": T_a,
        "M": M,
        "Pr_c": Pr_c,
        "Pr_f": Pr_f,
        "Beta": Beta,
        "b": b,
        "sigma": sigma,
        "T_max": T_max,
        "T_max_ab": T_max_ab
    }



def simulate_ramjet_engine(T_a, p_a, M, Pr_c, Pr_f, Beta, b, sigma, f, f_ab):

    p_01, T_01 = diffuser(p_a, T_a, M)
    # print("Diffuser: P_01 = {:.4f} Pa, T_01 = {:.4f} K".format(p_01, T_01))

    p_04, T_04, f, T_max = burner(p_01, T_01, f, b)
    # print("Burner: p_04 = {:.4f} Pa, T_04 = {:.4f} K".format(p_04, T_04))

    p_06, T_06, f_ab, T_max_ab = afterburner(p_04, T_04, f, f_ab)
    # print("Afterburner: p_06 = {:.4f} Pa, T_06 = {:.4f} K, f_ab = {:.4f}".format(p_06, T_06, f_ab))

    T_e, u_e, M_e, T_ef, u_ef, M_ef = nozzle(T_06, p_06, 0, 0, p_a / 1000, sigma)
    # print("Nozzle: T_e = {:.4f} K, u_e = {:.4f} m/s, M_e = {:.4f}, T_ef = {:.4f} K, u_ef = {:.4f} m/s, M_ef = {:.4f}".format(
        # T_e, u_e, M_e, T_ef, u_ef, M_ef))
    
    return {
        "T_01": T_01,
        "p_01": p_01,
        "T_02": 0,
        "p_02": 0,
        "T_03": 0,
        "p_03": 0,
        "T_04": T_04,
        "p_04": p_04,
        "p_f1": 0,
        "p_f2": 0,
        "T_051": 0,
        "p_051": 0,
        "T_051m": 0,
        "p_051m": 0,
        "T_052": 0,
        "p_052": 0,
        "T_06": T_06,
        "p_06": p_06,
        "T_07": 0,
        "p_07": 0,
        "T_e": T_e,
        "u_e": u_e,
        "M_e": M_e,
        "T_ef": T_ef,
        "u_ef": u_ef,
        "M_ef": M_ef,
        "f_ab": f_ab,
        "f": f,
        "w_f": 0,
        "w_c": 0,
        "w_p": 0,
        "p_a": p_a,
        "T_a": T_a,
        "M": M,
        "Pr_c": Pr_c,
        "Pr_f": Pr_f,
        "Beta": Beta,
        "b": b,
        "sigma": sigma,
        "T_max": T_max,
        "T_max_ab": T_max_ab
    }


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

def inputs_to_metrics(T_a, p_a, M, Pr_c, Pr_f, Beta, b, sigma, f, f_ab):
    outputs = simulate_turbojet_engine(T_a, p_a, M, Pr_c, Pr_f, Beta, b, sigma, f, f_ab)
    return performance_metrics(outputs)
