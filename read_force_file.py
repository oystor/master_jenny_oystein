import catmanreader as cr
import numpy as np
import matplotlib.pyplot as plt

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
    filename_bin = "C:/Users/jenny/OneDrive - NTNU/Master/Force measurements/Z_" + vel + "_1.bin"
    filename_TST = "C:/Users/jenny/OneDrive - NTNU/Master/Force measurements/Z_" + vel + "_1.TST"
    time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
    t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)

    Fx_zero_list.append(np.mean(Fx))
    Fz_zero_list.append(np.mean(Fz))

#plt.plot(velocities,Fx_zero)
#plt.show()


###############################################################################
# PLOT FX AND FZ FOR DIFFERENT FLOW VELOCITIES
###############################################################################

config = "S" # S/C
model = "J" # A/M/J/W

Fx_list = []
Fz_list = []

for i in range(10):
    Fx_zero = Fx_zero_list[i]
    Fz_zero = Fz_zero_list[i]

    run = str(config)+"_"+str(model)+"_"+str(velocities[i])+"_"+"1"
    filename_bin = "C:/Users/jenny/OneDrive - NTNU/Master/Force measurements/" + run + ".bin"
    filename_TST = "C:/Users/jenny/OneDrive - NTNU/Master/Force measurements/" + run + ".TST"

    time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
    t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)

    Fx_list.append(np.mean(Fx)-Fx_zero)
    Fz_list.append(np.mean(Fz)-Fz_zero)


plt.plot(velocities, Fx_list)
plt.title("Fx")
plt.show()

plt.plot(velocities, Fz_list, "k.")
plt.title("Fz")
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Force [N]")
plt.show()

