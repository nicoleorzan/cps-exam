from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import normal
import BatchReactor as Reactor
import Simple_PID

points = [0, 30, 50, 100, 140, 160, 200, 240, 300]
signal = [25, 30, 62, 85, 85, 77, 77, 85, 85]
f_signal = interp1d(points, signal)

points1 = [0, 20, 300]
signal1 = [25, 95, 95]
f_signal1 = interp1d(points1, signal1)

ek = 0
ek_1 = 0
ek_2 = 0
Tjsp = 20
TR = []
TJ = []
TJSP = []
QJ = []
QR = []
Set_point = []
Controlled_var = []
mmax = 299

R = Reactor.Reactor()
(Tr, Tj) = R.get_T()
M = R.get_M()
PID = Simple_PID.Simple_PID()
interval = 0.5
data = []
signal_data = []

for i, k in enumerate(np.arange(1, mmax, interval)):
    
    R.dynamics(Tr, Tj, Tjsp, M, interval)
    (Tr, Tj) = R.get_T()
    (Qr, Qj) = R.get_Q()
    M = R.get_M()
    
    QJ.append(Qj)
    QR.append(Qr)
    TR.append(Tr)
    #Tj = Tj + normal(0,1)*np.sqrt(0.04)
    TJ.append(Tj)
    
    setPoint = f_signal1(k+1) # o k?????????????????????
    Set_point.append(setPoint)
    
    Controlled_var.append(Tjsp)
    
    data.append((i,Tr))
    signal_data.append((i,setPoint))
    ek = setPoint - Tr
    
    PID.update_PID(ek, ek_1, ek_2, dt = interval)
    Tjsp = PID.get_PID()
    Tjsp = Tjsp + normal(0,1)*np.sqrt(0.04)
    
    if (Tjsp > 120):
        Tjsp = 120
    elif (Tjsp < 20):
        Tjsp = 20
        
    TJSP.append(Tjsp)

    # update errors

    ek_2 = ek_1
    ek_1 = ek
    
    
MAE = sum([abs(x - y) for x, y in zip(Set_point, Controlled_var)])/mmax


plt.figure(figsize=(8, 5))
plt.plot(np.arange(1,mmax,interval), TR)
#plt.plot(np.arange(1,mmax,interval), opt(np.arange(1,mmax,interval)) )
plt.plot(np.arange(1,mmax,interval), f_signal1(np.arange(1,mmax,interval)))
#plt.plot(np.arange(1,mmax,interval), TJ)
#plt.plot(np.arange(1,mmax,interval), TJSP, 'b')
plt.grid()
plt.savefig("reactor_temperature.png")