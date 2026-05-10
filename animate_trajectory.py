import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rc
import h5py
import sys
import os

rc('text', usetex=False)
rc('font', family='serif', size=24)

def read(hdf5file, group, dataset):
    with h5py.File(hdf5file, "r") as f:
        return np.array(f[group][dataset][()])

input_file = "structure.h5"

if not os.path.exists(input_file):
    print("The file " + input_file + " does not exist!\nPlease check again!\n")
    sys.exit()

t     = read(input_file, "TrussSystem", "time")
Nn    = int(read(input_file, "TrussSystem", "number_node")[0])
steps = t.size
N_step = 80

length = 0.505

fig = plt.figure(figsize=(9, 9))
plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.15)
ax = fig.add_subplot()

xmin =  0.0
xmax =  0.6
ymin = -0.4
ymax =  0.2

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_xlabel(r'$x$', fontsize=24)
ax.set_ylabel(r'$z$', fontsize=24)
ax.grid()

xdata, ydata = [], []
ln1, = ax.plot([], [], 'k-')
time_template = r"$t={:0.2f}\,$s"
time_text = ax.text(0.7, 0.1, '', transform=ax.transAxes, fontsize=24)

# Use a Python list
y_data_list = []

def init():
    pos = read(input_file, "TrussSystem", "XYZ_0")
    pos = np.reshape(pos, [Nn, 3])

    xdata = pos[:, 0] 
    ydata = pos[:, 1] 

    ln1.set_data(xdata, ydata)

    tt = t[0][0]
    time_text.set_text(time_template.format(tt))

    # store initial values
    y_data_list.append(ydata[-1])
    return ln1, time_text


def update(frame):
    pos = read(input_file, "TrussSystem", "XYZ_{:d}".format(frame))
    pos = np.reshape(pos, [Nn, 3])

    xdata = pos[:, 0] 
    ydata = pos[:, 1] 

    # store all y values
    y_data_list.append(ydata[-1])
    ln1.set_data(xdata, ydata)

    tt = t[frame][0]
    time_text.set_text(time_template.format(tt))

    return ln1, time_text


start_frame = 0
frames = np.arange(0, steps)

ani = animation.FuncAnimation(
    fig, update, frames=frames,
    interval=50.0, init_func=init, blit=True
)

from matplotlib.animation import FFMpegWriter

writervideo = FFMpegWriter(fps=10, bitrate=1800)
ani.save("blade_animation.mp4", writer=writervideo)

print("Saved animation to blade_animation.mp4")

# Convert to numpy and compute min/max
y_array = np.array(y_data_list)



#FFT of the steady-state values
steady_start_time = 15
steady_state_values = y_array[-int(steady_start_time*60):]  # last 15 seconds of data at 60 Hz
steady_state_values = steady_state_values - np.mean(steady_state_values)
start_time = 45-steady_start_time
steady_state_x_values = np.arange(start_time, start_time+steady_state_values.size/60, 1/60)
X = np.fft.fft(steady_state_values)
X_mag = np.abs(X)
print("Dominant frequency:", np.round(np.argmax(X_mag) * 60 / steady_state_values.size,2), "Hz")
print("Amplitude of oscillation:", np.round((np.max(steady_state_values) - np.min(steady_state_values)) / 2, 2), "m")

#Plotting the time series
plt.figure(figsize=(9, 6))
plt.plot(steady_state_x_values, steady_state_values, 'k-')
plt.xlabel('Time step', fontsize=24)
plt.ylabel('y value of the last node', fontsize=24)
plt.title('Steady-state y values of the last node', fontsize=24)
plt.grid()
plt.savefig("time_y_values.png", dpi=300)
plt.close()

#Plotting the frequency spectrum analysis
plt.figure(figsize=(9, 6)) 
freq = np.abs(np.fft.fftfreq(steady_state_values.size, d=1/60))
plt.plot(freq, X_mag, 'k-')
plt.xlim(0, 10)
plt.xlabel('Frequency (Hz)', fontsize=24)
plt.ylabel('Magnitude', fontsize=24)
plt.title('Frequency spectrum', fontsize=24)
plt.grid()
plt.savefig("spectrum_y_values.png", dpi=300)
print("Saved time series and frequency spectrum plots.")
plt.close()