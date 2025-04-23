import numpy as np
import matplotlib.pyplot as plt

def v_t_g_dist(test_marker, running_direction, TIMING_GATE_1_pos, TIMING_GATE_2_pos, Target_speed, Tolerance, fs, plot_figure):
    """
    Function to calculate mean speed and validate based on distance based methods.
    """

    # Adjust the range to include 0.5 meters before Timing Gate 1 and 0.5 meters after Timing Gate 2
    start_rec = TIMING_GATE_1_pos + 0.5  # Extend upper limit
    stop_rec = TIMING_GATE_2_pos - 0.5  # Extend lower limit

    # Filter the test_marker data to be within start_rec and stop_rec
    filtered_indices = np.where((test_marker[:, 1] >= stop_rec) & (test_marker[:, 1] <= start_rec))[0]
    if len(filtered_indices) == 0:
        raise ValueError("No data points found within the timing gate range.")
    test_marker = test_marker[filtered_indices]

    # Extract position data for the running direction
    if running_direction == 'y':
        Pos_data = test_marker[:, 1]
    elif running_direction == 'x':
        Pos_data = test_marker[:, 0]
    else:
        raise ValueError("Invalid running direction. Use 'x' or 'y'.")

    # Find the first and last indices within the timing gates
    index_within_range = np.where((Pos_data > TIMING_GATE_2_pos) & (Pos_data < TIMING_GATE_1_pos))[0]
    if len(index_within_range) == 0:
        raise ValueError("No data points found within the timing gate range for speed calculation.")

    # Calculate the time between the timing gates
    start_index = index_within_range[0]
    end_index = index_within_range[-1]
    time_between_gates = (end_index - start_index) / fs  # Time in seconds

    # Calculate the distance between the timing gates
    distance_between_gates = TIMING_GATE_1_pos - TIMING_GATE_2_pos  # Distance in meters

    # Calculate speed
    speed = distance_between_gates / time_between_gates

    # Define bounds for validation
    lower_bound = Target_speed * (1 - Tolerance / 100)
    upper_bound = Target_speed * (1 + Tolerance / 100)

    # Always generate the plot
    plt.figure(figsize=(10, 6))
    plt.axhline(speed, color='b', linewidth=2.5, label=f'Calculated Speed')
    plt.axhline(Target_speed, color='g', linestyle=':', label=f'Target Speed')
    plt.axhline(lower_bound, color='r', linestyle='--', label=f'Lower Bound')
    plt.axhline(upper_bound, color='r', linestyle='--', label=f'Upper Bound')
    plt.title(f'Speed: {speed:.2f} m/s - Valid: {"Yes" if lower_bound <= speed <= upper_bound else "No"}')
    plt.xlabel('Time (s)')
    plt.ylabel('Speed (m/s)')
    plt.legend()
    plt.grid()

    # Show the plot only if plot_figure is set to 1
    if plot_figure == 1:
        plt.show(block=False)
        plt.close()

    # Validate speed
    is_valid = lower_bound <= speed <= upper_bound
    return speed, is_valid