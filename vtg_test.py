import numpy as np
import matplotlib.pyplot as plt

def virtual_timing_gates_funv1(test_marker, running_direction, TIMING_GATE_1_pos, TIMING_GATE_2_pos, Target_speed, Tolerance, fs, plot_figure):
    """
    Function to calculate mean speed and validate based on timing gates.
    """

    # Adjust the range to include 0.5 meters before Timing Gate 1 and 0.5 meters after Timing Gate 2
    adjusted_gate_1_pos = TIMING_GATE_1_pos + 0.5  # Extend upper limit
    adjusted_gate_2_pos = TIMING_GATE_2_pos - 0.5  # Extend lower limit

    # Filter the data to only include points within the adjusted timing gates
    if running_direction == 'y':
        index_within_range = np.where((test_marker[:, 1] > adjusted_gate_2_pos) & (test_marker[:, 1] < adjusted_gate_1_pos))[0]
        if len(index_within_range) == 0:
            raise ValueError("No data points found within the timing gate range.")
        Pos_data = test_marker[index_within_range, 1]
    elif running_direction == 'x':
        index_within_range = np.where((test_marker[:, 0] > adjusted_gate_2_pos) & (test_marker[:, 0] < adjusted_gate_1_pos))[0]
        if len(index_within_range) == 0:
            raise ValueError("No data points found within the timing gate range.")
        Pos_data = test_marker[index_within_range, 0]
    else:
        raise ValueError("Invalid running direction. Use 'x' or 'y'.")

    # Calculate velocity
    velocity = np.diff(Pos_data) * fs
    velocity = np.append(velocity, velocity[-1])  # Match size of velocity to position vector

    # Calculate mean speed and bounds
    mean_speed = np.abs(np.mean(velocity))  # Ensure mean speed is always positive
    lower_bound = Target_speed * (1 - Tolerance / 100)
    upper_bound = Target_speed * (1 + Tolerance / 100)

    # Plot velocity profile with mean speed and bounds
    if plot_figure == 1:
        plt.figure(figsize=(10, 6))
        plt.plot(velocity, label='Velocity', linewidth=2, color='g')
        plt.axhline(mean_speed, color='b', linestyle='--', label=f'Mean Speed: {mean_speed:.2f} m/s')
        plt.axhline(lower_bound, color='r', linestyle='-', label=f'Lower Bound: {lower_bound:.2f} m/s')
        plt.axhline(upper_bound, color='r', linestyle='-', label=f'Upper Bound: {upper_bound:.2f} m/s')
        plt.title('Velocity Profile with Mean Speed and Bounds')
        plt.xlabel('Frame Index')
        plt.ylabel('Velocity (m/s)')
        plt.legend()
        plt.grid()
        plt.show(block=False)
        plt.close()

    # Validate speed
    is_valid = lower_bound <= mean_speed <= upper_bound
    return mean_speed, is_valid