import numpy as np
import h5py
import pickle
import matplotlib.pyplot as plt
import os
import sys

def read(hdf5file, group, dataset):
    with h5py.File(hdf5file, "r") as f:
        return np.array(f[group][dataset][()])
    
input_file = "structure.h5"
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

plt.savefig("load_plot.png", dpi=200)
print("Saved plot to load_plot.png")