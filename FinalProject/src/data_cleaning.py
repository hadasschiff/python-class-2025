import pandas as pd
def load_and_check_data(file_path):
    """
    Loads the EEG data from a CSV file, displays an overview, and checks for missing and duplicate rows.
    Returns the loaded DataFrame.

    Args:
        file_path (str): The file path to the CSV file containing the EEG data.

    Returns:
        eeg_data (DataFrame): The loaded DataFrame containing the EEG data.
    """
    # Load the data
    eeg_data = pd.read_csv(file_path)
    print("Data loaded successfully.")
    # Display the first few rows to ensure data was loaded correctly. 
    print("First few rows of the dataset:")
    print(eeg_data.head())

    # Check for missing values in any of the columns.
    missing_values = eeg_data.isnull().sum()
    if missing_values.sum() == 0:
        print("No missing values found in the dataset.")
    else:
        print("Missing values per column:")
        print(missing_values[missing_values > 0])

    # Check for duplicate rows
    duplicates = eeg_data[eeg_data.duplicated()]
    if duplicates.empty:
        print("No duplicate rows found.")
    else:
        print("Duplicate rows:")
        print(duplicates)

    return eeg_data

def clean_and_save_data(data, output_file_path):
    """
    Groups the clean data according to the events - by their 'VideoID', 'SubjectID', 'predefinedlabel', 'user-definedlabeln'.  cleans the data by calculating their numerical columns by the average.
    displays an overview of the cleaned data, counts events,
    and saves the cleaned data to a CSV file.

    Args:
        data (DataFrame): The DataFrame containing the raw EEG data.
        output_file_path (str): The file path where the cleaned data should be saved.

    Returns:
        clean_data (DataFrame): The cleaned DataFrame, grouped by events.
    """

    # Group and clean the data
    clean_data = data.groupby(['VideoID', 'SubjectID', 'predefinedlabel', 'user-definedlabeln']).mean().reset_index()
    print("Data grouped and cleaned.")

    # Display the first few rows of the grouped and cleaned data.
    print("First few rows of the cleaned data:")
    print(clean_data.head())

    # Checking how many events (rows) we have.
    # We should have 100 - 10 students watching 10 videos.
    print(f"Number of events (rows) in the cleaned data: {clean_data.shape[0]}")
    # The output confirms we have 100 events.

    # Saving the data for futre analysing
    clean_data.to_csv(output_file_path, index=False)
    print(f"--- Cleaned data saved to {output_file_path}. ---")

    return clean_data