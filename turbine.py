def turbine(p_0, T_0, b, w, f):
    # Accepts the compressor exit pressure (Pa) and temperature (K), 
    # the bypass ratio, the turbine work (J/kg), and the fuel-to-air ratio.
    if w == 0:
        return p_0, T_0
    
    C_p_over_R = lambda T_0:  3.38 + 0.700 * (T_0/1000) ** 2 - 0.200 * (T_0/1000) ** 3
    mw = 28.9
    R = 8314.5 / mw
    C_p = C_p_over_R(T_0) * R
    gamma = C_p / (C_p - R)
    eta_p = 0.94

    mass_ratio = 1 + f - b
    T_0_exit = T_0 -  w/C_p/mass_ratio
    Tr = T_0_exit / T_0
    eta = (Tr - 1) / (Tr ** (1/eta_p) - 1)
    p_0_exit = p_0 * (1 - (1 - Tr) / eta) ** (gamma / (gamma - 1))

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
