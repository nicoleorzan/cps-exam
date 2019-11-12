import numpy as np
import math
import signals
import random
import ReinforcementLearning as RF
import BatchReactor as Reactor
import matplotlib.pyplot as plt


debug = False
alpha = 0.4
gamma = 0.9999999

mmax = 299
interval = 2
times = np.arange(1, mmax, interval)

RF = RF.ReinforcementLearning()

TR = []

it = 0
while (it < RF.learning_episodes):

    epsilon = it/RF.learning_episodes
    print("epsilon: ", epsilon)

    # S
    if (it < RF.learning_episodes-1):
        R = Reactor.Reactor(random.randint(20,139), noise = None)
        Tjsp = random.randint(20,119)
    elif (it == RF.learning_episodes-1):
        R = Reactor.Reactor(20, noise = None)
        Tjsp = 20

    (Tr, Tj) = R.get_T()  
    Tr_slice = RF.find_slice_TR(Tr)
    Tjsp_slice = RF.find_slice_TJSP(Tjsp)
    M = R.get_M()

    # A   
    a = RF.select_action_slice(0, Tjsp_slice, Tr_slice)

    for _, k in enumerate(times):

        if (it == RF.learning_episodes-1):
            TR.append(Tr) 

        # R
        setpoint = signals.constant_signal(k) 
        reward = RF.reward(setpoint, Tr)

        R.dynamics(Tr, Tj, Tjsp, M, interval)
        (Tr1, Tj) = R.get_T()
        M = R.get_M()

        # S'
        Tr1_slice = RF.find_slice_TR(Tr1)

        if (Tr1 < 20):
            Tr1 = 20
        elif (Tr1 > 179):
            Tr1 = 179

        Tjsp1 = RF.update_state(Tjsp, a, it)
        Tjsp1_slice = RF.find_slice_TJSP(Tjsp1)

        # A'
        a1 = RF.select_action_slice(epsilon, Tjsp1_slice, Tr1_slice)
        
        if ( debug ):
            print("actual state Tjsp=", Tjsp, ", Tjsp_slice=", Tjsp_slice, ", Tr_slice=", \
                Tr_slice, ", Tr = ", Tr, ", a=", a)
            print("signal value=", setpoint, ", Tr=", Tr,", reward=", reward)
            print("next state Tjsp1=", Tjsp1, ", Tjsp1_slice=", Tjsp1_slice, ", Tr1_slice=", \
                Tr1_slice, ", Tr1=",Tr1)
            print("next action", a1, "\n")

        # Controls
        assert( math.isnan(reward) == False)
        assert( Tjsp1 >= 20 and Tjsp1 <= 119 )
        assert( math.isnan(RF.Q[Tjsp_slice, Tr_slice]) == False)
        assert( math.isnan(RF.Q[Tjsp1_slice, Tr1_slice]) == False)

        if (it != RF.learning_episodes-1):
            RF.fill_Q(Tjsp_slice, Tr_slice, reward, Tjsp1_slice, Tr1_slice)
            #RF.Q[Tjsp_slice, Tr_slice] = RF.Q[Tjsp_slice, Tr_slice] + alpha*(reward + \
            #                gamma*RF.Q[Tjsp1_slice, Tr1_slice] - RF.Q[Tjsp_slice, Tr_slice])           

        if (Tr1 >= 170):
            break

        Tr_slice = Tr1_slice
        Tjsp_slice = Tjsp1_slice
        Tr = Tr1
        Tjsp = Tjsp1
        a = a1

    it = it + 1


RF.printmat()

#np.savetxt('data/Q.txt', RF.Q, fmt='%d')
#Q = np.loadtxt('data/Q.txt', dtype=double)

plt.figure(figsize=(10, 7))
plt.plot(times, TR, label = "Tr")
plt.plot(times, signals.constant_signal(times), label = "signal")
plt.xlabel("time", fontsize=18)
plt.ylabel("T", fontsize=18)
plt.xticks(fontsize=17)
plt.yticks(fontsize=17)
plt.legend(fontsize=18)
plt.grid()
plt.show()