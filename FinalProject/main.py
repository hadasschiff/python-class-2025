from src.data_cleaning import load_and_check_data, clean_and_save_data
from src.data_analysis import load_and_prepare_data, check_normality, align_data, perform_t_tests, train_and_evaluate_decision_tree
from src.data_visualisation import plot_histograms, plot_boxplot, plot_paired_lines

def main():
    file_path = "./EEG_data.csv"
    output_file_path = "./Clean_EEG_Data.csv"
    # Loading the data and checking for missing and duplicate values.
    eeg_data = load_and_check_data(file_path)
    # Cleaning the data, displaying its overview, counting events, and saving it.
    clean_and_save_data(eeg_data, output_file_path)

    clean_file_path = "./clean_eeg_data.csv"
    
    # Pre-defined labels.
    print("\n--- Analyzing by Predefined Labels ---")
    # Load and divide data by pre-defined labels.
    print("\n Loading and Dividing Data ")
    eeg_data, not_confusing_predefined, confusing_predefined = load_and_prepare_data(clean_file_path, label_col='predefinedlabel')
    print("\n Visualizing Predefined Labels")
    plot_histograms(eeg_data, not_confusing_predefined, confusing_predefined, plot_dir="./plots/predefined/histograms", columns_to_exclude=['VideoID', 'SubjectID', 'predefinedlabel', 'user-definedlabeln', 'level_0', 'index'])
    # Checking normality for predefined labels - to see what colums we can analyse.
    print("\n Checking normality for predefined labels")
    predefined_normal_columns = check_normality(not_confusing_predefined, confusing_predefined, columns_to_exclude=['VideoID', 'SubjectID', 'predefinedlabel', 'user-definedlabeln', 'level_0', 'index'])
    # Aligning data - both datasets to be the same shape
    print("\n Aligning data in preperation for t-test")
    not_confusing_predefined,confusing_predefined = align_data(not_confusing_predefined,confusing_predefined)
    # Running paired t-tests for predefined labels. 
    print("\n Performing paired t-tests for predefined labels")
    predefined_t_test_results = perform_t_tests(not_confusing_predefined, confusing_predefined, predefined_normal_columns)
    # Visualisation of the results. 
    print("\n Visualizations for predefined labels")
    for column in predefined_normal_columns:
        t_stat = predefined_t_test_results[column]["t_stat"]
        p_value = predefined_t_test_results[column]["p_value"]
        # Box plot. 
        plot_boxplot(confusing_predefined, not_confusing_predefined, column=column, t_stat=t_stat, p_value=p_value, plot_dir="./plots/predefined/boxplots")
        # Paired line plot for each column.
        plot_paired_lines(confusing_predefined, not_confusing_predefined, column=column, t_stat=t_stat, p_value=p_value, plot_dir="./plots/predefined/paired_lines")
    # Train and evaluate decision tree model for predefined labels.
    print("\n Training and evaluating decision tree for predefined labels")
    train_and_evaluate_decision_tree(eeg_data, target_col='predefinedlabel',columns_to_exclude=['VideoID', 'SubjectID', 'index', 'user-definedlabeln', 'level_0'])

    # User-defined labels.
    print("\n--- Analyzing by User-Defined Labels ---")
    # Load and divide data by user-defined labels.
    print("\nLoading and Dividing Data ")
    eeg_data, not_confusing_user, confusing_user = load_and_prepare_data(clean_file_path, label_col='user-definedlabeln')
    print("\n Visualizing User-Defined Labels")
    plot_histograms(eeg_data, not_confusing_user, confusing_user, plot_dir="./plots/user_defined/histograms", columns_to_exclude=['VideoID', 'SubjectID', 'predefinedlabel', 'user-definedlabeln', 'level_0', 'index'])
    # Checking normality for user-defined labels - to see what colums we can analyze.
    print("\n Checking normality for user-defined labels")
    user_normal_columns = check_normality(not_confusing_user,confusing_user,columns_to_exclude=['VideoID', 'SubjectID', 'predefinedlabel', 'user-definedlabeln', 'level_0', 'index'])
    # Aligning data - both datasets to be the same shape.
    print("\n Aligning data in preperation for t-test")
    not_confusing_user,confusing_user = align_data(not_confusing_user,confusing_user)
    # Running paired t-tests for user-defined labels. 
    print("\n Performing paired t-tests for user-defined labels")
    user_t_test_results = perform_t_tests(not_confusing_user, confusing_user, user_normal_columns)
    # Visualisation of the results. 
    print("\n Visualizations for user defined labels")
    for column in user_normal_columns:
        t_stat = user_t_test_results[column]["t_stat"]
        p_value = user_t_test_results[column]["p_value"]
        # Box plot. 
        plot_boxplot(confusing_user, not_confusing_user, column=column, t_stat=t_stat, p_value=p_value, plot_dir="./plots/user_defined/boxplots")
        # Paired line plot for each column.
        plot_paired_lines(confusing_user, not_confusing_user, column=column, t_stat=t_stat, p_value=p_value, plot_dir="./plots/user_defined/paired_lines")
    # Train and evaluate decision tree model for user-defined labels.
    print("\n Training and evaluating decision tree for user-defined labels")
    train_and_evaluate_decision_tree(eeg_data, target_col='user-definedlabeln',columns_to_exclude=['VideoID', 'SubjectID', 'index', 'predefinedlabel', 'level_0'])

    print("\n--- Analysis Complete ---")

if __name__ == "__main__":
    main()