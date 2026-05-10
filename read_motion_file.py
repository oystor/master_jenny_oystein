import re
import numpy as np
import math
import matplotlib.pyplot as plt
import os

def readfile_motion(filename, config):
  #reads txt file with time, x and y values, returns lists

  #open txt file with time, x and y values
  with open(filename, encoding="utf-8") as f:
    lines = (f.readlines())

  #empty lists for time, x and y values
  t_arr = np.array([])
  x_arr = np.array([])
  y_arr = np.array([])

  def clean_number(s):
        if isinstance(s, str)==True:
          s = s.strip()
          s = s.replace('−', '-')  
          s = s.replace('–', '-')   
          s = s.replace('—', '-')   
          s = re.sub(r"[^\d\.\-Ee+]", "", s)
        return float(s)
 
  #skip header line and split by comma before setting correct numbers together to update list
  for line in lines[2:]:
      if config == "S":
        parts = line.strip().split(",")

        t = float(parts[0] + "." + parts[1])
        
        #If data is missing at some timesteps
        if len(parts)==4:
          x = math.nan
        elif len(parts)>4:
          x = parts[2] + "." + parts[3]
        
        if len(parts)==5:
          y = math.nan
        elif len(parts)==6:
          y = parts[4] + "." + parts[5]
      elif config == "C":
        parts = line.strip().split(",")
        t = float(parts[0])
        if parts[1] == "":
          x = math.nan
        else:
          x = parts[1]
        if parts[2] == "":
           y = math.nan
        else:
          y = parts[2] 
  
      #add values to arrays
      t_arr = np.append(t_arr, t)
      x_arr = np.append(x_arr, clean_number(x))
      y_arr = np.append(y_arr, clean_number(y))
  return t_arr, x_arr, y_arr

""" t, x_arr, y = readfile_motion("master_jenny_oystein/video_data/S_J_5_1.txt", "S")
y_values = y - np.nanmean(y)

plt.figure(figsize=(9, 6)) 
plt.plot(t, y_values)
plt.grid()
plt.title("Time series Single June 0.5 m/s", fontsize=16)
plt.xlabel("Time [s]")
plt.ylabel("Displacement [m]")
os.makedirs("Plots", exist_ok=True) 
filepath = os.path.join("Plots", "timeseries_example_S_J_5.png")
plt.savefig(filepath, dpi=300) """