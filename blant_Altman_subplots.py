import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def bland_altman_subplot(data1, data2, ax, title, y_limits=None):
    """
    Create a Bland-Altman plot on a given subplot axis.
    
    Parameters:
    - data1: First measurement method (e.g., IR timing gates).
    - data2: Second measurement method (e.g., differential or distance-based speed).
    - ax: Matplotlib axis to plot on.
    - title: Title of the subplot.
    - y_limits: Tuple specifying the y-axis limits (min, max).
    """
    # Calculate the mean and difference between the two methods
    mean = np.mean([data1, data2], axis=0)
    diff = data1 - data2  # Difference between methods
    mean_diff = np.mean(diff)  # Mean of the differences
    std_diff = np.std(diff)  # Standard deviation of the differences

    # Create the Bland-Altman plot
    ax.scatter(mean, diff, alpha=0.5, label='Differences')
    ax.axhline(mean_diff, color='lime', linestyle='--', label=f'Mean Difference')
    ax.axhline(mean_diff + 1.96 * std_diff, color='blue', linestyle='--', label=f'+1.96 SD')
    ax.axhline(mean_diff - 1.96 * std_diff, color='blue', linestyle='--', label=f'-1.96 SD')
    ax.axhline(0, color='black', linestyle='-', linewidth=2.5)  # Solid black line at 0
    ax.set_title(title)
    ax.grid(axis='y')

    # Set y-axis limits if provided
    if y_limits:
        ax.set_ylim(y_limits)

# Load the dataset
data_path = r'c:\Users\anderslu\OneDrive - nih.no\Documents\Programmering\vscode\speed_calculation\results\speed_comparison_pref_speed_bland_altman.xlsx'
df = pd.read_excel(data_path)

# Extract the relevant columns
ir_timing_gates = df.iloc[:, 0]  # Column A: IR timing gates
differential_speed = df.iloc[:, 1]  # Column B: Differential-based speed
distance_speed = df.iloc[:, 2]  # Column C: Distance-based speed

# Define fixed y-axis limits
y_limits = (-0.2, 0.2)

# Create a 2:1 subplot
fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 1 row, 2 columns

# Plot IR Timing Gates vs Differential-Based Speed
bland_altman_subplot(
    ir_timing_gates,
    differential_speed,
    ax=axes[0],
    title="IR Timing Gates vs Differential-Based Speed",
    y_limits=y_limits
)

# Plot IR Timing Gates vs Distance-Based Speed
bland_altman_subplot(
    ir_timing_gates,
    distance_speed,
    ax=axes[1],
    title="IR Timing Gates vs Distance-Based Speed",
    y_limits=y_limits
)

# Add shared labels
fig.text(0.5, 0.04, 'Measured Speed (m/s)', ha='center', fontsize=12)  # Shared x-axis label
fig.text(0.04, 0.5, 'Difference Between Methods (m/s)', va='center', rotation='vertical', fontsize=12)  # Shared y-axis label

# Add a single legend
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right', fontsize=10)

# Adjust layout and save the figure
plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])  # Adjust layout to add more space around the graph
save_path = r'c:\Users\anderslu\OneDrive - nih.no\Documents\Programmering\vscode\speed_calculation\results\bland_altman_combined_pref.png'
plt.savefig(save_path)
plt.close()
print(f"Bland-Altman combined plot saved to {save_path}")