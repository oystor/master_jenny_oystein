import catmanreader as cr
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
import scipy.signal as signal
#from plot_loads import get_numerical_loads

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
    filename_bin = "master_jenny_oystein/Force_measurements/Z_" + vel + "_1.bin"
    filename_TST = "master_jenny_oystein/Force_measurements/Z_" + vel + "_1.TST"
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

#Dimensions of the models
lengths = [0.3014, 0.437, 0.5142, 0.5208] # m
widths = [0.046, 0.063, 0.0728, 0.073] # m
d = [0.000849, 0.000953, 0.000903, 0.001449] # m (thickness)
rho = [850, 754, 852, 1159] # kg/m^3 (density)    
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
timeS_list = []
timeC_list = []


for config in config_list:
    for m in range(len(model_list)):
        Fx_model = []
        Fz_model = []
        Cd_model = []
        Ca_model = []
        time_model = []
        for i in range(10):
            Fx_zero = Fx_zero_list[i]
            Fz_zero = Fz_zero_list[i]

            run = str(config)+"_"+str(model_list[m])+"_"+str(velocities[i])+"_"+"1"
            run2 = str(config)+"_"+str(model_list[m])+"_"+str(velocities[i])+"_"+"2"
            filename_bin = "master_jenny_oystein/Force_measurements/" + run + ".bin"
            filename_TST = "master_jenny_oystein/Force_measurements/" + run + ".TST"

            #Calculate mean of all 5 runs for repeated runs, otherwise just use the single run
            if os.path.isfile("master_jenny_oystein/Force measurements/" + run2 + ".bin"):
                Fx_runs = []
                Fz_runs = []
                for j in range(1, 6):
                    run = str(config)+"_"+str(model_list[m])+"_"+str(velocities[i])+"_"+str(j)
                    filename_bin = "master_jenny_oystein/Force_measurements/" + run + ".bin"
                    filename_TST = "master_jenny_oystein/Force_measurements/" + run + ".TST"
                    time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
                    t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)
                    Fx_runs.append(np.mean(Fx))
                    Fz_runs.append(np.mean(Fz))
                Fx = Fx_runs
                Fz = Fz_runs
                time_model.append(t)    
            else:     
                time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
                t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)
                time_model.append(t)
            
            Fx_model.append(np.mean(Fx)-Fx_zero)
            Fz_model.append(np.mean(Fz)-Fz_zero)
            
            #Calculate Cd_bulk and Cauchy number for each run
            if config=="S":
                Cd_model.append(Cd_bulk(lengths[m], widths[m], U_list[i], np.mean(Fx)-Fx_zero))
                Ca_model.append(cauchy_number(lengths[m], widths[m], d[m], U_list[i], E))
            else: 
                # d = d*1.86 for cluster configuration and w = 3*w
                Cd_model.append(Cd_bulk(lengths[m], 3*widths[m], U_list[i], np.mean(Fx)-Fx_zero))
                Ca_model.append(cauchy_number(lengths[m], 3*widths[m], d[m]*t_c, U_list[i], E))
            
        if config=="S":
            FxS_list.append(Fx_model)
            FzS_list.append(Fz_model)
            Cd_bulkS_list.append(Cd_model)
            CaS_list.append(Ca_model)
            timeS_list.append(time_model)

        else: 
            FxC_list.append(Fx_model)
            FzC_list.append(Fz_model)
            Cd_bulkC_list.append(Cd_model)
            CaC_list.append(Ca_model)   
            timeC_list.append(time_model)




###############################################################################
# FINNE VOGEL EXPONENT
###############################################################################

""" def power_func(x, a, b):
    return a * x**b

exponent_list = []
curve_fit_list = []

for i in range(len(model_list)):
    params, covariance = curve_fit(power_func, U_list, FxC_list[i])
    a, b = params
    exponent_list.append(b)
    curve_fit_list.append(power_func(U_list, a, b))
    print(float(a))
print("Exponents:", exponent_list) """


###############################################################################
# NUMERICAL LOADS
###############################################################################

""" config = "C" # S/C
#model = "A" # A/M/J/W
model_list = ["M"]
#speed = "7" # 3=0.3m/s
velocities = ["03", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
CMs = ["01", "0102", "02", "03", "04", "06", "08", "10"]
CM_choice = 1 """


"""FxS_num = []
for model in model_list:
    Fx_mean_model_list = []
    #Looping through all vlelocities for the given config and model 
    for i in range(len(velocities)):
        if config == "S" and model == "J" and CMs[CM_choice] == "03":
            run = str(config)+"_"+str(model)+"_"+str(velocities[i])+"_"+CMs[CM_choice]
        elif config == "S" and model == "W" and CMs[CM_choice] == "03":
            run = str(config)+"_"+str(model)+"_"+str(velocities[i])+"_"+CMs[CM_choice]
        else:            
            if float(velocities[i]) < 4:
                run = str(config)+"_"+str(model)+"_"+str(velocities[i])+"_"+"10"
            else:
                run = str(config)+"_"+str(model)+"_"+str(velocities[i])+"_"+CMs[CM_choice]
        filename = "correct_results_num/" + str(config)+"_"+str(model)+ "/" + run + ".h5"
        time, loadx, loadz, loadx_mean = get_numerical_loads(filename)
        Fx_mean_model_list.append(loadx_mean)
    FxS_num.append(Fx_mean_model_list)  """
 
