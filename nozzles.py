
#   Core Nozzle method. Input T06, P06, and Pa to find Te, ue, Me
def coreNozzle(T06, P06, Pa):

    MW = 28.9
    CpoR = 3.45 + 0.55*(T06/1000)**2 - 0.15*(T06/1000)**3
    R = 8314 / MW
    etan = 0.96

    Cp = CpoR * R

    # Finds static exit temperature using isentropic relations
    Te = T06 * (Pa/P06)**(1/CpoR)

    # Find exit velocity
    ue = (2*Cp*etan*(T06-Te))**0.5

    # Find R and gamma using CPG relations
    R = Cp / CpoR
    gamma = Cp / (Cp - R)

    # Finds exit Mach number using above info
    Me = ue / (gamma * R * Te)**0.5

    return Te, ue, Me
    

print(coreNozzle(1403, 126900, 11000))
