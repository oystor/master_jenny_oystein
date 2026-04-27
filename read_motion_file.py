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
      parts = line.strip().split(",")

      t = float(parts[0] + "." + parts[1])
      
      #If data is missing at some timesteps
      if len(parts)==3:
        x = math.nan
      elif len(parts)>=4:
        x = parts[2] + "." + parts[3]
      
      if len(parts)==5:
        y = math.nan
      elif len(parts)==6:
        y = parts[4] + "." + parts[5]
     
      #add values to arrays
      t_arr = np.append(t_arr, t)
      x_arr = np.append(x_arr, clean_number(x))
      y_arr = np.append(y_arr, clean_number(y))
  return t_arr, x_arr, y_arr


#print(readfile_motion("C:/Users/jenny/OneDrive - NTNU/Master/Video/S_J_3_1.txt")[0])
