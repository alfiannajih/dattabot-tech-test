# first_name, last_name, age, country
from faker import Faker
import pandas as pd
from random import randint

import numpy as np
from random import random

# Function to randomly insert None
def insert_missing_values(df, column, rate, add_unknown_and_random_str=False):
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
        insert_missing_values(df, col, noise_rate)

    for col in ['age', 'country']:
        insert_missing_values(df, col, noise_rate)

    return df