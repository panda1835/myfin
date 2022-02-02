import pandas as pd                       #to perform data manipulation and analysis
import numpy as np                        #to cleanse data
from dash import dash_table

database_name = 'transaction.csv'

def init_database():
    df = pd.read_csv(database_name)

    # add month column
    df['date'] = df['date'].str.replace('/', '-')
    df['year_month'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')

    # cast amount into int
    df['amount'].astype('int64')

    return df

display_columns = ['date', 
                'date_of_week', 
                'transaction_type', 
                'category', 
                'sub_category',
                'amount', 
                'currency', 
                'note']

