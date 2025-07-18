
#   Nozzle method. Input T06, P06, T02, P02, sigma, and Pa to find Te, ue, Me, Tef, uef, Mef
def nozzle(T06, P06, T02, P02, Pa, sigma):

    split = True

    # Core Values
    MWc = 28.9
    CpoRc = 3.45 + 0.55*(T06/1000)**2 - 0.15*(T06/1000)**3
    Rc = 8314 / MWc
    etanc = 0.96
    Cpc = CpoRc * Rc

    # Bypass Values
    MWs = 28.9
    CpoRs = 3.5
    Rs = 8314 / MWs
    etans = 0.97
    Cps = CpoRs * Rs

    # See if Core and Bypass are completely mixed
    if (sigma == 0):
        split = False
        Tef = 'NaN'
        uef = 'NaN'
        Mef = 'Nan'


    # CORE Finds static exit temperature using isentropic relations
    Te = T06 * (1 - etanc * (1 - (Pa/P06)**(1/CpoRc))) 

    # CORE Find exit velocity
    ue = (2*Cpc*(T06-Te))**0.5

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
    

T06 = 1403
P06 = 126900
T02 = 289.2
P02 = 26960
Pa = 11000
sigma = 1
print(nozzle(T06, P06, T02, P02, Pa, sigma))
