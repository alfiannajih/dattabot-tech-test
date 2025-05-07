from timeit import timeit

from optimized_case_1 import optimized_clean_customer_data
from original_script import clean_customer_data

from utils import generate_dummy_data_case_1

if __name__ == "__main__":
    df = generate_dummy_data_case_1(n_rows=1000)

    df1 = df.copy()
    df2 = df.copy()

    original_script_time = timeit(lambda: clean_customer_data(df1), number=1)
    optimized_script_time = timeit(lambda: optimized_clean_customer_data(df2), number=1)
    
    print(f"Time taken for original script: {original_script_time:.4f} seconds")
    print(f"Time taken for optimized script: {optimized_script_time:.4f} seconds")

    assert df1.equals(df2) == True