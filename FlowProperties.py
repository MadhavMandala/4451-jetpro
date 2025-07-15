import numpy as np

class FlowProperties:
    def __init__(self):
        self.velocity = np.nan
        self.density = np.nan
        self.pressure = np.nan
        self.temperature = np.nan
        self.stagnation_temperature = np.nan
        self.stagnation_pressure = np.nan
        self.mach_number = np.nan
        self.specific_heat_capacity = np.nan
        self.enthalpy = np.nan
        self.stagnation_enthalpy = np.nan

