from read_force_file import cauchy_number, Cd_bulk
import numpy as np

config_list = ["S", "C"] 
model_list = ["A", "M", "J", "W"]
#model_list = ["W"]
lengths = np.array([31.55, 45.63, 53.93, 53.93]) * 10**(-2) # m 
widths = np.array([4.72, 6.54, 7.57, 7.57]) * 10**(-2) # m
d = 0.8 * 10**(-3) # m (thickness)
d_wavy = 1.2 * 10**(-3) # m (thickness for wavy model)
E = 1.26 * 10**6 # Pa
U_list = [0.03, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

for u in U_list:
    print(f"U: {u}")
    print(f"Ca *10**(-5) (t): {cauchy_number(lengths[1], widths[1], d, u, E)*10**(-5)}")
    #print(f"Ca *10**(-5) (5/3*t): {cauchy_number(lengths[0], 3*widths[0], (5/3)*d, u, E)*10**(-5)}")
    #print(f"Cd *10**(-5) (2*t): {cauchy_number(lengths[0], 3*widths[0], 2*d, u, E)*10**(-5)}")

