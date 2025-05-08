# Data Processing Optimization Benchmark
This directory benchmarks the performance of optimized data preprocessing scripts against their original counterparts across three different data cases:

* **Case 1: Customer Data Cleaning**

* **Case 2: Employee Time Entries Preprocessing**

* **Case 3: Sales Data Preprocessing**

Each test **compares the runtime** of the original script vs. the optimized script on a **dummy data that consist of 100,000**.

# Project Structure
```bash
Point 1/
├── .gitignore              # List of ignored files in git repo
├── dummy_data_case_1.csv   # Dummy data for case 1
├── dummy_data_case_2.csv   # Dummy data for case 2
├── dummy_data_case_3.csv   # Dummy data for case 3
├── experiment.ipynb        # Notebook for developing optmized scripts
├── main.py                 # Script to run the benchmark
├── opimized_case_1.py      # Optimized customer data cleaning
├── opimized_case_2.py      # Optimized time entries preprocessing
├── opimized_case_3.py      # Optimized sales data preprocessing
├── original_script.py      # Original scripts for all three cases
├── README.md               # Documentation
├── requirements.txt        # Library required to run the project
├── utils.py                # Helper function
```

# How to Run
1. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
2. Run the `main.py` script
    ```bash
    python main.py
    ```

# Example Output
```
======================================
RUNNING SCRIPT FOR CASE 1: CUSTOMER DATA
Time taken for original script: 4.3625 seconds
Time taken for optimized script: 0.2105 seconds
END OF SCRIPT FOR CASE 1: CUSTOMER DATA
======================================
RUNNING SCRIPT FOR CASE 2: TIME ENTRIES DATA
Time taken for original script: 6.9253 seconds
Time taken for optimized script: 0.9419 seconds
END OF SCRIPT FOR CASE 2: TIME ENTRIES DATA
======================================
RUNNING SCRIPT FOR CASE 3: SALES DATA
Time taken for original script: 1.2667 seconds
Time taken for optimized script: 0.9782 seconds
END OF SCRIPT FOR CASE 3: SALES DATA
======================================
```
The optimized scripts **demonstrate significant improvements** in execution time across all cases.