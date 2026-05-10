import numpy as np
import h5py
import os
import matplotlib.pyplot as plt
import scipy.signal as signal


def read(hdf5file, group, dataset):
    with h5py.File(hdf5file, "r") as f:
        return np.array(f[group][dataset][()])


def get_tip_displacement(h5_file):
    """
    Reads an HDF5 simulation file and returns:
    
    - time_list: list of time values
    - tip_y_list: list of vertical displacement values
                  for the last node (tip of the blade)
    """

    # Read time array
    t = read(h5_file, "TrussSystem", "time")
    time_list = t.flatten()

    # Number of nodes
    Nn = int(read(h5_file, "TrussSystem", "number_node")[0])

    # Number of timesteps
    steps = len(time_list)

    # Store tip displacement
    tip_y_list = []

    for frame in range(steps):

        # Read node positions
        pos = read(h5_file, "TrussSystem", f"XYZ_{frame}")

        # Reshape to [nodes, coordinates]
        pos = np.reshape(pos, [Nn, 3])

        # Vertical displacement of last node
        y_tip = pos[-1, 1]

        tip_y_list.append(y_tip)

    return list(time_list), tip_y_list


def freq_spectrum(time, y, cutoff_freq):
    
    #subtract mean to focus on oscillations
    y_values = y - np.nanmean(y)

    #sample rate
    dt = np.mean(np.diff(time))
    fs = 1 / dt

    #filtering with a high-pass Butterworth filter to remove low-frequency drift
    b, a = signal.butter(5, cutoff_freq, btype='high', fs=fs)
    filtered_values = signal.filtfilt(b, a, y_values)

    #FFT (rfft for real-valued input)
    X = np.fft.rfft(y_values)
    X_filtered = np.fft.rfft(filtered_values)

    freq = np.fft.rfftfreq(len(y_values), dt)

    X_mag = np.abs(X)
    X_filtered_mag = np.abs(X_filtered)

    #Dominant frequency[Hz] and max y[m]
    freq_dominant = np.round(freq[np.argmax(X_mag[1:]) + 1], 2)
    freq_dominant_filtered = np.round(freq[np.argmax(X_filtered_mag[1:]) + 1], 2)
    y_max = np.round(np.max(np.abs(y_values)), 2)

    return freq_dominant, y_max, freq_dominant_filtered, freq, X_mag, X_filtered_mag

config = "S" # S/C
model = "J" # A/M/J/W

speeds = ["2", "3", "4", "5", "6", "7", "8", "9"] 
vel = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

speeds = speeds[1:-1] 
vel = vel[1:-1]

# freq_dominant, y_max, freq_dominant_filtered, freq, X_mag, X_filtered_mag = make_freq_spectrum(file, run, config, cutoff_freq)

freq_list = []
X_mag_list = []
X_filtered_mag_list = []
freq_dominant_list = []
freq_dominant_filtered_list = []
y_max_list = []

#speeds = speeds[2:]
#vel = vel[2:]

for speed in speeds:
    run = str(config)+"_"+str(model)+"_"+str(speed)+"_1"
    file = "master_jenny_oystein/correct_results_num/" + run + ".txt"

    #Need to be changed for each model
    if int(speed) < 7:
        cutoff_freq = 1
    else:
        cutoff_freq = 1
    #print(cutoff_freq)
    freq_dominant, y_max, freq_dominant_filtered, freq, X_mag, X_filtered_mag = freq_spectrum(file, run, config, cutoff_freq)
    
    freq_list.append(freq)
    X_mag_list.append(X_mag)
    X_filtered_mag_list.append(X_filtered_mag)
    freq_dominant_list.append(freq_dominant)
    freq_dominant_filtered_list.append(freq_dominant_filtered)
    y_max_list.append(y_max) 

    #Print frequencies
print("Dominant frequencies unfiltered:")
print(freq_dominant_list)
print("Dominant frequency filtered:")
for i in range(len(speeds)):
    print(freq_dominant_filtered_list[i]) 

os.makedirs("Spectrums_comparison_filtered", exist_ok=True) 


#Filtered spectrum 
""" os.makedirs("Spectrums_comparison_filtered", exist_ok=True) 
for i in range(len(speeds)): 
    plt.figure(figsize=(10, 6)) 
    plt.plot(freq_list[i], X_filtered_mag_list[i], label = "0."+speeds[i]+" m/s")
    plt.legend()    
    plt.xlim(0, 10) 
    plt.xlabel('Frequency (Hz)', fontsize=14) 
    plt.ylabel('Magnitude', fontsize=14) 
    plt.grid()
    plt.title("Frequency spectrum Cluster April "+ "0."+speeds[i]+" m/s", fontsize=16)

    filepath = os.path.join("Spectrums_comparison_filtered", "spectrum_filtered_values_"+str(config)+"_"+str(model)+"_"+str(speeds[i])+".png")
    plt.savefig(filepath, dpi=300)
    plt.close() """