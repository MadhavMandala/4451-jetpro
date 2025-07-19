import numpy
import math

# Nozzle Mixer: Feeds into the core nozzle
def nozzleMixer(T06,P06,T02,P02,Pa,sigma,beta,f,fab):

    MW = 28.9
    P06 = P06 * 1000
    P02 = P02 * 1000
    Pa = Pa * 1000

    # Finds estimated nozzle mixer output temp if both flows had the same Cp/R
    T07p = ( ( (1-sigma) * beta * T02 ) + ( (1+f+fab) * T06 ) ) / ( ((1-sigma) * beta) + (1+f+fab))

    # Finds T0 bar for the core and bypass
    T0bc = (T06 + T07p) / 2
    T0bby = (T02 + T07p) / 2

    # Finds the Cp/R for the core
    CpoRc = 3.44 + 0.79 * (T0bc / 1000) ** 2 - 0.27 * (T0bc / 1000) ** 3

    # Finds Cp/R for the bypass
    CpoRs = 3.43 + 0.79 * (T0bby / 1000) ** 2 - 0.28 * (T0bby / 1000) ** 3

    # Finds R
    R = 8314.462618 / MW

    # Finds Cp for the core air
    Cpc = CpoRc * R

    # Finds Cp for the bypass air
    Cps = CpoRs * R

    # Finds stagnation temp coming out of mixer
    T07 = ( ((1-sigma) * beta * Cps * T02) + ((1+f+fab) * Cpc * T06) ) / ( ((1-sigma) * beta * Cps) + ((1+f+fab) * Cpc) )

    # Finds reversible stagnation pressure coming out of the mixer
    exp1 = ((1-sigma) * beta) / ((1-sigma) * beta + 1 + f + fab)
    exp2 = (1 + f + fab) / ((1-sigma) * beta + 1 + f + fab)
    P07rev = (P02 ** exp1) * (P06 ** exp2) * ((T07/T06) ** (exp2 * CpoRc)) * ((T07/T02) ** (exp1 * CpoRs))

    # Finds adjusted stagnation pressure coming out of mixer
    Cnm = 2
    mdot1 = (1-sigma) * beta
    mdot2 = 1 + f

    if (mdot1 < mdot2):
        mr = mdot2 / mdot1
    else:
        mr = mdot1 / mdot2

    Prnm = math.e ** (-Cnm / (1 + mr ** 0.5))

    P07 = P07rev * Prnm

    P07 = P07 / 1000

    return T07, P07




#   Nozzle method. Input T06, P06, T02, P02, sigma, and Pa to find Te, ue, Me, Tef, uef, Mef
def nozzle(T07, P07, T02, P02, Pa, sigma):

    P07 = P07 * 1000
    P02 = P02 * 1000
    Pa = Pa * 1000

    # Core Values
    MWc = 28.9
    CpoRc = 3.45 + 0.55*(T07/1000)**2 - 0.15*(T07/1000)**3
    Rc = 8314.462618 / MWc
    etanc = 0.96
    Cpc = CpoRc * Rc

    # Bypass Values
    MWs = 28.9
    CpoRs = 3.5
    Rs = 8314.462618 / MWs
    etans = 0.97
    Cps = CpoRs * Rs

    # See if Core and Bypass are completely mixed
    if (sigma == 0):
        Tef = 'NaN'
        uef = 'NaN'
        Mef = 'Nan'


    # CORE Finds static exit temperature using isentropic relations
    Te = T07 * (1 - etanc * (1 - (Pa/P07)**(1/CpoRc))) 

    # CORE Find exit velocity
    ue = (2*Cpc*(T07-Te))**0.5

    # CORE Find R and gamma using CPG relations
    R = Cpc / CpoRc
    gamma = Cpc / (Cpc - R)

    # CORE Finds exit Mach number using above info
    Me = ue / (gamma * R * Te)**0.5

    # BYPASS Finds static exit temperature using isentropic relations
    Tef = T02 * (1 - etans * (1 - (Pa/P02)**(1/CpoRs))) 

    # BYPASS Find exit velocity
    uef = (2*Cps*(T02-Tef))**0.5

    # BYPASS Find R and gamma using CPG relations
    R = Cps / CpoRs
    gammas = Cps / (Cps - Rs)

    # BYPASS Finds exit Mach number using above info
    Mef = uef / (gammas * Rs * Tef)**0.5



    return Te, ue, Me, Tef, uef, Mef
    
T07, P07 = nozzleMixer(1403,126.9,289.2,26.96,11,0.72,1.5,0.025,0.005)
#T07 = 1403
#P07 = 126900
T02 = 289.2
P02 = 26.96
Pa = 11
sigma = 0.72
print(nozzle(T07, P07, T02, P02, Pa, sigma))
