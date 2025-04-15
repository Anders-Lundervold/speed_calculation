import numpy as np
import matplotlib.pyplot as plt


def v_t_g(test_marker, running_direction, TIMING_GATE_1_pos, TIMING_GATE_2_pos, Target_speed, Tolerance, fs, plot_figure):
    """
    Function to calculate mean speed and validate based on timing gates.
    """

    # Adjust the range to include 0.5 meters before the timing gates
    start_rec = TIMING_GATE_1_pos + 0.5  # Extend upper limit
    stop_rec = TIMING_GATE_2_pos - 0.5  # Extend lower limit

    # Filter the test_marker data to be within start_rec and stop_rec
    filtered_indices = np.where((test_marker[:, 1] >= stop_rec) & (test_marker[:, 1] <= start_rec))[0]
    test_marker = test_marker[filtered_indices]

    if plot_figure == 1:
        # Plot a 3D coordinate system
        origin = [0, 0, 0]
        x_axis = [1, 0, 0]
        y_axis = [0, 1, 0]
        z_axis = [0, 0, 1]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.quiver(*origin, *x_axis, color='r', linewidth=2)
        ax.quiver(*origin, *y_axis, color='g', linewidth=2)
        ax.quiver(*origin, *z_axis, color='b', linewidth=2)

        ax.text(1, 0, 0, 'X', color='r', fontsize=12)
        ax.text(0, 1, 0, 'Y', color='g', fontsize=12)
        ax.text(0, 0, 1, 'Z', color='b', fontsize=12)
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Z-axis')
        ax.set_title('3D Coordinate System')
        ax.grid(True)
        ax.view_init(elev=0, azim=90)


        # Plot Timing Gate 1 as a plane
        x = np.linspace(-0.5, 1.5, 10)
        z = np.linspace(0, 2, 10)
        X, Z = np.meshgrid(x, z)
        Y1 = np.full_like(X, TIMING_GATE_1_pos)
        ax.plot_surface(X, Y1, Z, alpha=0.5, color='gray', edgecolor='none')
        ax.text(0, TIMING_GATE_1_pos, 2.5, 'Timing Gate 1', horizontalalignment='center', fontsize=8)

        # Plot Timing Gate 2 as a plane
        Y2 = np.full_like(X, TIMING_GATE_2_pos)
        ax.plot_surface(X, Y2, Z, alpha=0.5, color='gray', edgecolor='none')
        ax.text(0, TIMING_GATE_2_pos, 2.5, 'Timing Gate 2', horizontalalignment='center', fontsize=8)

        # Find indices within the range of the timing gates
        index_within_range = np.where((test_marker[:, 1] > TIMING_GATE_2_pos) & (test_marker[:, 1] < TIMING_GATE_1_pos))[0]
        Pos_data = test_marker[index_within_range, 1]

        # Scatter plot for test_marker points
        ax.scatter(test_marker[:, 0], test_marker[:, 1], test_marker[:, 2], c='k', marker='o')
        plt.show()

    # Handle empty index_within_range
    if len(index_within_range) == 0:
        raise ValueError("No data points found within the timing gate range.")

    # Calculate velocity
    velocity = np.diff(Pos_data) * fs
    velocity = np.append(velocity, velocity[-1])  # Match size of velocity to position vector

    if plot_figure == 1:
        plt.figure()
        plt.plot(velocity, linewidth=2, color='g')
        plt.axhline(np.mean(velocity), color='b', linestyle='--')
        plt.text(len(velocity) / 2, np.mean(velocity), f"{np.mean(velocity):.2f}")
        plt.title(f"{np.mean(velocity):.2f} m/s")
        plt.axhline(Target_speed * (1 - Tolerance / 100), color='r', linewidth=2)
        plt.text(len(velocity) / 2, Target_speed * (1 - Tolerance / 100), 'Lower boundary')
        plt.axhline(Target_speed * (1 + Tolerance / 100), color='r', linewidth=2)
        plt.text(len(velocity) / 2, Target_speed * (1 + Tolerance / 100), 'Upper boundary')
        plt.box(False)
        plt.ylabel('Velocity [m/s]')
        plt.xlabel('# Frames')
        plt.show(block=False)  # Non-blocking
        plt.close()  # Automatically close the plot

    # Validate speed
    mean_speed = np.abs(np.mean(velocity))  # Ensure mean speed is always positive
    is_valid = Target_speed * (1 - Tolerance / 100) <= mean_speed <= Target_speed * (1 + Tolerance / 100)

    # Plot validation result
    if plot_figure == 1:
        plt.figure()
        plt.axhline(mean_speed, color='blue', linewidth=3, label='Mean Speed')
        plt.axhline(Target_speed * (1 - Tolerance / 100), color='r', linestyle='--', label='Lower Tolerance')
        plt.axhline(Target_speed * (1 + Tolerance / 100), color='r', linestyle='--', label='Upper Tolerance')
        plt.axhline(Target_speed, color='lime', linestyle='--', label='Target Speed')
        plt.title(f"Mean Speed: {mean_speed:.2f} m/s {'(Valid)' if is_valid else '(Invalid)'}")
        plt.ylabel('Speed [m/s]')
        plt.legend()
        plt.show()

    return mean_speed, is_valid
