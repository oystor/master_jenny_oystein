from read_motion_file import readfile_motion
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import os
from scipy.ndimage import gaussian_filter1d
from scipy.signal import savgol_filter

def make_freq_spectrum(file, run, config, cutoff_freq):

    time, x, y = readfile_motion(file, config)

    # fill missing y values with interpolation
    nans = np.isnan(y)
    y[nans] = np.interp(np.flatnonzero(nans), np.flatnonzero(~nans), y[~nans])
    
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

     # Second dominant frequency
    sorted_indices = np.argsort(X_mag[1:]) + 1
    sorted_indices_filtered = np.argsort(X_filtered_mag[1:]) + 1

    freq_second_dominant = np.round(freq[sorted_indices[-2]], 2)
    freq_second_dominant_filtered = np.round(freq[sorted_indices_filtered[-2]], 2)

    return (freq_dominant, freq_second_dominant, y_max, freq_dominant_filtered, freq_second_dominant_filtered, freq, X_mag, X_filtered_mag)



###############################################################################
# Repeatability test
###############################################################################

""" config = "S" # S/C
model = "J" # A/M/J/W
speed = "7" # 3=0.3m/s
cutoff_freq = 1 # Hz (to remove low-frequency drift)

freq_dominant = np.array([])
freq_dominant_filtered = np.array([])
y_max = np.array([])
#Looping through all 5 runs 
for i in range(1, 6):
    run = str(config)+"_"+str(model)+"_"+str(speed)+"_"+str(i)
    file = "master_jenny_oystein/video_data/" + run + ".txt"
    freq, y, freq_filtered, freqs_spectrum, X_mag, X_filtered_mag = make_freq_spectrum(file, run, config, cutoff_freq)

    freq_dominant = np.append(freq_dominant, float(freq))
    freq_dominant_filtered = np.append(freq_dominant_filtered, float(freq_filtered))
    y_max = np.append(y_max, float(y))

print(freq_dominant)
print(y_max)

print(str(config)+"_"+str(model)+"_"+str(speed))
print("Max amplitude:")
for i in range(5):
    print(y_max[i])
print("Dominant frequency:")
for i in range(5):
    print(freq_dominant[i])
print("Dominant frequency filtered:")
for i in range(5):
    print(freq_dominant_filtered[i])  """

###############################################################################
# Compare speeds (frequency cpectrums)
###############################################################################

config = "S" # S/C
model = "M" # A/M/J/W
#speed = "3" # 3=0.3 m/s
#cutoff_freq = 0.1 # Hz (to remove low-frequency drift)

speeds = ["2", "3", "4", "5", "6", "7", "8", "9"] 
vel = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

speeds = speeds[1:] 
vel = vel[1:]

# freq_dominant, y_max, freq_dominant_filtered, freq, X_mag, X_filtered_mag = make_freq_spectrum(file, run, config, cutoff_freq)

freq_list = []
X_mag_list = []
X_filtered_mag_list = []
freq_dominant_list = []
freq_dominant_filtered_list = []
y_max_list = []
freq_second_dominant_filtered_list = []

#speeds = speeds[2:]
#vel = vel[2:]

for speed in speeds:
    run = str(config)+"_"+str(model)+"_"+str(speed)+"_1"
    file = "master_jenny_oystein/video_data/" + run + ".txt"

    #Need to be changed for each model
    if int(speed) < 6:
        cutoff_freq = 0.5
    else:
        cutoff_freq = 1
    #print(cutoff_freq)
    freq_dominant, freq_second_dominant, y_max, freq_dominant_filtered, freq_second_dominant_filtered, freq, X_mag, X_filtered_mag = make_freq_spectrum(file, run, config, cutoff_freq)
    
    freq_list.append(freq) 
    X_mag_list.append(X_mag) 
    X_filtered_mag_list.append(X_filtered_mag) 
    freq_dominant_list.append(freq_dominant) 
    freq_dominant_filtered_list.append(freq_dominant_filtered) 
    y_max_list.append(y_max) 
    freq_second_dominant_filtered_list.append(freq_second_dominant_filtered) 

os.makedirs("Spectrums_comparison_filtered", exist_ok=True) 

#Unfiltered spectrum 
""" for i in range(len(speeds)):
    plt.plot(freq_list[i], X_mag_list[i], label = "0."+speeds[i]+" m/s")
plt.legend()    
plt.xlim(0, 7)
plt.xlabel('Frequency (Hz)', fontsize=18)
plt.ylabel('Magnitude', fontsize=18)
plt.title('Frequency spectrum comparison unfiltered', fontsize=18)

os.makedirs("Spectrums_comparison", exist_ok=True) 
filepath = os.path.join("Spectrums_comparison", "spectrum_unfiltered_values_"+str(config)+"_"+str(model)+".png")
plt.savefig(filepath, dpi=300)
plt.close() """


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

#Print frequencies
""" print("Dominant frequencies unfiltered:")
print(freq_dominant_list)
#print("Dominant frequencies filtered:")
#print(freq_dominant_filtered_list)
"""
print("Dominant frequency filtered:")
for i in range(len(speeds)):
    print(freq_dominant_filtered_list[i]) 
print("Second dominant frequency filtered:")
for i in range(len(speeds)):
    print(freq_second_dominant_filtered_list[i]) 


#Dominant frequencies vs velocity
""" plt.plot(vel, freq_dominant_filtered_list)   
plt.ylabel('Frequency (Hz)', fontsize=14)
plt.xlabel('Current velocity [m/s]', fontsize=14)
plt.grid()
plt.title("Dominant frequency Cluster Wavy", fontsize=16)

#os.makedirs("Spectrums_comparison", exist_ok=True) 
filepath = os.path.join("Spectrums_comparison_filtered", "dominant frequency_"+str(config)+"_"+str(model)+".png")
plt.savefig(filepath, dpi=300)
plt.close() """


""" #Plot max amplitude vs velocity
os.makedirs("Flutter_Amplitude", exist_ok=True) 
plt.figure(figsize=(10, 6))
plt.plot(vel, y_max_list)
plt.ylabel('Flutter amplitude [m]', fontsize=14)
plt.xlabel('Current velocity [m/s]', fontsize=14)
#plt.legend()    
#plt.xlim(0, 7)
plt.xlabel('Current velocity [m/s]', fontsize=14)
plt.ylabel('Amplitude (m)', fontsize=14)
plt.grid()
plt.title("Max Amplitude Cluster April", fontsize=16)

filepath = os.path.join("Flutter_Amplitude", "amplitude_"+str(config)+"_"+str(model)+".png")
plt.savefig(filepath, dpi=300)
plt.close()

#Print amplitudes
print("Amplitudes:")
for i in range(len(speeds)):
    print(y_max_list[i]) """


""" #Smoothed frequency spectrums
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
plt.title("Smoothed frequency spectra Cluster April")
plt.legend()
plt.grid(True)
filepath = os.path.join("Spectrums_comparison_filtered", "spectrum_smoothed_"+str(config)+"_"+str(model)+"_.png")
plt.savefig(filepath, dpi=300)
plt.close()  """