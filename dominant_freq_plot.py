import numpy as np
import matplotlib.pyplot as plt
import os

# Dominant frequency data
S_J = [0.65, 0.85, 1.84, 1.76, 4.41, 2.16, 5.7]
C_J = [0.59, 1.23, 1.93, 2.76, 3.84, 4.95, 5.18, 7.32]
S_W = [0.32, 0.37, 0.37, 0.49, 1.27, 1.68, 2.06]
C_W = [0.37, 0.64, 0.92, 1.28, 1.97, 1.21]
S_M = [0.65, 1.54, 0.84, 1.41, 4.25, 1.81, 5.33]
C_M = [1.13, 1.8, 2.29, 4.62, 5.24, 5.65, 7.72]
S_A = [1.18, 1.87, 2.86, 3.39, 3.85, 5.55, 6.57]
C_A = [1.13, 2.52, 2.75, 4.02, 5.49, 6.86]

S_J_second = [0.62, 0.73, 0.88, 1.73, 3.26, 3.85, 2.65]
S_M_second = [0.85, 0.8, 1.02, 1.31, 1.91, 4.96, 5.8]

S_J_highest = [0.65, 0.85, 1.84, 1.76, 4.41, 3.85, 5.7]
S_J_second_top = [3.26, 2.16, 2.65]

S_M_highest = [0.65, 1.54, 0.84, 1.41, 4.25, 4.96, 5.33]
S_M_second_top = [1.91, 1.81]

S_J_num = [1.15, 2.2, 3.05, 3.95, 4.9, 5.85, 6.79]
S_W_num = [0.4, 0.75, 0.65, 2.75, 3.55, 4.4, 5.25]
S_M_num = [0.85, 1.35, 2.4, 3.15, 4.25, 5.1, 7.04]
S_A_num = [0.7, 1.35, 3.55, 3.55, 4.8, 5.95, 6.99]

#Cauchy number data
S_A_Ca = [3.74e+02, 4.15e+03, 1.66e+04, 3.74e+04, 6.65e+04,
          1.04e+05, 1.50e+05, 2.04e+05, 2.66e+05, 3.37e+05]
#C_A_Ca = [5.81e+01, 6.46e+02, 2.58e+03, 5.81e+03, 1.03e+04,
#          1.61e+04, 2.32e+04, 3.16e+04, 4.13e+04, 5.23e+04]
S_M_Ca = [8.06e+02, 8.95e+03, 3.58e+04, 8.06e+04, 1.43e+05,
          2.24e+05, 3.22e+05, 4.39e+05, 5.73e+05, 7.25e+05]
#C_M_Ca = [1.25e+02, 1.39e+03, 5.57e+03, 1.25e+04, 2.23e+04,
#          3.48e+04, 5.01e+04, 6.82e+04, 8.90e+04, 1.13e+05]
S_J_Ca = [1.54e+03, 1.71e+04, 6.86e+04, 1.54e+05, 2.74e+05,
          4.29e+05, 6.17e+05, 8.40e+05, 1.10e+06, 1.39e+06]
#C_J_Ca = [2.40e+02, 2.66e+03, 1.07e+04, 2.40e+04, 4.26e+04,
#          6.66e+04, 9.59e+04, 1.31e+05, 1.71e+05, 2.16e+05]
S_W_Ca = [3.88e+02, 4.31e+03, 1.72e+04, 3.88e+04, 6.90e+04,
          1.08e+05, 1.55e+05, 2.11e+05, 2.76e+05, 3.49e+05]
#C_W_Ca = [6.03e+01, 6.70e+02, 2.68e+03, 6.03e+03, 1.07e+04,
#          1.68e+04, 2.41e+04, 3.28e+04, 4.29e+04, 5.43e+04]


C_A_Ca = [1.16e+02, 1.29e+03, 5.17e+03, 1.16e+04, 2.07e+04,
          3.23e+04, 4.65e+04, 6.33e+04, 8.26e+04, 1.05e+05]

C_M_Ca = [2.50e+02, 2.78e+03, 1.11e+04, 2.50e+04, 4.45e+04,
          6.96e+04, 1.00e+05, 1.36e+05, 1.78e+05, 2.25e+05]

C_J_Ca = [4.80e+02, 5.33e+03, 2.13e+04, 4.80e+04, 8.53e+04,
          1.33e+05, 1.92e+05, 2.61e+05, 3.41e+05, 4.32e+05]

C_W_Ca = [1.21e+02, 1.34e+03, 5.36e+03, 1.21e+04, 2.14e+04,
          3.35e+04, 4.82e+04, 6.57e+04, 8.58e+04, 1.09e+05]

u = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

#Spectrum comparison plots
""" #June
plt.figure(figsize=(10, 6))
plt.plot(u[1:], S_J, ".-", label="Single")
plt.plot(u, C_J, ".-", label="Cluster")
plt.grid()
plt.legend()
plt.title("Dominant Frequency June")
plt.xlabel("Current Velocity [m/s]")
plt.ylabel("Dominant Frequency [Hz]")

os.makedirs("Spectrums_comparison_filtered", exist_ok=True) 
filepath = os.path.join("Spectrums_comparison_filtered", "frequency_June_comparison.png")
plt.savefig(filepath, dpi=300)
plt.close()

#May
plt.figure(figsize=(10, 6))
plt.plot(u[1:], S_M, ".-", label="Single")
plt.plot(u[1:], C_M, ".-", label="Cluster")
plt.grid()
plt.legend()
plt.title("Dominant Frequency May")
plt.xlabel("Current Velocity [m/s]")
plt.ylabel("Dominant Frequency [Hz]")

filepath = os.path.join("Spectrums_comparison_filtered", "frequency_May_comparison.png")
plt.savefig(filepath, dpi=300)
plt.close()

#April
plt.figure(figsize=(10, 6))
plt.plot(u[1:], S_A, ".-", label="Single")
plt.plot(u[1:-1], C_A, ".-", label="Cluster")
plt.grid()
plt.legend()
plt.title("Dominant Frequency April")
plt.xlabel("Current Velocity [m/s]")
plt.ylabel("Dominant Frequency [Hz]")

filepath = os.path.join("Spectrums_comparison_filtered", "frequency_April_comparison.png")
plt.savefig(filepath, dpi=300)
plt.close()

#Wavy
plt.figure(figsize=(10, 6))
plt.plot(u[1:], S_W, ".-", label="Single")
plt.plot(u[2:], C_W, ".-", label="Cluster")
plt.grid()
plt.legend()
plt.title("Dominant Frequency Wavy")
plt.xlabel("Current Velocity [m/s]")
plt.ylabel("Dominant Frequency [Hz]")

filepath = os.path.join("Spectrums_comparison_filtered", "frequency_Wavy_comparison.png")
plt.savefig(filepath, dpi=300)
plt.close() """


config_list = ["S", "C"] 
model_list = ["A", "M", "J", "W"]

os.makedirs("Spectrums_comparison_Ca_Num", exist_ok=True) 


plt.figure(figsize=(8, 6))
plt.plot(S_W_Ca[3:], S_W, ".--", label="Experimental") 
#plt.plot(S_M_Ca[-3:-1], S_M_second_top, "D", label="Experiemntal second frequency top") 
plt.plot(S_W_Ca[3:], S_W_num, ".-", label="Numerical")    
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0)) 
plt.ylabel('Frequency (Hz)', fontsize=14) 
plt.xlabel('Ca', fontsize=14)
plt.legend()
plt.grid()

filepath = os.path.join("Spectrums_comparison_Ca_Num", "dominant frequency_S_W.png")
plt.savefig(filepath, dpi=300)
plt.close() 

