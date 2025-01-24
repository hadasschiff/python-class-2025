import unittest
import pandas as pd
import os
from sklearn.metrics import precision_score, accuracy_score, recall_score
import sys
from src.data_analysis import load_and_prepare_data,check_normality, align_data, perform_t_tests,train_and_evaluate_decision_tree


class TestDataAnalysis(unittest.TestCase):
    def setUp(self):
        """
        Setting up the test environment. Creating a sample dataset and saving it to a temporary CSV file.
        """
        # Creating our sample dataset.
        self.sample_data = pd.DataFrame({
            'VideoID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            'SubjectID': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120],
            'predefinedlabel': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            'user-definedlabeln': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            'Theta': [100, 300, 500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300, 2500, 2700, 2900, 3100, 3300, 3500, 3700, 3900],
            'Alpha1': [50, 70, 90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330, 350, 370, 390, 410, 430]
        })
        # Saving it to a temporary file.
        self.test_file_path = "test_analysis_data.csv"
        self.sample_data.to_csv(self.test_file_path, index=False)

    def tearDown(self):
        """
        Cleaning up after the tests. Removing temporary files.
        """
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_load_and_prepare_data(self):
        """
        Testing the load_and_prepare_data function from data_analysis.py to ensure data is loaded and divided correctly.
        """
        data, not_confusing, confusing = load_and_prepare_data(self.test_file_path, 'predefinedlabel')

        # Checking the data is loaded correctly.
        self.assertEqual(len(data), len(self.sample_data))
        self.assertEqual(len(not_confusing), 10) 
        self.assertEqual(len(confusing), 10) 

        # Ensure all columns match
        self.assertEqual(list(data.columns), list(self.sample_data.columns))

    def test_check_normality(self):
        """
        Testing the check_normality function from data_analysis.py to ensure it correctly identifies normal columns.
        """
        eeg_data, not_confusing, confusing = load_and_prepare_data(self.test_file_path, 'predefinedlabel')

        # Checking normality excluding the non-numeric columns,
        normal_columns = check_normality(not_confusing,confusing,columns_to_exclude=['VideoID', 'SubjectID', 'predefinedlabel', 'user-definedlabeln'])

        # Verifying that it identifies normally distributed columns.
        self.assertIn('Theta', normal_columns)
        self.assertIn('Alpha1', normal_columns)

def test_align_data(self):
    """
    Testing the align_data function from data_analysis.py to ensure it aligns the datasets correctly.
    """
    eeg_data, not_confusing, confusing = load_and_prepare_data(self.test_file_path, 'predefinedlabel')

    # Align the data
    not_confusing_aligned, confusing_aligned = align_data(not_confusing, confusing)

    # Verify that the aligned datasets have the same shape.
    self.assertEqual(not_confusing_aligned.shape, confusing_aligned.shape)

    # Ensure the alignment preserves data integrity (no missing values or unexpected duplicates)
    self.assertFalse(not_confusing_aligned.isnull().values.any())
    self.assertFalse(confusing_aligned.isnull().values.any())

    # Ensure SubjectID alignment between the two datasets
    self.assertTrue((not_confusing_aligned['SubjectID'] == confusing_aligned['SubjectID']).all())


    def test_perform_t_tests(self):
        """
        Testing the perform_t_tests function from data_analysis.py to ensure it runs paired t-tests correctly.
        """
        eeg_data, not_confusing, confusing = load_and_prepare_data(self.test_file_path, 'predefinedlabel')

        # Align the data before running t-tests
        not_confusing_aligned, confusing_aligned = align_data(not_confusing, confusing)
        
        # Define normally distributed columns for testing.
        normal_columns = ['Theta', 'Alpha1']

        # Perform the t-tests.
        t_test_results = perform_t_tests(not_confusing_aligned, confusing_aligned, normal_columns)

        # Check to see if the results are generated for normal columns.
        self.assertIn('Theta', t_test_results)
        self.assertIn('Alpha1', t_test_results)

        # Verify the structure of the results.
        self.assertTrue('t_stat' in t_test_results['Theta'])
        self.assertTrue('p_value' in t_test_results['Theta'])

    def test_train_and_evaluate_decision_tree(self):
        """
        Testing the train_and_evaluate_decision_tree function from data_analysis.py to ensure the model is trained and evaluated correctly.
        """
        data, not_confusing, confusing = load_and_prepare_data(self.test_file_path, 'predefinedlabel')

        # Columns to exclude for training.
        columns_to_exclude = ['VideoID', 'SubjectID', 'predefinedlabel', 'user-definedlabeln']

        # Testing the decision tree model.
        try:
            train_and_evaluate_decision_tree(data, 'predefinedlabel', columns_to_exclude, n_experiments=10)
        except Exception as e:
            self.fail(f"Decision tree training and evaluation failed: {e}")

if __name__ == "__main__":
    # Add the project root directory to sys.path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    sys.path.append(project_root)

    unittest.main()