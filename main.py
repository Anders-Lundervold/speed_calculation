import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from virtual_timing_gates_funv1 import virtual_timing_gates_funv1

# Folder containing the TSV files
folder_path = r'C:\Users\anderslu\OneDrive - nih.no\Documents\Qualisys\PhD_course\Data\raw_data\FP01\fixed_speed'
output_folder = r'C:\Users\anderslu\OneDrive - nih.no\Documents\Qualisys\PhD_course\Data\raw_data\processed_data'
os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists

# Parameters
running_direction = 'y'  # According to the lab coordinate system
TIMING_GATE_1_pos = 1.7  # Position in meters of timing gate 1
TIMING_GATE_2_pos = -0.5  # Position in meters of timing gate 2
Target_speed = 3.5  # Target speed in m/s
Tolerance = 10  # Tolerance in percentage (+/-)
fs = 200  # Marker sampling frequency (e.g., 200 Hz)
plot_figure = 0  # Do not display plots

# Initialize a list to store results
results = []

# Loop through all TSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.tsv'):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {filename}")

        # Read the TSV file
        try:
            data = pd.read_csv(file_path, sep='\t', skiprows=11)  # Skip metadata rows
        except Exception as e:
            print(f"Error: Failed to read TSV file {filename}. {e}")
            continue

        # Extract SIPS_left and SIPS_right x, y, z columns
        try:
            left_x = data['SIPS_left X'].to_numpy() / 1000  # Convert to meters
            left_y = data['SIPS_left Y'].to_numpy() / 1000  # Convert to meters
            left_z = data['SIPS_left Z'].to_numpy() / 1000  # Convert to meters
            right_x = data['SIPS_right X'].to_numpy() / 1000  # Convert to meters
            right_y = data['SIPS_right Y'].to_numpy() / 1000  # Convert to meters
            right_z = data['SIPS_right Z'].to_numpy() / 1000  # Convert to meters
        except KeyError as e:
            print(f"Error: Missing column in TSV data {filename}. {e}")
            continue

        # Compute the midpoint between SIPS_left and SIPS_right
        mid_x = (left_x + right_x) / 2
        mid_y = (left_y + right_y) / 2
        mid_z = (left_z + right_z) / 2

        # Combine the midpoint coordinates into a single array
        marker_to_use = np.column_stack((mid_x, mid_y, mid_z))

        # Call the function
        try:
            mean_speed, is_valid = virtual_timing_gates_funv1(
                marker_to_use,
                running_direction,
                TIMING_GATE_1_pos,
                TIMING_GATE_2_pos,
                Target_speed,
                Tolerance,
                fs,
                plot_figure
            )
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            continue

        # Save the results
        results.append({'Filename': filename, 'Mean Speed (m/s)': mean_speed})

        # Save the velocity plot
        velocity_plot_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_velocity_plot.png")
        plt.savefig(velocity_plot_path)
        plt.close()

        # Create and save the 3D coordinate system plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(mid_x, mid_y, mid_z, label='Midpoint Trajectory')
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.legend()
        ax.set_title(f"3D Trajectory for {filename}")
        trajectory_plot_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_3d_trajectory.png")
        plt.savefig(trajectory_plot_path)
        plt.close()

# Save results to a CSV file
results_df = pd.DataFrame(results)
results_csv_path = os.path.join(output_folder, 'mean_speeds.csv')
results_df.to_csv(results_csv_path, index=False)
print(f"Results saved to {results_csv_path}")
