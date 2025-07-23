from optimize import optimize
import numpy as np

# Takeoff conditions
print("Takeoff conditions:")

T_a = 288
p_a = 101300
M = 0.2
ST = 1230
x0 = np.array([T_a, p_a, M, 47, 1.15, 8.88, 0, 0, 0.03, 0])

optimize(T_a, p_a, M, ST, x0)

print("Optimization complete.")
print("_________________________________")

# Low cruise conditions
print("Low cruise conditions:")

T_a = 223
p_a = 26400
M = 0.95
ST = 1050
x0 = np.array([T_a, p_a, M, 47, 1.15, 8.88, 0, 0, 0.03, 0])

optimize(T_a, p_a, M, ST, x0)

print("Optimization complete.")
print("_________________________________")

# High cruise conditions
print("High cruise conditions:")

T_a = 223
p_a = 26400
M = 0.95
ST = 1460
x0 = np.array([T_a, p_a, M, 47, 1.15, 8.88, 0, 0, 0.03, 0])

optimize(T_a, p_a, M, ST, x0)

print("Optimization complete.")
print("_________________________________")

# Supersonic conditions
print("Supersonic conditions:")

T_a = 216
p_a = 9810
M = 1.6
ST = 874
x0 = np.array([T_a, p_a, M, 47, 1.15, 8.88, 0, 0, 0.03, 0])

optimize(T_a, p_a, M, ST, x0)

print("Optimization complete.")
print("_________________________________")
