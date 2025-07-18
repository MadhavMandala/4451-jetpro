def turbine(p_0, T_0, T_max, b, w, f):
    C_p_over_R = lambda T_0:  3.38 + 0.700 * (T_0/1000) ** 2 - 0.200 * (T_0/1000) ** 3
    mw = 28.9
    R = 8314 / mw
    C_p = C_p_over_R(T_0) * R
    gamma = C_p / (C_p - R)
    T_max = T_max + 700 * (b/0.15) ** 0.6
    eta_p = 0.94

    mass_ratio = 1 + f - b
    T_0_exit = T_0 -  w/C_p/mass_ratio
    Tr = T_0_exit / T_0
    eta = (Tr - 1) / (Tr ** (1/eta_p) - 1)
    p_0_exit = p_0 * (1 - (1 - Tr) / eta) ** (gamma / (gamma - 1))

    return p_0_exit, T_0_exit
