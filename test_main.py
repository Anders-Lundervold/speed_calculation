
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from virtual_timing_gates_funv1 import virtual_timing_gates_funv1

# Load marker data from the TSV file
file_path = r'C:\Users\anderslu\OneDrive - nih.no\Documents\Programmering\vscode\PhD_code\HFIMV9053\Running_FIX 1.tsv'

# Read the TSV file
try:
    data = pd.read_csv(file_path, sep='\t', skiprows=11)  # Skip metadata rows
except Exception as e:
    print(f"Error: Failed to read TSV file. {e}")
    exit()

# Read the TSV file
data = pd.read_csv(file_path, sep='\t', skiprows=11)

# Extract SIPS_left and SIPS_right x, y, z columns
left_x = data['SIPS_left X'].to_numpy()
left_y = data['SIPS_left Y'].to_numpy()
left_z = data['SIPS_left Z'].to_numpy()
right_x = data['SIPS_right X'].to_numpy()
right_y = data['SIPS_right Y'].to_numpy()
right_z = data['SIPS_right Z'].to_numpy()

# Compute the midpoint between SIPS_left and SIPS_right
mid_x = (left_x + right_x) / 2
mid_y = (left_y + right_y) / 2
mid_z = (left_z + right_z) / 2

# Combine the midpoint coordinates into a single array
marker_to_use = np.column_stack((mid_x, mid_y, mid_z))

# Plot the trajectories
plt.figure(figsize=(10, 6))
plt.plot(mid_y, mid_x, label='Midpoint Trajectory')
plt.axvline(x=1200, color='r', linestyle='--', label='Timing Gate 1')
plt.axvline(x=-1200, color='b', linestyle='--', label='Timing Gate 2')
plt.xlabel('Y Coordinate')
plt.ylabel('X Coordinate')
plt.title('Midpoint Trajectories with Timing Gates')
plt.legend()
plt.grid(True)
plt.show()

# Plot the distribution of y-coordinates
plt.figure(figsize=(10, 6))
plt.hist(mid_y, bins=50, alpha=0.75)
plt.axvline(x=1.2, color='r', linestyle='--', label='Timing Gate 1')
plt.axvline(x=-1.2, color='b', linestyle='--', label='Timing Gate 2')
plt.xlabel('Y Coordinate')
plt.ylabel('Frequency')
plt.title('Distribution of Y Coordinates')
plt.legend()
plt.grid(True)
plt.show()
