import pickle
import numpy as np
import matplotlib.pyplot as plt
import signals
import PID_Loop
import mtl

num_trajectories = 50
noise = 3
TR = {}
for i in range(num_trajectories):
    TR[i] = PID_Loop.loop(signals.constant_signal, noise=noise)

with open('data/stat_constant_noise'+str(noise)+'.pickle', 'wb') as handle:
    pickle.dump(TR, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('data/stat_constant_noise'+str(noise)+'.pickle', 'rb') as handle:
    TR = pickle.load(handle)

# Falsification: let's see if there is a trace which goes under 20 or above 160

print("1) Falsify the requirement G( Tr(t) > 20 & Tr(t) < 160 ) for a set of 100 traces with noise=", noise)
min_val = 20
max_val = 160
mmax = 299
interval = 0.5
times = np.arange(1,mmax,interval)


plt.figure(figsize=(10, 7))
for i, TRi in TR.items():
    plt.plot(times, TRi)
plt.xlabel("time", fontsize=18)
plt.ylabel("T", fontsize=18)
plt.xticks(fontsize=17)
plt.yticks(fontsize=17)
plt.grid()
plt.savefig("stat_constant_noise"+str(noise)+".png", bbox_inches='tight')
plt.show()


robustness = {}
for i, TRi in TR.items():

    a = [(i,t-min_val) for i,t in zip(times, TRi)]
    b = [(i,t-max_val) for i,t in zip(times, TRi)]

    data = {
        'a': a,
        'b': b
    }
    phi = mtl.parse('G(a & ~b)')
    #out = phi(data, time=None)
    #print(out)
    r = phi(data, quantitative=True)
    robustness[i] = r
    #print("robustness = ", robustness)
    #beta = phi(data, quantitative=False)

print(robustness)

beta0 = 0
beta1 = 0
for i, r in robustness.items():
    if (r < 0): 
        beta0 = beta0 + 1
    else:
        beta1 = beta1 + 1

print("Fraction of traces which falsify the requirement:", beta0/(beta0 + beta1))
print("Fraction of traces which verifies the requirement:", beta1/(beta0 + beta1))
