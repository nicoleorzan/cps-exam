from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import normal
import BatchReactor as Reactor
import Simple_PID


def plotter(name, times, plot_vals1, plot_vals2, label1, label2, ylab, xlab = 'time', colors = ['#1f77b4', '#ff7f0e']):
    plt.figure(figsize=(10, 7))
    plt.plot(times, plot_vals1, label = label1, color = colors[0])
    plt.plot(times, plot_vals2, label = label2, color = colors[1])
    plt.xlabel(xlab, fontsize=18)
    plt.ylabel(ylab, fontsize=18)
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=17)
    plt.legend(fontsize=18)
    plt.grid()
    plt.savefig(name+".png", bbox_inches='tight')

points = [0, 30, 50, 100, 140, 160, 200, 240, 300]
signal = [25, 30, 62, 85, 85, 77, 77, 85, 85]
f_signal = interp1d(points, signal)

points1 = [0, 20, 300]
signal1 = [25, 95, 95]
constant_signal = interp1d(points1, signal1)

mmax = 299
interval = 0.5

def loop(signal_function, mmax = mmax, interval = interval):
    
    TR = [];    TJ = [];    TJSP = []   
    QJ = [];    QR = []
    MA = [];    MB = [];    MC = [];    MD = []
    Set_point = [];    Controlled_var = []

    # variables initialization
    ek = 0
    ek_1 = 0
    ek_2 = 0
    Tjsp = 20
    R = Reactor.Reactor()
    (Tr, Tj) = R.get_T()
    M = R.get_M()
    PID = Simple_PID.Simple_PID()

    for _, k in enumerate(np.arange(1, mmax, interval)):
        
        R.dynamics(Tr, Tj, Tjsp, M, interval)
        (Tr, Tj) = R.get_T()
        (Qr, Qj) = R.get_Q()
        M = R.get_M()
        MA.append(M[0])
        MB.append(M[1])
        MC.append(M[2])
        MD.append(M[3])
        QJ.append(Qj)
        QR.append(Qr)
        TR.append(Tr)
        #Tj = Tj + normal(0,1)*np.sqrt(0.04)
        TJ.append(Tj)
        Controlled_var.append(Tjsp)
        
        setpoint = signal_function(k) # k+1?
        Set_point.append(setpoint)
        
        ek = setpoint - Tr

        PID.update_PID(ek, ek_1, ek_2, dt = interval)
        #PID.update_PID(setpoint, Tr, dt = interval)
        Tjsp = PID.get_PID()
        Tjsp = Tjsp + normal(0,1)*np.sqrt(0.04)
        
        if (Tjsp > 120):
            Tjsp = 120
        elif (Tjsp < 20):
            Tjsp = 20
            
        TJSP.append(Tjsp)

        # update errors

        ek_2 = ek_1
        ek_1 = ek
    

    MAE = sum([abs(x - y) for x, y in zip(Set_point, Controlled_var)])/mmax

    return (TJ, TR, QJ, QR, TJSP, Set_point, Controlled_var, MA, MB, MC, MD)



TJ, TR, QJ, QR, TJSP, Set_point, Controlled_var, MA, MB, MC, MD =  loop(constant_signal)
TJ1, TR1, QJ1, QR1, TJSP1, Set_point1, Controlled_var1, MA1, MB1, MC1, MD1 =  loop(f_signal)

plotter("reactor_temperature1", np.arange(1,mmax,interval), TR, \
        constant_signal(np.arange(1,mmax,interval)), "Reactor temperature", \
        "Set Point", "Temperature", xlab = 'time')

plotter("reactor_temperature", np.arange(1,mmax,interval), TR1, \
        f_signal(np.arange(1,mmax,interval)), "Reactor temperature", \
        "Set Point", "Temperature", xlab = 'time')

plotter("MA_MB_moles1", np.arange(1,mmax,interval), MA1, MB1, \
        "MA", "MB", ylab = "kmol", xlab = 'time')

plotter("MC_MD_moles1", np.arange(1,mmax,interval), MC1, MD1, \
        "MC", "MD", ylab = "kmol", xlab = 'time', colors = ['green', 'orange'])

