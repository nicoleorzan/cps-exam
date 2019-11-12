import numpy as np
import random

class ReinforcementLearning():

    def __init__(self, n_actions=3, alpha=0.4, gamma=0.9999999, learning_episodes = 6000):
        self.Tjsp_values = [20, 25, 26, 30, 35, 40, 45, 50, 52, 57, 60, 65, 70, 72, 80, 90, 94, 96, 100, 120] # [20, 30, 40, 50, 60, 90, 96, 100, 120]
        self.n_tjsp = len(self.Tjsp_values)
        self.Tr_values = [20, 30, 90, 100, 140] #[20, 30, 50, 60, 90, 100, 120, 140]
        self.n_tr = len(self.Tr_values)
        self.n_actions = n_actions
        self.Q = np.random.rand(self.n_tjsp,self.n_tr)
        self.alpha = alpha
        self.gamma = gamma
        self.learning_episodes = learning_episodes

    def state(self, Tjsp, Tr):
        self.s_tjsp = Tjsp
        self.s_tr = Tr

    def update_state(self, Tjsp, a, it):
        if (a == 2 and it == self.learning_episodes-1):
            Tjsp1 = Tjsp + a
        else:
            Tjsp1 = Tjsp + a - 1
        return Tjsp1

    def fill_Q(self, Tjsp_slice, Tr_slice, reward, Tjsp1_slice, Tr1_slice):
        self.Q[Tjsp_slice, Tr_slice] = self.Q[Tjsp_slice, Tr_slice] + self.alpha*(reward + \
            self.gamma*self.Q[Tjsp1_slice, Tr1_slice] - self.Q[Tjsp_slice, Tr_slice])

    def find_slice_TR(self, Tr):
        slice = 0
        for i in range(self.n_tr-1):
            if (Tr >= self.Tr_values[i] and Tr < self.Tr_values[i+1]):
                slice = i
        return slice

    def find_slice_TJSP(self, Tjsp):
        slice = 0
        for i in range(self.n_tjsp-1):
            if (Tjsp >= self.Tjsp_values[i] and Tjsp < self.Tjsp_values[i+1]):
                slice = i
        return slice

    def reward(self, T_set_point, T_r):
        reward = -abs(T_set_point - T_r)
        if (abs(T_set_point - T_r) < 5):
            reward = 1
        return reward

    def printmat(self):
        np.set_printoptions(precision=3)
        for idx, row in enumerate(self.Q):
            print("Tjsp= ",idx, ' '.join(map(str,np.round(row,2))))

    def select_action(self, epsilon, Tjsp_slice, Tr_slice):

        probab = random.randint(0,100)

        if (probab >= epsilon*100):
            if (Tjsp_slice == 0):
                a1 = 2
            elif(Tjsp_slice == self.n_tjsp-2):
                a1 = 0
            else:
                a1 = random.randint(0,2)

        else:
            if (Tjsp_slice == 0):
                arr = [-300000000000, self.Q[Tjsp_slice, Tr_slice], self.Q[Tjsp_slice+1, Tr_slice] ]
            elif (Tjsp_slice == self.n_tjsp-2):
                arr = [self.Q[Tjsp_slice-1, Tr_slice], self.Q[Tjsp_slice, Tr_slice], -300000000000]
            else:
                arr = [self.Q[Tjsp_slice-1, Tr_slice], self.Q[Tjsp_slice, Tr_slice], 
                        self.Q[Tjsp_slice+1, Tr_slice]]

            maxval = -100000
            for index, value in enumerate(arr):
                if (value > maxval):
                    a1 = index
                    maxval = value

        return a1