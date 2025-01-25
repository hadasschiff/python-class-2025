# Imports. 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def calc_mean_erp(trial_points, ecog_data):
    """
    Calculate the mean Event-Related Potentials (ERP) for finger movements from ecog data.

    Args:
        trial_points (str): Path to a CSV file containing information about finger movement events.    
        ecog_data (str): Path to a CSV file containing ecog data.

    Returns:
        fingers_erp_mean (np.ndarray): A 5x1201 matrix containing the averaged ERP signals per finger.

    """

    # Load trial points data and give the columns names.
    trial_points = pd.read_csv(trial_points, header=None, names=['starting_point', 'peak_point', 'finger_id'])
    # Ensure all values are ints
    trial_points = trial_points.astype(int) 

    # Load ecog data, assumong one columsm, and making a numpy array.
    ecog_data = pd.read_csv(ecog_data, header=None).iloc[:, 0].values

    # Initialize the matrix for finger epochs. 
    # 5 rows for fingers, 1201 columns for the signal window. 
    fingers_matrix = {1: [], 2: [], 3: [], 4: [], 5: []}
    
    # Extract epochs for each trial
    for _, row in trial_points.iterrows():
        # Get the starting point.
        start_idx = row['starting_point']
        # Get finger id.
        finger = row['finger_id']

        # Calculate epoch boundaries. 
        epoch_start = start_idx - 200
        epoch_end = start_idx + 1000 + 1 

        # Validate boundaries - exactly 1201.
        if epoch_start >= 0 and epoch_end <= len(ecog_data):
            epoch = ecog_data[epoch_start:epoch_end]
            # Adding the epoch to the fingers list.
            if len(epoch) == 1201:
                fingers_matrix[finger].append(epoch)

    # Calculate mean erp per finger.
    # Creating the matrix.
    fingers_erp_mean = np.zeros((5, 1201))
    # Going over all the fingers.
    for finger in range(1, 6):
        if fingers_matrix[finger]:
            fingers_erp_mean[finger-1] = np.mean(fingers_matrix[finger], axis=0)

    # Plot results.
    # Creating the figure.
    plt.figure(figsize=(12, 6))
    # Creating a time vector from -200 to 1000, with 1201 points.
    time = np.linspace(-200, 1000, 1201)
    colors = ['deepskyblue', 'seagreen', 'r', 'darkcyan', 'hotpink']

    # For each finger. 
    for i in range(5):
        # Plots the mean erp per finger.
        plt.plot(time, fingers_erp_mean[i], color=colors[i], label=f'Finger {i+1}')
        # Adding a line at t=0.
        plt.axvline(0, color='k', linestyle='--', label='Movement Onset')
        # Adding title.
        plt.title('Average Event-Related Potentials by Finger')
        plt.xlabel('Time from Movement Onset (ms)')
        plt.ylabel('ECoG Amplitude (μV)')
        plt.legend()
        plt.grid(True)

        # Save the plot to a folder
        output_folder = "./plots"
        # Create folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True) 
        plot_path = os.path.join(output_folder, f"average_erp_finger_{i+1}.png")
        plt.savefig(plot_path, dpi=300)
        plt.close() 
    
    return fingers_erp_mean

def main():
    # Paths to files 
    trial_points = "./mini_project_2_data/events_file_ordered.csv"
    ecog_data = "./mini_project_2_data/brain_data_channel_one.csv"
    fingers_erp_mean = calc_mean_erp(trial_points, ecog_data)
    return fingers_erp_mean

if __name__ == "__main__":
    results = main()