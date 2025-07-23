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

lower_bounds = np.array([])
upper_bounds = np.array([])
bounds = Bounds(lower_bounds, upper_bounds)


