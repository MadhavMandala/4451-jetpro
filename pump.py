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
    return p_out, w
    # Returns specific work in kJ/kg.

# print(pump(11, 404.4, 0.025, 0.005))
