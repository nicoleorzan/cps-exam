import numpy as np
import pickle
import mtl
import signals

with open("data/TR.txt", "rb") as fp:  
    TR = pickle.load(fp)

mmax = 299
interval = 0.5
min_val = 20
max_val = 160
times = np.arange(1,mmax,interval)

# 1) ======================  Check if signal is contained into defined limits ======================= 

print("Requirement: G( Tr(t) > 20 & Tr(t) < 160 )")

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
print("beta = ",beta, "\n")


# 2) ======================  Check if signal oscillations are contained ======================  

print("Requirement: F[1,100] (G(|Tr(t) - constant_signal| < 0.5))")

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
print("beta = ",beta)


# 3) ====================== Computing step function ====================== 

c = 0.5
tau = 5

diff = [x - xref for x, xref in zip(TR, signals.f_signal(times))]
a = [ (t, d - c) for t, d in zip(np.arange(1,mmax,interval),diff)]
b = [ (t, d + c) for t, d in zip(np.arange(1,mmax,interval),diff)]

data = {
    'a': a, # x - xref < 0.5  ===> x - xref - 0.5 < 0     change sign
    'b': b  # x - xref > -0.5 ===> x - xref + 0.5 > 0
}
phi = mtl.parse('G[0,5](~a & b)')
out = phi(data, time=None)

def step(TR, t, tau):
    if (t+tau < len(TR)):
        return TR[t+tau] - TR[t]

steps = [step(TR, i, tau) if (i < len(TR)-tau) else 0 for i,t in enumerate(times)]
# define a real step when the step value is bigger or equal 1
steps_bool = [(t, 1) if (elem >=1) else (t, 0) for t, elem in zip(times, steps)]