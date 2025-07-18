def pump(pa, pc, f, eta):
    rho = 780
    dpf = 20.7 * 1000
    dpinj = 572 * 1000
    p_in = pa + dpf
    p_out = pc + dpinj
    dp = p_out - p_in
    w = dp * f / eta / rho
    return w