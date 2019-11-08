class Simple_PID():
    
    def __init__(self, Kc = 32.54, Ki = 4.87, Kd = 0.43, P = 25):
        
        self.Kc = Kc
        self.Ki = Ki 
        self.Kd = Kd 
        self.P = P
        
    def update_PID(self, ek, ek_1, ek_2, dt):
        self.P = self.P + self.Kc*((ek-ek_1) + dt/self.Ki*ek + self.Kd/dt*(ek - 2*ek_1 + ek_2))
        
    def get_PID(self):
        return self.P