# Imports.
import pandas as pd
from scipy.stats import shapiro , ttest_rel
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score, accuracy_score, recall_score

# Load, preprocess, and divide data by column.
def load_and_prepare_data(file_path, label_col):
    """
    Load the dataset, and divide into two groups: 
    'confusing' and 'not confusing' based on a the specified column:
    predefined or user-defined label.

    Args:
        file_path (str): Path to the dataset file.
        label_col (str): Column name to divide the data by ('predefinedlabel' or 'user-definedlabeln').

    Returns:
        tuple: Full dataset, not_confusing dataset, confusing dataset
    """

    # Load clean data set.
    data = pd.read_csv(file_path)
    print("Data loaded successfully.")

    # Dividing the events based on their lables -
    # Confusing or not. 
    not_confusing = data[data[label_col] == 0]
    confusing = data[data[label_col] == 1]

    return data, not_confusing, confusing

# Now, to know what we can do with our data - we need to check normality.
def check_normality(not_confusing, confusing, columns_to_exclude):
    """
    Check for normality in both datasets and return columns with normal distributions in both.

    Args:
        not_confusing (DataFrame): dataset where label=0.
        confusing (DataFrame): dataset where label=1.
        columns_to_exclude (list): List of columns to exclude from normality check.

    Returns:
        normal_cols (list): Columns that are normally distributed in both datasets.
    """

    # Creating empty lists for the normal and not normal columns we find. 
    normal_confusing_columns = []
    normal_not_confusing_columns = []
    # Dropping all non - numeric columns, and converting the relevent ones to a list. 
    # Axis = 1 is to specify that the right columns should be dropped.
    numeric_cols = not_confusing.drop(columns=columns_to_exclude, axis=1, errors='ignore').columns.to_list()

    for col in numeric_cols:
        # Making sure there is enough data.
        if len(not_confusing[col]) < 3 or len(confusing[col]) < 3:
            print(f"Skipping column {col} due to insufficient data for normality test.")
            continue
        # Perform Shapiro-Wilk test on each column to determine normality for not confusing dataset.
        stat, p = shapiro(not_confusing[col])
        # If data is normaly distributed: 
        if p > 0.05:
            # Adding the normal columns from the not confusing videos to the list.
            normal_not_confusing_columns.append(col)

        # Perform Shapiro-Wilk test on each column to determine normality for confusing dataset.
        stat, p = shapiro(confusing[col])
        # If data is normaly distributed: 
        if p > 0.05:
            # Adding the normal columns from the confusing videos to the list.
            normal_confusing_columns.append(col)

    # To know what data we can analyze - we need to know what data from each of the datasets is normal.
    # We convert both lists to sets and then find the common columns between the two.
    normal_cols = list(set(normal_not_confusing_columns).intersection(normal_confusing_columns))
    print(f"Normal columns in both datasets: {normal_cols}")
    return normal_cols

# Align data.
def align_data(not_confusing, confusing):
    """
    Align the data to make sure its prepared for the paired t-test.
    Making sure both data sets - confused and not confused are the same shape. 

    Args:
        not_confusing (DataFrame): dataset where label=0.
        confusing (DataFrame): dataset where label=1.
    
    Returns:
        not_confusing_sorted (DataFrame): dataset where label=0, sorted to be the same shape as the confused dataset.
        confusing_sorted (DataFrame): dataset where label=1 , sorted to be the same shape as the not confused dataset.
    """

    # We need to make sure the data is arranged right for the test. 
    # If they dont have the same shape - we need to align them.
    #pd.options.mode.chained_assignment = None  # Turn off the SettingWithCopyWarning
    if not_confusing.shape != confusing.shape:
        print("Shapes are not aligned. Adjusting the datasets")
        # By the results we see the shapes are not the same - 
        # There is a different number of videos classified as confusing vs. not confusing. 
        # We will drop the rows we dont need.
        # How will we decide? 
        # We want each Student to have the same number of videos they found confusing and not confusing. 
        # We can check how many each of them have in every dataset and by that drop the rows.
        # Copying the datasets to work on.
        not_confusing = not_confusing.copy()
        confusing = confusing.copy() 
        # Adding within-group sequence numbers to both data sets.
        not_confusing['_seq'] = not_confusing.groupby('SubjectID').cumcount()
        confusing['_seq'] = confusing.groupby('SubjectID').cumcount()
        # Makes a merge of SubjectID and sequence numbers to find common pairs.
        common_pairs = pd.merge(not_confusing[['SubjectID', '_seq']],confusing[['SubjectID', '_seq']],on=['SubjectID', '_seq'],how='inner')
        # Kepping only the rows that were in common_pairs, and dropping the 'seq' column.
        not_confusing = not_confusing.merge(common_pairs, on=['SubjectID', '_seq']).drop('_seq', axis=1)
        confusing = confusing.merge(common_pairs, on=['SubjectID', '_seq']).drop('_seq', axis=1)
        if len(not_confusing) == 0 or len(confusing) == 0:
            raise ValueError("Aligned datasets have no samples left after adjustment.")
        # Verify alignment
        print(f"Aligned shapes: Confusing - {confusing.shape}, Not Confusing - {not_confusing.shape}")
    
    # Sorting the videos by SubjectID, reseting the index and droping the old one.
    not_confusing_sorted = not_confusing.sort_values(by='SubjectID').reset_index(drop=True)
    confusing_sorted = confusing.sort_values(by='SubjectID').reset_index(drop=True)
    return (not_confusing_sorted,confusing_sorted)

