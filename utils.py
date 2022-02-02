import pandas as pd                       #to perform data manipulation and analysis
import numpy as np                        #to cleanse data
from datetime import datetime             #to manipulate dates
import datetime
import json
import calendar

import init_database

df = init_database.init_database()

# declare today
today_date = datetime.datetime.now().strftime("%d").zfill(2)
today_month = datetime.datetime.now().strftime("%m").zfill(2)
today_month_EN = datetime.datetime.now().strftime("%B")
today_year = datetime.datetime.now().strftime("%Y")

# declare first date in the df
first_day_df = pd.to_datetime(df['date']).min()
first_day_date = first_day_df.strftime("%d")
first_day_month = first_day_df.strftime("%m")
first_day_year = first_day_df.strftime("%Y")
first_day_df = first_day_df.strftime("%Y-%m-%d")

display_columns = ['date', 
                'date_of_week', 
                'transaction_type', 
                'category', 
                'sub_category',
                'amount', 
                'currency', 
                'note']

transaction_list = df['transaction_type'].unique().tolist()
transaction_list = ['All'] + transaction_list

transaction_sub_category = df['sub_category'].unique().tolist()
transaction_sub_category = ['All'] + transaction_sub_category

def money_in_visa_card(df):
    return df[df['sub_category'] == 'VISA']['amount'].sum()

def money_in_acb_card(df):
    return df[df['sub_category'] == 'ACB']['amount'].sum()

def money_in_finhay(df):
    return df[df['sub_category'] == 'Finhay']['amount'].sum()

def money_in_cash(df):
    return df[df['sub_category'] == 'Cash']['amount'].sum()

def money_in_home(df):
    return df[df['sub_category'] == 'Home']['amount'].sum()

def money_in_moca(df):
    return df[df['sub_category'] == 'MOCA']['amount'].sum()

def get_last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]

# fill in missing date
def fill_in_missing_date(missing_df, start_date, end_date):
    idx = pd.date_range(start_date, end_date)
    
    missing_df.index = pd.DatetimeIndex(missing_df['date'])
        
    missing_df = missing_df.reindex(idx, fill_value=0)
    
    missing_df['date'] = missing_df.index
    return missing_df

