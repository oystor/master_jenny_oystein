import numpy as np

def cauchy_number(length, width, thickness, velocity, E):
    rho = 1000
    Cd = 1.95
    I = (width*thickness**3)/12
    Ca = 0.5* (rho*Cd*width*velocity**2*length**3)/(E*I)
    return float(Ca)

def reduced_u(velocity, length, width, thickness, m_a, E):
    I = (width*thickness**3)/12
    U_red = velocity * length * np.sqrt(m_a/(E*I))
    return float(U_red)

def m_a(width):
    rho = 1000
    m_a = np.pi * rho * width**2 / 4
    return float(m_a)

#Configurations, models and velocities
config_list = ["S", "C"] 
model_list = ["A", "M", "J", "W"]
U = [0.03, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

#Dimensions of the models
lengths = [0.3014, 0.437, 0.5142, 0.5208] # m
widths = [0.046, 0.063, 0.0728, 0.073] # m
d = [0.000849, 0.000953, 0.000903, 0.001449] # m (thickness)
rho = [850, 754, 852, 1159] # kg/m^3 (density)    
E = 1.26 * 10**6 # Pa
t_c = 1.86 # cluster thickness parameter


""" print("SINGLE CONFIGURATION")
for i in range(len(model_list)):
    Ca_list = []
    reduced_u_list = []
    length = lengths[i]
    width = widths[i]
    thickness = d[i]
    ma = m_a(width)
    for j in range(len(U)):
        velocity = U[j]
        Ca = cauchy_number(length, width, thickness, velocity, E)
        u_red = reduced_u(velocity, length, width, thickness, ma, E)
        Ca_list.append(Ca)
        reduced_u_list.append(u_red)
    print("Model: ", model_list[i], ", added mass: ", ma)
    print ("Cauchy numbers: ")
    for k in range(len(U)):
        print(Ca_list[k])
    print ("Reduced velocities: ")
    for k in range(len(U)):
        print(reduced_u_list[k])

print("CLUSTER CONFIGURATION")
for i in range(len(model_list)):
    Ca_list = []
    reduced_u_list = []
    length = lengths[i]
    width = widths[i]*3
    thickness = d[i]*1.86
    ma = m_a(width)
    for j in range(len(U)):
        velocity = U[j]
        Ca = cauchy_number(length, width, thickness, velocity, E)
        u_red = reduced_u(velocity, length, width, thickness, ma, E)
        Ca_list.append(Ca)
        reduced_u_list.append(u_red)
    print("Model: ", model_list[i], ", added mass: ", ma)
    print ("Cauchy numbers: ")
    for k in range(len(U)):
        print(Ca_list[k])
    print ("Reduced velocities: ")
    for k in range(len(U)):
        print(reduced_u_list[k]) """

print("Length to width ratio")   
for i in range(len(model_list)):
    print("Model: ", model_list[i], ", L/W ratio: ", lengths[i]/widths[i])
    
