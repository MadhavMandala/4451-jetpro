
#   Core Nozzle method. Input T06, P06, and Pa to find Te, ue, Me
def coreNozzle(T06, P06, Pa, CpoR, Cp):

    # Finds static exit temperature using isentropic relations
    Te = T06 * (Pa/P06)^(1/CpoR)

    # Find exit velocity
    ue = sqrt(2*Cp*(T06-Te))

    # Find R and gamma using CPG relations
    R = Cp / CpoR
    gamma = Cp / (Cp - R)

    # Finds exit Mach number using above info
    Me = ue / sqrt(gamma * R * Te)

    return Te, ue, Me
    