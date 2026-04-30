from read_motion_file import readfile_motion
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import os

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

    #filter
    def highpass_filter(data, cutoff_freq, sample_rate, order=5):
        nyquist = sample_rate / 2
        normal_cutoff = cutoff_freq / nyquist
        b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
        return signal.filtfilt(b, a, data)  
    
    #filtered values 
    filtered_values = highpass_filter(y_values, cutoff_freq, sample_rate=fs)

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

    """ #PLOTS time series filtered
    plt.figure(figsize=(9, 6))
    plt.plot(time, filtered_values, 'k-')
    plt.title('Time series of filtered values '+run, fontsize=18)

    os.makedirs("Filtered_timeseries", exist_ok=True) 
    filepath = os.path.join("Filtered_timeseries", "filtered_timeseries_"+run+".png")
    plt.savefig(filepath, dpi=300)
    plt.close() """
    
    """ #Unfiltered time series
    plt.figure(figsize=(9, 6))
    plt.plot(time, y_values, 'k-')
    plt.title('Time series of un-filtered values '+run, fontsize=18)

    os.makedirs("Unfiltered_timeseries", exist_ok=True) 
    filepath = os.path.join("Unfiltered_timeseries", "timeseries_"+run+".png")
    plt.savefig(filepath, dpi=300)
    plt.close() """

    """ #Frequency spectrum plots
    plt.figure(figsize=(9, 6)) 
    plt.plot(freq, X_mag, 'k-')
    plt.xlim(0, 10)
    plt.xlabel('Frequency (Hz)', fontsize=18)
    plt.ylabel('Magnitude', fontsize=18)
    plt.title('Frequency spectrum '+run, fontsize=18)
    plt.grid()

    os.makedirs("Unfiltered_spectrums", exist_ok=True)
    filepath = os.path.join("Unfiltered_spectrums", "spectrum_y_values_"+run+".png")
    plt.savefig(filepath, dpi=300)
    plt.close()

    #Filtered frequency spectrum
    plt.figure(figsize=(9, 6)) 
    plt.plot(freq, X_filtered_mag, 'k-')
    plt.xlim(0, 10)
    plt.xlabel('Frequency (Hz)', fontsize=18)
    plt.ylabel('Magnitude', fontsize=18)
    plt.title('Frequency spectrum '+run, fontsize=18)
    plt.grid()

    os.makedirs("Filtered_spectrums", exist_ok=True) 
    filepath = os.path.join("Filtered_spectrums", "spectrum_filtered_values_"+run+".png")
    plt.savefig(filepath, dpi=300)
    plt.close() """

    return freq_dominant, y_max, freq_dominant_filtered, freq, X_mag, X_filtered_mag

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

config = "C" # S/C
model = "M" # A/M/J/W
#speed = "3" # 3=0.3 m/s
#cutoff_freq = 0.1 # Hz (to remove low-frequency drift)

speeds = ["3", "4", "5", "6", "7", "8", "9"]
vel = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

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
    file = "master_jenny_oystein/video_data/" + run + ".txt"

    if int(speed) < 5:
        cutoff_freq = 0.5
    else:
        cutoff_freq = 1
    #print(cutoff_freq)
    freq_dominant, y_max, freq_dominant_filtered, freq, X_mag, X_filtered_mag = make_freq_spectrum(file, run, config, cutoff_freq)
    freq_list.append(freq)
    X_mag_list.append(X_mag)
    X_filtered_mag_list.append(X_filtered_mag)
    freq_dominant_list.append(freq_dominant)
    freq_dominant_filtered_list.append(freq_dominant_filtered)
    y_max_list.append(y_max)   

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



os.makedirs("Spectrums_comparison_filtered", exist_ok=True) 
for i in range(len(speeds)):
    plt.plot(freq_list[i], X_filtered_mag_list[i], label = "0."+speeds[i]+" m/s")
    plt.legend()    
    plt.xlim(0, 7)
    plt.xlabel('Frequency (Hz)', fontsize=14)
    plt.ylabel('Magnitude', fontsize=14)
    plt.grid()
    plt.title("Frequency spectrum Cluster May "+ "0."+speeds[i]+" m/s", fontsize=16)

    filepath = os.path.join("Spectrums_comparison_filtered", "spectrum_filtered_values_"+str(config)+"_"+str(model)+"_"+str(speeds[i])+".png")
    plt.savefig(filepath, dpi=300)
    plt.close()

print("Dominant frequencies unfiltered:")
print(freq_dominant_list)
#print("Dominant frequencies filtered:")
#print(freq_dominant_filtered_list)

print("Dominant frequency filtered:")
for i in range(len(speeds)):
    print(freq_dominant_filtered_list[i])


plt.plot(vel, freq_dominant_filtered_list)   
plt.ylabel('Frequency (Hz)', fontsize=14)
plt.xlabel('Current velocity [m/s]', fontsize=14)
plt.grid()
plt.title("Dominant frequency Cluster May", fontsize=16)

#os.makedirs("Spectrums_comparison", exist_ok=True) 
filepath = os.path.join("Spectrums_comparison_filtered", "dominant frequency_"+str(config)+"_"+str(model)+".png")
plt.savefig(filepath, dpi=300)
plt.close()
