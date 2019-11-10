import numpy as np
import pickle
import mtl

with open("data/TR.txt", "rb") as fp:  
    TR = pickle.load(fp)

mmax = 299
interval = 0.5
min_val = 20
max_val = 160

# 1) == Check if signal is contained into defined limits == 
print("Requirement: G( Tr(t) > 20 & Tr(t) < 160 )")

phi1 = [(i,t-min_val) for i,t in zip(np.arange(1,mmax,interval), TR)]
phi2 = [(i,t-max_val) for i,t in zip(np.arange(1,mmax,interval), TR)]

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


# 2) == Check if signal oscillations are contained == 

print("Requirement: F[1,100] (G(|Tr(t) - constant_signal| < 0.5))")

signal = 95
limit = 0.5

TRprim = [x - signal for x in TR]
a = [ (t, T - limit) for t, T in zip(np.arange(1,mmax,interval),TRprim)]
b = [ (t, T + limit) for t, T in zip(np.arange(1,mmax,interval),TRprim)]

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