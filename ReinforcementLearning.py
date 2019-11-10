import numpy as np
import random

class ReinforcementLearning():

    def __init__(self, n_tjsp=100, n_tr=10, n_actions=3):
        #tjsp va da 20 a 120
        #tr va da 20 a 200
        self.n_tjsp = n_tjsp
        self.n_tr = n_tr
        self.Tr_values = [20, 40, 50, 60, 70, 80, 90, 100, 120, 140]
        self.n_actions = n_actions
        self.Q = np.random.rand(n_tjsp,n_tr)*0.0001 # np.zeros((n_tjsp, n_tr))

    def state(self, Tjsp, Tr):
        self.s_tjsp = Tjsp
        self.s_tr = Tr

    def find_slice(self, Tr):
        slice = 0
        for i in range(self.n_tr-1):

            if (Tr >= self.Tr_values[i] and Tr < self.Tr_values[i+1]):
                slice = i
        return slice

    def reward(self, T_set_point, T_r):
        divid = T_set_point - T_r
        if (T_set_point - T_r < 0.05):
            divid = 0.005
        reward = 1/divid
        return reward

    def printmat(self):
        np.set_printoptions(precision=3)
        for idx, row in enumerate(self.Q):
            print("Tjsp= ",idx, ' '.join(map(str,np.round(row,2))))

    def select_action(self, epsilon, Tjsp, Tr_slice):

        probab = random.randint(0,100)
        if (probab >= epsilon*100):
            print("random\n")
            if (Tjsp == 20):
                a1 = 2
            elif(Tjsp == 119 or Tjsp == 118):
                a1 = 0
            else:
                a1 = random.randint(0,2)
        else:
            if (Tjsp == 20):
                #print('1')
                arr = [-3000, self.Q[Tjsp-20, Tr_slice], self.Q[Tjsp-20+2, Tr_slice] ]
            elif (Tjsp == 119 or Tjsp == 118):
                #print('2')
                arr = [self.Q[Tjsp-20-1, Tr_slice], self.Q[Tjsp-20, Tr_slice], -3000]
            else:
                #print('3 Tjsp=', Tjsp," Tr=", Tr_slice)
                arr = [self.Q[Tjsp-20-1, Tr_slice], self.Q[Tjsp-20, Tr_slice], self.Q[Tjsp-20+1, Tr_slice]]
            #print(arr)
            maxval = -100000
            for index, value in enumerate(arr):
                if (value > maxval):
                    a1 = index
                    maxval = value

        #print("a1 =", a1)
        return a1
        


