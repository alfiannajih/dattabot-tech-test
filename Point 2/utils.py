from dateutil.relativedelta import relativedelta
from datetime import datetime
import pandas as pd
import re

gender_map = {
    'M': 'M',
    'Male': 'M',
    'Man': 'M',
    'Pria': 'M',
    'Laki-laki': 'M',
    'F': 'W',
    'Female': 'W',
    'Wanita': 'W',
    'Perempuan': 'W',
}


edu_map = {
    "SLTA": "SMA",
    "D1": "D1",
    "D3": "D3",
    "D4": "D4",
    "S1": "S1",
    "S2": "S2"
}


province_map = {
    # Jakarta
    'DKI Jakarta': 'DKI Jakarta',
    'JKT': 'DKI Jakarta',
    'Jakarta': 'DKI Jakarta',
    'East Jakarta': 'DKI Jakarta',
    'South Jakarta': 'DKI Jakarta',
    'Jakarta Selatan': 'DKI Jakarta',
    'Kalideres': 'DKI Jakarta',
    
    # Jawa Barat
    'West Java': 'Jawa Barat',
    'Jawa Barat': 'Jawa Barat',
    'Jabar': 'Jawa Barat',
    'Depok': 'Jawa Barat',
    'Bekasi': 'Jawa Barat',
    'Bogor': 'Jawa Barat',
    'Sukabumi': 'Jawa Barat',
    'Purwakarta': 'Jawa Barat',
    'Bandung': 'Jawa Barat',
    'Tangerang Selatan': 'Banten',  # Optional: could also be West Java regionally
    
    # Yogyakarta
    'DIY': 'DI Yogyakarta',
    'Yogyakarta': 'DI Yogyakarta',
    'Purwokerto': 'Jawa Tengah',  # Adjust as needed

    # Bali
    'Bali': 'Bali',
    'Denpasar': 'Bali',
}


def age_to_birthdate(age: str, reference_date: datetime):
    match = re.match(r'(\d+)\s+years,\s+(\d+)\s+month,\s+(\d+)\s+days', age)
    if match:
        years, months, days = map(int, match.groups())
        birthdate = reference_date - relativedelta(years=years, months=months, days=days)
        
        return birthdate.date()
    
    return pd.NaT


def clean_phone_number(phone):
    phone = str(phone).strip()

    if phone.isdigit():
        if phone.startswith('62'):
            return phone
        
        elif phone.startswith('0'):
            return '62' + phone[1:]
        
        else:
            return '62' + phone

    return None