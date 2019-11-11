import numpy as np
import BatchReactor as Reactor
import Simple_PID

def loop(signal_function, noise = None, mmax = 299, interval = 0.5):
    
    TR = []

    # variables initialization
    ek = 0
    ek_1 = 0
    ek_2 = 0
    Tjsp = 20
    if (noise != None):
        R = Reactor.Reactor(noise)
    else:
        R = Reactor.Reactor()
    (Tr, Tj) = R.get_T()
    M = R.get_M()
    PID = Simple_PID.Simple_PID()

    for _, k in enumerate(np.arange(1, mmax, interval)):
        
        R.dynamics(Tr, Tj, Tjsp, M, interval)
        (Tr, Tj) = R.get_T()
        if (noise == True):
            Tj = Tj + np.random.normal(0,1)*np.sqrt(0.5)

        M = R.get_M()
        TR.append(Tr)
        
        setpoint = signal_function(k)
        
        ek = setpoint - Tr

        PID.update_PID(ek, ek_1, ek_2, dt = interval)
        #PID.update_PID(setpoint, Tr, dt = interval)
        Tjsp = PID.get_PID()

        if (noise != None):
            Tjsp = Tjsp + np.random.normal(0,1)*np.sqrt(noise)
        else:
            Tjsp = Tjsp + np.random.normal(0,1)*np.sqrt(0.04)
        
        if (Tjsp > 120):
            Tjsp = 120
        elif (Tjsp < 20):
            Tjsp = 20
            
        #TJSP.append(Tjsp)

        # update errors

        ek_2 = ek_1
        ek_1 = ek
    

    #MAE = sum([abs(x - y) for x, y in zip(Set_point, Controlled_var)])/mmax

    return TR