# Perform paired t-tests
def perform_t_tests(not_confusing, confusing, normal_cols):
    """
    Perform paired t-tests on the specified columns.
    We want to do a paired t test - because we have the same students watching both types of videos. 

    Args:
        not_confusing (DataFrame): dataset where label=0.
        confusing (DataFrame): dataset where label=1.
        normal_cols (list): Columns to perform t-tests on.
    
    Returns:
        t_test_results (dict): A dictionary containing t-statistics and p-values for each column.
    """

    
    # Dictionary to store t-test results
    t_test_results = {}
    # Perform the paired t-test.
    # Comparing the mean of the two groups under different conditions. 
    for col in normal_cols:
        t_stat, p_value = ttest_rel(confusing[col],not_confusing[col])
        # Display results.
        print(f"T-test for {col}: t-statistic={t_stat:.4f}, p-value={p_value:.4f}")

        # Setting the significance level.
        alpha = 0.05 
        # Interpret the results.
        if p_value < alpha:
            print(f"The difference in '{col}' is statistically significant (p < 0.05).")
        else:
            print(f"The difference in '{col}' is not statistically significant (p >= 0.05).")
        # Store results in the dictionary.
        t_test_results[col] = {"t_stat": t_stat, "p_value": p_value}
    return t_test_results

# Train and evaluate decision tree model.
def train_and_evaluate_decision_tree(data, target_col, columns_to_exclude, n_experiments=1000):
    """
    Train and evaluate a decision tree model for classification using cross-validation.

    Args:
        data (DataFrame): Full clean dataset.
        target_col (str): Name of the target column for classification.
        columns_to_exclude (list): Columns to exclude from training features.
        n_experiments (int): Number of experiments for cross-validation.
    """

    # Counts for accuracy, precision and recall.
    acc, prec, recall = 0, 0, 0
    # We will do 1000 experiments to ensure accuracy.
    for exp in range(n_experiments):
        # Splitting the data into a training set, and testing set. 
        # Dropping columns not needed for prediction.
        # The data is split 75% for training, and 25% for testing.
        train_x, test_x, train_y, test_y = train_test_split(data.drop(columns=columns_to_exclude + [target_col],axis=1, errors = 'ignore'), data[target_col], test_size=0.25)
        # Creating the decision tree model.
        model = DecisionTreeClassifier()
        # Training the model on the training data, with the right labels.
        model.fit(train_x,train_y)
        # Generating the prediction for the tarining data.
        # model_pred_train = model.predict(train_x)
        # Generating the prediction for the test data.
        preds = model.predict(test_x)

        # The % of correctly predicted samples.
        acc += accuracy_score(test_y,preds)
        # The % of the true positives predictions out of all the positive predictions.
        prec += precision_score(test_y,preds, zero_division=0)
        # The % of true positive predictions out all of the positives overall.
        recall += recall_score(test_y,preds, zero_division=0)

    # Overall results: 
    # The average percent of accracy.
    # How often did the model make correct predictions.
    print(f"Average Accuracy: {acc / n_experiments:.4f}")
    # The average percent of precision.
    # How often was there a true positive from all positive predictions.
    print(f"Average Precision: {prec / n_experiments:.4f}")
    # The average percent of recall.
    # How often was there a true positive from all the positive instinces.
    print(f"Average Recall: {recall / n_experiments:.4f}")