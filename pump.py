def pump(dpf, dpinj, pa, pc, f, eta):
    rho = 780
    p_in = pa + dpf
    p_out = pc + dpinj
    dp = p_out - p_in
    w = dp * f / eta / rho
    return w