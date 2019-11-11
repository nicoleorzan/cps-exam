import numpy as np
import pickle
import mtl
import signals

# UPLOAD DATA


with open("data/TR.txt", "rb") as fp:  
    TR = pickle.load(fp)

with open("data/TR1.txt", "rb") as fp:  
    TR1 = pickle.load(fp)

mmax = 299
interval = 0.5
min_val = 20
max_val = 160
times = np.arange(1,mmax,interval)


# ==================================   REQUIREMENT 1   =========================================
# ==============  Check if signal is contained into defined limits: CONSTANT SIGNAL ============ 


print(" 1) Requirement: G( Tr(t) > 20 & Tr(t) < 160 )")

phi1 = [(i,t-min_val) for i,t in zip(times, TR)]
phi2 = [(i,t-max_val) for i,t in zip(times, TR)]

data = {
    'phi1': phi1,
    'phi2': phi2
}
phi3 = mtl.parse('G(phi1 & ~phi2)')
out = phi3(data, time=None)

robustness = phi3(data, quantitative=True)
beta = phi3(data, quantitative=False)
print("robustness = ", robustness)
print("\n")


# ==================================   REQUIREMENT 2   ========================================
# 2) ==============  Check if signal oscillations are contained: CONSTANT SIGNAL ==============  


print(" 2) Requirement: Eventually from a time between 0 and 100, the distance between the output\
 and the real signal becomes smaller than 0.5 \nF[1,100] (G(|Tr(t) - constant_signal| < 0.5))")

signal = 95
limit = 0.5

TRprim = [x - signal for x in TR]
a = [ (t, T - limit) for t, T in zip(times,TRprim)]
b = [ (t, T + limit) for t, T in zip(times,TRprim)]

data = {
    'a': a, # Trprim - 0.5 > 0 --> change sign
    'b': b  # Trprim + 0.5 > 0
}
phi = mtl.parse('G(~a & b)') #  ~a because I want to evaluate a<0
out = phi(data, time=None) # out is QUANTITATIVE, and > 0 when G is true, < 0 when G is false

data1 = {
    'out': out
}

phi2 = mtl.parse('F[1,100](out)')
out1 = phi2(data1, time=None)
robustness = phi2(data1, quantitative=True)
beta = phi2(data1, quantitative=False)
print("robustness = ", robustness)
print("\n")


# ===================================   REQUIREMENT 3   ======================================
# 3) ======================== Computing step function: VARYING SIGNAL ======================== 


c = 1
tau = 5

print(" 3) Requirement: each time there is a step in the output, evetually in", tau, "time steps\
the distance between the output and the real signal becomes smaller than", c)   
print("G(step(TR) -> F[0,",tau,"]|TR - signal| <",c,")")

diff = [x - xref for x, xref in zip(TR1, signals.f_signal(times))]
a = [ (t, d - c) for t, d in zip(np.arange(1,mmax,interval),diff)]
b = [ (t, d + c) for t, d in zip(np.arange(1,mmax,interval),diff)]

data = {
    'a': a, # x - xref < 0.5  ===> x - xref - 0.5 < 0     change sign
    'b': b  # x - xref > -0.5 ===> x - xref + 0.5 > 0
}
phi = mtl.parse('G[0,5](~a & b)')
out = phi(data, time=None)

def step(tr, t, tau):
    if (t+tau < len(tr)):
        return tr[t+tau] - tr[t]

steps = [(t, step(TR1, i, tau)) if (i < len(TR1)-tau) else (t, 0)  for i,t in enumerate(times)]
#out_bool = [(s[0], 1) if (s[1]>0) else (s[0], 0) for idx, s in enumerate(out)]
#steps_bool = [(t, 1) if (elem[1] >= 1) else (t, 0) for t, elem in zip(times, steps)]

data = {
    'out': out,
    'step': steps
}
phi = mtl.parse('G(step -> out)')
phi(data, time=None)

robustness = phi(data, quantitative=True)
print("robsutness = ", robustness) # NEGATIVE
beta = phi(data, quantitative=False)
print("False for the first 100 time steps, cutting them:")

# ====> cutting the first 100 time steps (50 min)
steps1 = steps[100:]
out1 = out[100:]

data = {
    'out': out1,
    'step': steps1
}
phi = mtl.parse('G(step -> out)')
phi(data, time=None)

robustness = phi(data, quantitative=True)
print("robsutness = ", robustness) 
beta = phi(data, quantitative=False)