# README for `main.py`

## Overview

This script, `main.py`, is part of a university project designed to analyze motion capture data and calculate running speed using two distinct methods: **numerical differentiation** and **virtual timing gates**. The script processes 3D marker trajectory data, validates the calculated speeds against a target speed, and generates visualizations and summary outputs for evaluation.

---

## Features

1. **Speed Calculation**:
   - **Numerical Differentiation**: Calculates speed based on instantaneous velocity derived from positional data.
   - **Virtual Timing Gates**: Calculates speed based on the time taken to traverse a fixed distance between two predefined positions.

2. **Validation**:
   - Compares calculated speeds to a target speed with a specified tolerance range.

3. **Outputs**:
   - Saves results to an Excel file for comparison and further analysis.
   - Generates 2D plots for both speed calculation methods.
   - Creates 3D trajectory visualizations with timing gates.

---

## Input Data

The script processes `.tsv` files containing 3D marker trajectory data. Each file must include the following columns:
- `SIPS_left X`, `SIPS_left Y`, `SIPS_left Z`: Coordinates of the left posterior superior iliac spine (SIPS) marker.
- `SIPS_right X`, `SIPS_right Y`, `SIPS_right Z`: Coordinates of the right posterior superior iliac spine (SIPS) marker.

---

## How the Script Works

1. **File Processing**:
   - The script loops through all `.tsv` files in the specified input folder.
   - For each file, it extracts the midpoint trajectory of the left and right SIPS markers.

2. **Speed Calculation**:
   - **Numerical Differentiation**: Calculates the mean speed based on velocity derived from positional changes.
   - **Virtual Timing Gates**: Calculates the average speed based on the time taken to traverse the distance between two timing gates.

3. **Validation**:
   - Both methods validate the calculated speeds against a target speed (e.g., 4.5 m/s) with a tolerance (e.g., ±10%).

4. **Output**:
   - Results are saved to an Excel file (`speed_comparison.xlsx`) with the following columns:
     - `Filename`: Name of the processed file.
     - `Mean Speed (m/s)`: Speed calculated using numerical differentiation.
     - `Valid (Mean Speed)`: Whether the mean speed is within the target range.
     - `Distance-Based Speed (m/s)`: Speed calculated using virtual timing gates.
     - `Valid (Distance-Based Speed)`: Whether the distance-based speed is within the target range.
     - `Target Speed (m/s)`, `Lower Bound (m/s)`, `Upper Bound (m/s)`: Validation parameters.

5. **Visualization**:
   - Saves 2D plots for both speed calculation methods.
   - Generates 3D trajectory plots showing the subject's movement through the timing gates.

6. **3D Plot Generation**:
   - For each processed file, the script generates a 3D plot of the subject's trajectory.
   - The midpoint trajectory is visualized in a 3D coordinate system with labeled axes.
   - Timing gates are represented as semi-transparent planes at predefined positions.

---

## Parameters

The following parameters can be adjusted in the script:

- **`folder_path`**: Path to the folder containing the `.tsv` files.
- **`output_folder`**: Path to the folder where results and plots will be saved.
- **`running_direction`**: Direction of movement (`'x'` or `'y'`).
- **`TIMING_GATE_1_pos`**: Position of Timing Gate 1 (e.g., 1.7 m).
- **`TIMING_GATE_2_pos`**: Position of Timing Gate 2 (e.g., -0.5 m).
- **`Target_speed`**: Target speed for validation (e.g., 4.5 m/s).
- **`Tolerance`**: Tolerance for validation in percentage (e.g., 10%).
- **`fs`**: Sampling frequency of the motion capture data (e.g., 200 Hz).
- **`plot_figure`**: Set to `1` to display plots during execution, or `0` to suppress them.

---

## Outputs

1. **Excel File**:
   - `speed_comparison.xlsx`: Contains calculated speeds, validation results, and target speed parameters.

2. **Plots**:
   - 2D plots for velocity-based and distance-based speed calculations.
   - 3D trajectory plots showing the subject's movement through the timing gates.

3. **Log Messages**:
   - The script prints progress and error messages to the console for each processed file.

---

## How to Run

1. Place the `.tsv` files in the folder specified by `folder_path`.
2. Adjust the parameters in the script as needed.
3. Run the script using Python:
   ```bash
   python main.py
