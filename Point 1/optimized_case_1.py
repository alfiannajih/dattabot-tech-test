import pandas as pd

KNOWN_COUNTRIES = ["US", "UK", "ID", "SG"]

def clean_customer_name(name: str):
    if pd.isna(name):
        return "Unknown"
    
    return name

def clean_customer_age(age: int):
    if pd.isna(age) or str(age).strip().lower() == "unknown":
        return -1
    
    try:
        return int(age)
    except:
        return -1

def is_customer_adult(age: int):
    return age >= 18

def clean_customer_country(country: str):
    if country not in KNOWN_COUNTRIES or country is None:
        return  "XX"

    return country

def optimized_clean_customer_data(df: pd.DataFrame):
    df["full_name"] = df["first_name"].apply(clean_customer_name) + " " + df["last_name"].apply(clean_customer_name)
    df["cleaned_age"] = df["age"].apply(clean_customer_age)
    df["is_adult"] = df["cleaned_age"].apply(is_customer_adult)
    df["country_code"] = df["country"].apply(clean_customer_country)

    return df