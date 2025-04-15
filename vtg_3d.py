import numpy as np
import matplotlib.pyplot as plt


def plot_3d(test_marker, running_direction, TIMING_GATE_1_pos, TIMING_GATE_2_pos, Target_speed, Tolerance, fs, plot_figure, save_path=None):
    """
    Function to calculate trajectory path and show virtual timing gates.
    """

    # Adjust the range to include 0.5 meters before the timing gates
    start_rec = TIMING_GATE_1_pos + 0.5  # Extend upper limit
    stop_rec = TIMING_GATE_2_pos - 0.5  # Extend lower limit

    # Filter the test_marker data to be within start_rec and stop_rec
    filtered_indices = np.where((test_marker[:, 1] >= stop_rec) & (test_marker[:, 1] <= start_rec))[0]
    if len(filtered_indices) == 0:
        raise ValueError("No data points found within the timing gate range.")
    test_marker = test_marker[filtered_indices]

    # Find indices within the range of the timing gates
    index_within_range = np.where((test_marker[:, 1] > TIMING_GATE_2_pos) & (test_marker[:, 1] < TIMING_GATE_1_pos))[0]
    if len(index_within_range) == 0:
        raise ValueError("No data points found within the timing gate range for plotting.")

    Pos_data = test_marker[index_within_range, 1]

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
    ax.set_xlabel('X-axis (m)')
    ax.set_ylabel('Y-axis (m)')
    ax.set_zlabel('Z-axis (m)')
    ax.set_title('3D Coordinate System with Timing Gates')
    ax.grid(True)

    # Rotate the figure by 90 degrees
    ax.view_init(elev=45, azim=45)  # Set elevation to 90 degrees and azimuth to 0 degrees

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

    # Scatter plot for test_marker points
    ax.scatter(test_marker[:, 0], test_marker[:, 1], test_marker[:, 2], c='k', marker='o')

    # Save the plot if a save path is provided
    if save_path:
        plt.savefig(save_path)
        print(f"3D plot saved to {save_path}")

    # Close the plot to free memory
    plt.close(fig)
