import numpy as np
import h5py
import pickle
import matplotlib.pyplot as plt
import os
import sys

def read(hdf5file, group, dataset):
    with h5py.File(hdf5file, "r") as f:
        return np.array(f[group][dataset][()])

def get_numerical_loads(input_file):
    
    t     = read(input_file, "TrussSystem", "time")
    Nt    = int(read(input_file, "TrussSystem", "number_truss")[0])
    Nn    = int(read(input_file, "TrussSystem", "number_node")[0])
    t     = t[:, 0]
    steps = t.size

    loads = np.zeros((steps, 2))
    for i in range(steps):
        load = read(input_file, "TrussSystem", "Load_{:d}".format(i))
        loads[i, 0] = load[0]
        loads[i, 1] = load[2]

    t     = t[1:]
    loadx = loads[1:, 0]
    loadz = loads[1:, 1]

    loadx_mean = np.average(loadx)

    return t, loadx, loadz, loadx_mean

config = "S" # S/C
#model = "A" # A/M/J/W
model_list = ["A", "M", "J"]
speed = "7" # 3=0.3m/s
velocities = ["03", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

Fx_mean = []
for model in model_list:
    Fx_mean_model_list = []
    #Looping through all vlelocities for the given config and model 
    for i in range(len(velocities)):
        run = str(config)+"_"+str(model)+"_"+str(velocities[i])
        filename = "master_jenny_oystein/results_num/" + str(config)+"_"+str(model)+ "/" + run + ".h5"
        time, loadx, loadz, loadx_mean = get_numerical_loads(filename)
        Fx_mean_model_list.append(loadx_mean)
        #print(f"Run: {run}, loadx_mean: {loadx_mean}")
    Fx_mean.append(Fx_mean_model_list)

os.makedirs("Numerical Plots", exist_ok=True)

plt.figure(figsize=(9, 6)) 
plt.plot(velocities, Fx_mean[0], '-', color='blue', label="April")
plt.plot(velocities, Fx_mean[1], '-', color='orange', label="May")
plt.plot(velocities, Fx_mean[2], '-', color='green', label="June")
#plt.plot(velocities, Fx_mean[3], '.', color='red', label="Wavy")

"""  plt.plot(U_list, curve_fit_list[0], '--', color='blue', label="Curve fit April")
plt.plot(U_list, curve_fit_list[1], '--', color='orange', label="Curve fit May")
plt.plot(U_list, curve_fit_list[2], '--', color='green', label="Curve fit June")
plt.plot(U_list, curve_fit_list[3], '--', color='red', label="Curve fit Wavy") """

plt.plot(0, 0, 'black', marker='o', label="Origo")
plt.legend()
plt.grid()
plt.title("Numerical Single")
plt.xlabel("Flow velocity [m/s]")
plt.ylabel("Drag force [N]")
filepath = os.path.join("Numerical Plots", "load_plot.png")
plt.savefig(filepath, dpi=300)
#plt.show()







""" #plotting
fig, axes = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.15)

axes[0].plot(t, loadx, '-+')
axes[0].set_ylabel("loadx")

axes[1].plot(t, loadz)
axes[1].set_ylabel("loadz")

axes[2].plot(t, loadx + loadz)
axes[2].set_ylabel("loadx + loadz")

axes[2].set_xlabel("time (s)")

print(loadx.size, loadx_mean)

#plt.show()

os.makedirs("Numerical Plots", exist_ok=True) 
filepath = os.path.join("Numerical Plots", "load_plot.png")
plt.savefig(filepath, dpi=300)
print("Saved plot to load_plot.png") """