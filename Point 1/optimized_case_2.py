import pandas as pd

def calculate_work_duration(entry_time, exit_time, break_duration):
    total_seconds = (exit_time - entry_time).dt.seconds - (break_duration * 60)
    work_duration = pd.to_timedelta(total_seconds, unit="s")

    return work_duration
    
    
def label_work_duration(total_hours):
    if pd.isna(total_hours):
        return "Invalid Entry"
    
    else:
        if total_hours < 5:
            return 'Short Day'
        elif total_hours >= 8:
            return 'Long Day'
        else:
            return 'Regular Day'


def clean_deparment(department):
    if pd.notna(department) and department.strip() != "":
        return department
    else:
        return "Unknown"
    
    
def optimized_preprocess_time_entries(df):
    entry_time = pd.to_datetime(df["entry_time"], format="%H:%M:%S", errors="coerce")
    exit_time = pd.to_datetime(df["exit_time"], format="%H:%M:%S", errors="coerce")
    break_duration = pd.to_numeric(df["break_duration"], "coerce").fillna(0)
    
    df["work_duration"] = calculate_work_duration(entry_time, exit_time, break_duration)

    work_duration_hour = df["work_duration"].dt.seconds/3600
    
    df["work_day_label"] = work_duration_hour.apply(label_work_duration)
    df["department"] = df["department"].apply(clean_deparment)

    df["work_duration"] = df["work_duration"].astype(str).str.replace(r"0 days 0|0 days", "", regex=True).str.strip()
    df["work_duration"] = df["work_duration"].str.replace("NaT", "Invalid Time")