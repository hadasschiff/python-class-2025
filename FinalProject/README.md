# FinalProject: EEG Signal Analysis for Confusion Detection
**A study on brainwave patterns to differentiate confusion in educational videos.**

## Project Purpose
This project investigates whether differences exist in EEG signals (brain waves) of students when they watched confusing vs. non-confusing videos.
We also explored the discrepancies between:
* Videos classified as confusing by predefined criteria.
* Videos self-reported as confusing by the students.

### Hypothesis
This project aims to analyze EEG signals to detect patterns associated with cognitive confusion during educational video viewing. We hypothesize that:

* Distinct EEG Patterns for Confusion: When a participant experiences confusion, specific brainwave frequencies will show distinguishable changes compared to neutral comprehension states.
* Predefined vs. Self-Reported Confusion: Videos labeled as “confusing” by design will induce EEG activity similar to self-reported confusion, validating the approach.

### Key Finding
We observed a stronger difference in brain waves patterns when students self-identified videos as confusing compared to predefined classifications.
Detailed results and visualizations are stored in the `plots/` directory.

---
## Dataset
The EEG dataset used in this project consists of recordings from participants watching educational videos. The dataset includes:

- EEG Signal Data: Raw and preprocessed EEG recordings from 10 participants.
- Confusion Annotations: Labels from predefined confusing videos and self-reported confusion instances.
- Metadata: Participant details (age, background) and video timestamps for confusion markers. We did not use this data in our research.  
📂 Access the Dataset: https://www.kaggle.com/datasets/wanghaohan/confused-eeg

---
## Project Structure
The repository is organized as follows:

```
FinalProject/
 ├── plots/                        # Generated plots from analysis 
 ├── src/                          # Source code 
 │  ├── init.py                    # Module initialization 
 │  ├── data_analysis.py           # Performs EEG data analysis 
 │  ├── data_cleaning.py           # Cleans raw EEG data 
 │  └── data_visualisation.py      # Visualizes EEG data insights 
 ├── test/                         # Test suite 
 │  ├── init.py                    # Module initialization for testing 
 │  ├── test_analysis.py           # Tests for data analysis 
 │  └── test_cleaning.py           # Tests for data cleaning 
 ├── clean_eeg_data.csv            # Cleaned EEG dataset 
 ├── EEG_data.csv                  # Raw EEG dataset 
 ├── main.py                       # Entry point for running the project 
 ├── pyproject.toml                # Project dependencies and configuration 
 ├── my_project.code-workspace     # VSCode workspace configuration 
 └── README.md                     # Project documentation (this file)
```
---

## Installation Instructions
To set up and run the project locally:
1. Clone the repository:
```
git clone https://github.com/hadasschiff/python-class-2025.git
cd FinalProject
```
2. Create and activate a virtual environment (recommended):
``` 
python -m venv venv
source .venv/bin/activate        # On macOS/Linux
.venv\Scripts\activate           # On Windows
```
3. Install dependencies:
`pip install -e .`
4. Install additional development dependencies (optional):
`pip install -r requirements-dev.txt`

## Usage Instructions
To run the project, execute the main.py script:
`python main.py`

---

## Features:
* Data Cleaning: Processes raw EEG data to a structured format.
* Analysis: Compares EEG signals under different conditions.
* Visualization: Generates histograms and paired plots for analysis results.

### Outputs:
After running main.py, you will see:  
1.Generated Plots: View saved plots in the plots/ directory to visualize results (e.g., histograms, box plots).  
2.Console Output: The script will print t-test results, decision tree accuracy, precision, and recall.

---

## Testsing
Run the tests using pytest:  
1.Install testing dependencies (if not already installed):
`pip install pytest pytest-cov`  
2.Execute tests:
`pytest test/`

---

## Contributors
* Hadas Schiff
* Yotam Netser 

If you have any questions or need help, feel free to reach out via:  
Email: hadasharr@gmail.com  
 yotamn2000@gmail.com  