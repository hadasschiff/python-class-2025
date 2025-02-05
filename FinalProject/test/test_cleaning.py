import unittest
import pandas as pd
import os
import sys
from src.data_cleaning import load_and_check_data, clean_and_save_data

class test_data_cleaning(unittest.TestCase):

    def setUp(self):
        """
        Setting up the test environment. Creating a sample dataset and saving it to a temporary CSV file.
        """
        # Creating a sample dataset with a selection of columns.
        self.sample_data = pd.DataFrame({'VideoID': [1, 1, 2, 2, 3, 3],'SubjectID': [101, 101, 102, 102, 103, 103],'predefinedlabel': [0, 0, 1, 1, 0, 0],'user-definedlabeln': [1, 1, 0, 0, 1, 1],'Theta': [100, 200, 300, 400, 500, 600],'Alpha1': [50, 60, 70, 80, 90, 100]})

        # Saving it to a temporary file
        self.test_file_path = "test_eeg_data.csv"
        self.output_file_path = "test_cleaned_eeg_data.csv"
        self.sample_data.to_csv(self.test_file_path, index=False)

    def tearDown(self):
        """
        Cleaning up after the tests. Removing the temporary files.
        """
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        if os.path.exists(self.output_file_path):
            os.remove(self.output_file_path)

    def test_load_and_check_data(self):
        """
        Testing the load_and_check_data function from data_cleaning.py to ensure it loads the data correctly and identifies missing and duplicate rows.
        """
        # Calling the function.
        loaded_data = load_and_check_data(self.test_file_path)

        # Ensuring the data is loaded correctly.
        self.assertEqual(len(loaded_data), len(self.sample_data))
        self.assertEqual(list(loaded_data.columns), list(self.sample_data.columns))

        # Checking that there are no missing or duplicate rows.
        self.assertEqual(loaded_data.isnull().sum().sum(), 0) 
        self.assertEqual(loaded_data.duplicated().sum(), 0) 

    def test_clean_and_save_data(self):
        """
        Testing the clean_and_save_data function from data_cleaning.py to ensure it cleans, groups, and saves the data correctly.
        """
        # Loading the sample data.
        loaded_data = pd.read_csv(self.test_file_path)

        # Calling the function
        cleaned_data = clean_and_save_data(loaded_data, self.output_file_path)

        # Checking the cleaned data is grouped correctly.
        expected_rows = len(loaded_data.groupby(['VideoID', 'SubjectID', 'predefinedlabel', 'user-definedlabeln']))
        self.assertEqual(len(cleaned_data), expected_rows)

        # Checking the cleaned data is saved correctly.
        self.assertTrue(os.path.exists(self.output_file_path))

        # Loading the saved file and checking its contents.
        saved_data = pd.read_csv(self.output_file_path)
        pd.testing.assert_frame_equal(cleaned_data, saved_data)

        # Makinfg sure numerical columns are averaged.
        grouped = loaded_data.groupby(['VideoID', 'SubjectID', 'predefinedlabel', 'user-definedlabeln']).mean().reset_index()
        pd.testing.assert_frame_equal(cleaned_data, grouped)

if __name__ == "__main__":
    # Add the project root directory to sys.path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    sys.path.append(project_root)
    unittest.main()