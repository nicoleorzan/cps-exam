import numpy as np
import math
import random
import ReinforcementLearning as RF
import BatchReactor as Reactor
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

learning_episodes = 3000
alpha = 0.8
gamma = 0.9999999

points1 = [0, 20, 300]
signal1 = [95, 95, 95]
constant_signal = interp1d(points1, signal1)

mmax = 299
interval = 2

RF = RF.ReinforcementLearning(n_tjsp = 100, n_tr = 10)
#RF.printmat()

TR = []
TJSP = []

for it in range(learning_episodes):

    epsilon = it/learning_episodes
    print("epsilon: ", epsilon)

    # S

    if (it < learning_episodes-1):
        R = Reactor.Reactor(random.randint(0,130))
        Tjsp = random.randint(0,119)
    elif (it == learning_episodes-1):
        R = Reactor.Reactor(20)
        Tjsp = 20
    (Tr, Tj) = R.get_T()
    Tr_slice = RF.find_slice(Tr)
    M = R.get_M()

    # A   
    a = RF.select_action(0, Tjsp, Tr)

    for _, k in enumerate(np.arange(1, mmax, interval)):

        print("actual state Tjsp=", Tjsp, ", Tr_slice=", Tr_slice, ", Tr = ", Tr, ", a=", a)

        if (it == learning_episodes-1):
            print(it)
            TR.append(Tr)
            #TJSP.append(Tjsp)

        # R
        setpoint = constant_signal(k) 
        reward = RF.reward(setpoint, Tr)
        if (math.isnan(reward)):
            break
        print("signal value=", setpoint, ", Tr=", Tr,", reward=", reward)

        R.dynamics(Tr, Tj, Tjsp, M, interval)
        (Tr1, Tj) = R.get_T()
        M = R.get_M()
        Tr1_slice = RF.find_slice(Tr1)

        if (Tr1 < 20):
            Tr1 = 20
            print("limiting Tr1 ", Tr1)
        elif (Tr1 > 179):
            Tr1 = 179
            print("limiting Tr1 ", Tr1)

        if (a == 0):
            Tjsp1 = Tjsp - 1
        elif(a == 1):
            Tjsp1 = Tjsp
        elif(a == 2):
            Tjsp1 = Tjsp + 1

        # S'
        print("next state Tjsp=", Tjsp1, ", Tr1_slice=", Tr1_slice, ", Tr1=",Tr1)
        if (Tjsp1 < 20):
            print("Tjsp1 = \nbreak", Tjsp1)
            break
        if (Tjsp1 > 119):
            print("Tjsp1 = \nbreak", Tjsp1)
            break

        # A'
        a1 = RF.select_action(epsilon, Tjsp1, Tr1_slice)
        print("next action", a1, "\n")

        if (math.isnan(RF.Q[Tjsp-20, Tr_slice])):
            print("nan ", RF.Q[Tjsp-20, Tr_slice])
            break
        if (math.isnan(RF.Q[Tjsp1-20, Tr1_slice])):
            print("nan ", RF.Q[Tjsp1-20, Tr1_slice])
            break

        RF.Q[Tjsp-20, Tr_slice] = RF.Q[Tjsp-20, Tr_slice] + alpha*(reward + \
                            gamma*RF.Q[Tjsp1-20, Tr1_slice] - RF.Q[Tjsp-20, Tr_slice])

        Tr_slice = Tr1_slice
        Tr = Tr1
        Tjsp = Tjsp1
        a = a1
        #print("\n")

RF.printmat()

times = np.arange(1, mmax, interval)
plt.figure(figsize=(10, 7))
plt.plot(times, TR, label = "Tr")
plt.plot(times, constant_signal(times), label = "signal")
plt.xlabel("time", fontsize=18)
plt.ylabel("T", fontsize=18)
plt.xticks(fontsize=17)
plt.yticks(fontsize=17)
plt.legend(fontsize=18)
plt.grid()
plt.show()
plt.savefig("prova.png")