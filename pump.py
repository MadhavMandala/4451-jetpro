def pump(pa, pc, f):
    rho = 780
    dpf = 20.7
    dpinj = 572
    eta = 0.48
    p_in = pa + dpf
    p_out = pc + dpinj
    dp = p_out - p_in
    w = dp * f / eta / rho
    return w

print(pump(11, 26.96, 0.025))
