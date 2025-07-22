import numpy as np
import sympy as sp
import math

T = sp.symbols('T')

def diffuser(ta, pa, M):
    n = 0.94
    cp_R = 3.5

    if 1 < M < 5:
        r_d = 1 - 0.075 * (M - 1) ** 1.35
    else:
        r_d = 1

    gamma = cp_R/(cp_R-1)
    t0a = ta * (1 + ((gamma-1)/2)*M**2)
    p01 = pa * r_d * (1 + n * ((gamma-1)/2)*M**2)**(gamma/(gamma-1))
    t01 = t0a
    return np.array([t01, p01])


def fan(t0i, p0i, b, pr): 
    n = 0.92
    cp_R = 3.5

    gamma = cp_R/(cp_R-1)
    p0o = p0i * pr
    t0o = t0i * pr**((gamma-1) / (gamma * n))
    work = (cp_R * 8314.462/28.9) * (t0o - t0i)
    return np.array([t0o, p0o, work])

def compressor(t0i, p0i, b, pr): 
    n = 0.91
    cp_R = 3.62

    gamma = cp_R/(cp_R-1)
    p0o = p0i * pr
    t0o = t0i * pr**((gamma-1) / (gamma * n))
    work = (cp_R * 8314.462/28.9) * (t0o - t0i)
    return np.array([t0o, p0o, work])

def burner(t0i, p0i, f):
    n = 0.99
    cp_R = 3.7 + .66*(t0i/1000)**2 - 0.2*(t0i/1000)**34
    hr = 43520000
    pr = 0.95

    cp = cp_R * 8314.462/28.9
    t0o = (n*f*hr/cp + t0i)/(1+f)
    p0o = p0i * pr
    return np.array([t0o, p0o])


def turbine(t0i, p0i, f, b, work):
    n = 0.94
    cp_R = 3.38 + 0.7*(t0i/1000)**2 - 0.2*(t0i/1000)**3

    cp = cp_R * 8314.462/28.9
    gamma = cp_R/(cp_R - 1)
    t0o = t0i - work/cp/((1 + f - b))
    p0o = p0i * (t0o / t0i)**((gamma / (gamma-1)) / n)
    return np.array([t0o, p0o])

def turbineMixer(t0i1, p0i1, t0i2, p0i2, m1, m2):
    cp_R1 = 3.70 + 0.78*(t0i1/1000)**2 - 0.36*(t0i1/1000)**3
    cp_R2 = 3.43 + 0.78*(t0i2/1000)**2 - 0.27*(t0i2/1000)**3
    
    cp1 = cp_R1 * 8314.462/28.9
    cp2 = cp_R2 * 8314.462/28.9
    t0e = (m2*cp2*t0i2 + m1*cp1*t0i1)/(m2*cp2 + m1*cp1)
    p0e = p0i1**(m1/(m1+m2)) * p0i2**(m2/(m1+m2)) * (t0e/t0i1)**(cp_R1 * (m1/(m1+m2))) * (t0e/t0i2)**(cp_R2 * (m2/(m1+m2)))
    return np.array([t0e, p0e])

def fanturbine(t0i, p0i, f, b, work): #DOESNT WORK FIX
    n = 0.94
    cp_R = 3.4 + 0.63*(t0i/1000)**2 - 0.2*(t0i/1000)**3

    cp = cp_R * 8314.462/28.9
    gamma = cp_R/(cp_R - 1)
    t0o = t0i - work/cp/((1 + f - b))
    p0o = p0i * (t0o / t0i)**((gamma / (gamma-1)) / n)
    return np.array([t0o, p0o])

def afterburner(t0i, p0i, f, m):
    n = 0.96
    cp_R = 3.5 + 0.72*(t0i/1000)**2 - 0.210*(t0i/1000)**3
    hr = 43520000
    pr = 0.97

    cp = cp_R * 8314.462/28.9
    t0o = (n*f*hr/cp + m*t0i)/(m+f)
    p0o = p0i * pr
    return np.array([t0o, p0o])


