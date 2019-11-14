import numpy as np
import signals
import pickle
import mtl

def pickle_load(path):
    with open(path, 'rb') as handle:
        dict_values = pickle.load(handle)
    return dict_values

min_val = 20
max_val = 110
mmax = 299
interval = 0.5
times = np.arange(1,mmax,interval)

Signals = []
Signals.append(pickle_load(path='data/TRf1.txt'))
Signals.append(pickle_load(path='data/TRf2.txt'))
Signals.append(pickle_load(path='data/TRf3.txt'))
Signals.append(pickle_load(path='data/TRf4.txt'))
Signals.append(pickle_load(path='data/TRf5.txt'))
Signals.append(pickle_load(path='data/TRf6.txt'))
Signals.append(pickle_load(path='data/TRf7.txt'))
Signals.append(pickle_load(path='data/TRf8.txt'))

for TR in Signals:
    #print(TR[0], TR[1], TR[2], TR[100], TR[200])

    a = [(i,t-min_val) for i,t in zip(times, TR)]
    b = [(i,t-max_val) for i,t in zip(times, TR)]

    data = {
            'a': a,
            'b': b
        }
    phi = mtl.parse('G(a & ~b)')
    r = phi(data, quantitative=True)
    #robustness = r
    print(r)