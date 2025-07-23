import numpy as np
from scipy.optimize import minimize, Bounds, NonlinearConstraint
from engines import *


ta = 288
pa = 101300
M = 0.2
ST = 1.23

def objective(x):
    Prc, Prf, f, fab, b, beta, sigma = x
    pm = turbofan_afterburner_separate(ta, pa, M, Prc, Prf, f, fab, b, beta, sigma)
    return pm[1]  # TSFC

# --- Bounds (example) ---
lb = [0.0001, 1.15, 0.0001, 0, 0, 0, 0.0001]
ub = [55, 1.7, 0.06, 0.01, 0.15, 15, 1]
bounds = Bounds(lb, ub)

# --- Nonlinear constraints (examples) ---
def thrust_constraint(x):
    pm = turbofan_afterburner_separate(ta, pa, M, *x)
    return ST - pm[0]  # require at least 100 kN

def pth(x):
    pm = turbofan_afterburner_separate(ta, pa, M, *x)
    return pm[2]

def pp(x):
    pm = turbofan_afterburner_separate(ta, pa, M, *x)
    return pm[3]

def po(x):
    pm = turbofan_afterburner_separate(ta, pa, M, *x)
    return pm[4]

def cmax(x):
    pm = turbofan_afterburner_separate(ta, pa, M, *x)
    return pm[5]

def abmax(x):
    pm = turbofan_afterburner_separate(ta, pa, M, *x)
    return pm[6]

nlc = NonlinearConstraint(thrust_constraint, 0.0, 0)
nlc2 = NonlinearConstraint(pth, 0.0, .8)
nlc3 = NonlinearConstraint(pp, 0.0, 1)
nlc4 = NonlinearConstraint(po, 0.0, 1)
nlc5 = NonlinearConstraint(cmax, 0, 1400)
nlc5 = NonlinearConstraint(abmax, 0, 2300)


x0 = np.array([10.0, 1.2, 0.03, 0.0, 0.06, 2, 0.5])

res = minimize(objective, x0, method="SLSQP",
               bounds=bounds, constraints=[nlc, nlc2, nlc3, nlc4],
               options=dict(maxiter=2000, ftol=1e-9))

print("Status:", res.message)
print("TSFC  :", res.fun)
print("x*    :", res.x)

print(turbofan_afterburner_separate(ta, pa, M, *res.x))