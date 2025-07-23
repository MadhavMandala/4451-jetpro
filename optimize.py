from scipy.optimize import minimize, Bounds, LinearConstraint, NonlinearConstraint
from simulator import inputs_to_metrics
import numpy as np

def vectorized_engine(inputs):
    return inputs_to_metrics(inputs[0], inputs[1], inputs[2], inputs[3], inputs[4], inputs[5], inputs[6], inputs[7], inputs[8], inputs[9])

def optimize(T_a, p_a, M, ST, x0):

    # T_a, p_a, M, Pr_c, Pr_f, Beta, b, sigma, f, f_ab
    lower_bounds = [T_a, p_a, M, 1, 1.15, 0, 0.15, 0, 0, 0]
    upper_bounds = [T_a, p_a, M, 55, 1.7, 15, 0.15, 0, 0.05, 0.05]
    bounds = Bounds(lower_bounds, upper_bounds)

    Pr_const = NonlinearConstraint(lambda x: vectorized_engine(x)["Pr_c"] * vectorized_engine(x)["Pr_f"], 1, 55)
    Tb_const = NonlinearConstraint(lambda x: vectorized_engine(x)["T_04"] - vectorized_engine(x)["T_max"], -2401, 0)
    Tb_ab_const = NonlinearConstraint(lambda x: vectorized_engine(x)["T_06"] - vectorized_engine(x)["T_max_ab"], -2401, 0)
    ST_const = NonlinearConstraint(lambda x: vectorized_engine(x)["ST"], ST, ST)

    # T_a, p_a, M, Pr_c, Pr_f, Beta, b, sigma, f, f_ab
    res = minimize(
        lambda x: vectorized_engine(x)["TSFC"],
        x0,
        bounds=bounds,
        constraints=[Pr_const, Tb_const, Tb_ab_const, ST_const],
        method='SLSQP',
        options={'maxiter': 20000, 'ftol': 1e-9}
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

    return res.x

if __name__ == "__main__":
    T_a = 216
    p_a = 9810
    M = 1.6
    ST = 874
    x = np.array([T_a, p_a, M, 35.60106161672914, 1.15, 1.280819092652712, 0.15, 0.0, 0.02729479, 0])

    outputs = vectorized_engine(x)

    # print(outputs)
    print("TSFC:", outputs["TSFC"]*3600*1000)  # Convert to kg/kN/h
    print("Specific Thrust:", outputs["ST"]/1000)
