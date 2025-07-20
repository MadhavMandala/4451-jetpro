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