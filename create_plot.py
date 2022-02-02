import pandas as pd                       #to perform data manipulation and analysis
import numpy as np                        #to cleanse data
from datetime import datetime             #to manipulate dates
import plotly.express as px               #to create interactive charts
import plotly.graph_objects as go         #to create interactive charts
from dash.dependencies import Input, Output, State
import datetime
import json
import calendar

import init_database
import utils

# read constant
with open('data.json','r') as f:
    data = json.load(f)
    NECESSITY_MONEY = data['constant']['MONEY_ALLOCATED_FOR_NECESSITY_PER_MONTH']
    EDUCATION_AND_ENTERTAINMET = data['constant']['MONEY_ALLOCATED_FOR_EDUCATION_AND_ENTERTAINMENT_PER_MONTH']
    

def create_expenses_by_category(df, category, month, year):
    expenses_df = df.copy()
    expenses_df = expenses_df[expenses_df['year_month'] == f'{year}-{month}']
    expenses_df = expenses_df[expenses_df['transaction_type'] == 'Expenses']    
    expenses_df = expenses_df[expenses_df['category'].isin(category)]
    expenses_df = expenses_df.groupby('date')['amount'].sum().reset_index(name ='sum')
    
    expenses_df = utils.fill_in_missing_date(expenses_df, f'{year}-{month}-01', 
                                                    f'{year}-{month}-{utils.get_last_day_of_month(int(year), int(month))}')
    
    expenses_df['cumulative_sum'] = expenses_df['sum'].cumsum()
    expenses_df['Remain'] = NECESSITY_MONEY-expenses_df['cumulative_sum']
    expenses_df['Date'] = expenses_df['date']
    
    fig = px.area(expenses_df, x='Date', 
                               y='Remain')
    return fig

def create_plot_for_category(df):
    category_df = df.copy()
    category_df['date'] = pd.to_datetime(category_df['date'])  
    category_df = category_df[(category_df['date'] >= '2018-01-01') & (category_df['date'] <= datetime.datetime.now())]
    category_df = category_df[category_df['transaction_type'] == 'Expenses']    
    category_df = category_df.groupby(['year_month','category']).sum().reset_index()
    
    category_df['Amount'] = category_df['amount']
    category_df['Month'] = category_df['year_month']
    fig = px.line(category_df, x='Month', y='Amount', color='category')
    
    return fig

def create_daily_expenses_plot(df, year, month):
    daily_df = df.copy()
    daily_df = daily_df[daily_df['year_month'] == f'{year}-{month}']
    daily_df = daily_df[daily_df['transaction_type'] == 'Expenses']
    daily_df = daily_df.groupby('date')['amount'].sum().reset_index(name ='sum')

    daily_df = utils.fill_in_missing_date(daily_df, f'{year}-{month}-01', 
                                                f'{year}-{month}-{utils.get_last_day_of_month(int(year), int(month))}')
    
    
    Daily_Expenses = go.Figure(
            data = go.Scatter(x = daily_df["date"], y = daily_df['sum']),
            layout = go.Layout(
                title = go.layout.Title(text=f"Daily expenses in {calendar.month_name[int(month)]}, {year}")
            )
    )
    Daily_Expenses.update_layout(
            xaxis_title = "Date",
            yaxis_title = "Daily Expenses (VND)",
            hovermode = 'x unified'
        )
    Daily_Expenses.update_xaxes(
        tickangle = 45)
    
    return Daily_Expenses

def create_cumulative_monthly_expenses_plot(df, year, month):
    cumsum_df = df.copy()
    cumsum_df = cumsum_df[cumsum_df['year_month'] == f'{year}-{month}']
    cumsum_df = cumsum_df[cumsum_df['transaction_type'] == 'Expenses']
    cumsum_df = cumsum_df.groupby('date')['amount'].sum().reset_index(name ='sum')
    
    cumsum_df = utils.fill_in_missing_date(cumsum_df, f'{year}-{month}-01', 
                                                f'{year}-{month}-{utils.get_last_day_of_month(int(year), int(month))}')
    
    cumsum_df['cumulative_sum'] = cumsum_df['sum'].cumsum()
    
    
    Cumulative_Monthly_Expenses = go.Figure(
        data = go.Scatter(x = cumsum_df["date"], y = cumsum_df['cumulative_sum']),
        layout = go.Layout(
            title = go.layout.Title(text=f"Cumulative expenses in {calendar.month_name[int(month)]}, {year}")
        )
    )
    Cumulative_Monthly_Expenses.update_layout(
        xaxis_title = "Date",
        yaxis_title = "Cumulative Expenses (VND)",
        hovermode = 'x unified'
    )
    Cumulative_Monthly_Expenses.update_xaxes(
        tickangle = 45)
    
    return Cumulative_Monthly_Expenses


def create_category_pie_chart(df, start_day, end_day):
    category_df = df.copy()
    category_df['date'] = pd.to_datetime(category_df['date'])  
    category_df = category_df[(category_df['date'] >= start_day) & (category_df['date'] <= end_day)]
    category_df = category_df[category_df['transaction_type'] == 'Expenses']    
    category_df = category_df.groupby('category')['amount'].sum().reset_index(name='sum')
    
    category_df['Amount'] = category_df['sum']
    category_df['Category'] = category_df['category']
    fig = px.pie(category_df, values='Amount', names='Category')
    
    return fig
