import numpy as np
import math
import random
import ReinforcementLearning as RF
import BatchReactor as Reactor
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

#kind of working with le = 3000 and tjsp slices = [20, 30, 50, 60, 70, 80, 90, 100, 120]
learning_episodes = 6000 # 2000
alpha = 0.4 #0.4
gamma = 0.9999999

points1 = [0, 20, 300]
signal1 = [95, 95, 95]
constant_signal = interp1d(points1, signal1)

mmax = 299
interval = 2

RF = RF.ReinforcementLearning()
RF.printmat()

TR = []
TJSP = []

it = 0
while (it < learning_episodes):

    epsilon = it/learning_episodes
    print("epsilon: ", epsilon)

    # S
    if (it < learning_episodes-1):
        R = Reactor.Reactor(random.randint(20,139), noise = None)
        Tjsp = random.randint(20,119)
    elif (it == learning_episodes-1):
        R = Reactor.Reactor(20, noise = None)
        Tjsp = 20
    (Tr, Tj) = R.get_T()
    Tr_slice = RF.find_slice_TR(Tr)
    Tjsp_slice = RF.find_slice_TJSP(Tjsp)
    M = R.get_M()

    # A   
    a = RF.select_action_slice(0, Tjsp_slice, Tr_slice)
    #a = RF.select_action(epsilon, Tjsp, Tr_slice)

    for _, k in enumerate(np.arange(1, mmax, interval)):

        #print("actual state Tjsp=", Tjsp, ", Tjsp_slice=", Tjsp_slice, ", Tr_slice=", Tr_slice, ", Tr = ", Tr, ", a=", a)

        if (it == learning_episodes-1):
            TR.append(Tr)
            #TJSP.append(Tjsp)

        # R
        setpoint = constant_signal(k) 
        reward = RF.reward(setpoint, Tr)
        if (math.isnan(reward)):
            it = learning_episodes
            break
        #print("signal value=", setpoint, ", Tr=", Tr,", reward=", reward)

        R.dynamics(Tr, Tj, Tjsp, M, interval)
        (Tr1, Tj) = R.get_T()
        (Qr, Qj) = R.get_Q()
        #print("Qr = ", Qr, "Qj =", Qj)
        M = R.get_M()
        Tr1_slice = RF.find_slice_TR(Tr1)

        if (Tr1 < 20):
            Tr1 = 20
            #print("limiting Tr1 ", Tr1)
        elif (Tr1 > 179):
            Tr1 = 179
            #print("limiting Tr1 ", Tr1)

        if (a == 0):
            Tjsp1 = Tjsp - 1
        elif(a == 1):
            Tjsp1 = Tjsp
        elif(a == 2 and it == learning_episodes-1):
            Tjsp1 = Tjsp + 2
        elif(a == 2):
            Tjsp1 = Tjsp + 1
        Tjsp1_slice = RF.find_slice_TJSP(Tjsp1)

        # S'
        #print("next state Tjsp1=", Tjsp1, ", Tjsp1_slice=", Tjsp1_slice, ", Tr1_slice=", Tr1_slice, ", Tr1=",Tr1)
        if (Tjsp1 < 20):
            print("=====>Tjsp1 = ", Tjsp1, "break\n")
            it = it + learning_episodes
            break
        if (Tjsp1 > 119):
            print("=====>Tjsp1 = ", Tjsp1, "break\n")
            it = it + learning_episodes
            break

        # A'
        a1 = RF.select_action_slice(epsilon, Tjsp1_slice, Tr1_slice)
        #a1 = RF.select_action(epsilon, Tjsp1, Tr1_slice)
        #print("next action", a1, "\n")

        if (math.isnan(RF.Q[Tjsp_slice, Tr_slice])):
            it = learning_episodes
            print("nan ", RF.Q[Tjsp_slice, Tr_slice])
            break
        if (math.isnan(RF.Q[Tjsp1_slice, Tr1_slice])):
            it = learning_episodes
            print("nan ", RF.Q[Tjsp1_slice, Tr1_slice])
            break

        if (Tr1 >= 170):
            RF.Q[Tjsp_slice, Tr_slice] = RF.Q[Tjsp_slice, Tr_slice] + alpha*(reward + \
                            gamma*RF.Q[Tjsp1_slice, Tr1_slice] - RF.Q[Tjsp_slice, Tr_slice])
            break

        if (it != learning_episodes-1):
            RF.Q[Tjsp_slice, Tr_slice] = RF.Q[Tjsp_slice, Tr_slice] + alpha*(reward + \
                            gamma*RF.Q[Tjsp1_slice, Tr1_slice] - RF.Q[Tjsp_slice, Tr_slice])

        Tr_slice = Tr1_slice
        Tjsp_slice = Tjsp1_slice
        Tr = Tr1
        Tjsp = Tjsp1
        a = a1
        #print("\n")

    if (it == learning_episodes-1):
            RF.printmat()
    it = it + 1
#RF.printmat()

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
plt.savefig("rl.png")