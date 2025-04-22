import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def bland_altman_plot(data1, data2, title, save_path):
    """
    Create a Bland-Altman plot to compare two measurement methods.
    
    Parameters:
    - data1: First measurement method (e.g., IR timing gates).
    - data2: Second measurement method (e.g., differential or distance-based speed).
    - title: Title of the plot.
    - save_path: Path to save the plot.
    """
    # Calculate the mean and difference between the two methods
    mean = np.mean([data1, data2], axis=0)
    diff = data1 - data2  # Difference between methods
    mean_diff = np.mean(diff)  # Mean of the differences
    std_diff = np.std(diff)  # Standard deviation of the differences

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.scatter(mean, diff, alpha=0.5, label='Differences')
    plt.axhline(mean_diff, color='red', linestyle='--', label=f'Mean Difference: {mean_diff:.2f}')
    plt.axhline(mean_diff + 1.96 * std_diff, color='blue', linestyle='--', label=f'+1.96 SD: {mean_diff + 1.96 * std_diff:.2f}')
    plt.axhline(mean_diff - 1.96 * std_diff, color='blue', linestyle='--', label=f'-1.96 SD: {mean_diff - 1.96 * std_diff:.2f}')
    plt.title(title)
    plt.ylabel('Difference Between Methods')
    plt.xlabel('measured speed (m/s)')
    plt.legend(loc='upper right', bbox_to_anchor=(1.33, 1))  # Move legend outside the graph on the upper right
    plt.grid()
    plt.tight_layout()

    # Save the plot
    plt.savefig(save_path)
    plt.close()
    print(f"Bland-Altman plot saved to {save_path}")

# Load the dataset
# Replace 'your_dataset.xlsx' with the path to your Excel file
data_path = r'c:\Users\anderslu\OneDrive - nih.no\Documents\Programmering\vscode\speed_calculation\results\speed_comparison_pref_speed_bland_altman.xlsx'
df = pd.read_excel(data_path)

# Extract the relevant columns
ir_timing_gates = df.iloc[:, 0]  # Column A: IR timing gates
differential_speed = df.iloc[:, 1]  # Column B: Differential-based speed
distance_speed = df.iloc[:, 2]  # Column C: Distance-based speed

# Create Bland-Altman plots
bland_altman_plot(
    ir_timing_gates,
    differential_speed,
    title="Fixed speed: IR Timing Gates vs Differential-Based Speed",
    save_path=r'c:\Users\anderslu\OneDrive - nih.no\Documents\Programmering\vscode\speed_calculation\results\bland_altman_diff_pref.png'
)

bland_altman_plot(
    ir_timing_gates,
    distance_speed,
    title="Fixed speed: IR Timing Gates vs Distance-Based Speed",
    save_path=r'c:\Users\anderslu\OneDrive - nih.no\Documents\Programmering\vscode\speed_calculation\results\bland_altman_dist_pref.png'
)