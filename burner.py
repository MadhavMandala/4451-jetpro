def afterburner(p_0, T_0, f, f_ab):
    # Accepts the fan turbine exit stagnation pressure (Pa) and temperature (K),
    # the fuel-to-air ratio, and the afterburner fuel-to-air ratio.
    if f_ab == 0:
        return p_0, T_0, f_ab
 
    Pr = 0.97
    mw = 28.9
    R = 8314.5 / mw
    dhr = 43.52 * 1000000
    T_max = 2300
    C_p = (3.50 + 0.720*(T_0/1000)**2 - 0.210*(T_0/1000)**3) * R
    eta = 0.96

    mass_ratio = 1 + f + f_ab
    p_0_exit = p_0 * Pr
    T_0_exit = (eta*f_ab*dhr/C_p + (1+f)*T_0) / mass_ratio

    if T_0_exit > T_max:
        T_0_exit = T_max
        f_ab = (T_0_exit/T_0 - 1) / ((eta*dhr/C_p/T_0) - T_0_exit/T_0)

    return p_0_exit, T_0_exit, f_ab
    # Returns the stagnation pressure (Pa), stagnation temperature (K), 
    # and afterburner fuel-to-air ratio.

# print(afterburner(130800, 1242, 0.025, 0.005))

def burner(p_0, T_0, f, b):
    if f == 0:
        return p_0, T_0, f
 
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

    if T_0_exit > T_max:
        T_0_exit = T_max
        f = (T_0_exit/T_0 - 1) / ((eta*dhr/C_p/T_0) - T_0_exit/T_0)

    return p_0_exit, T_0_exit, f

# print(burner(404350, 657.9, 0.025, 0.06))
