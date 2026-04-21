import re
import numpy as np
import math

def readfile_motion(filename):
  #reads txt file with time, x and y values, returns lists

  #open txt file with time, x and y values
  with open(filename, encoding="utf-8") as f:
    lines = (f.readlines())

  #empty lists for time, x and y values
  t_arr = np.array([])
  x_arr = np.array([])
  y_arr = np.array([])

  #skip header line and split by comma before setting correct numbers together to update list
  for line in lines[2:]:
      parts = line.strip().split(",")

      t = float(parts[0] + "." + parts[1])
      #If data is missing at some timesteps
      if len(parts)==3:
        x = math.nan
      elif len(parts)==4:
        x = parts[2] + "." + parts[3]
      elif len(parts)==5:
         y = math.nan
      elif len(parts)==6:
        y = parts[4] + "." + parts[5]

      #fix encoding for x and y values
      x = x.replace('−', '-')
      x = re.sub(r"[^\d\.\-Ee+]", "", x)
      if len(parts)==6:
        y = y.replace('−', '-')
        y = re.sub(r"[^\d\.\-Ee+]", "", y)

      #add values to arrays
      t_arr = np.append(t_arr, t)
      x_arr = np.append(x_arr, float(x))
      y_arr = np.append(y_arr, float(y))
  return t_arr, x_arr, y_arr


