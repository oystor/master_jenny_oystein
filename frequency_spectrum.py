from read_motion_file import readfile_motion
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import os

def make_freq_spectrum(file, run):

    time, x, y = readfile_motion(file)

    nans = np.isnan(y)
    y[nans] = np.interp(np.flatnonzero(nans), np.flatnonzero(~nans), y[~nans])
    
    #FFT of the steady-state values
    y_values = y - np.nanmean(y)

    def highpass_filter(data, cutoff_freq, sample_rate, order=5):
        nyquist = sample_rate / 2
        normal_cutoff = cutoff_freq / nyquist
        b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
        return signal.filtfilt(b, a, data)  
    
    #Sample rate 

    filtered_values = highpass_filter(y_values, cutoff_freq=0.1, sample_rate=60)

    X = np.fft.fft(y_values)
    X_mag = np.abs(X)

    #Dominant frequency [Hz] and max y [m]
    #freq_dominant = np.round(np.argmax(X_mag) * 60 / y_values.size,2)
    freq = np.fft.fftfreq(y_values.size, d=1/60)
    freq_dominant = np.round(freq[np.argmax(X_mag[1:]) + 1], 2)
    y_max = np.round(np.max(np.abs(y_values)), 2)

    X_filtered = np.fft.fft(filtered_values)
    X_filtered_mag = np.abs(X_filtered)

    #PLOTS time series filtered
    plt.figure(figsize=(9, 6))
    plt.plot(time, filtered_values, 'k-')
    plt.title('Time series of filtered values '+run, fontsize=18)

    os.makedirs("Filtered_timeseries", exist_ok=True) 
    filepath = os.path.join("Filtered_timeseries", "filtered_timeseries_"+run+".png")
    plt.savefig(filepath, dpi=300)
    plt.close()
    
    #Unfiltered time series
    plt.figure(figsize=(9, 6))
    plt.plot(time, y_values, 'k-')
    plt.title('Time series of un-filtered values '+run, fontsize=18)

    os.makedirs("Unfiltered_timeseries", exist_ok=True) 
    filepath = os.path.join("Unfiltered_timeseries", "timeseries_"+run+".png")
    plt.savefig(filepath, dpi=300)
    plt.close()

    #Frequency spectrum plots unfiltered
    plt.figure(figsize=(9, 6)) 
    #freq = np.abs(np.fft.fftfreq(y_values.size, d=1/60))
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

    #Filtered
    plt.figure(figsize=(9, 6)) 
    freq_filtered = np.abs(np.fft.fftfreq(filtered_values.size, d=1/60))
    plt.plot(freq_filtered, X_filtered_mag, 'k-')
    plt.xlim(0, 10)
    plt.xlabel('Frequency (Hz)', fontsize=18)
    plt.ylabel('Magnitude', fontsize=18)
    plt.title('Frequency spectrum '+run, fontsize=18)
    plt.grid()

    os.makedirs("Filtered_spectrums", exist_ok=True) 
    filepath = os.path.join("Filtered_spectrums", "spectrum_filtered_values_"+run+".png")
    plt.savefig(filepath, dpi=300)
    plt.close()

    return freq_dominant, y_max

###############################################################################
# Repeatability test
###############################################################################

""" config = "S" # S/C
model = "J" # A/M/J/W
speed = "3" # 3=0.3m/s

freq_dominant = np.array([])
y_max = np.array([])
#Looping through all 5 runs 
for i in range(1, 6):
    run = str(config)+"_"+str(model)+"_"+str(speed)+"_"+str(i)
    file = "video_data/" + run + ".txt"
    freq, y = make_freq_spectrum(file, run)

    freq_dominant = np.append(freq_dominant, float(freq))
    y_max = np.append(y_max, float(y))

print(freq_dominant)
print(y_max) """
