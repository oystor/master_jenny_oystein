import catmanreader as cr
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from plot_loads import get_numerical_loads

def experiment_data(filename_bin, filename_TST):
    #Read file
    binary = cr.import_catman_binary(filename_bin)

    #Get data into lists  
    channels = list(range(8, 15))
    data, keys = binary.get_data(channels)
    channel_lists = {}

    for ch, values in data.items():
        name = binary.chanheaders[ch]['name']
        channel_lists[name] = values.tolist()

    water_speed = channel_lists['Water_Speed']
    Fx = channel_lists['Fx_calc']
    Fy = channel_lists['Fy_calc'] 
    Fz = channel_lists['Fz_calc']
    Mx = channel_lists['Mx_calc']
    My = channel_lists['My_calc']
    Mz = channel_lists['Mz_calc']

    #Make time series using the .TST file
    with open(filename_TST, encoding="utf-8") as f:
        lines = (f.readlines())
        fs = int(lines[12].split("=")[1].split(" ")[0])
        N = int(lines[15].split("=")[1].split("\n")[0])
    dt = 1 / fs
    time = np.arange(N) * dt

    return time, water_speed, Fx, Fy, Fz, Mx, My, Mz

def cut_timeseries(time1, time2, time, Fx, Fz):
    index_1 = np.argmin(np.abs(time - time1))
    index_2 = np.argmin(np.abs(time - time2))
    t = time[index_1:index_2]
    Fx = Fx[index_1:index_2]
    Fz = Fz[index_1:index_2]
    return t, Fx, Fz

###############################################################################
# ZERO VALUES
###############################################################################

velocities = ["03", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

#zero value is set as average of time series between 100 and 200s
Fx_zero_list = []
Fz_zero_list = []


for vel in velocities:
    filename_bin = "./Force_measurements/Z_" + vel + "_1.bin"
    filename_TST = "./Force_measurements/Z_" + vel + "_1.TST"
    time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
    t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)

    Fx_zero_list.append(np.mean(Fx))
    Fz_zero_list.append(np.mean(Fz))

#Fx_zero_list = [0, 0,0,0,0,0,0,0,0,0] # Set zero values to 0 for numerical comparison

#plt.plot(velocities,Fx_zero)
#plt.show()

###############################################################################
# CD BULK AND CAUCHY NUMBER
###############################################################################

def Cd_bulk(length, width, velocity, F_mean):
    rho = 1000
    return F_mean/(0.5*rho*width*length*velocity**2)

def cauchy_number(length, width, thickness, velocity, E):
    rho = 1000
    Cd = 1.95
    I = (width*thickness**3)/12
    Ca = 0.5* (rho*Cd*width*velocity**2*length**3)/(E*I)
    return float(Ca)

###############################################################################
# REPEATABIILITY
###############################################################################

""" config = "S" # S/C
model = "J" # A/M/J/W
speed = "3" # 3=0.3m/s
Fx_zero = Fx_zero_list[int(speed)] 

Fx_mean = []
Fx_max = []

#Looping through all 5 runs 
for i in range(1, 6):
    run = str(config)+"_"+str(model)+"_"+str(speed)+"_"+str(i)
    filename_bin = "Force measurements/" + run + ".bin"
    filename_TST = "Force measurements/" + run + ".TST"
    time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
    t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)
    Fx_mean.append(np.mean(Fx)-Fx_zero)
    Fx_max.append(np.max(Fx)-Fx_zero)

print(str(config)+"_"+str(model)+"_"+str(speed))
print("Mean Fx:")
for i in range(5):
    print(Fx_mean[i])
print("Max Fx:")
for i in range(5):
    print(Fx_max[i]) """


###############################################################################
# PLOT MEAN FX AND FZ FOR DIFFERENT FLOW VELOCITIES
###############################################################################

config_list = ["S", "C"] 
model_list = ["A", "M", "J", "W"]
#model_list = ["W"]
lengths = np.array([29.04, 42.60, 50.32, 50.32]) * 10**(-2) # m
widths = np.array([4.6, 6.3, 7.28, 7.28]) * 10**(-2) # m
ds = np.array([0.00084867, 0.00095333, 0.00090267, 0.00090267])
d_wavy = 0.00144867 # m (thickness for wavy model)
E = 1.26 * 10**6 # Pa
t_c = 1.86 # cluster thickness parameter

