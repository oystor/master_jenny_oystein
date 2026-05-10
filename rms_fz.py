import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os
from read_motion_file import readfile_motion
from read_force_file import experiment_data, cut_timeseries

###############################################################################
# FUNCTIONS
###############################################################################

def rms_fluctuations(values):
    values = np.asarray(values)
    values = values - np.nanmean(values)
    return np.sqrt(np.nanmean(values**2))


def bandpass_filter(data, time, lowcut, highcut, order=5):
    dt = np.nanmean(np.diff(time))
    fs = 1 / dt

    b, a = signal.butter(
        order,
        [lowcut, highcut],
        btype='bandpass',
        fs=fs
    )
    filtered = signal.filtfilt(b, a, data)
    return filtered

def highpass_filter(data, time, cutoff_freq, order=5):
    dt = np.nanmean(np.diff(time))
    fs = 1 / dt

    b, a = signal.butter(
        order,
        cutoff_freq,
        btype='highpass',
        fs=fs
    )
    filtered = signal.filtfilt(b, a, data)
    return filtered



###############################################################################
# FZ ZERO VALUES
###############################################################################

velocities = ["03", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

#zero value is set as average of time series between 100 and 200s
Fz_zero_dict = {}

for vel0 in velocities:
    filename_bin = "master_jenny_oystein/Force_measurements/Z_" + vel0 + "_1.bin"
    filename_TST = "master_jenny_oystein/Force_measurements/Z_" + vel0 + "_1.TST"
    time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
    t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)

    Fz_zero_dict[vel0] = np.mean(Fz)

###############################################################################
# RMS VALUES
###############################################################################

config = "C"
model = "J"

speeds = ["2", "3", "4", "5", "6", "7", "8", "9"]
vel = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

y_rms_list = []
Fz_rms_list = []

for speed in speeds:
    run = f"{config}_{model}_{speed}_1"

    # Motion data
    motion_file = f"master_jenny_oystein/video_data/{run}.txt"
    time_y, x, y = readfile_motion(motion_file, config)

    # fill missing y values with interpolation
    nans = np.isnan(y)
    y[nans] = np.interp(np.flatnonzero(nans), np.flatnonzero(~nans), y[~nans])

    # high-pass filter motion to remove slow drift
    #Need to be changed for each model
    if int(speed) < 5:
        lowcut = 0.5
    else:
        lowcut = 1.5
    y_filtered = highpass_filter(y, time_y, lowcut)

    y_rms = rms_fluctuations(y_filtered)
    y_rms_list.append(y_rms)


    # Force data
    filename_bin = f"master_jenny_oystein/Force_measurements/{run}.bin"
    filename_TST = f"master_jenny_oystein/Force_measurements/{run}.TST"

    time, water_speed, Fx, Fy, Fz, Mx, My, Mz = experiment_data(filename_bin, filename_TST)
    t, Fx, Fz = cut_timeseries(100, 200, time, Fx, Fz)

    # remove zero value 
    Fz = Fz - Fz_zero_dict[speed]

    highcut = 15
    # filter values
    Fz_filtered = bandpass_filter(Fz, t, lowcut, highcut)

    Fz_rms = rms_fluctuations(Fz_filtered)
    Fz_rms_list.append(Fz_rms)



###############################################################################
# RMS VALUES
###############################################################################

os.makedirs("RMS_plots", exist_ok=True) 
plt.figure(figsize=(7, 5))
plt.scatter(y_rms_list, Fz_rms_list)

for i, speed in enumerate(speeds):
    plt.annotate(f"0.{speed} m/s", (y_rms_list[i], Fz_rms_list[i]))

plt.xlabel("Vertical displacement RMS [m]", fontsize=14)
plt.ylabel(r"$F_z$ RMS [N]", fontsize=14)
plt.grid()
plt.title("Fluctuations Vertical motion vs. vertical force Cluster June")
plt.tight_layout()
filepath = os.path.join("RMS_plots", "RMS_plot_"+str(config)+"_"+str(model)+"_.png")
plt.savefig(filepath, dpi=300)
#plt.show()




