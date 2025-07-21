import numpy as np
import sympy as sp
import math
import matplotlib

T = sp.symbols('T')

def diffuser(ta, pa, M, n, cp_R):

    if 1 < M < 5:
        r_d = 1 - 0.075 * (M - 1) ** 1.35
    else:
        r_d = 1

    gamma = cp_R/(cp_R-1)
    t0a = ta * (1 + ((gamma-1)/2)*M**2)
    p01 = pa * r_d * (1 + n * ((gamma-1)/2)*M**2)**(gamma/(gamma-1))
    t01 = t0a
    return np.array([t01, p01])


def compressor(t0i, p0i, n, b, cp_R, pr): 
    gamma = cp_R/(cp_R-1)
    p0o = p0i * pr
    t0o = t0i * pr**((gamma-1) / (gamma * n))
    work = (cp_R * 8314.462/28.9) * (t0o - t0i)
    return np.array([t0o, p0o, work])


def burner(t0i, p0i, n, cp_R, f, hr, pr):
    delH = n*f*hr
    cp = cp_R * 8314.462/28.9
    indefinite = sp.integrate(cp, T)
    eq = indefinite - delH
    solution = sp.solve(eq, T)
    t0o = solution[0] + t0i
    p0o = p0i * pr
    return np.array([t0o, p0o])

def afterburner(t0i, p0i, n, cp_R, f, m, hr, pr):
    delH = n*f*hr
    cp = cp_R.subs(T, t0i).evalf() * 8314.462/28.9
    t0o = (n*f*hr/cp + m*t0i)/(m+f)
    p0o = p0i * pr
    return np.array([t0o, p0o])


def turbine(t0i, p0i, f, b, n, cp_R, work): #DOESNT WORK FIX
    cp = cp_R * 8314.462/28.9
    gamma = cp_R.subs(T, t0i).evalf()/(cp_R.subs(T, t0i).evalf() - 1)
    t0o = t0i - work/cp.subs(T, t0i).evalf()/((1 + f - b))
    p0o = p0i * (t0o / t0i)**((gamma / (gamma-1)) / n)
    return np.array([t0o, p0o])

def turbineMixer(t0i1, p0i1, t0i2, p0i2, m1, m2, cp_R1, cp_R2):
    cp_R1s = cp_R1.subs(T, t0i1).evalf()
    cp_R2s = cp_R2.subs(T, t0i2).evalf()
    cp1 = cp_R1.subs(T, t0i1).evalf() * 8314.462/28.9
    cp2 = cp_R2.subs(T, t0i2).evalf() * 8314.462/28.9

    t0e = (m2*cp2*t0i2 + m1*cp1*t0i1)/(m2*cp2 + m1*cp1)

    p0e = p0i1**(m1/(m1+m2)) * p0i2**(m2/(m1+m2)) * (t0e/t0i1)**(cp_R1s * (m1/(m1+m2))) * (t0e/t0i2)**(cp_R2s * (m2/(m1+m2)))
    return np.array([t0e, p0e])

def nozzle(t0i, p0i, pa, n, cp_R):
    cp = cp_R * 8314.462/28.9
    gamma = cp_R.subs(T, t0i).evalf()/(cp_R.subs(T, t0i).evalf() - 1)
    te = t0i * (1 - n * (1 - (pa/p0i)**((gamma-1)/gamma)))
    ue = (2 * cp.subs(T, t0i).evalf() * (t0i - te))**(0.5)
    Me = ue / (te * gamma * 8314.5 / 28.9)**(0.5)
    return np.array([te, ue, Me])

def nozzleMixer(t0i1, p0i1, t0i2, p0i2, m1, m2, cp_R1, cp_R2):
    t0prime = (m1*t0i1 + m2*t0i2) / (m1+m2)
    t0b1 = (t0i1 + t0prime) / 2
    t0b2 = (t0i2 + t0prime) / 2
    cp_R1 = cp_R1.subs(T, t0b1).evalf()
    cp_R2 = cp_R2.subs(T, t0b2).evalf()
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


def performanceMetrics(ue1, ue2, M, ta, f, fab, beta, sigma, cp_R, hr):
    gamma = cp_R/(cp_R-1)
    u = M * (ta * gamma * 8314.462/28.9)**0.5
    ST = (ue1 * (1+f+fab + beta*(1-sigma)) + ue2*beta*sigma - u) / 1000
    TSFC = (f+fab)/ST * 3600
    n_p = ST*1000 * u / ((1+f+fab + beta*(1-sigma))*ue1**2 + (beta*sigma)*ue2**2 - u**2)
    n_o = ST*1000 * u / ((f + fab) * hr)
    n_th = ((1+f+fab + beta*(1-sigma))*ue1**2 + (beta*sigma)*ue2**2 - u**2) / ((f+fab)*hr)
    return np.array([ST, TSFC, n_th, n_p, n_o])
