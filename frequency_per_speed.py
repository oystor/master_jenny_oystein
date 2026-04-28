import numpy as np
import matplotlib.pyplot as plt
import os
from read_motion_file import readfile_motion
from frequency_spectrum import make_freq_spectrum
import scipy.signal as signal

def make_freq_spectrum_with_speeds(config, model, speeds):
    colors = ['k', 'b', 'g', 'r', 'c', 'm', 'y', 'orange', 'purple']
    times = []
    xs = []
    ys = []
    freqs = []
    y_maxs = []
    freq_dominants = []
    X_mags = []
    freq_filtereds = []
    X_filtered_mags = []
    for i in range(0, len(speeds)):
        run = str(config)+"_"+str(model)+"_"+str(speeds[i])+"_"+str(1)
        print(run)
        file = "video_data/" + run + ".txt"
        time, x, y = readfile_motion(file)
        times.append(time)
        xs.append(x)
        ys.append(y)

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
            #sample rate
        dt = np.mean(np.diff(time))
        fs = 1 / dt

        filtered_values = highpass_filter(y_values, cutoff_freq=0.1, sample_rate=fs)

        X = np.fft.rfft(y_values)

        X_mag = np.abs(X)
        X_mags.append(X_mag)

        #Dominant frequency [Hz] and max y [m]
        #freq_dominant = np.round(np.argmax(X_mag) * 60 / y_values.size,2)
        freq = np.fft.rfftfreq(y_values.size, d=1/60)
        freqs.append(freq)

        freq_dominant = np.round(freq[np.argmax(X_mag[1:]) + 1], 2)
        freq_dominants.append(freq_dominant)

        y_max = np.round(np.max(np.abs(y_values)), 2)
        y_maxs.append(y_max)


        X_filtered = np.fft.fft(filtered_values)
        X_filtered_mag = np.abs(X_filtered)
        X_filtered_mags.append(X_filtered_mag)




        freq_filtered = np.abs(np.fft.fftfreq(filtered_values.size, d=1/60))
        freq_filtereds.append(freq_filtered)



        #PLOTS time series filtered
        plt.figure(figsize=(9, 6))
        plt.plot(time, filtered_values, 'k-')
        plt.title('Time series of filtered values '+run, fontsize=18)

        os.makedirs("Filtered_timeseries_speed_comparison", exist_ok=True) 
        filepath = os.path.join("Filtered_timeseries_speed_comparison", "filtered_timeseries_"+run+".png")
        plt.savefig(filepath, dpi=300)
        plt.close()
        
        #Unfiltered time series
        plt.figure(figsize=(9, 6))
        plt.plot(time, y_values, 'k-')
        plt.title('Time series of un-filtered values '+run, fontsize=18)

        os.makedirs("Unfiltered_timeseries_speed_comparison", exist_ok=True) 
        filepath = os.path.join("Unfiltered_timeseries_speed_comparison", "timeseries_"+run+".png")
        plt.savefig(filepath, dpi=300)
        plt.close()

    #Frequency spectrum plots unfiltered
    plt.figure(figsize=(9, 6)) 
    #freq = np.abs(np.fft.fftfreq(y_values.size, d=1/60))
    for i in range(0, len(speeds)):

        plt.plot(freqs[i], X_mags[i], 'k-', label="Speed "+speeds[i], color=colors[i])
    plt.xlim(0, 10)
    plt.xlabel('Frequency (Hz)', fontsize=18)
    plt.ylabel('Magnitude', fontsize=18)
    plt.legend()
    plt.title(f'Unfiltered frequency spectrum, {config}_{model}', fontsize=18)
    plt.grid()

    os.makedirs("Unfiltered_spectrums_speed_comparison", exist_ok=True)
    filepath = os.path.join("Unfiltered_spectrums_speed_comparison", "total_spectrum_y_values_"+run+".png")
    plt.savefig(filepath, dpi=300)
    plt.close()

    #Filtered
    plt.figure(figsize=(9, 6)) 
    for i in range(0, len(speeds)):
        plt.plot(freq_filtereds[i], X_filtered_mags[i], 'k-', label="Speed "+speeds[i], color=colors[i])
    plt.xlim(0, 10)
    plt.xlabel('Frequency (Hz)', fontsize=18)
    plt.ylabel('Magnitude', fontsize=18)
    plt.legend()
    plt.title(f'Filtered frequency spectrum, {config}_{model}', fontsize=18)
    plt.grid()

    os.makedirs("Filtered_spectrums_speed_comparison", exist_ok=True) 
    filepath = os.path.join("Filtered_spectrums_speed_comparison", "total_spectrum_filtered_values_"+run+".png")
    plt.savefig(filepath, dpi=300)
    plt.close()


    return freq_dominants, y_maxs

