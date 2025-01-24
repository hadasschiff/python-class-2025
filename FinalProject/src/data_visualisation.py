import os
import matplotlib.pyplot as plt

# Plot histograms for each column
def plot_histograms(eeg_data, not_confusing, confusing, plot_dir, columns_to_exclude):
    """
    Plot histograms for all numeric columns in the dataset, comparing not_confusing and confusing groups.

    Args:
        eeg_data (DataFrame): Full EEG dataset.
        not_confusing (DataFrame): Group where label=0.
        confusing (DataFrame): Group where label=1.
        plot_dir (str): Directory to save histogram plots.
        columns_to_exclude (list): List of columns to exclude from histogram plots.

    """
    # Creating the directory for histograms if it doesn't exist
    os.makedirs(plot_dir, exist_ok=True)

    # We want to look only at the numeric columns, so we drop the columns we dont want, and make the othres in to a list.
    numeric_cols = eeg_data.drop(columns=columns_to_exclude, axis=1,errors='ignore').columns.to_list()
    # Our for loop goes throgh all remaing columns and creates plots for each group - Confusing vs not Confusing.
    # In the plots: the frequency of the values of the columns. 
    for col in numeric_cols:
        # Creating new figure for the plot. 
        plt.figure(figsize=(7, 5))
        # Histogram of the not confusing videos. 
        # We take the data ranging from 0 to 0.99 percentile to exlude extreme outliers. 
        plt.hist(not_confusing[col], alpha=0.5,range=(0,not_confusing[col].quantile(0.99)), label='Not Confusing Videos', bins=50)
        # The same Histogram for the confusing videos.
        plt.hist(confusing[col], alpha=0.5,range=(0,confusing[col].quantile(0.99)), label='Confusing Videos', bins=50)
        # Adding title.
        plt.title(f'Histogram of {col}')
        # Adding title for x-axis.
        plt.xlabel(col)
        # Adding title for y-axis.
        plt.ylabel('Frequency')
        # Adding a legend to explain the labels.
        plt.legend(loc='upper right')
        
        # Joins the whole path for the file to be saved.
        plt_path = os.path.join(plot_dir, f"histogram_{col}.png")
        # Saving the plot.
        plt.savefig(plt_path)
        print(f"Saved histogram for {col} to {plt_path}")
        plt.close()

# Showing the t-test results in a box plot.
def plot_boxplot(confusing_sorted, not_confusing_sorted, column, t_stat, p_value, plot_dir):
    """
    Plot a box plot comparing the distribution of a specific column in confusing and not_confusing groups.

    Args:
        confusing_sorted (DataFrame): Confusing group, sorted and aligned.
        not_confusing_sorted (DataFrame): Not confusing group, sorted and aligned.
        column (str): Column to compare.
        t_stat (float): T-statistic from the t-test.
        p_value (float): P-value from the t-test.
        plot_dir (str): Directory to save box plot.

    """
    # Creating the directory for box plots if it doesn't exist
    os.makedirs(plot_dir, exist_ok=True)

    # Creating new figure.
    plt.figure(figsize=(7, 5))
    # Creating box plot showing the distribution for each group.
    plt.boxplot([confusing_sorted[column], not_confusing_sorted[column]],labels=['Confusing Videos', 'Not Confusing Videos'])
    # Adding title.
    plt.title(f'Distribution of {column} Between Groups (t-stat={t_stat:.2f}, p={p_value:.3f})')
    # Adding title to y-axis.
    plt.ylabel('Theta')
    # Adding grid lines
    plt.grid(axis='y')
    
    # Joins the whole path for the file to be saved.
    plt_path = os.path.join(plot_dir, f"boxplot_{column}.png")
    # Saving the plot.
    plt.savefig(plt_path)
    print(f"Saved box plot for {column} to {plt_path}")
    plt.close()

# Showing the t-test results in a paired line plot.
def plot_paired_lines(confusing_sorted, not_confusing_sorted, column, t_stat, p_value, plot_dir):
    """
    Plot paired comparisons of a specific column between confusing and not_confusing groups.

    Args:
        confusing_sorted (DataFrame): Confusing group, sorted and aligned.
        not_confusing_sorted (DataFrame): Not confusing group, sorted and aligned.
        column (str): Column to compare.
        t_stat (float): T-statistic from the t-test.
        p_value (float): P-value from the t-test.
        plot_dir (str): Directory to save paired line plot.

    """

    # Creating the directory for paired line plots if it doesn't exist.
    os.makedirs(plot_dir, exist_ok=True)

    # Creating the figure.
    plt.figure(figsize=(10, 6))

    # Going over all the rows in the data set and draws a line connecting the same SubjectID watching the two types of videos.
    for i in range(len(confusing_sorted)):
        plt.plot(['Confusing Videos', 'Not Confusing Videos'],[confusing_sorted[column].iloc[i], not_confusing_sorted[column].iloc[i]],marker='o',color='gray',alpha=0.5)
    # Adding scatter points for both groups.
    plt.scatter(['Confusing Videos'] * len(confusing_sorted), confusing_sorted[column], color='blue', label='Confusing Videos', alpha=0.7, s=50)
    plt.scatter(['Not Confusing Videos'] * len(not_confusing_sorted), not_confusing_sorted[column], color='orange', label='Not Confusing Videos', alpha=0.7, s=50)
    # Adding title.
    plt.title(f'Paired Comparison of {column} Values\n(t-stat={t_stat:.2f}, p={p_value:.3e})', fontsize=14)
    # Adding label to y-axis.
    plt.ylabel(column, fontsize=12)
    # Chnaging font sizes.
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)
    # Adding grid line.
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # Add horizontal line for the average of each group.
    plt.axhline(y=confusing_sorted[column].mean(), color='blue', linestyle='--', alpha=0.7, label=f'Confusing Mean: {confusing_sorted[column].mean():.2f}')
    plt.axhline(y=not_confusing_sorted[column].mean(), color='orange', linestyle='--', alpha=0.7, label=f'Not Confusing Mean: {not_confusing_sorted[column].mean():.2f}')
    # Adding legend.
    plt.legend(fontsize=12)
    # Making sure all the elements fit into the figure.
    plt.tight_layout()
   
    # Joins the whole path for the file to be saved.
    plt_path = os.path.join(plot_dir, f"paired_lines_{column}.png")
    # Saving the plot.
    plt.savefig(plt_path)
    print(f"Saved paired line plot for {column} to {plt_path}")
    plt.close()