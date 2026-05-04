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

u = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

#June
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
plt.close()