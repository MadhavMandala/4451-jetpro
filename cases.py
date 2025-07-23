from optimize import optimize, vectorized_engine
import numpy as np

# Reduce this number for a better runtime.
# Too many iterations can lead to overfitting
# and may not yield better results.
# Set to 1 for quick testing, or increase for thorough optimization.
# Consider using 2 iterations for low risk and high reward.
iter_count = 2

# Takeoff conditions
print("Takeoff conditions:")

T_a = 288
p_a = 101300
M = 0.2
ST = 1230
x0 = np.array([T_a, p_a, M, 47, 1.15, 8.88, 0, 0, 0.03, 0])

for i in range(iter_count):
    print("_________________________________")
    print(f"Iteration {i+1}/{iter_count}:")
    x0 = optimize(T_a, p_a, M, ST, x0)
    x0[0] = T_a
    x0[1] = p_a
    x0[2] = M
    x0 = x0.round(4)

takeoff_metrics = vectorized_engine(x0)

print("Optimization complete.")
print("_________________________________")

# Low cruise conditions
print("Low cruise conditions:")

T_a = 223
p_a = 26400
M = 0.95
ST = 1050
x0 = np.array([T_a, p_a, M, 47, 1.15, 8.88, 0, 0, 0.03, 0])

for i in range(iter_count):
    print("_________________________________")
    print(f"Iteration {i+1}/{iter_count}:")
    x0 = optimize(T_a, p_a, M, ST, x0)
    x0[0] = T_a
    x0[1] = p_a
    x0[2] = M
    x0 = x0.round(4)

low_cruise_metrics = vectorized_engine(x0)

print("Optimization complete.")
print("_________________________________")

# High cruise conditions
print("High cruise conditions:")

T_a = 223
p_a = 26400
M = 0.95
ST = 1460
x0 = np.array([T_a, p_a, M, 47, 1.15, 8.88, 0, 0, 0.03, 0])

for i in range(iter_count):
    print("_________________________________")
    print(f"Iteration {i+1}/{iter_count}:")
    x0 = optimize(T_a, p_a, M, ST, x0)
    x0[0] = T_a
    x0[1] = p_a
    x0[2] = M
    x0 = x0.round(4)

high_cruise_metrics = vectorized_engine(x0)

print("Optimization complete.")
print("_________________________________")

# Supersonic conditions
print("Supersonic conditions:")

T_a = 216
p_a = 9810
M = 1.6
ST = 874
x0 = np.array([T_a, p_a, M, 47, 1.15, 8.88, 0, 0, 0.03, 0])

for i in range(iter_count):
    print("_________________________________")
    print(f"Iteration {i+1}/{iter_count}:")
    x0 = optimize(T_a, p_a, M, ST, x0)
    x0[0] = T_a
    x0[1] = p_a
    x0[2] = M
    x0 = x0.round(4)

supersonic_metrics = vectorized_engine(x0)

print("Optimization complete.")
print("_________________________________")
