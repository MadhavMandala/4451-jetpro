import numpy as np
from optimize import vectorized_engine
from scipy.optimize import minimize, Bounds, LinearConstraint, NonlinearConstraint

x_takeoff = lambda T, p, M, b, f, f_ab: np.array([T, p, M, 44, 1.25, 9.2, b, 1, f, 0])
x_low_trans = lambda T, p, M, b, f, f_ab: np.array([T, p, M, 35, 1.57, 1.79, b, 0, f, 0])
x_high_trans = lambda T, p, M, b, f, f_ab: np.array([T, p, M, 0.95, 30, 1.15, 2.52, b, 0, f, f_ab])
x_super = lambda T, p, M, b, f, f_ab: np.array([T, p, M, 35.60106161672914, 1.15, 1.280819092652712, b, 0.0, f, 0])

def optim_x(ins, func):
    x = func(*ins)
    return 1/vectorized_engine(x)["ST"]

lower_bounds = lambda T, p, M: np.array([T, p, M, 0, 0, 0])
upper_bounds = lambda T, p, M: np.array([T, p, M, 0.15, 0.05, 0.05])
bounds = Bounds(lower_bounds, upper_bounds)

x0 = lambda T, p, M: np.array([T, p, M, 0.1, 0.025, 0.005])

Pr_const = NonlinearConstraint(lambda x: vectorized_engine(x)["Pr_c"] * vectorized_engine(x)["Pr_f"], 1, 55)
Tb_const = NonlinearConstraint(lambda x: vectorized_engine(x)["T_04"] - vectorized_engine(x)["T_max"], -2401, 0)
Tb_ab_const = NonlinearConstraint(lambda x: vectorized_engine(x)["T_06"] - vectorized_engine(x)["T_max_ab"], -2401, 0)

minimizer = lambda T, p, M: minimize(
        lambda x: optim_x(x, ),
        x0,
        bounds=bounds,
        constraints=[Pr_const, Tb_const, Tb_ab_const],
        method='SLSQP',
        options={'maxiter': 2000, 'ftol': 1e-6}
    )