U_list = [0.03, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]


#Empty lists for single and cluster condiguration
FxS_list = []
FzS_list = []
FxC_list = []
FzC_list = []
Cd_bulkS_list = []
Cd_bulkC_list = []
CaS_list = []
CaC_list = []


for config in config_list:
    for m in range(len(model_list)):
        Fx_model = []
        Fz_model = []
        Cd_model = []
        Ca_model = []
        for i in range(10):
            Fx_zero = Fx_zero_list[i]
            Fz_zero = Fz_zero_list[i]

            run = str(config)+"_"+str(model_list[m])+"_"+str(velocities[i])+"_"+"1"
            run2 = str(config)+"_"+str(model_list[m])+"_"+str(velocities[i])+"_"+"2"
            filename_bin = "./Force_measurements/" + run + ".bin"
            filename_TST = "./Force_measurements/" + run + ".TST"

            #Calculate mean of all 5 runs for repeated runs, otherwise just use the single run
            if os.path.isfile("./Force_measurements/" + run2 + ".bin"):
                Fx_runs = []
                Fz_runs = []
                for j in range(1, 6):
                    run = str(config)+"_"+str(model_list[m])+"_"+str(velocities[i])+"_"+str(j)
                    filename_bin = "./Force_measurements/" + run + ".bin"
                    filename_TST = "./Force_measurements/" + run + ".TST"
                    time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
                    t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)
                    Fx_runs.append(np.mean(Fx))
                    Fz_runs.append(np.mean(Fz))
                Fx = Fx_runs
                Fz = Fz_runs    
            else:     
                time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
                t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)
            
            Fx_model.append(np.mean(Fx)-Fx_zero)
            Fz_model.append(np.mean(Fz)-Fz_zero)
            
            #Calculate Cd_bulk and Cauchy number for each run
            if config=="S":
                Cd_model.append(Cd_bulk(lengths[m], widths[m], U_list[i], np.mean(Fx)-Fx_zero))
                Ca_model.append(cauchy_number(lengths[m], widths[m], ds[m], U_list[i], E))
            else: 
                # d = d*1.86 for cluster configuration and w = 3*w
                Cd_model.append(Cd_bulk(lengths[m], 3*widths[m], U_list[i], np.mean(Fx)-Fx_zero))
                Ca_model.append(cauchy_number(lengths[m], 3*widths[m], ds[m]*1.86, U_list[i], E))
            
        if config=="S":
            FxS_list.append(Fx_model)
            FzS_list.append(Fz_model)
            Cd_bulkS_list.append(Cd_model)
            CaS_list.append(Ca_model)

        else: 
            FxC_list.append(Fx_model)
            FzC_list.append(Fz_model)
            Cd_bulkC_list.append(Cd_model)
            CaC_list.append(Ca_model)   

Cas_S_A = CaS_list[0]
Cas_S_M = CaS_list[1]
Cas_S_J = CaS_list[2]
Cas_S_W = CaS_list[3]
Cas_C_A = CaC_list[0]
Cas_C_M = CaC_list[1]
Cas_C_J = CaC_list[2]
Cas_C_W = CaC_list[3]
Cas_S_A_origo = np.append(Cas_S_A, 0)
Cas_S_A_origo = np.sort(Cas_S_A_origo)
Cas_S_M_origo = np.append(Cas_S_M, 0)
Cas_S_M_origo = np.sort(Cas_S_M_origo)
Cas_S_J_origo = np.append(Cas_S_J, 0)
Cas_S_J_origo = np.sort(Cas_S_J_origo)
Cas_S_W_origo = np.append(Cas_S_W, 0)
Cas_S_W_origo = np.sort(Cas_S_W_origo)
Cas_C_A_origo = np.append(Cas_C_A, 0)
Cas_C_A_origo = np.sort(Cas_C_A_origo)
Cas_C_M_origo = np.append(Cas_C_M, 0)
Cas_C_M_origo = np.sort(Cas_C_M_origo)
Cas_C_J_origo = np.append(Cas_C_J, 0)
Cas_C_J_origo = np.sort(Cas_C_J_origo)
Cas_C_W_origo = np.append(Cas_C_W, 0)
Cas_C_W_origo = np.sort(Cas_C_W_origo)

###############################################################################
# FINNE VOGEL EXPONENT
###############################################################################

def power_func(x, a, b):
    return a * x**b

