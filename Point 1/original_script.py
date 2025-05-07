# CASE 1
def clean_customer_data(df):
    known_countries = ["US", "UK", "ID", "SG"]
    full_names = []
    cleaned_ages = []
    is_adults = []
    standardized_countries = []

    for i in range(len(df)):
        row = df.iloc[i]

        # String concat with NaN checking
        first = str(row['first_name']) if pd.notna(row['first_name']) else "Unknown"
        last = str(row['last_name']) if pd.notna(row['last_name']) else "Unknown"
        full_name = first + " " + last
        full_names.append(full_name)

        # Data type conversion & filtering
        age_raw = row['age']
        if pd.isna(age_raw) or str(age_raw).strip().lower() == 'unknown':
            age = -1
        else:
            try:
                age = int(age_raw)
            except:
                age = -1
        cleaned_ages.append(age)

        # NA + conditional logic
        is_adults.append(True if age >= 18 else False)

        # String cleaning & filtering
        country = str(row['country']).strip().upper() if pd.notna(row['country']) else "XX"
        if country not in known_countries:
            country = "XX"
        standardized_countries.append(country)

    # Add results back to DataFrame
    df['full_name'] = full_names
    df['cleaned_age'] = cleaned_ages
    df['is_adult'] = is_adults
    df['country_code'] = standardized_countries

    return df

# CASE 2
from datetime import datetime

def preprocess_time_entries(df):
    work_durations = []
    work_day_labels = []
    departments = []
    
    for i in range(len(df)):
        row = df.iloc[i]
        
        # Clean entry_time and exit_time, convert to datetime
        try:
            entry_time = datetime.strptime(str(row['entry_time']), '%H:%M:%S')
        except ValueError:
            entry_time = None
        
        try:
            exit_time = datetime.strptime(str(row['exit_time']), '%H:%M:%S')
        except ValueError:
            exit_time = None
        
        # Handle break_duration, converting to minutes or setting to 0 if invalid
        try:
            break_duration = int(row['break_duration'])
        except (ValueError, TypeError):
            break_duration = 0
        
        # Calculate work duration in seconds, then convert to HH:MM:SS
        if entry_time and exit_time:
            total_seconds = (exit_time - entry_time).seconds - (break_duration * 60)
            work_duration = str(datetime.timedelta(seconds=total_seconds))
            work_durations.append(work_duration)
        else:
            work_durations.append('Invalid Time')
        
        # Assign work day labels based on work duration
        if entry_time and exit_time:
            total_hours = (exit_time - entry_time).seconds / 3600 - break_duration / 60
            if total_hours < 5:
                work_day_labels.append('Short Day')
            elif total_hours >= 8:
                work_day_labels.append('Long Day')
            else:
                work_day_labels.append('Regular Day')
        else:
            work_day_labels.append('Invalid Entry')
        
        # Clean department column
        department = row['department'] if pd.notna(row['department']) and row['department'].strip() != "" else "Unknown"
        departments.append(department)
    
    # Add results back to the DataFrame
    df['work_duration'] = work_durations
    df['work_day_label'] = work_day_labels
    df['department'] = departments
    
    return df

# CASE 3
import pandas as pd

def preprocess_sales_data(df):
    # Clean the 'sales_amount' column, remove currency symbols and convert to float
    sales_amounts = []
    for amount in df['sales_amount']:
        cleaned_amount = ''.join(c for c in amount if c.isdigit() or c == '.')
        try:
            sales_amounts.append(float(cleaned_amount))
        except ValueError:
            sales_amounts.append(0.0)
    
    df['sales_amount'] = sales_amounts
    
    # Convert 'sale_date' to datetime format
    df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
    
    # Calculate total sales per sales rep
    total_sales_per_rep = df.groupby('sales_rep')['sales_amount'].sum()
    df['total_sales'] = df['sales_rep'].map(total_sales_per_rep)
    
    # Aggregate unique products sold by each sales rep
    unique_products_per_rep = df['products_sold'].str.split(',').apply(lambda x: set(x))
    products_per_rep = unique_products_per_rep.groupby(df['sales_rep']).apply(lambda x: set([item for sublist in x for item in sublist]))
    df['unique_products'] = df['sales_rep'].map(products_per_rep)
    
    # Calculate the average sales amount per sales rep
    avg_sales_per_rep = df.groupby('sales_rep')['sales_amount'].mean()
    df['average_sales_amount'] = df['sales_rep'].map(avg_sales_per_rep)
    
    # Count the number of sales where a discount was applied
    discount_counts = df.groupby('sales_rep')['discount_applied'].apply(lambda x: (x == 'Yes').sum())
    df['discount_count'] = df['sales_rep'].map(discount_counts)
    
    return df
