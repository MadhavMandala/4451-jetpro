import numpy as np
from optimize import vectorized_engine

x_takeoff = np.array([288, 101300, 0.2, 44, 1.25, 9.2, 0, 1, 0.010784998404094956, 0])
x_low_trans = np.array([223, 26400, 0.95, 35, 1.57, 1.79, 0.15, 0, 0.026267573006153986, 0])
x_high_trans = np.array([223, 26400, 0.95, 30, 1.15, 2.52, 0.15, 0, 0.031952769231086565, 0.0036410601514871694])
x_super = np.array([216, 9810, 1.6, 35.60106161672914, 1.15, 1.280819092652712, 0.15, 0.0, 0.02729479, 0])

takeoff = vectorized_engine(x_takeoff)
low_trans = vectorized_engine(x_low_trans)
high_trans = vectorized_engine(x_high_trans)
supersonic = vectorized_engine(x_super)

# I reccomend accessing the data below this line as you need it rather than
# just printing the whole thing out. There's... a lot.
