import pickle
import numpy as np
import matplotlib.pyplot as plt
import signals
import PID_Loop

mmax = 299
interval = 0.5
times = np.arange(1,mmax,interval)

TRf1 =  PID_Loop.loop(signals.F1, mmax = mmax, interval = interval)
with open("data/TRf1.txt", "wb") as fp:   
    pickle.dump(TRf1, fp)
TRf2 =  PID_Loop.loop(signals.F2, mmax = mmax, interval = interval)
with open("data/TRf2.txt", "wb") as fp:   
    pickle.dump(TRf2, fp)
TRf3 =  PID_Loop.loop(signals.F3, mmax = mmax, interval = interval)
with open("data/TRf3.txt", "wb") as fp:   
    pickle.dump(TRf3, fp)
TRf4 =  PID_Loop.loop(signals.F4, mmax = mmax, interval = interval)
with open("data/TRf4.txt", "wb") as fp:   
    pickle.dump(TRf4, fp)
TRf5 =  PID_Loop.loop(signals.F5, mmax = mmax, interval = interval)
with open("data/TRf5.txt", "wb") as fp:   
    pickle.dump(TRf5, fp)
TRf6 =  PID_Loop.loop(signals.F6, mmax = mmax, interval = interval)
with open("data/TRf6.txt", "wb") as fp:   
    pickle.dump(TRf6, fp)
TRf7 =  PID_Loop.loop(signals.F7, mmax = mmax, interval = interval)
with open("data/TRf7.txt", "wb") as fp:   
    pickle.dump(TRf7, fp)
TRf8 =  PID_Loop.loop(signals.F8, mmax = mmax, interval = interval)
with open("data/TRf8.txt", "wb") as fp:   
    pickle.dump(TRf8, fp)

#TR =  PID_Loop.loop(signals.f_signal, mmax = mmax, interval = interval)
#TR1 =  PID_Loop.loop(signals.f_signal, mmax = mmax, interval = interval)

# Saving reactor temperature data

"""with open("data/TR.txt", "wb") as fp:   
    pickle.dump(TR, fp)

with open("data/TR1.txt", "wb") as fp:   
    pickle.dump(TR1, fp)"""

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

"""plotter("f1", times, TRf1, \
        signals.F1(times), "Reactor temperature", \
        "Set Point", "Temperature", xlab = 'time')
plotter("f2", times, TRf2, \
        signals.F2(times), "Reactor temperature", \
        "Set Point", "Temperature", xlab = 'time')
plotter("f3", times, TRf3, \
        signals.F3(times), "Reactor temperature", \
        "Set Point", "Temperature", xlab = 'time')
plotter("f4", times, TRf4, \
        signals.F4(times), "Reactor temperature", \
        "Set Point", "Temperature", xlab = 'time')
plotter("f5", times, TRf5, \
        signals.F5(times), "Reactor temperature", \
        "Set Point", "Temperature", xlab = 'time')
plotter("f6", times, TRf6, \
        signals.F6(times), "Reactor temperature", \
        "Set Point", "Temperature", xlab = 'time')
plotter("f7", times, TRf7, \
        signals.F7(times), "Reactor temperature", \
        "Set Point", "Temperature", xlab = 'time')
plotter("f8", times, TRf8, \
        signals.F8(times), "Reactor temperature", \
        "Set Point", "Temperature", xlab = 'time')"""


fig = plt.figure()
fig.subplots_adjust(hspace=0.4, wspace=0.4)
for i in range(1, 7):
    ax = fig.add_subplot(2, 3, i)
    plt.plot(times, TRf7)
plt.savefig("prova.png")

fig, axs = plt.subplots(2, 4, sharex='col', sharey='row',
gridspec_kw={'hspace': 0, 'wspace': 0}, figsize=(20, 10))
(ax1, ax2, ax3, ax4),(ax5, ax6, ax7, ax8)= axs
ax1.plot(times, TRf1, label = "1")
ax1.plot(times, signals.F1(times), label = "1")
ax1.set_xlabel("Time", size = 20)
ax1.set_ylabel("Temperature (s)", size = 20)
ax1.grid()
ax2.plot(times, TRf2, label = "1")
ax2.plot(times, signals.F2(times), label = "1")
ax2.grid()
ax3.plot(times, TRf3, label = "1")
ax3.plot(times, signals.F3(times), label = "1")
ax3.grid()
ax4.plot(times, TRf4, label = "1")
ax4.plot(times, signals.F4(times), label = "1")
ax5.set_xlabel("Time", size = 20)
ax5.set_ylabel("Temperature (s)", size = 20)
ax4.grid()
ax5.plot(times, TRf5, label = "1")
ax5.plot(times, signals.F5(times), label = "1")
ax5.grid()
ax6.plot(times, TRf6, label = "1")
ax6.plot(times, signals.F6(times), label = "1")
ax6.set_xlabel("Time", size = 20)
ax6.grid()
ax7.plot(times, TRf7, label = "1")
ax7.plot(times, signals.F7(times), label = "1")
ax7.set_xlabel("Time", size = 20)
ax7.grid()
ax8.plot(times, TRf8, label = "1")
ax8.plot(times, signals.F8(times), label = "1")
ax8.set_xlabel("Time", size = 20)
ax8.grid()
plt.savefig('alltogheter.png', bbox_inches='tight')


"""plotter("reactor_temperature1", times, TR, \
        signals.constant_signal(times), "Reactor temperature", \
        "Set Point", "Temperature", xlab = 'time')

plotter("reactor_temperature", times, TR1, \
        signals.f_signal(times), "Reactor temperature", \
        "Set Point", "Temperature", xlab = 'time')

plotter("MA_MB_moles1", times, MA, MB, \
        "MA", "MB", ylab = "kmol", xlab = 'time')

plotter("MC_MD_moles1", times, MC, MD, \
        "MC", "MD", ylab = "kmol", xlab = 'time', colors = ['green', 'orange'])
"""