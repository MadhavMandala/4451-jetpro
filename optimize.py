from scipy.optimize import minimize, Bounds, LinearConstraint, NonlinearConstraint
from simulator import inputs_to_metrics
import numpy as np

T_a = 223
p_a = 26400
M = 0.95
ST = 1050

def vectorized_engine(inputs):
    return inputs_to_metrics(inputs[0], inputs[1], inputs[2], inputs[3], inputs[4], inputs[5], inputs[6], inputs[7], inputs[8], inputs[9])

# T_a, p_a, M, Pr_c, Pr_f, Beta, b, sigma, f, f_ab
lower_bounds = [T_a, p_a, M,      1, 1.15, 1,    0, 0,    0, 0]
upper_bounds = [T_a, p_a, M, np.inf, 1.7, 15, 0.15, 1, 0.05, 0.05]
bounds = Bounds(lower_bounds, upper_bounds)

Pr_const = NonlinearConstraint(lambda x: vectorized_engine(x)["Pr_c"] * vectorized_engine(x)["Pr_f"], 0, 55)
Tb_const = NonlinearConstraint(lambda x: vectorized_engine(x)["T_04"] - vectorized_engine(x)["T_max"], -np.inf, 0)
Tb_ab_const = NonlinearConstraint(lambda x: vectorized_engine(x)["T_06"] - vectorized_engine(x)["T_max_ab"], -np.inf, 0)
ST_const = NonlinearConstraint(lambda x: vectorized_engine(x)["ST"], ST, ST)

# T_a, p_a, M, Pr_c, Pr_f, Beta, b, sigma, f, f_ab
x0 = np.array([288, 101300, 0.2, 10.0, 1.2, 0.03, 0.0, 0.06, 2, 0.5])
res = minimize(
    lambda x: vectorized_engine(x)["TSFC"],
    x0,
    method="SLSQP",
    bounds=bounds,
    constraints=[Pr_const, Tb_const, Tb_ab_const, ST_const],
    options=dict(maxiter=10000, ftol=1e-15)
)
print(res.message)
outputs = vectorized_engine(res.x)
print("TSFC:", outputs["TSFC"]*3600*1000)  # Convert to kg/kN/h
print("Specific Thrust:", outputs["ST"]/1000)
print("Overall Efficiency:", outputs["eta_o"]*100)
# print("T_a, p_a, M, Pr_c, Pr_f, Beta, b, sigma, f, f_ab:\n", res.x)
print("T_a:", res.x[0])
print("p_a:", res.x[1])
print("M:", res.x[2])
print("Pr_c:", res.x[3])
print("Pr_f:", res.x[4])
print("Beta:", res.x[5])
print("b:", res.x[6])
print("sigma:", res.x[7])
print("f:", res.x[8])
print("f_ab:", res.x[9])
