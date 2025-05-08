import pandas as pd
from typing import Union

def calculate_work_duration(
    entry_time: pd.Series,
    exit_time: pd.Series,
    break_duration: pd.Series
) -> pd.Timedelta:
    total_seconds = (exit_time - entry_time).dt.seconds - (break_duration * 60)
    work_duration = pd.to_timedelta(total_seconds, unit="s")

    return work_duration
    
    
def label_work_duration(total_hours: Union[int, str]) -> str:
    if pd.isna(total_hours):
        return "Invalid Entry"
    
    else:
        if total_hours < 5:
            return 'Short Day'
        elif total_hours >= 8:
            return 'Long Day'
        else:
            return 'Regular Day'


def clean_deparment(department: str) -> str:
    if pd.notna(department) and department.strip() != "":
        return department
    else:
        return "Unknown"
    
    
def optimized_preprocess_time_entries(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses a DataFrame of employee time entries by computing and labeling work durations,
    and cleaning the department information.

    Steps performed:
    1. Parses 'entry_time' and 'exit_time' as datetime objects.
    2. Converts 'break_duration' to numeric, filling missing values with 0.
    3. Calculates the net 'work_duration' after subtracting breaks.
    4. Converts 'work_duration' to hours and labels it using `label_work_duration`.
    5. Cleans the 'department' field using `clean_deparment`.
    6. Formats 'work_duration' to 'HH:MM:SS' string, removing invalid or redundant parts.

    Parameters:
        df (pd.DataFrame): A DataFrame with at least the columns 'entry_time', 'exit_time',
                           'break_duration', and 'department'.

    Returns:
        pd.DataFrame: The modified DataFrame with cleaned and computed fields.
    """
    # Calculate total work duration
    entry_time = pd.to_datetime(df["entry_time"], format="%H:%M:%S", errors="coerce")
    exit_time = pd.to_datetime(df["exit_time"], format="%H:%M:%S", errors="coerce")
    break_duration = pd.to_numeric(df["break_duration"], "coerce").fillna(0)
    
    df["work_duration"] = calculate_work_duration(entry_time, exit_time, break_duration)

    work_duration_hour = df["work_duration"].dt.seconds/3600
    
    # Label work duration
    df["work_day_label"] = work_duration_hour.apply(label_work_duration)

    # Clean department column
    df["department"] = df["department"].apply(clean_deparment)

    # Convert word duration from '0 days HH:MM:SS' -> 'HH:MM:SS'
    df["work_duration"] = df["work_duration"].astype(str).str.replace(r"0 days 0|0 days", "", regex=True).str.strip()
    df["work_duration"] = df["work_duration"].str.replace("NaT", "Invalid Time")

    return df