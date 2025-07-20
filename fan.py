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
