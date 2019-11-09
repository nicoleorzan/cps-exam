import numpy as np

class Reactor():
    
    def __init__(self):
        # CONSTANTS

        self.MWa = 30
        self.MWb = 100
        self.MWc = 130
        self.MWd = 160
        self.Crhoa = 75.31
        self.Crhob = 167.36
        self.Crhoc = 217.57
        self.Crhod = 334.73
        self.Crhoj = 1.8828

        self.k11 = 20.9057
        self.k12 = 10000
        self.k21 = 38.9057
        self.k22 = 17000

        self.DH1 = -41840
        self.DH2 = -25105
        self.U = 40.842
        self.rho = 1000
        self.rhoj = 1000
        
        self.r = 0.5
        self.Fj = 0.348
        self.Vj = 0.6921
        self.A = 6.24

        #initial conditions
        self.Ma = 12
        self.Mb = 12
        self.Mc = 0
        self.Md = 0
        
        self.Tr = 20
        self.Tj = 20

        self.M = [self.Ma, self.Mb, self.Mc, self.Md]
        
        
    def dynamics(self, Tr, Tj, Tjsp, M, dt):

        k1 = np.exp(self.k11 - self.k12/(Tr + 273.15))
        k2 = np.exp(self.k21 - self.k22/(Tr + 273.15))

        dM0 = - k1*M[0]*M[1] - k2*M[0]*M[2]
        dM1 = - k1*M[0]*M[1]
        dM2 = k1*M[0]*M[1] - k2*M[0]*M[2]
        dM3 = k2*M[0]*M[2]

        self.M[0] = M[0] + dM0*dt
        self.M[1] = M[1] + dM1*dt
        self.M[2] = M[2] + dM2*dt
        self.M[3] = M[3] + dM3*dt

        Mr = self.M[0] + self.M[1] + self.M[2] + self.M[3]
        Crhor = (self.Crhoa*self.M[0] + self.Crhob*self.M[1] + self.Crhoc*self.M[2] +  self.Crhod*self.M[3])/Mr
        #W = self.MWa*self.M[0] + self.MWb*self.M[1] + self.MWc*self.M[2] + self.MWd*self.M[3] 

        self.Qj = self.U*self.A*(Tj - Tr)
        self.Qr = -self.DH1*(k1*self.M[0]*self.M[1]) - self.DH2*(k2*self.M[0]*self.M[2]) #Qr = -DH1*R[0] - DH2*R[1]

        dTr = (self.Qr+self.Qj)/(Mr*Crhor)
        dTj = (self.Fj*self.rhoj*self.Crhoj*(Tjsp-Tj)-self.Qj)/(self.Vj*self.rhoj*self.Crhoj)

        self.Tr = Tr + dTr*dt
        self.Tj = Tj + dTj*dt

        if (Tj > 120):
            Tj = 120
        elif (Tj < 20):
            Tj = 20
  
    def get_T(self):
        return (self.Tr, self.Tj)
    
    def get_Q(self):
        return (self.Qr, self.Qj)
    
    def get_M(self):
        return self.M