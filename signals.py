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