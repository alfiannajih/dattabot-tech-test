import pandas as pd
import numpy as np
from datetime import datetime
import argparse
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Date, MetaData, CHAR
from sqlalchemy.dialects.postgresql import insert

from utils import gender_map, edu_map, province_map, age_to_birthdate, clean_phone_number

REFERENCE_DATE = datetime.today()

def extract(excel_path: str) -> pd.DataFrame:
    """
    Extracts data from all sheets in the given Excel file.

    Args:
        excel_path (str): Path to the Excel file.

    Returns:
        pd.DataFrame: Combined DataFrame containing data from all sheets.
    """
    print(f"[INFO] Extracting data from '{excel_path}'...")
    xl = pd.ExcelFile(excel_path)

    df = []
    for sheet_name in xl.sheet_names:
        df.append(xl.parse(sheet_name))

    df = pd.concat(df)
    df = df.reset_index(drop=True)

    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and transforms the raw employee data.

    Operations performed:
        - Removes duplicate employee IDs.
        - Maps categorical values (gender, education, province).
        - Converts age to birth date.
        - Converts score to numeric.
        - Cleans phone numbers.
        - Converts first day of employment to datetime.
        - Renames columns to standardized format.

    Args:
        df (pd.DataFrame): Raw employee data.

    Returns:
        pd.DataFrame: Transformed employee data.
    """
    print("[INFO] Transforming data...")
    # Drop duplicates employee id
    df = df.drop_duplicates("Employee_ID")

    # Transform gender column
    df["GENDER"] = df["GENDER"].map(lambda x: gender_map.get(x, "Others"))

    # Transform education column
    df["EDU_LVL"] = df["EDU_LVL"].map(lambda x: edu_map.get(x, "Others"))

    # Transform age column
    df["birth_date"] = df["AGE"].apply(lambda x: age_to_birthdate(x, REFERENCE_DATE))
    df.drop(columns="AGE", inplace=True)

    # Transform age column
    df["Score"] = pd.to_numeric(df["Score"], "coerce")

    # Transform phone number column
    df["Phone Number"] = df["Phone Number"].apply(clean_phone_number)

    # Transform domicile province
    df["Domicile_Province"] = df["Domicile_Province"].map(lambda x: province_map.get(x, "Others"))

    # Transform first day employment
    df["First_Day_Employment"] = pd.to_datetime(df["First_Day_Employment"], format="mixed", errors="coerce")

    # Rename columns:
    df = df.rename({
        "Employee_ID": "employee_id",
        "Name": "name",
        "GENDER": "gender",
        "EDU_LVL": "education_level",
        "JOB_CATEGORY": "job_category",
        "Score": "score",
        "Phone Number": "phone_number",
        "Domicile_Province": "domicile_province",
        "First_Day_Employment": "first_day_employement"
    }, axis=1)
    df = df.replace({np.nan: None})

    return df


def load(df: pd.DataFrame) -> None:
    """
    Loads the transformed employee data into a PostgreSQL database.

    Creates the `employees` table if it does not exist, then inserts rows
    with conflict handling on employee_id.

    Args:
        df (pd.DataFrame): Transformed employee data to load into the database.
    
    Returns:
        None.
    """
    print("[INFO] Loading data into database...")
    # Create SQLAlchemy engine (adjust credentials as needed)
    engine = create_engine("postgresql+psycopg2://dattabot:dattabot@localhost:5432/data_warehouse")

    # Define metadata and table
    metadata = MetaData()

    employees = Table(
        'employees', metadata,
        Column('employee_id', Integer, primary_key=True),
        Column('name', String),
        Column('gender', CHAR),
        Column('education_level', String),
        Column('job_category', String),
        Column('score', Float),
        Column('phone_number', String),
        Column('domicile_province', String),
        Column('first_day_employement', Date),
        Column('birth_date', Date),
    )

    # Create the table if not exists
    metadata.create_all(engine)

    # Convert all NaN/NA to None
    records = df.to_dict(orient='records')

    stmt = insert(employees).values(records).on_conflict_do_nothing(index_elements=['employee_id'])

    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel_path")

    args = parser.parse_args()

    print("[INFO] Starting ETL process...")
    df = extract(args.excel_path)
    df = transform(df)
    load(df)
    print("[INFO] ETL process completed successfully.")