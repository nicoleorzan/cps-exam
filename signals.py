from scipy.interpolate import interp1d

points = [0, 30, 50, 100, 140, 160, 200, 240, 300]
signal = [25, 30, 62, 85, 85, 77, 77, 85, 85]
f_signal = interp1d(points, signal)

points1 = [0, 20, 300]
signal1 = [25, 95, 95]
constant_signal = interp1d(points1, signal1)

points1 = [0, 20, 300]
signal1 = [95, 95, 95]
c_signal = interp1d(points1, signal1)

# Falsification traces

points = [0, 20, 30, 50, 100, 200, 300]
signal= [25, 10, 5, 50, 100, 95, 95]
F1 = interp1d(points, signal)

points = [0, 50, 70, 100, 140, 200, 250, 300]
signal= [25, 25, 50, 100, 130, 120, 100, 100]
F2 = interp1d(points, signal)

points = [0, 70, 100, 150, 200, 300]
signal= [25, 70, 100, 150, 150, 150]
F3 = interp1d(points, signal)

points = [0, 20, 70, 120, 170, 210, 250, 300]
signal= [25, 50, 20, 70, 100, 30, 30, 70]
F4 = interp1d(points, signal)

points = [0, 100, 300]
signal= [25, 50, 80]
F5 = interp1d(points, signal)

points = [0, 50, 100, 120, 150, 200, 300]
signal= [25, 20, 25, 50, 25, 50, 25]
F6 = interp1d(points, signal)

points = [0, 50, 220, 300]
signal= [25, 100, 120, 120]
F7 = interp1d(points, signal)

points = [0, 50, 220, 300]
signal= [25, 120, 170, 170]
F8 = interp1d(points, signal)