""" 
FxC_num = []
for model in model_list:
    Fx_mean_model_list = []
    #Looping through all vlelocities for the given config and model 
    for i in range(len(velocities)):
        if config == "C" and model == "A" and CMs[CM_choice] == "01":
            run = str(config)+"_"+str(model)+"_"+str(velocities[i])+"_"+CMs[CM_choice]
        elif config == "C" and model == "M" and CMs[CM_choice] == "0102":
            run = str(config)+"_"+str(model)+"_"+str(velocities[i])+"_"+CMs[CM_choice]
        else:
            if float(velocities[i]) < 4:
                run = str(config)+"_"+str(model)+"_"+str(velocities[i])+"_"+"10"
            else:
                run = str(config)+"_"+str(model)+"_"+str(velocities[i])+"_"+CMs[CM_choice]
        filename = "correct_results_num/" + str(config)+"_"+str(model)+ "/" + run + ".h5"
        time, loadx, loadz, loadx_mean = get_numerical_loads(filename)
        Fx_mean_model_list.append(loadx_mean)
    FxC_num.append(Fx_mean_model_list)  """  

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
plt.plot(U_list_origo, FxS_list[0], 'D', color='blue', label="April")
plt.plot(U_list, FxS_num[0], ls="dashed", marker=".", color='blue', label="April Numerical")
#plt.plot(U_list, curve_fit_list[0], '--', color='blue', label="Curve fit April")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Single blade - April, with C_M: " + CMs[CM_choice])
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Drag force [N]")
savename = "Fx_Mean_Single_April_CM_" + CMs[CM_choice] + ".png"
filepath = os.path.join("Plots", savename)
plt.savefig(filepath, dpi=300)
plt.close()"""

"""
plt.figure(figsize=(10, 7)) 
plt.plot(U_list_origo, FxS_list[1], '.', color='orange', label="May")
plt.plot(U_list, FxS_num[1], '-', color='orange', label="May Numerical")
#plt.plot(U_list, curve_fit_list[1], '--', color='orange', label="Curve fit May")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("May")
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Drag force [N]")
filepath = os.path.join("Plots", "Fx_Mean_May.png")
plt.savefig(filepath, dpi=300)
plt.close()


plt.figure(figsize=(10, 7)) 
plt.plot(U_list_origo, FxS_list[2], '.', color='green', label="June")
plt.plot(U_list, FxS_num[2], '-', color='green', label="June Numerical")
#plt.plot(U_list, curve_fit_list[2], '--', color='green', label="Curve fit June")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("June")
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Drag force [N]")
filepath = os.path.join("Plots", "Fx_Mean_June.png")
plt.savefig(filepath, dpi=300)
plt.close()
"""
"""
#subplots for single configuration
plt.figure(figsize=(10, 7)) 
plt.plot(U_list_origo, FxS_list[2], 'D', color='blue', label="June Experimental")
plt.plot(U_list, FxS_num[0], ls="dashed", marker=".", color='blue', label="June Numerical")
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

""" #subplots for cluster configuration
plt.figure(figsize=(10, 7)) 
plt.plot(U_list_origo, FxC_list[0], 'D', color='blue', label="April")
plt.plot(U_list, FxC_num[0], ls='dashed', marker=".", color='blue', label="April Numerical")
#plt.plot(U_list, curve_fit_list[0], '--', color='blue', label="Curve fit April")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Cluster - April, with C_M: " + CMs[CM_choice])
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Drag force [N]")
savename = "Fx_Mean_Cluster_April_CM_" + CMs[CM_choice] + ".png"
filepath = os.path.join("Plots", savename)
plt.savefig(filepath, dpi=600)
plt.close() """

""" 
plt.figure(figsize=(10, 7)) 
plt.plot(U_list_origo, FxC_list[1], marker='D', color='orange', label="May")
plt.plot(U_list, FxC_num[0], ls='dashed', marker=".", color='orange', label="May Numerical")
#plt.plot(U_list, curve_fit_list[1], '--', color='orange', label="Curve fit May")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Cluster - May, with C_M: " + CMs[CM_choice])
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Drag force [N]")
savename = "Fx_Mean_Cluster_May_CM_" + CMs[CM_choice] + ".png"
filepath = os.path.join("Plots", savename)
plt.savefig(filepath, dpi=300)
plt.close() """
"""

plt.figure(figsize=(10, 7)) 
plt.plot(U_list_origo, FxC_list[2], '.', color='green', label="June")
plt.plot(U_list, FxC_num[2], '-', color='green', label="June Numerical")
#plt.plot(U_list, curve_fit_list[2], '--', color='green', label="Curve fit June")
plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("June Cluster")
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Drag force [N]")
filepath = os.path.join("Plots", "Fx_Mean_June_Cluster.png")
plt.savefig(filepath, dpi=300)
plt.close() """


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
plt.savefig(filepath, dpi=300)
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
plt.plot(CaC_list[0][1:], Cd_bulkC_list[0][1:], '.--', label="April")
plt.plot(CaC_list[1][2:], Cd_bulkC_list[1][2:], '.--', label="May")
plt.plot(CaC_list[2][2:], Cd_bulkC_list[2][2:], '.--', label="June")
plt.plot(CaC_list[3][1:], Cd_bulkC_list[3][1:], '.--', label="Wavy")
plt.legend()
plt.grid()
#plt.ylim(0.03, 0.12)
#plt.yticks(np.arange(0.03, 15, 2))
#plt.xticks(np.arange(0.01e5, 2.5e5, 0.1e5))
plt.title(r"$C_{D,bulk}$ Cluster")
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.xlabel("Ca")
plt.ylabel(r"$C_{D,bulk}$")
filepath = os.path.join("Cd_bulk Plots", "CD_bulk_Cluster_2.png")
plt.savefig(filepath, dpi=300)
#plt.show()   """ """


