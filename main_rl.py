import numpy as np
import ReinforcementLearning as RL
import BatchReactor as Reactor
import matplotlib.pyplot as plt
import Shield
import signals
import random
import math


debug = False

mmax = 299
interval = 2
times = np.arange(1, mmax, interval)

def train(Q_filename):

    RF = RL.ReinforcementLearning()
    it = 0
    while (it < RF.learning_episodes):

        epsilon = it/RF.learning_episodes
        print("epsilon: ", epsilon)

        # S
        R = Reactor.Reactor(random.randint(20,139), noise = None)
        Tjsp = random.randint(20,119)

        (Tr, Tj) = R.get_T()  
        M = R.get_M()
        Tr_slice = RF.find_slice_TR(Tr)
        Tjsp_slice = RF.find_slice_TJSP(Tjsp)

        # A   
        a = RF.select_action(0, Tjsp_slice, Tr_slice)

        for _, k in enumerate(times):

            # R
            reward = RF.reward(signals.c_signal(k), Tr)

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
            a1 = RF.select_action(epsilon, Tjsp1_slice, Tr1_slice)
            
            if ( debug ):
                print("actual state Tjsp=", Tjsp, ", Tjsp_slice=", Tjsp_slice, ", Tr_slice=", \
                    Tr_slice, ", Tr = ", Tr, ", a=", a)
                print("signal value=", signals.constant_signal(k) , ", Tr=", Tr,", reward=", reward)
                print("next state Tjsp1=", Tjsp1, ", Tjsp1_slice=", Tjsp1_slice, ", Tr1_slice=", \
                    Tr1_slice, ", Tr1=",Tr1)
                print("next action", a1, "\n")

            # Controls
            assert( math.isnan(reward) == False)
            assert( Tjsp1 >= 20 and Tjsp1 <= 119 )
            assert( math.isnan(RF.Q[Tjsp_slice, Tr_slice]) == False)
            assert( math.isnan(RF.Q[Tjsp1_slice, Tr1_slice]) == False)

            RF.fill_Q(Tjsp_slice, Tr_slice, reward, Tjsp1_slice, Tr1_slice)
                
            if (Tr1 >= 170):
                break

            Tr_slice = Tr1_slice
            Tjsp_slice = Tjsp1_slice
            Tr = Tr1
            Tjsp = Tjsp1
            a = a1

        it = it + 1

    RF.printmat()
    np.savetxt(Q_filename, RF.Q, fmt='%d')



def test(epsilon, file):

    TR = []
    RF = RL.ReinforcementLearning()
    RF.Q = np.loadtxt(file)

    R = Reactor.Reactor(20, noise = None)
    Tjsp = 20

    (Tr, Tj) = R.get_T()  
    M = R.get_M()
    Tr_slice = RF.find_slice_TR(Tr)
    Tjsp_slice = RF.find_slice_TJSP(Tjsp)

    a = RF.select_action(0, Tjsp_slice, Tr_slice)

    for _,_ in enumerate(times):

        TR.append(Tr)

        R.dynamics(Tr, Tj, Tjsp, M, interval)
        M = R.get_M()
        (Tr, Tj) = R.get_T()

        if (Tr < 20):
            Tr = 20
        elif (Tr > 179):
            Tr = 179

        Tr_slice = RF.find_slice_TR(Tr)

        Tjsp = RF.update_state(Tjsp, a, it=RF.learning_episodes)
        Tjsp_slice = RF.find_slice_TJSP(Tjsp)

        a = RF.select_action(epsilon, Tjsp_slice, Tr_slice)

    return TR




#train(Q_filename='data/Q.txt')

TR = test(epsilon = 1, file ='data/Q.txt')


plt.figure(figsize=(10, 7))
plt.plot(times, TR, label = "Tr")
plt.plot(times, signals.c_signal(times), label = "signal")
plt.xlabel("time", fontsize=18)
plt.ylabel("T", fontsize=18)
plt.xticks(fontsize=17)
plt.yticks(fontsize=17)
plt.legend(fontsize=18)
plt.grid()
plt.show()