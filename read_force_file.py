import catmanreader as cr
import numpy as np
import matplotlib.pyplot as plt
import os

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
    filename_bin = "Force measurements/Z_" + vel + "_1.bin"
    filename_TST = "Force measurements/Z_" + vel + "_1.TST"
    time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
    t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)

    Fx_zero_list.append(np.mean(Fx))
    Fz_zero_list.append(np.mean(Fz))

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
    Cd = 2
    I = (width*thickness**3)/12
    Ca = 0.5* (rho*Cd*width*velocity**2*length**3)/(E*I)
    return float(Ca)


###############################################################################
# REPEATABILITY TEST
###############################################################################

config = "C" # S/C
model = "W" # A/M/J/W
speed = "7" # 3=0.3m/s

Fx_mean = []
Fx_max = []

#Finding fx_zero works for all speeds except 0.03m/s
Fx_zero = Fx_zero_list[int(speed)]
#print(Fx_zero_list)
#print(Fx_zero)

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
    print(Fx_max[i])

    

""" ###############################################################################
# PLOT MEAN FX AND FZ FOR DIFFERENT FLOW VELOCITIES
###############################################################################

config_list = ["S", "C"] 
model_list = ["A", "M", "J", "W"]
lengths = np.array([31.55, 45.63, 53.93, 53.93]) * 10**(-2) # m
widths = np.array([4.72, 6.54, 7.57, 7.57]) * 10**(-2) # m
d = 0.8 * 10**(-3) # m (thickness)
E = 1.26 * 10**6 # Pa
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
            filename_bin = "Force measurements/" + run + ".bin"
            filename_TST = "Force measurements/" + run + ".TST"

            time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
            t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)

            Fx_model.append(np.mean(Fx)-Fx_zero)
            Fz_model.append(np.mean(Fz)-Fz_zero)
            
            Cd_model.append(Cd_bulk(lengths[m], widths[m], U_list[i], np.mean(Fx)-Fx_zero))
            Ca_model.append(cauchy_number(lengths[m], widths[m], d, U_list[i], E))
            
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

#Plots

os.makedirs("Plots", exist_ok=True) 

plt.figure(figsize=(9, 6)) 
plt.plot(U_list, FxS_list[0], '.-', label="April")
plt.plot(U_list, FxS_list[1], '.-', label="May")
plt.plot(U_list, FxS_list[2], '.-', label="June")
plt.plot(U_list, FxS_list[3], '.-', label="Wavy")
plt.legend()
plt.title("Fx Single")
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Mean Force [N]")
filepath = os.path.join("Plots", "Fx_Mean_Single.png")
plt.savefig(filepath, dpi=300)
#plt.show()

plt.figure(figsize=(9, 6)) 
plt.plot(U_list, FzS_list[0], '.-', label="April")
plt.plot(U_list, FzS_list[1], '.-', label="May")
plt.plot(U_list, FzS_list[2], '.-', label="June")
plt.plot(U_list, FzS_list[3], '.-', label="Wavy")
plt.legend()
plt.title("Fz Single")
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Mean Force [N]")
filepath = os.path.join("Plots", "Fz_Mean_Single.png")
plt.savefig(filepath, dpi=300)
#plt.show()

plt.figure(figsize=(9, 6)) 
plt.plot(U_list, FxC_list[0], '.-', label="April")
plt.plot(U_list, FxC_list[1], '.-', label="May")
plt.plot(U_list, FxC_list[2], '.-', label="June")
plt.plot(U_list, FxC_list[3], '.-', label="Wavy")
plt.legend()
plt.title("Fx Cluster")
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Mean Force [N]")
filepath = os.path.join("Plots", "Fx_Mean_Cluster.png")
plt.savefig(filepath, dpi=300)
#plt.show()

plt.figure(figsize=(9, 6)) 
plt.plot(U_list, FzC_list[0], '.-', label="April")
plt.plot(U_list, FzC_list[1], '.-', label="May")
plt.plot(U_list, FzC_list[2], '.-', label="June")
plt.plot(U_list, FzC_list[3], '.-', label="Wavy")
plt.legend()
plt.title("Fz Cluster")
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Mean Force [N]")
filepath = os.path.join("Plots", "Fz_Mean_Cluster.png")
plt.savefig(filepath, dpi=300)
#plt.show()

plt.figure(figsize=(9, 6)) 
plt.plot(CaS_list[0][1:], Cd_bulkS_list[0][1:], '.-', label="April")
plt.plot(CaS_list[1][1:], Cd_bulkS_list[1][1:], '.-', label="May")
plt.plot(CaS_list[2][1:], Cd_bulkS_list[2][1:], '.-', label="June")
plt.plot(CaS_list[3][1:], Cd_bulkS_list[3][1:], '.-', label="Wavy")
plt.legend()
plt.title("Single")
plt.xlabel("Ca")
plt.ylabel("Cd")
filepath = os.path.join("Plots", "CD_bulk_Single.png")
plt.savefig(filepath, dpi=300)
#plt.show()

plt.figure(figsize=(9, 6)) 
plt.plot(CaC_list[0][1:], Cd_bulkC_list[0][1:], '.-', label="April")
plt.plot(CaC_list[1][1:], Cd_bulkC_list[1][1:], '.-', label="May")
plt.plot(CaC_list[2][1:], Cd_bulkC_list[2][1:], '.-', label="June")
plt.plot(CaC_list[3][1:], Cd_bulkC_list[3][1:], '.-', label="Wavy")
plt.legend()
plt.title("Cluster")
plt.xlabel("Ca")
plt.ylabel("Cd")
filepath = os.path.join("Plots", "CD_bulk_Cluster.png")
plt.savefig(filepath, dpi=300)
#plt.show() """