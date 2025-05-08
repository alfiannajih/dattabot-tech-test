from faker import Faker
import pandas as pd
from random import randint, random, sample
from datetime import datetime
import numpy as np

def insert_noise_values(
    df: pd.DataFrame,
    column: list,
    rate: float,
    add_unknown_and_random_str: bool = False
) -> None:
    mask = np.random.rand(len(df)) < rate
    if add_unknown_and_random_str:
        prob = random()
        if prob < 0.5:
            df.loc[mask, column] = "Unknown"
        else:
            df.loc[mask, column] = "cfasew"
    else:
        df.loc[mask, column] = None


def generate_dummy_data_case_1(
    n_rows: int = 100000,
    noise_rate: float = 0.2
) -> pd.DataFrame:
    # Generate dummy data
    faker = Faker()
    countries = [
        "US", "UK", "ID", "SG", "MA",
        "TO", "GH", "IS", "ER", "BB"
    ]

    dummy_data = []

    for i in range(n_rows):
        name = faker.name().split()
        first_name, last_name = name[0], name[-1]
        age = randint(10, 60)
        country = countries[randint(0, 9)]

        dummy_data.append({
            "first_name": first_name,
            "last_name": last_name,
            "age": str(age),
            "country": country
        })

    df = pd.DataFrame(dummy_data)

    # Add noisy data
    for col in ['first_name', 'last_name', 'age', 'country']:
        insert_noise_values(df, col, noise_rate)

    for col in ['age', 'country']:
        insert_noise_values(df, col, noise_rate, add_unknown_and_random_str=True)

    return df


def generate_dummy_data_case_2(
    n_rows: int = 100000,
    noise_rate: float = 0.2
) -> pd.DataFrame:
    # Generate dummy data
    possible_departments = [
        "Sales", "Logistics", "Data", "Marketing", "Accounting",
        "Finance", "IT", "Product" 
    ]

    dummy_data = []
    for i in range(n_rows):
        dummy_data.append({
            "entry_time": f"{randint(8, 10):02}:{randint(0, 59):02}:{randint(0, 59):02}",
            "exit_time": f"{randint(16, 18):02}:{randint(0, 59):02}:{randint(0, 59):02}",
            "break_duration": f"{randint(30, 90)}",
            "department": possible_departments[randint(0, 7)]
        })

    df = pd.DataFrame(dummy_data)

    # Add noisy data
    for col in ['entry_time', 'exit_time', 'break_duration', 'department']:
        insert_noise_values(df, col, noise_rate)

    for col in ['entry_time', 'exit_time', 'break_duration', 'department']:
        insert_noise_values(df, col, noise_rate, add_unknown_and_random_str=True)

    return df


def generate_dummy_data_case_3(
    n_rows: int = 100000,
    noise_rate: float = 0.2
) -> pd.DataFrame:
    # Generate dummy data
    start_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
    end_date = datetime.strptime("2025-01-01", "%Y-%m-%d")

    faker = Faker()

    faker.random_element()
    possible_products = [
        "Television", "Refrigerator", "Handphone", "Camera", "Parfume",
        "Skin Care", "Keyboard", "Mouse", "Books", "Smart Watch"
    ]
    sales_reps = [faker.name() for i in range(6000)]

    dummy_data = []
    for i in range(n_rows):
        dummy_data.append({
            "sales_amount": f"USD {random()*randint(100, 2500)}",
            "sale_date": faker.date_between(start_date, end_date).strftime("%Y-%m-%d"),
            "sales_rep": sample(sales_reps, 1)[0],
            "products_sold": ", ".join(sample(possible_products, randint(1, 7))),
            "discount_applied": "Yes" if random() > 0.5 else "No"
        })

    df = pd.DataFrame(dummy_data)
    
    # Add noisy data
    for col in ["sale_date", "discount_applied"]:
        insert_noise_values(df, col, noise_rate)

    for col in ["sale_date", "discount_applied"]:
        insert_noise_values(df, col, noise_rate, add_unknown_and_random_str=True)

    return df