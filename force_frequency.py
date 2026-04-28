import numpy as np
import matplotlib.pyplot as plt
from read_force_file import experiment_data, cut_timeseries

###############################################################################
# ZERO VALUES
###############################################################################

velocities = ["03", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

#zero value is set as average of time series between 100 and 200s
Fx_zero_list = []
Fz_zero_list = []


for vel in velocities:
    filename_bin = "Force measurements/Z_" + vel + "_1.bin"
    filename_TST = "Force measurements/Z_" + vel + "_1.TST"
    time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
    t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)

    Fx_zero_list.append(np.mean(Fx))
    Fz_zero_list.append(np.mean(Fz))


config = "S" # S/C
model = "M" # A/M/J/W
speed = "6" # 3=0.3 m/s

run = str(config)+"_"+str(model)+"_"+str(speed)+"_1"
filename_bin = "Force measurements/" + run + ".bin"
filename_TST = "Force measurements/" + run + ".TST"
time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
time, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)

Fz = Fz - Fz_zero_list[int(speed)] # Subtract zero value from Fz

fs = 200 # Sampling frequency Hz
Fz = Fz - np.mean(Fz) # Remove mean from Fz to focus on oscillations

# FFT
N = len(Fz)
fft_vals = np.fft.fft(Fz)
fft_vals = np.abs(fft_vals) / N 
freqs = np.fft.fftfreq(N, 1/fs)

mask = freqs >= 0
freqs = freqs[mask]
fft_vals = fft_vals[mask]

print("Dominant frequency: ", freqs[np.argmax(fft_vals)], "Hz")

plt.figure(figsize=(9, 6)) 
plt.plot(freqs, fft_vals)
plt.xlabel("Frequency (Hz)")
plt.ylabel('Magnitude')
plt.title('Frequency spectrum '+run, fontsize=18)
plt.show()