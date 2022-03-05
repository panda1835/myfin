import pandas as pd
import numpy as np
import json

with open('data.json','r') as f:
    data = json.load(f)
    database_name = data['constant']['DATABASE_NAME']

def init_database(database_name=database_name):
    df = pd.read_csv(database_name)

    if "?" in df.columns:
        # remove '?' column
        df.drop(columns=['?'], inplace=True)
        df.drop(columns=['pending/cleared'], inplace=True)


        # seprarate account into categories
        transaction_type = []
        category = []
        sub_category = [] 

        for i in df['account']:
            transaction_type.append(i.split(':')[0])    
            category.append(i.split(':')[1])
            try:
                sub_category.append(i.split(':')[2])
            except:
                print(i)

        df['transaction_type'] = transaction_type
        df['category'] = category
        df['sub_category'] = sub_category

    # add month column
    df['date'] = df['date'].str.replace('/', '-')
    df['year_month'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')

    # cast amount into int
    df['amount'].astype('int64')

    return df


