# first_name, last_name, age, country
from faker import Faker
import pandas as pd
from random import randint

import numpy as np
from random import random

def insert_noise_values(df, column, rate, add_unknown_and_random_str=False):
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
):
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

    for col in ['first_name', 'last_name', 'age', 'country']:
        insert_noise_values(df, col, noise_rate)

    for col in ['age', 'country']:
        insert_noise_values(df, col, noise_rate, add_unknown_and_random_str=True)

    return df


def generate_dummy_data_case_2(
    n_rows: int = 100000,
    noise_rate: float = 0.2
):
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

    for col in ['entry_time', 'exit_time', 'break_duration', 'department']:
        insert_noise_values(df, col, noise_rate)

    for col in ['entry_time', 'exit_time', 'break_duration', 'department']:
        insert_noise_values(df, col, noise_rate, add_unknown_and_random_str=True)

    return df