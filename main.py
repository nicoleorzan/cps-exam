import pickle
import matplotlib.pyplot as plt
import signals
import PID_Loop

TR =  PID_Loop.loop(signals.constant_signal)
TR1 =  PID_Loop.loop(signals.f_signal)

# Saving reactor temperature data

with open("data/TR.txt", "wb") as fp:   
    pickle.dump(TR, fp)

with open("data/TR1.txt", "wb") as fp:   
    pickle.dump(TR1, fp)

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

# PLOTTING STUFF

"""plotter("reactor_temperature1", np.arange(1,mmax,interval), TR, \
        signals.constant_signal(np.arange(1,mmax,interval)), "Reactor temperature", \
        "Set Point", "Temperature", xlab = 'time')

plotter("reactor_temperature", np.arange(1,mmax,interval), TR1, \
        signals.f_signal(np.arange(1,mmax,interval)), "Reactor temperature", \
        "Set Point", "Temperature", xlab = 'time')

plotter("MA_MB_moles1", np.arange(1,mmax,interval), MA1, MB1, \
        "MA", "MB", ylab = "kmol", xlab = 'time')

plotter("MC_MD_moles1", np.arange(1,mmax,interval), MC1, MD1, \
        "MC", "MD", ylab = "kmol", xlab = 'time', colors = ['green', 'orange'])
"""