def make_freq_spectrum_with_configs(config, models, speed):
    colors = ['k', 'b', 'g', 'r', 'c', 'm', 'y', 'orange', 'purple']
    times = []
    xs = []
    ys = []
    freqs = []
    y_maxs = []
    freq_dominants = []
    X_mags = []
    freq_filtereds = []
    X_filtered_mags = []
    for i in range(0, len(models)):
        run = str(config)+"_"+str(models[i])+"_"+str(speed)+"_"+str(1)
        print(run)
        file = "video_data/" + run + ".txt"
        time, x, y = readfile_motion(file)
        times.append(time)
        xs.append(x)
        ys.append(y)

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
        dt = np.mean(np.diff(time))
        fs = 1 / dt

        filtered_values = highpass_filter(y_values, cutoff_freq=0.1, sample_rate=fs)

        X = np.fft.rfft(y_values)

        X_mag = np.abs(X)
        X_mags.append(X_mag)

        #Dominant frequency [Hz] and max y [m]
        #freq_dominant = np.round(np.argmax(X_mag) * 60 / y_values.size,2)
        freq = np.fft.rfftfreq(y_values.size, d=1/60)
        freqs.append(freq)

        freq_dominant = np.round(freq[np.argmax(X_mag[1:]) + 1], 2)
        freq_dominants.append(freq_dominant)

        y_max = np.round(np.max(np.abs(y_values)), 2)
        y_maxs.append(y_max)


        X_filtered = np.fft.fft(filtered_values)
        X_filtered_mag = np.abs(X_filtered)
        X_filtered_mags.append(X_filtered_mag)




        freq_filtered = np.abs(np.fft.fftfreq(filtered_values.size, d=1/60))
        freq_filtereds.append(freq_filtered)



        #PLOTS time series filtered
        plt.figure(figsize=(9, 6))
        plt.plot(time, filtered_values, 'k-')
        plt.title('Time series of filtered values '+run, fontsize=18)

        os.makedirs("Filtered_timeseries_config_comparison", exist_ok=True) 
        filepath = os.path.join("Filtered_timeseries_config_comparison", "filtered_timeseries_"+run+".png")
        plt.savefig(filepath, dpi=300)
        plt.close()
        
        #Unfiltered time series
        plt.figure(figsize=(9, 6))
        plt.plot(time, y_values, 'k-')
        plt.title('Time series of un-filtered values '+run, fontsize=18)

        os.makedirs("Unfiltered_timeseries_config_comparison", exist_ok=True) 
        filepath = os.path.join("Unfiltered_timeseries_config_comparison", "timeseries_"+run+".png")
        plt.savefig(filepath, dpi=300)
        plt.close()

    #Frequency spectrum plots unfiltered
    plt.figure(figsize=(9, 6)) 
    #freq = np.abs(np.fft.fftfreq(y_values.size, d=1/60))
    for i in range(0, len(models)):

        plt.plot(freqs[i], X_mags[i], 'k-', label="Model "+models[i], color=colors[i])
    plt.xlim(0, 10)
    plt.xlabel('Frequency (Hz)', fontsize=18)
    plt.ylabel('Magnitude', fontsize=18)
    plt.legend()
    plt.title(f'Unfiltered frequency spectrum, {config}_{model}', fontsize=18)
    plt.grid()

    os.makedirs("Unfiltered_spectrums_config_comparison", exist_ok=True)
    filepath = os.path.join("Unfiltered_spectrums_config_comparison", "total_spectrum_y_values_"+run+".png")
    plt.savefig(filepath, dpi=300)
    plt.close()

    #Filtered
    plt.figure(figsize=(9, 6)) 
    for i in range(0, len(models)):
        plt.plot(freq_filtereds[i], X_filtered_mags[i], 'k-', label="Model "+models[i], color=colors[i])
    plt.xlim(0, 10)
    plt.xlabel('Frequency (Hz)', fontsize=18)
    plt.ylabel('Magnitude', fontsize=18)
    plt.legend()
    plt.title(f'Filtered frequency spectrum, {config}_{model}', fontsize=18)
    plt.grid()

    os.makedirs("Filtered_spectrums_config_comparison", exist_ok=True) 
    filepath = os.path.join("Filtered_spectrums_config_comparison", "total_spectrum_filtered_values_"+run+".png")
    plt.savefig(filepath, dpi=300)
    plt.close()

    
    return freq_dominants, y_maxs


def freq_plot_multiple_speeds(config, model, speeds):
    freq_dominants_all = []
    y_maxs_all = []
    for speed in speeds:
        freq_dominants, y_maxs = make_freq_spectrum_with_speeds(config, model, speed)  
        freq_dominants_all.append(freq_dominants)
        y_maxs_all.append(y_maxs)
    
    #Plotting dominant frequencies vs speeds
    plt.figure(figsize=(9, 6))
    plt.plot(speeds, freq_dominants_all, 'k-', marker='o')
    plt.xlabel('Speed', fontsize=18)
    plt.ylabel('Dominant Frequency (Hz)', fontsize=18)
    plt.title(f'Dominant Frequency vs Speed for {config}_{model}', fontsize=18)
    plt.grid()
    plt.savefig(f"Dominant_Frequency_vs_Speed_{config}_{model}.png", dpi=300)
    plt.close()


all_configs = ["S", "C"]
all_models = ["A", "M", "J", "W"]
all_speeds = ["03", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

for model in all_models[:3]:
    freq_plot_multiple_speeds("S", model, all_speeds[2:9])





