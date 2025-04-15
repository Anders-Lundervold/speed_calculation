import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from vtg_speed import v_t_g
from vtg_3d import plot_3d
from vtg_dist import v_t_g_dist

# Folder containing the TSV files
folder_path = r'C:\Users\anderslu\OneDrive - nih.no\Documents\Qualisys\PhD_course\Data\raw_data\FP02\pref_speed'
output_folder = r'C:\Users\anderslu\OneDrive - nih.no\Documents\Programmering\vscode\speed_calculation\raw_data\FP02\pref_speed'
os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists

# Parameters
running_direction = 'y'  # According to the lab coordinate system
TIMING_GATE_1_pos = 1.7  # Position in meters of timing gate 1
TIMING_GATE_2_pos = -0.5  # Position in meters of timing gate 2
Target_speed = 4.04  # Target speed in m/s
Tolerance = 10  # Tolerance in percentage (+/-)
fs = 200  # Marker sampling frequency (e.g., 200 Hz)
plot_figure = 0  # Do not display plots

# Initialize a list to store results
results = []

def process_file(file_path, filename):
    """
    Process a single TSV file to calculate mean speed and validate it.
    """
    try:
        # Read the TSV file
        data = pd.read_csv(file_path, sep='\t', skiprows=11)  # Skip metadata rows
    except Exception as e:
        print(f"Error: Failed to read TSV file {filename}. {e}")
        return None

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
        return None

    # Compute the midpoint between SIPS_left and SIPS_right
    mid_x = (left_x + right_x) / 2
    mid_y = (left_y + right_y) / 2
    mid_z = (left_z + right_z) / 2

    # Combine the midpoint coordinates into a single array
    marker_to_use = np.column_stack((mid_x, mid_y, mid_z))

    # Call the velocity-based speed calculation function
    try:
        mean_speed, is_valid = v_t_g(
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
        print(f"Error processing file {filename} with v_t_g: {e}")
        return None

    # Save the velocity plot
    velocity_plot_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_velocity_plot.png")
    plt.savefig(velocity_plot_path)  # Save the plot generated in v_t_g
    plt.close()

    # Call the distance-based speed calculation function
    try:
        dist_speed, dist_is_valid = v_t_g_dist(
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
        print(f"Error processing file {filename} with v_t_g_dist: {e}")
        return None

    # Save the distance-based speed plot
    dist_plot_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_distance_plot.png")
    plt.savefig(dist_plot_path)  # Save the plot generated in v_t_g_dist
    plt.close()

    return {
        'Filename': filename,
        'Mean Speed (m/s)': mean_speed,
        'Valid (Mean Speed)': is_valid,
        'Distance-Based Speed (m/s)': dist_speed,
        'Valid (Distance-Based Speed)': dist_is_valid
    }

# Loop through all TSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.tsv'):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {filename}")
        result = process_file(file_path, filename)
        if result:
            results.append(result)

# Save results to an Excel file
results_df = pd.DataFrame(results)

# Add additional columns for target speed, upper and lower bounds
results_df['Target Speed (m/s)'] = Target_speed
results_df['Lower Bound (m/s)'] = Target_speed * (1 - Tolerance / 100)
results_df['Upper Bound (m/s)'] = Target_speed * (1 + Tolerance / 100)

# Define the Excel file path
results_excel_path = os.path.join(output_folder, 'speed_comparison.xlsx')

# Save to Excel
results_df.to_excel(results_excel_path, index=False)
print(f"Results saved to {results_excel_path}")

# Generate a 3D plot for each processed file
for result in results:
    file_path = os.path.join(folder_path, result['Filename'])
    print(f"Generating 3D plot for: {result['Filename']}")
    try:
        # Reprocess the file to extract marker_to_use
        data = pd.read_csv(file_path, sep='\t', skiprows=11)
        if data.empty:
            print(f"Warning: File {result['Filename']} is empty. Skipping 3D plot generation.")
            continue
        left_x = data['SIPS_left X'].to_numpy() / 1000
        left_y = data['SIPS_left Y'].to_numpy() / 1000
        left_z = data['SIPS_left Z'].to_numpy() / 1000
        right_x = data['SIPS_right X'].to_numpy() / 1000
        right_y = data['SIPS_right Y'].to_numpy() / 1000
        right_z = data['SIPS_right Z'].to_numpy() / 1000
        mid_x = (left_x + right_x) / 2
        mid_y = (left_y + right_y) / 2
        mid_z = (left_z + right_z) / 2
        marker_to_use = np.column_stack((mid_x, mid_y, mid_z))

        # Generate and save the 3D plot
        plot_3d_path = os.path.join(output_folder, f"{os.path.splitext(result['Filename'])[0]}_3d_plot.png")
        plot_3d(
            marker_to_use,
            running_direction,
            TIMING_GATE_1_pos,
            TIMING_GATE_2_pos,
            Target_speed,
            Tolerance,
            fs,
            plot_figure,
            save_path=plot_3d_path
        )
        plt.close()
    except Exception as e:
        print(f"Error generating 3D plot for {result['Filename']}: {e}")

