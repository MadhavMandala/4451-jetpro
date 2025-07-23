import numpy as np
from optimize import vectorized_engine
from scipy.optimize import minimize, Bounds, LinearConstraint, NonlinearConstraint

x_takeoff = lambda T, p, M, b, f, f_ab: np.array([T, p, M, 44, 1.25, 9.2, b, 1, f, 0])
x_low_trans = lambda T, p, M, b, f, f_ab: np.array([T, p, M, 35, 1.57, 1.79, b, 0, f, 0])
x_high_trans = lambda T, p, M, b, f, f_ab: np.array([T, p, M, 30, 1.15, 2.52, b, 0, f, f_ab])
x_super = lambda T, p, M, b, f, f_ab: np.array([T, p, M, 35.60106161672914, 1.15, 1.280819092652712, b, 0.0, f, 0])

def optim_x(ins, func):
    x = func(*ins)
    return vectorized_engine(x)

lower_bounds = lambda T, p, M: np.array([T, p, M, 0, 0, 0])
upper_bounds = lambda T, p, M: np.array([T, p, M, 0.15, 0.05, 0.05])

x0 = lambda T, p, M: np.array([T, p, M, 0.1, 0.025, 0.005])

minimizer = lambda T, p, M, params: minimize(
        lambda x: -optim_x(x, params)["ST"],
        x0(T, p, M),
        bounds=Bounds(lower_bounds(T, p, M), upper_bounds(T, p, M)),
        constraints=[NonlinearConstraint(lambda x: optim_x(x, params)["Pr_c"] * optim_x(x, params)["Pr_f"], 1, 55), 
                     NonlinearConstraint(lambda x: optim_x(x, params)["T_04"] - optim_x(x, params)["T_max"], -2401, 0), 
                     NonlinearConstraint(lambda x: optim_x(x, params)["T_06"] - optim_x(x, params)["T_max_ab"], -2401, 0)],
        method='SLSQP',
        options={'maxiter': 2000, 'ftol': 1e-6}
    )

takeoff_conditions = [288, 101325, 0.2]
transonic_conditions = [233, 26400, 0.95]
super_conditions = [216, 9810, 1.6]

def conditions_to_params(conditions, engine_vector):
    result = minimizer(*conditions, engine_vector)
    return vectorized_engine(engine_vector(*result.x))

# test = conditions_to_params(super_conditions, x_high_trans)
# print("ST: ", test["ST"]/1000)
# print("TSFC: ", test["TSFC"]*3.6e6)
# print(test)
