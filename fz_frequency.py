import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
import scipy.signal as signal
from read_force_file import experiment_data, cut_timeseries
from read_motion_file import readfile_motion
from scipy.ndimage import gaussian_filter1d


###############################################################################
# FZ ZERO VALUES
###############################################################################

velocities = ["03", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

#zero value is set as average of time series between 100 and 200s
Fz_zero_list = []


for vel in velocities:
    filename_bin = "master_jenny_oystein/Force_measurements/Z_" + vel + "_1.bin"
    filename_TST = "master_jenny_oystein/Force_measurements/Z_" + vel + "_1.TST"
    time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
    t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)

    Fz_zero_list.append(np.mean(Fz))


#####################################################ß##########################
# FREQUENCY SPECTRUM FZ
###############################################################################

def frequency_spectrum_fz(time, Fz, lowcut, highcut):
    #Calculate frequency spectrum using FFT
    #sample rate
    dt = np.mean(np.diff(time))
    fs = 1 / dt

    #filtering with a bandpass Butterworth filter to remove low-frequency drift and high-frequency noise
    #b, a = signal.butter(5, cutoff_freq, btype='high', fs=fs)
    b, a = signal.butter(5, [lowcut, highcut],btype='bandpass',fs=fs)
    filtered_values = signal.filtfilt(b, a, Fz)

    # FFT (rfft for real-valued input)
    Fz_fft = np.fft.rfft(Fz)
    Fz_fft_filtered = np.fft.rfft(filtered_values)

    freq = np.fft.rfftfreq(len(Fz), dt)

    Fz_fft_mag = np.abs(Fz_fft)
    Fz_fft_filtered_mag = np.abs(Fz_fft_filtered)

    # Normalize spectrum so maximum peak = 1
    Fz_fft_mag = Fz_fft_mag / np.max(Fz_fft_mag[1:])
    Fz_fft_filtered_mag = Fz_fft_filtered_mag / np.max(Fz_fft_filtered_mag[1:])

    # Dominant frequency [Hz]
    freq_dominant = np.round(freq[np.argmax(Fz_fft_mag[1:]) + 1], 2)
    freq_dominant_filtered = np.round(freq[np.argmax(Fz_fft_filtered_mag[1:]) + 1], 2)

    return freq, Fz_fft_mag, Fz_fft_filtered_mag, freq_dominant, freq_dominant_filtered


#freq, Fz_fft_mag, Fz_fft_filtered_mag, freq_dominant, freq_dominant_filtered = frequency_spectrum_fz(time, Fz, cutoff_freq)

#####################################################ß##########################
# PLOT FREQUENCY SPECTRUM FZ
###############################################################################

config = "C" # S/C
model = "W" # A/M/J/W

speeds = ["2", "3", "4", "5", "6", "7", "8", "9"] 
vel = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

speeds = speeds[2:] 
vel = vel[2:]

freq_list = []
Fz_fft_mag_list = []
Fz_fft_filtered_mag_list = []
freq_dominant_list = []
freq_dominant_filtered_list = []

for speed in speeds:
    run = str(config)+"_"+str(model)+"_"+str(speed)+"_1"
    file = "master_jenny_oystein/Force_measurements/" + run + ".txt"

    filename_bin = "master_jenny_oystein/Force_measurements/" + run + ".bin"
    filename_TST = "master_jenny_oystein/Force_measurements/" + run + ".TST"
    time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
    t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)
    Fz = Fz - Fz_zero_list[speeds.index(speed)] #zero value is set as average of time series between 100 and 200s
    #Need to be changed for each model
    if int(speed) < 7:
        lowcut = 0.3
    else:
        lowcut = 1
    highcut = 15
    freq, Fz_fft_mag, Fz_fft_filtered_mag, freq_dominant, freq_dominant_filtered = frequency_spectrum_fz(t, Fz, lowcut, highcut)
    
    freq_list.append(freq)
    Fz_fft_mag_list.append(Fz_fft_mag)
    Fz_fft_filtered_mag_list.append(Fz_fft_filtered_mag)
    freq_dominant_list.append(freq_dominant)
    freq_dominant_filtered_list.append(freq_dominant_filtered)


""" #Print frequencies
print("Dominant frequencies unfiltered:")
for i in range(len(speeds)):
    print(freq_dominant_list[i]) 

print("Dominant frequency filtered:")
for i in range(len(speeds)):
    print(freq_dominant_filtered_list[i])  """


os.makedirs("Fz_frequency", exist_ok=True) 
#Filtered spectrum 

""" for i in range(len(speeds)): 
    plt.figure(figsize=(10, 6)) 
    plt.plot(freq_list[i], Fz_fft_filtered_mag_list[i], label = "0."+speeds[i]+" m/s")
    plt.legend()    
    plt.xlim(0, 15) 
    plt.xlabel('Frequency (Hz)', fontsize=14) 
    plt.ylabel('Normalized magnitude', fontsize=14) 
    plt.grid()
    plt.title("Fz Frequency spectrum Cluster Wavy "+ "0."+speeds[i]+" m/s", fontsize=16)

    filepath = os.path.join("Fz_frequency", "spectrum_filtered_"+str(config)+"_"+str(model)+"_"+str(speeds[i])+".png")
    plt.savefig(filepath, dpi=300)
    plt.close()

#Smoothed frequency spectrums
plt.figure(figsize=(8,5))

for i, speed in enumerate(speeds):
    freq = freq_list[i]
    Fz = Fz_fft_filtered_mag_list[i]

    Fz_smooth = gaussian_filter1d(Fz, sigma=20)

    plt.plot(freq, Fz_smooth, label=f"{vel[i]} m/s")
plt.xlim(0, 15)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Normalised smoothed magnitude")
plt.title("Smoothed frequency spectra Cluster Wavy")
plt.legend()
plt.grid(True)
filepath = os.path.join("Fz_frequency", "spectrum_smoothed_"+str(config)+"_"+str(model)+"_.png")
plt.savefig(filepath, dpi=300)
plt.close()  """