def corenozzle(t0i, p0i, pa):
    n = 0.96
    cp_R = 3.45 + 0.55*(t0i/1000)**2 - 0.15*(t0i/1000)**3

    cp = cp_R * 8314.462/28.9
    gamma = cp_R/(cp_R - 1)
    te = t0i * (1 - n * (1 - (pa/p0i)**((gamma-1)/gamma)))
    ue = (2 * cp * (t0i - te))**(0.5)
    Me = ue / (te * gamma * 8314.5 / 28.9)**(0.5)
    return np.array([te, ue, Me])

def fannozzle(t0i, p0i, pa):
    n = 0.97
    cp_R = 3.5
    
    cp = cp_R * 8314.462/28.9
    gamma = cp_R/(cp_R - 1)
    te = t0i * (1 - n * (1 - (pa/p0i)**((gamma-1)/gamma)))
    ue = (2 * cp * (t0i - te))**(0.5)
    Me = ue / (te * gamma * 8314.5 / 28.9)**(0.5)
    return np.array([te, ue, Me])

def nozzleMixer(t0i1, p0i1, t0i2, p0i2, m1, m2):
    t0prime = (m1*t0i1 + m2*t0i2) / (m1+m2)
    t0b1 = (t0i1 + t0prime) / 2
    t0b2 = (t0i2 + t0prime) / 2

    cp_R1 = 3.44 + 0.79*(t0b1/1000)**2 - 0.27*(t0b1/1000)**3
    cp_R2 = 3.43 + 0.79*(t0b2/1000)**2 - 0.28*(t0b2/1000)**3

    cp1 = cp_R1 * 8314.462/28.9
    cp2 = cp_R2 * 8314.462/28.9
    t0e = ((m2*cp2*t0i2) + (m1*cp1*t0i1) ) / ((m2*cp2) + (m1*cp1))
    p0temp = p0i1**(m1/(m1+m2)) * p0i2**(m2/(m1+m2)) * (t0e/t0i1)**(cp_R1 * (m1/(m1+m2))) * (t0e/t0i2)**(cp_R2 * (m2/(m1+m2)))

    cnm = 2
    if ((m2 < m1) & (m2 > 0)):
        Prnm = math.e ** (-cnm / (1 + (m1/m2)**0.5))
        p0e = p0temp * Prnm
    else:
        mr = m2 / m1
        p0e = p0temp
    
    return np.array([t0e, p0e])

def combinednozzle(t0i, p0i, pa):
    n = 0.96
    cp_R = 3.45 + 0.550*(t0i/1000.0)**2 - 0.150*(t0i/1000.0)**3

    cp = cp_R * 8314.462/28.9
    gamma = cp_R/(cp_R - 1)
    te = t0i * (1 - n * (1 - (pa/p0i)**((gamma-1)/gamma)))
    ue = (2 * cp * (t0i - te))**(0.5)
    Me = ue / (te * gamma * 8314.5 / 28.9)**(0.5)
    return np.array([te, ue, Me])


def performanceMetrics(ue1, ue2, M, ta, f, fab, beta, sigma):
    cp_R = 3.5
    hr = 43520000

    gamma = cp_R/(cp_R-1)
    u = M * (ta * gamma * 8314.462/28.9)**0.5
    ST = (ue1 * (1+f+fab + beta*(1-sigma)) + ue2*beta*sigma - u) / 1000
    TSFC = (f+fab)/ST * 3600
    n_p = ST*1000 * u / ((1+f+fab + beta*(1-sigma))*ue1**2 + (beta*sigma)*ue2**2 - u**2)
    n_o = ST*1000 * u / ((f + fab) * hr)
    n_th = ((1+f+fab + beta*(1-sigma))*ue1**2 + (beta*sigma)*ue2**2 - u**2) / ((f+fab)*hr)
    return np.array([ST, TSFC, n_th, n_p, n_o])
