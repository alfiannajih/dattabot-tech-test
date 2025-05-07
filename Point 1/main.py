from timeit import timeit

from optimized_case_1 import optimized_clean_customer_data
from optimized_case_2 import optimized_preprocess_time_entries
from original_script import clean_customer_data, preprocess_time_entries

from utils import generate_dummy_data_case_1, generate_dummy_data_case_2

def test_case_1():
    print("RUNNING SCRIPT FOR CASE 1: CUSTOMER DATA")
    df = generate_dummy_data_case_1(n_rows=1000)

    df1 = df.copy()
    df2 = df.copy()

    original_script_time = timeit(lambda: clean_customer_data(df1), number=1)
    optimized_script_time = timeit(lambda: optimized_clean_customer_data(df2), number=1)
    
    print(f"Time taken for original script: {original_script_time:.4f} seconds")
    print(f"Time taken for optimized script: {optimized_script_time:.4f} seconds")

    assert df1.equals(df2) == True

    print("END OF SCRIPT FOR CASE 1: CUSTOMER DATA")


def test_case_2():
    print("RUNNING SCRIPT FOR CASE 2: TIME ENTRIES DATA")
    df = generate_dummy_data_case_2(n_rows=1000)

    df1 = df.copy()
    df2 = df.copy()

    original_script_time = timeit(lambda: preprocess_time_entries(df1), number=1)
    optimized_script_time = timeit(lambda: optimized_preprocess_time_entries(df2), number=1)
    
    print(f"Time taken for original script: {original_script_time:.4f} seconds")
    print(f"Time taken for optimized script: {optimized_script_time:.4f} seconds")

    assert df1.equals(df2) == True

    print("END OF SCRIPT FOR CASE 2: TIME ENTRIES DATA")


if __name__ == "__main__":
    test_case_1()
    print("==================================")
    test_case_2()