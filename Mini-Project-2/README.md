# Mini Project 2: Finger Movement Analysis using ECoG Data
## Project Overview
This project analyzes ECoG (Electrocorticography) brain signals to understand neural activity associated with finger movements. Using provided datasets, the project calculates the average Event-Related Potentials (ERPs) for each finger movement, visualizes the results, and saves the generated plots.

---

## Directory Structure
```
MINI-PROJECT-2/

├── mini_project_2_data/                # Data folder containing the input datasets    
│   ├── brain_data_channel_one.csv      # Time series of ECoG data from a single electrode  
│   ├── events_file_ordered.csv         # Starting points, peak points, and finger IDs  
│   └── finger_data.csv                 # Additional data (not used directly in this script)  
├── plots/                              # Folder to store generated plots  
│   ├── average_erp_finger_1.png        # Plot of average ERP for Finger 1  
│   ├── average_erp_finger_2.png        # Plot of average ERP for Finger 2  
│   ├── average_erp_finger_3.png        # Plot of average ERP for Finger 3  
│   ├── average_erp_finger_4.png        # Plot of average ERP for Finger 4  
│   └── average_erp_finger_5.png        # Plot of average ERP for Finger 5  
├── main.py                             # Python script for processing and analysis  
└── README.md                           # Project documentation (this file)  
```

---

## Installation Instructions
To set up and run the project locally, follow these steps:

1. Clone the repository:
```
git clone https://github.com/hadasschiff/python-class-2025.git
cd MINI-PROJECT-2
``` 
2. Set up a virtual environment (recommended):
```
python -m venv venv
source venv/bin/activate        # On macOS/Linux
.\venv\Scripts\activate         # On Windows
```
3. Install required dependencies:
```
pip install pandas numpy matplotlib
```

## Usage
To run the analysis, execute the main.py script:
```
python main.py
```
This script will:
* Process the input datasets.
* Calculate average ERPs for each finger movement.
* Save the ERP plots in the plots/ directory.

---

## Features
* Data Cleaning: Ensures valid indices and data types for trial points.
* ERP Calculation: Extracts and averages 1201-point windows of ECoG data for each finger movement.
* Visualization: Generates time-series plots for ERPs, labeled by finger movement.

---

Contributors
* Hadas Schiff

If you have any questions or need help, feel free to reach out via:

Email: hadasharr@gmail.com