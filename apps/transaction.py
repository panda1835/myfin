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
import init_database

df = init_database.init_database()

layout = html.Div([
    html.Div([
        html.H1("Culmulative Expenses in Month"),
        html.Div([
            dcc.Dropdown(
                id="month_cumulative",
                options=[{"label": 'January'  , "value": '01'},
                            {"label": 'February' , "value": '02'},
                            {"label": 'March'    , "value": '03'},
                            {"label": 'April'    , "value": '04'},
                            {"label": 'May'      , "value": '05'},
                            {"label": 'June'     , "value": '06'},
                            {"label": 'July'     , "value": '07'},
                            {"label": 'August'   , "value": '08'},
                            {"label": 'September', "value": '09'},
                            {"label": 'October'  , "value": '10'},
                            {"label": 'November' , "value": '11'},
                            {"label": 'December' , "value": '12'}],
                value=utils.today_month,
                clearable=False
            ),
        ], style={'width': '18%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id="year_cumulative",
                options=[{"label": i, "value": i} for i in range(int(utils.first_day_year), datetime.datetime.now().year+1)],
                value=utils.today_year,
                clearable=False
            ),
        ], style={'width': '10%', 'display': 'inline-block'}),             

        dcc.Graph(id='cumulative_monthly_expenses')
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.H1("Daily Expenses in Month"),
            html.Div([
                dcc.Dropdown(
                    id="month_daily",
                    options=[{"label": 'January'  , "value": '01'},
                                {"label": 'February' , "value": '02'},
                                {"label": 'March'    , "value": '03'},
                                {"label": 'April'    , "value": '04'},
                                {"label": 'May'      , "value": '05'},
                                {"label": 'June'     , "value": '06'},
                                {"label": 'July'     , "value": '07'},
                                {"label": 'August'   , "value": '08'},
                                {"label": 'September', "value": '09'},
                                {"label": 'October'  , "value": '10'},
                                {"label": 'November' , "value": '11'},
                                {"label": 'December' , "value": '12'}],
                    value=utils.today_month,
                    clearable=False
                ),
            ], style={'width': '18%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id="year_daily",
                    options=[{"label": i, "value": i} for i in range(int(utils.first_day_year), datetime.datetime.now().year+1)],
                    value=utils.today_year,
                    clearable=False
                ),
            ], style={'width': '10%', 'display': 'inline-block'}),             

            dcc.Graph(id='daily_expenses')
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.H1("Transaction History"),
        
        # ---------
        html.Div([
            html.Div("From", 
                        style={'width': '10%', 
                            'height':'50%',
                            'display': 'block',
                        }),

            html.Div([
                dcc.Dropdown(
                    id="start-date-transaction",
                    options=[{"label": str(i).zfill(2), "value": str(i).zfill(2)} for i in range(1, 32)],
                    value=utils.today_date.zfill(2),
                    clearable=False
                ),
            ], style={'width': '20%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id="start-month-transaction",
                    options=[{"label": 'January'  , "value": '01'},
                                {"label": 'February' , "value": '02'},
                                {"label": 'March'    , "value": '03'},
                                {"label": 'April'    , "value": '04'},
                                {"label": 'May'      , "value": '05'},
                                {"label": 'June'     , "value": '06'},
                                {"label": 'July'     , "value": '07'},
                                {"label": 'August'   , "value": '08'},
                                {"label": 'September', "value": '09'},
                                {"label": 'October'  , "value": '10'},
                                {"label": 'November' , "value": '11'},
                                {"label": 'December' , "value": '12'}],
                    value=utils.today_month,
                    clearable=False
                ),
            ], style={'width': '35%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id="start-year-transaction",
                    options=[{"label": i  , "value": i} for i in range(int(utils.first_day_year), datetime.datetime.now().year+1)],
                    value=utils.today_year,
                    clearable=False
                ),
            ], style={'width': '20%', 'display': 'inline-block'})
        ], style={'width': '25%', 'display': 'inline-block'}),
        #----------
        
        html.Div([
            html.Div("To", 
                            style={'width': '10%', 
                                'height':'50%',
                                'display': 'block',
                            }),
            html.Div([
                dcc.Dropdown(
                    id="end-date-transaction",
                    options=[{"label": str(i).zfill(2), "value": str(i).zfill(2)} for i in range(1, 32)],
                    value=utils.today_date,
                    clearable=False
                ),
            ], style={'width': '10%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id="end-month-transaction",
                    options=[{"label": 'January'  , "value": '01'},
                                {"label": 'February' , "value": '02'},
                                {"label": 'March'    , "value": '03'},
                                {"label": 'April'    , "value": '04'},
                                {"label": 'May'      , "value": '05'},
                                {"label": 'June'     , "value": '06'},
                                {"label": 'July'     , "value": '07'},
                                {"label": 'August'   , "value": '08'},
                                {"label": 'September', "value": '09'},
                                {"label": 'October'  , "value": '10'},
                                {"label": 'November' , "value": '11'},
                                {"label": 'December' , "value": '12'}],
                    value=utils.today_month,
                    clearable=False
                ),
            ], style={'width': '18%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Dropdown(
                    id="end-year-transaction",
                    options=[{"label": i  , "value": i} for i in range(int(utils.first_day_year), datetime.datetime.now().year+1)],
                    value=utils.first_day_year,
                    clearable=False
                ),
            ], style={'width': '10%', 'display': 'inline-block'})
        ], style={'width': '50%', 'display': 'inline-block'}),
        # ---------             

        html.Div([
            html.Div([
                html.Div("Type", 
                        style={'width': '10%', 
                            'height':'50%',
                            'display': 'block',
                        }),
                
                dcc.Dropdown(
                    id="transaction-type-filter",
                    options=[{"label": i, "value": i} for i in utils.transaction_list],
                    value='Expenses',
                    clearable=False
                ),
            ], style={'width': '8%', 'display': 'inline-block'}),

            html.Div([
                html.Div("Category", 
                        style={'width': '10%', 
                            'height':'50%',
                            'display': 'block',
                        }),
                
                dcc.Dropdown(
                    id="transaction-category-filter",
                    value='All',
                    clearable=False
                ),
            ], style={'width': '11%', 'display': 'inline-block'}),

            html.Div([
                
                html.Div("Sub-category", 
                        style={
                            'display': 'block',
                        }),
                
                dcc.Dropdown(
                    id="transaction-sub-category-filter",
                    value='All',
                    clearable=False
                ),
            ], style={'width': '12%', 'display': 'inline-block'})
        ], style={'display': 'block'}),
        
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
    if transaction_type == 'All':
        transaction_category = df['category'].unique().tolist()
        transaction_category = ['All'] + transaction_category
    else:
        transaction_category = df[df['transaction_type'] == transaction_type]['category'].unique().tolist()
        transaction_category = ['All'] + transaction_category
    
    return [{"label": i, "value": i} for i in transaction_category]

# update sub-category list when category changes
@app.callback(
    Output("transaction-sub-category-filter", "options"), 
    [Input("transaction-type-filter", "value"),
     Input("transaction-category-filter", "value")]
)
def create_list_for_transaction_sub_category(transaction_type, category):
    if transaction_type == 'All':
        transaction_sub_category = df['sub_category'].unique().tolist()
        transaction_sub_category = ['All'] + transaction_sub_category
        
    elif category == 'All':
        transaction_sub_category = df[(df['transaction_type'] == transaction_type)]['sub_category'].unique().tolist()
        transaction_sub_category = ['All'] + transaction_sub_category
    else:
        transaction_sub_category = df[(df['transaction_type'] == transaction_type) & ((df['category'] == category))]['sub_category'].unique().tolist()
        transaction_sub_category = ['All'] + transaction_sub_category
    
    return [{"label": i, "value": i} for i in transaction_sub_category]


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