exponent_S_list = []
exponent_C_list = []
curve_fit_S_list = []
curve_fit_C_list = []
for i in range(len(model_list)):
    params, covariance = curve_fit(power_func, U_list, FxS_list[i])
    a, b = params
    exponent_S_list.append(b)
    curve_fit_S_list.append(power_func(U_list, a, b))

for i in range(len(model_list)):
    params, covariance = curve_fit(power_func, U_list, FxC_list[i])
    a, b = params
    exponent_C_list.append(b)
    curve_fit_C_list.append(power_func(U_list, a, b))
###############################################################################
# NUMERICAL LOADS
###############################################################################

config = "S" # S/C
#model = "A" # A/M/J/W
model_list = ["M"]
#speed = "7" # 3=0.3m/s
velocities = ["03", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
CMs = ["0035", "0456", "0489","005","01", "0102","014","015", "02", "0253","0293", "03", "04", "06", "08", "10"]
CM_choice = 9
CM_list = ["0293", "0244"]

FxS_num = []
for CM in CM_list:
    for model in model_list:
        Fx_mean_model_list = []
        #Looping through all vlelocities for the given config and model 
        for i in range(len(velocities)):

            run = str(config)+"_"+str(model)+"_"+str(velocities[i])+"_"+CM
            filename = "correct_results_num/" + str(config)+"_"+str(model)+ "/" + run + ".h5"
            time, loadx, loadz, loadx_mean = get_numerical_loads(filename)
            Fx_mean_model_list.append(loadx_mean)
        FxS_num.append(Fx_mean_model_list)  
"""

FxC_num = []
for CM in CM_list:
    for model in model_list:
        Fx_mean_model_list = []
        #Looping through all vlelocities for the given config and model 
        for i in range(len(velocities)):

            run = str(config)+"_"+str(model)+"_"+str(velocities[i])+"_"+CM
            filename = "correct_results_num/" + str(config)+"_"+str(model)+ "/" + run + ".h5"
            time, loadx, loadz, loadx_mean = get_numerical_loads(filename)
            Fx_mean_model_list.append(loadx_mean)
        FxC_num.append(Fx_mean_model_list)    
"""
#####################################################ß##########################
# PLOTS
###############################################################################

#Add origo to Fx list
for i in range(len(FxS_list)):
    FxS_list[i].insert(0, 0)
    FxC_list[i].insert(0, 0)


U_list_origo = np.append(U_list, 0)
U_list_origo = np.sort(U_list_origo) 


os.makedirs("Plots", exist_ok=True) 

""" #Fx mean plots for single configuration
plt.figure(figsize=(9, 6)) 
plt.plot(U_list_origo, FxS_list[0], '.-', label="April")
plt.plot(U_list_origo, FxS_list[1], '.-', label="May")
plt.plot(U_list_origo, FxS_list[2], '.-', label="June")
plt.plot(U_list_origo, FxS_list[3], '.-', label="Wavy")

plt.plot(U_list, curve_fit_list[0], '--', color='blue', label="Curve fit April")
plt.plot(U_list, curve_fit_list[1], '--', color='orange', label="Curve fit May")
plt.plot(U_list, curve_fit_list[2], '--', color='green', label="Curve fit June")
plt.plot(U_list, curve_fit_list[3], '--', color='red', label="Curve fit Wavy")

plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Single")
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Drag force [N]")
filepath = os.path.join("Plots", "Fx_Mean_Single.png")
plt.savefig(filepath, dpi=300)
#plt.show()  """
"""
#subplots for single configuration
plt.figure(figsize=(10, 7)) 
plt.plot(Cas_S_A_origo, FxS_list[0], 'D', color='blue', label="Model: April, Experimental")
plt.plot(Cas_S_A, FxS_num[0], ls="dashed", marker=".", color='orange', label="Model: April, Numerical with CM: 0.228")
plt.plot(Cas_S_A, FxS_num[1], ls="dashed", marker=".", color='green', label="Model: April, Numerical with CM: 0.274")
plt.plot(Cas_S_A, curve_fit_S_list[0], '--', color='blue', label="Curve fit experimental data April")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Single blade - April, with C_M: " + CM_list[0])
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Drag force [N]")
savename = "Fx_Mean_Single_April_CM_" + CM_list[0] + "_" + CM_list[1] + ".png"
filepath = os.path.join("Plots", savename)
plt.savefig(filepath, dpi=300)
plt.close()
"""

plt.figure(figsize=(10, 7)) 
plt.plot(Cas_S_M_origo, FxS_list[1], 'D', color='orange', label="Model: May, Experimental")
plt.plot(Cas_S_M, FxS_num[0], ls="dashed", marker=".", color='blue', label="Model: May, Numerical with CM: 0.293")
plt.plot(Cas_S_M, FxS_num[1], ls="dashed", marker=".", color='green', label="Model: May, Numerical with CM: 0.244")
plt.plot(Cas_S_M, curve_fit_S_list[1], '--', color='orange', label="Curve fit experimental data May")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Single blade - May with C_M: " + CM_list[0])
plt.xlabel("Cauchy number [-]")
plt.ylabel("Drag force [N]")
savename = "Fx_Mean_Single_May_CM_" + CM_list[0] + "_" + CM_list[1] + ".png"
filepath = os.path.join("Plots", savename)
plt.savefig(filepath, dpi=300)
plt.close()

"""
plt.figure(figsize=(10, 7)) 
plt.plot(Cas_S_J_origo, FxS_list[2], 'D', color='blue', label="Model: June Experimental")
plt.plot(Cas_S_J, FxS_num[0], ls='dashed', marker=".", color='orange', label="Model: June Numerical")
plt.plot(Cas_S_J, curve_fit_S_list[2], '--', color='blue', label="Curve fit experimental data June")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Single blade - June with C_M: " + CM_list[0])
plt.xlabel("Cauchy number [-]")
plt.ylabel("Drag force [N]")
savename = "Fx_Mean_Single_June_CM_" + CM_list[0] + ".png"
filepath = os.path.join("Plots", savename)
plt.savefig(filepath, dpi=300)
plt.close()
"""
"""
#subplots for single configuration
plt.figure(figsize=(10, 7)) 
plt.plot(U_list_origo, FxS_list[2], 'D', color='blue', label="June Experimental")
plt.plot(U_list, FxS_num[0], ls="dashed", marker=".", color='orange', label="June Numerical")
#plt.plot(U_list, curve_fit_list[2], '--', color='blue', label="Curve fit June")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Single blade - June, with C_M: " + CMs[CM_choice])
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Drag force [N]")
savename = "Fx_Mean_Single_June_CM_" + CMs[CM_choice] + ".png"
filepath = os.path.join("Plots", savename)
plt.savefig(filepath, dpi=300)
plt.close()"""
"""
#subplots for single configuration
""""""
#Plot for finding the best CM for Single_june
plt.figure(figsize=(10, 7)) 
plt.plot(Cas_S_J_origo, FxS_list[2], 'D', color='orange', label="June Experimental")
plt.plot(Cas_S_J, FxS_num[0], ls="dashed", marker=".", color='red', label="June Numerical with CM: 0.2")
plt.plot(Cas_S_J, FxS_num[1], ls="dashed", marker=".", color='green', label="June Numerical with CM: 0.25")
plt.plot(Cas_S_J, FxS_num[2], ls="dashed", marker=".", color='blue', label="June Numerical with CM: 0.3")
plt.plot(Cas_S_J, curve_fit_S_list[2], '--', color='orange', label="Curve fit experimental data June")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.xlabel("Cauchy number [-]")
plt.ylabel("Drag force [N]")
savename = "Fx_Mean_Single_June_CMs_" + CM_list[0] + "_" + CM_list[1] + "_" + CM_list[2] + ".png"
filepath = os.path.join("Plots", savename)
plt.savefig(filepath, dpi=300)
plt.close()

"""
""" plt.figure(figsize=(10, 7)) 
plt.plot(U_list_origo, FxS_list[3], 'D', color='red', label="Wavy Experimental")
plt.plot(U_list, FxS_num[0], ls="dashed", marker=".", color='red', label="Wavy Numerical")
#plt.plot(U_list, curve_fit_list[3], '--', color='red', label="Curve fit Wavy")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Single blade - Wavy with C_M: " + CMs[CM_choice])
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Drag force [N]")
savename = "Fx_Mean_Single_Wavy_CM_" + CMs[CM_choice] + ".png"
filepath = os.path.join("Plots", savename)
plt.savefig(filepath, dpi=300)
plt.close()  """
"""
 #subplots for cluster configuration
plt.figure(figsize=(10, 7)) 
plt.plot(Cas_C_A_origo, FxC_list[0], 'D', color='blue', label="Model: April, Experimental")
plt.plot(Cas_C_A, FxC_num[0], ls='dashed', marker=".", color='orange', label="Model: April, Numerical")
plt.plot(Cas_C_A, curve_fit_C_list[0], '--', color='blue', label="Curve fit experimental data April")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Cluster - April, with C_M: " + CMs[CM_choice])
plt.xlabel("Cauchy number [-]")
plt.ylabel("Drag force [N]")
savename = "Fx_Mean_Cluster_April_CM_" + CMs[CM_choice] + ".png"
filepath = os.path.join("Plots", savename)
plt.savefig(filepath, dpi=600)
plt.close() 
"""
"""
plt.figure(figsize=(10, 7)) 
plt.plot(Cas_C_M_origo, FxC_list[1], 'D', color='orange', label="Model: May, Experimental")
plt.plot(Cas_C_M, FxC_num[0], ls='dashed', marker=".", color='blue', label="Model: May, Numerical")
plt.plot(Cas_C_M, curve_fit_C_list[1], '--', color='orange', label="Curve fit May")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Cluster - May, with C_M: " + CMs[CM_choice])
plt.xlabel("Cauchy number [-]")
plt.ylabel("Drag force [N]")
savename = "Fx_Mean_Cluster_May_CM_" + CMs[CM_choice] + ".png"
filepath = os.path.join("Plots", savename)
plt.savefig(filepath, dpi=300)
plt.close
"""
"""
plt.figure(figsize=(10, 7)) 
plt.plot(Cas_C_J_origo, FxC_list[2], 'D', color='green', label="Model: June, Experimental")
plt.plot(Cas_C_J, FxC_num[0], ls='dashed', marker=".", color='red', label="Model: June, Numerical, CM: " + CM_list[0])
plt.plot(Cas_C_J, FxC_num[1], ls='dashed', marker=".", color='blue', label="Model: June, Numerical, CM: " + CM_list[1])
plt.plot(Cas_C_J, curve_fit_C_list[2], '--', color='green', label="Curve fit June")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Cluster - June, with C_Ms: " + CM_list[0] + ", " + CM_list[1])
plt.xlabel("Cauchy number [-]")
plt.ylabel("Drag force [N]")
savename = "Fx_Mean_Cluster_June_CM_" + CMs[CM_choice] + ".png"
filepath = os.path.join("Plots", savename)
plt.savefig(filepath, dpi=300)
plt.close() 
""""""
plt.figure(figsize=(10, 7)) 
plt.plot(Cas_C_J_origo, FxC_list[2], 'D', color='orange', label="June Experimental")
plt.plot(Cas_C_J, FxC_num[0], ls="dashed", marker=".", color='red', label="June Numerical with CM: " + CM_list[0])
plt.plot(Cas_C_J, FxC_num[1], ls="dashed", marker=".", color='green', label="June Numerical with CM: " + CM_list[1])
plt.plot(Cas_C_J, FxC_num[2], ls="dashed", marker=".", color='blue', label="June Numerical with CM: " + CM_list[2])
plt.plot(Cas_C_J, curve_fit_C_list[2], ls='dashed', color='orange', label="Curve fit experimental data June")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Cluster - June, with varying C_Ms")
plt.xlabel("Cauchy number [-]")
plt.ylabel("Drag force [N]")
savename = "Fx_Mean_Cluster_June_CMs_" + CM_list[0] + "_" + CM_list[1] + "_" + CM_list[2] + ".png"
filepath = os.path.join("Plots", savename)
plt.savefig(filepath, dpi=300)
plt.close()"""
"""
plt.figure(figsize=(10, 7)) 
plt.plot(Cas_C_W_origo, FxC_list[3], 'D', color='orange', label="Wavy Experimental")
plt.plot(Cas_C_W, FxC_num[0], ls="dashed", marker=".", color='red', label="Wavy Numerical with CM: " + CM_list[0])
plt.plot(Cas_C_W, curve_fit_C_list[3], ls='dashed', color='orange', label="Curve fit experimental data Wavy")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Cluster - Wavy, with C_M: " + CM_list[0])
plt.xlabel("Cauchy number [-]")
plt.ylabel("Drag force [N]")
savename = "Fx_Mean_Cluster_Wavy_CMs_" + CM_list[0] + ".png"
filepath = os.path.join("Plots", savename)
plt.savefig(filepath, dpi=300)
plt.close()"""
""""""
#Fz plots for single configuration
""" plt.figure(figsize=(10, 7)) 
plt.plot(U_list, FzS_list[0], '.-', label="April")
plt.plot(U_list, FzS_list[1], '.-', label="May")
plt.plot(U_list, FzS_list[2], '.-', label="June")
plt.plot(U_list, FzS_list[3], '.-', label="Wavy")
plt.legend()
plt.grid()
plt.title("Fz Single")
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Mean Force [N]")
filepath = os.path.join("Plots", "Fz_Mean_Single.png")
plt.savefig(filepath, dpi=300)"""
#plt.show() """

#Fx plots for cluster configuration
""" plt.figure(figsize=(9, 6)) 
plt.plot(U_list_origo, FxC_list[0], '.', color='blue', label="April")
plt.plot(U_list_origo, FxC_list[1], '.', color='orange', label="May")
plt.plot(U_list_origo, FxC_list[2], '.', color='green', label="June")
plt.plot(U_list_origo, FxC_list[3], '.', color='red', label="Wavy")

 plt.plot(U_list, curve_fit_list[0], '--', color='blue', label="Curve fit April")
plt.plot(U_list, curve_fit_list[1], '--', color='orange', label="Curve fit May")
plt.plot(U_list, curve_fit_list[2], '--', color='green', label="Curve fit June")
plt.plot(U_list, curve_fit_list[3], '--', color='red', label="Curve fit Wavy")

plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Cluster")
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Drag force [N]")
filepath = os.path.join("Plots", "Fx_Mean_Cluster.png")
plt.savefig(filepath, dpi=300)
#plt.show() """

#Fz plots for cluster configuration
""" plt.figure(figsize=(9, 6)) 
plt.plot(U_list, FzC_list[0], '.-', label="April")
plt.plot(U_list, FzC_list[1], '.-', label="May")
plt.plot(U_list, FzC_list[2], '.-', label="June")
plt.plot(U_list, FzC_list[3], '.-', label="Wavy")
plt.legend()
plt.grid()
plt.title("Fz Cluster")
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Mean Force [N]")
filepath = os.path.join("Plots", "Fz_Mean_Cluster.png")
plt.savefig(filepath, dpi=300)
#plt.show() """
"""
os.makedirs("Cd_bulk Plots", exist_ok=True) 
#Cd_bulk plots 
plt.figure(figsize=(9, 6)) 
plt.plot(CaS_list[0][2:], Cd_bulkS_list[0][2:], '.--', label="April")
plt.plot(CaS_list[1][2:], Cd_bulkS_list[1][2:], '.--', label="May")
plt.plot(CaS_list[2][2:], Cd_bulkS_list[2][2:], '.--', label="June")
plt.plot(CaS_list[3][2:], Cd_bulkS_list[3][2:], '.--', label="Wavy")
plt.legend()
plt.grid()
plt.title("Single")
plt.xlabel(r"$Ca$", fontsize=16)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.ylabel(r"$C_{D,bulk}$", fontsize=16)
filepath = os.path.join("Cd_bulk Plots", "CD_bulk_Single_2.png")
plt.savefig(filepath, dpi=300)

plt.figure(figsize=(9, 6)) 
plt.plot(CaC_list[0], Cd_bulkC_list[0], '.--', label="April")
plt.plot(CaC_list[1][2:], Cd_bulkC_list[1][2:], '.--', label="May")
plt.plot(CaC_list[2][2:], Cd_bulkC_list[2][2:], '.--', label="June")
plt.plot(CaC_list[3][2:], Cd_bulkC_list[3][2:], '.--', label="Wavy")
plt.legend()
plt.grid()
plt.ylim(0.03, 15)
plt.yticks(np.arange(0.03, 15, 2))
plt.xticks(np.arange(0.01e5, 2.5e5, 0.1e5))
plt.title(r"$C_{D,bulk}$ Cluster")
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.xlabel("Ca")
plt.ylabel(r"$C_{D,bulk}$")
filepath = os.path.join("Cd_bulk Plots", "CD_bulk_Cluster_2.png")
plt.savefig(filepath, dpi=300)"""
#plt.show()  