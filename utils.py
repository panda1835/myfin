import pandas as pd                       #to perform data manipulation and analysis
import numpy as np                        #to cleanse data
from datetime import datetime             #to manipulate dates
import datetime
import json
import calendar

import init_database

def get_last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]

# fill in missing date
def fill_in_missing_date(missing_df, start_date, end_date):
    idx = pd.date_range(start_date, end_date)
    
    missing_df.index = pd.DatetimeIndex(missing_df['date'])
        
    missing_df = missing_df.reindex(idx, fill_value=0)
    
    missing_df['date'] = missing_df.index
    return missing_df

