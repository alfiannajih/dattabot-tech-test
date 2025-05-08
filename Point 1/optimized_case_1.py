import pandas as pd

KNOWN_COUNTRIES = ["US", "UK", "ID", "SG"]

def clean_customer_name(name: str) -> str:
    if pd.isna(name):
        return "Unknown"
    
    return name


def clean_customer_age(age: int) -> int:
    if pd.isna(age) or str(age).strip().lower() == "unknown":
        return -1
    
    try:
        return int(age)
    except:
        return -1


def is_customer_adult(age: int) -> bool:
    return age >= 18


def clean_customer_country(country: str) -> str:
    if country not in KNOWN_COUNTRIES or country is None:
        return  "XX"

    return country


def optimized_clean_customer_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and enriches customer data by standardizing names, validating age, 
    determining adulthood, and formatting country information.

    Steps performed:
    1. Cleans 'first_name' and 'last_name' using `clean_customer_name` and combines them into 'full_name'.
    2. Cleans the 'age' column using `clean_customer_age` and stores the result in 'cleaned_age'.
    3. Determines whether the customer is an adult using `is_customer_adult` and stores the result in 'is_adult'.
    4. Cleans the 'country' column to generate a standardized 'country_code' using `clean_customer_country`.

    Parameters:
        df (pd.DataFrame): A DataFrame with columns 'first_name', 'last_name', 'age', and 'country'.

    Returns:
        pd.DataFrame: The updated DataFrame with new columns:
                      'full_name', 'cleaned_age', 'is_adult', and 'country_code'.
    """
    df["full_name"] = df["first_name"].apply(clean_customer_name) + " " + df["last_name"].apply(clean_customer_name)
    df["cleaned_age"] = df["age"].apply(clean_customer_age)
    df["is_adult"] = df["cleaned_age"].apply(is_customer_adult)
    df["country_code"] = df["country"].apply(clean_customer_country)

    return df