import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import calendar
import datetime
from dash import dash_table
import pandas as pd


from app import app

import create_plot
import utils
import utils_plotly
import init_database

df = init_database.init_database()

def layout():
    return html.Div([
    html.Div([
        html.H1("Culmulative Expenses in Month"),
        html.Div(
            utils_plotly.month_year_dropdown(
                {
                    "id_month": "month_cumulative",
                    "id_year": "year_cumulative"
                },
                {
                    "value_month": utils.today_month,
                    "value_year": utils.today_year
                }
            )
        ),           
        dcc.Graph(id='cumulative_monthly_expenses')
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.H1("Daily Expenses in Month"),
        html.Div(
            utils_plotly.month_year_dropdown(
                {
                    "id_month": "month_daily",
                    "id_year": "year_daily"
                },
                {
                    "value_month": utils.today_month,
                    "value_year": utils.today_year
                }
            )
        ),           
        dcc.Graph(id='daily_expenses')
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.H1("Transaction History"),
        #---------- From ---------
        html.Div(
            utils_plotly.date_month_year_dropdown(
                "From",
                {
                    "id_date": "start-date-transaction",
                    "id_month": "start-month-transaction",
                    "id_year": "start-year-transaction"
                },
                {
                    "value_date": utils.first_day_date.zfill(2),
                    "value_month": utils.first_day_month,
                    "value_year": utils.first_day_year,
                }
            ), style={'width': '50%', 'display': 'inline-block'}
        ),
        #---------- To ---------
        html.Div(
            utils_plotly.date_month_year_dropdown(
                "To",
                {
                    "id_date": "end-date-transaction",
                    "id_month": "end-month-transaction",
                    "id_year": "end-year-transaction",
                },
                {
                    "value_date": utils.today_date,
                    "value_month": utils.today_month,
                    "value_year": utils.today_year,
                }
            ), style={'width': '50%', 'display': 'inline-block'}
        ),
        # ---------             

        html.Div(
            utils_plotly.type_category_subcategory_dropdown(
                {
                    "id_type": "transaction-type-filter",
                    "id_category": "transaction-category-filter",
                    "id_subcategory": "transaction-sub-category-filter",
                },
                {
                    "value_type": 'Expenses',
                    "value_category": 'All',
                    "value_subcategory": 'All',
                }
            ), style={'width': '100%', 'display': 'inline-block'}
        ),
        
        # --------
        
        dash_table.DataTable(
                id='transaction-history',
                data=df[utils.display_columns].to_dict('records'),
                columns=[{"name": i, "id": i} for i in utils.display_columns],
                export_format='xlsx',
                export_headers='display',
                merge_duplicate_headers=True,
                fixed_rows={'headers': True},
                style_table={'height': 400},
                style_cell={
                    'minWidth': 80, 'maxWidth': 250, 'width': 95
                }
            ),

        
    ]),

    html.Br(),    
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

])

# cumulative expenses
@app.callback(
    Output("cumulative_monthly_expenses", "figure"), 
    [Input("month_cumulative", "value"), Input("year_cumulative", "value")]
)
def display_cumulative_monthly_expenses(month_cumulative, year_cumulative):
    
    return create_plot.create_cumulative_monthly_expenses_plot(df, year_cumulative, month_cumulative)

# daily expenses
@app.callback(
    Output("daily_expenses", "figure"), 
    [Input("month_daily", "value"), Input("year_daily", "value")]
)
def display_daily_expenses(month_daily, year_daily):
    
    return create_plot.create_daily_expenses_plot(df, year_daily, month_daily)

# update category list when transaction_type changes
@app.callback(
    Output("transaction-category-filter", "options"), 
    [Input("transaction-type-filter", "value")]
)
def create_list_for_transaction_category(transaction_type):
    return utils_plotly.create_list_for_transaction_category(transaction_type)

# update sub-category list when category changes
@app.callback(
    Output("transaction-sub-category-filter", "options"), 
    [Input("transaction-type-filter", "value"),
     Input("transaction-category-filter", "value")]
)
def create_list_for_transaction_sub_category(transaction_type, transaction_category):
    return utils_plotly.ceate_list_for_transaction_sub_category(transaction_type, transaction_category)


# default All when new option
@app.callback(
    Output("transaction-category-filter", "value"), 
    [Input("transaction-type-filter", "value")]
)
def default_all_category(transaction_type):
    return "All"

# reset transaction_type when update category
# UPDATE: wont do because will create dependency cycle: 
# transaction-type-filter.value -> transaction-category-filter.value -> transaction-type-filter.value

# default All when new option
@app.callback(
    Output("transaction-sub-category-filter", "value"), 
    [Input("transaction-type-filter", "value"),
     Input("transaction-category-filter", "value")]
)
def default_all_sub_category(transaction_type, category):
    return "All"

# transaction history
@app.callback(
    Output("transaction-history", "data"), 
    [Input("start-date-transaction", "value"), 
     Input("start-month-transaction", "value"),
     Input("start-year-transaction", "value"), 
     Input("end-date-transaction", "value"),
     Input("end-month-transaction", "value"), 
     Input("end-year-transaction", "value"),
     Input("transaction-type-filter", "value"),
     Input("transaction-category-filter", "value"),
     Input("transaction-sub-category-filter", "value")]
)
def display_daily_expenses(start_date, start_month, start_year,
                           end_date, end_month, end_year,
                           transaction_type,
                           category,
                           sub_category):
    
    transaction_df = df.copy()
    transaction_df['date'] = pd.to_datetime(transaction_df['date'])
    start_day = f"{start_year}-{start_month}-{start_date}"
    end_day = f"{end_year}-{end_month}-{end_date}"

    transaction_df = transaction_df[(transaction_df['date'] >= start_day) & (transaction_df['date'] <= end_day)]
    
    transaction_df['date'] = transaction_df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
    if transaction_type != "All":
        transaction_df = transaction_df[transaction_df['transaction_type'] == transaction_type]
        
    if category != "All":
        transaction_df = transaction_df[transaction_df['category'] == category]
        
    if sub_category != "All":
        transaction_df = transaction_df[transaction_df['sub_category'] == sub_category]
        
    transaction_df = transaction_df.append(transaction_df.sum(numeric_only=True), ignore_index=True)
    
    transaction_df.loc[len(transaction_df)-1, 'date'] = 'Sum'
    
    # cast from float to int to format
    transaction_df['amount'] = transaction_df['amount'].astype('int64')
    transaction_df['amount'] = transaction_df['amount'].map('{:,d}'.format)
    return transaction_df.to_dict('records')