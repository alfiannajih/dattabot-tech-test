import re
from collections import defaultdict
import pandas as pd

def clean_sales_amount(sales_amount: str) -> float:
    match = re.search(r"[A-Z]{3}\s([\d,]+\.\d+)", sales_amount)

    if match:
        amount = float(match.group(1).replace(",", ""))
    else:
        amount = 0.0

    return amount


def optimized_preprocess_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and enriches sales data with computed metrics and aggregations per sales representative.

    Steps performed:
    1. Cleans 'sales_amount' values using `clean_sales_amount` and converts them to floats.
    2. Converts 'sale_date' to datetime format, coercing invalid entries to NaT.
    3. Calculates the total and average sales amount per sales representative.
    4. Aggregates the set of unique products sold by each sales rep from the 'products_sold' column.
    5. Counts the number of transactions per sales rep where a discount was applied.

    Parameters:
        df (pd.DataFrame): A DataFrame with at least the following columns:
                           'sales_amount', 'sale_date', 'sales_rep', 'products_sold',
                           and 'discount_applied'.

    Returns:
        pd.DataFrame: The enriched DataFrame including:
                      'total_sales', 'unique_products', 'average_sales_amount', and 'discount_count'.
    """
    # Convert sales amount to float
    df["sales_amount"] = df["sales_amount"].apply(clean_sales_amount)

    # Convert 'sale_date' to datetime format
    df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
    
    # Calculate total sales per sales rep
    total_sales_per_rep = df.groupby('sales_rep')['sales_amount'].sum()
    df['total_sales'] = df['sales_rep'].map(total_sales_per_rep)
    
    # Aggregate unique products sold by each sales rep
    products_per_rep = defaultdict(set)
    for rep, products in zip(df['sales_rep'], df['products_sold']):
        for product in products.split(','):
            products_per_rep[rep].add(product)
            
    df['unique_products'] = df['sales_rep'].map(products_per_rep)
    
    # Calculate the average sales amount per sales rep
    avg_sales_per_rep = df.groupby('sales_rep')['sales_amount'].mean()
    df['average_sales_amount'] = df['sales_rep'].map(avg_sales_per_rep)
    
    # Count the number of sales where a discount was applied
    discount_counts = df.groupby('sales_rep')['discount_applied'].apply(lambda x: (x == 'Yes').sum())
    df['discount_count'] = df['sales_rep'].map(discount_counts)
    
    return df