import numpy as np
import h5py
import os
import matplotlib.pyplot as plt
import scipy.signal as signal
from scipy.ndimage import gaussian_filter1d


def read(hdf5file, group, dataset):
    with h5py.File(hdf5file, "r") as f:
        return np.array(f[group][dataset][()])


def get_tip_displacement(h5_file):

    #Read time
    t = read(h5_file, "TrussSystem", "time")
    time_list = t.flatten()

    #Number of nodes
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

         # Keep only the last half
    half_index = steps // 2

    time_list = time_list[half_index:]
    tip_y_list = tip_y_list[half_index:]

    return list(time_list), tip_y_list


def freq_spectrum(h5_file, cutoff_freq):

    time, y = get_tip_displacement(h5_file)
    
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

config = "C" # S/C
model = "W" # A/M/J/W
cm = "014"

speeds = ["2", "3", "4", "5", "6", "7", "8", "9"] 
vel = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] 

speeds = speeds[2:] 
vel = vel[2:] 


freq_list = []
X_mag_list = []
X_filtered_mag_list = []
freq_dominant_list = []
freq_dominant_filtered_list = []
y_max_list = []

for speed in speeds:
    run = str(config)+"_"+str(model)+"_"+str(speed)+"_"+str(cm)
    file = "master_jenny_oystein/correct_results_num/"+str(config)+"_"+str(model)+"/" + run + ".h5"

    #Need to be changed for each model
    if int(speed) < 7:
        cutoff_freq = 0.3
    else:
        cutoff_freq = 1
    #print(cutoff_freq)
    freq_dominant, y_max, freq_dominant_filtered, freq, X_mag, X_filtered_mag = freq_spectrum(file, cutoff_freq)
    
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



#Filtered spectrum 
os.makedirs("Numerical_Spectrums", exist_ok=True) 
for i in range(len(speeds)): 
    plt.figure(figsize=(10, 6)) 
    plt.plot(freq_list[i], X_filtered_mag_list[i], label = "0."+speeds[i]+" m/s")
    plt.legend()    
    plt.xlim(0, 10) 
    plt.xlabel('Frequency (Hz)', fontsize=14) 
    plt.ylabel('Magnitude', fontsize=14) 
    plt.grid()
    plt.title("Frequency spectrum numerical Cluster Wavy "+ "0."+speeds[i]+" m/s", fontsize=16)

    filepath = os.path.join("Numerical_Spectrums", "num_spectrum_filtered_"+str(config)+"_"+str(model)+"_"+str(speeds[i])+".png")
    plt.savefig(filepath, dpi=300)
    plt.close()


#Smoothed frequency spectrums
plt.figure(figsize=(8,5))

for i, speed in enumerate(speeds):
    freq = freq_list[i]
    X = X_filtered_mag_list[i]

    X_norm = X / np.max(X)
    X_smooth = gaussian_filter1d(X_norm, sigma=15)

    plt.plot(freq, X_smooth, label=f"{vel[i]} m/s")

plt.xlim(0, 10)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Normalised smoothed magnitude")
#plt.title("Smoothed frequency spectra Cluster April")
plt.legend()
plt.grid(True)
filepath = os.path.join("Numerical_Spectrums", "num_spectrum_smoothed_"+str(config)+"_"+str(model)+"_.png")
plt.savefig(filepath, dpi=300)
plt.close() 