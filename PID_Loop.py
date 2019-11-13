import numpy as np
import BatchReactor as Reactor
import Simple_PID

def loop(signal_function, noise = None, mmax = 299, interval = 0.5):
    
    TR = []
    MA = []
    MB = []
    MC = []
    MD = []

    # variables initialization
    ek = 0
    ek_1 = 0
    ek_2 = 0
    Tjsp = 20
    R = Reactor.Reactor(T0 = 20, noise=noise)
    (Tr, Tj) = R.get_T()
    M = R.get_M()
    PID = Simple_PID.Simple_PID()

    for _, k in enumerate(np.arange(1, mmax, interval)):
        
        R.dynamics(Tr, Tj, Tjsp, M, interval)
        (Tr, Tj) = R.get_T()
        if (noise != None):
            Tj = Tj + np.random.normal(0,1)*np.sqrt(noise)

        M = R.get_M()
        MA.append(M[0])
        MB.append(M[1])
        MC.append(M[2])
        MD.append(M[3])
        TR.append(Tr)
    
        ek = signal_function(k) - Tr

        PID.update_PID(ek, ek_1, ek_2, dt = interval)

        Tjsp = PID.get_PID()

        if (noise != None):
            Tjsp = Tjsp + np.random.normal(0,1)*np.sqrt(noise)
        else:
            Tjsp = Tjsp + np.random.normal(0,1)*np.sqrt(0.04)
        
        if (Tjsp > 120):
            Tjsp = 120
        elif (Tjsp < 20):
            Tjsp = 20

        ek_2 = ek_1
        ek_1 = ek

    return TR, MA, MB, MC, MD