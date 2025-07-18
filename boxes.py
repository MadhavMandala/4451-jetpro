import numpy as np
import sympy as sp
import matplotlib

T = sp.symbols('T')

def diffuser(ta, pa, M, n, cp_R):
    gamma = cp_R/(cp_R-1)
    t0a = ta * (1 + ((gamma-1)/2)*M**2)
    p01 = pa * (1 + n*((gamma-1)/2)*M**2)**(gamma/(gamma-1))
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


def turbine(t0i, p0i, n, cp_R, work):
    t0e = sp.symbols("t0e")
    cp = cp_R * 8314.462/28.9
    workEq = sp.integrate(cp, (T, t0e, t0i))
    solution = sp.solve(workEq - work/n, t0e)
    t0o = solution[0]
    gamma = cp_R.subs(T, t0i).evalf()/(cp_R.subs(T, t0i).evalf()-1)
    p0o = p0i * (t0o / t0i)**(gamma / (gamma-1))
    return np.array([t0o, p0o])


"""
def fuelPump():




def turbine():




def fanTurbine():




def bypassNozzle():




def coreNozzle():




def combinedNozzle():






def afterburner():




def turbineMixer():




def nozzleMixer():





"""
