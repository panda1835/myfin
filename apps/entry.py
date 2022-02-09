import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash import dash_table
import datetime
import pandas as pd
import json

from app import app

import create_plot
import utils
import utils_plotly
import init_database

with open('data.json','r') as f:
    data = json.load(f)
    database_name = data['constant']['DATABASE_NAME']

df = init_database.init_database(database_name)

layout = html.Div([

    dcc.Tabs([
        dcc.Tab(label='Add New Entry', children=[
            dash_table.DataTable(
                        id='entry-db-table',
                        data=df[utils.display_columns].iloc[::-1].to_dict('records'),
                        columns=[{"name": i, "id": i} for i in utils.display_columns],
                        editable=True,
                        page_size=10,
            #                             fixed_rows={'headers': True},
            #                             style_table={'height': 400},
                        style_cell={
                                    'minWidth': 80, 'maxWidth': 250, 'width': 80
                        }
                    ),
            html.Div([
                html.Div([
                    html.Div("On Date", 
                        style={'display':'block'}
                    ),

                    dcc.DatePickerSingle(
                            id='entry-date',
                            min_date_allowed=datetime.date(2001, 6, 4),
                            max_date_allowed=datetime.datetime.now(),
                            initial_visible_month=datetime.datetime.now(),
                            date=datetime.datetime.now(),
                            display_format='DD/MM/YYYY'
                    ),
                ], style={'display':'inline-block', 'float':'left'}),

                html.Div([
                    html.Div("Cash In/Out", 
                        style={
                            'display': 'block',
                        }),

                    dcc.Dropdown(
                        id="entry-in-out",
                        options=[{"label": i, "value": i} for i in ['Cash In', 'Cash Out']],
                        value='Cash In',
                        clearable=False
                    ),
                ], style={'width':'10%', 'display': 'inline-block', 'float':'left'}),

                html.Div([
                    html.Div("Type", 
                        style={
                            'display': 'block',
                        }),

                    dcc.Dropdown(
                        id="entry-transaction-type",
                        options=[{"label": i, "value": i} for i in df['transaction_type'].unique()],
                        value='Expenses',
                        clearable=False
                    ),
                ], style={'width':'10%', 'display': 'inline-block', 'float':'left'}),

                html.Div([
                    html.Div("Category", 
                        style={
                            'display': 'block',
                        }),

                    dcc.Dropdown(
                        id="entry-category",
                        clearable=False
                    ),
                ], style={'width': '10%', 'display': 'inline-block', 'float':'left'}),

                html.Div([
                    html.Div("Sub-category", 
                        style={
                            'display': 'block',
                        }),

                    dcc.Dropdown(
                        id="entry-sub-category",
                        clearable=False
                    ),
                ], style={'width': '10%', 'display': 'inline-block', 'float':'left'}),

                html.Div([

                    html.Div("Amount", 
                        style={
                            'display': 'block',
                        }),

                    dcc.Input(
                        id="entry-amount",
                        type='number'
                    ),
                ], style={'width': '10%', 'display': 'inline-block', 'float':'left', 
                        'margin-right':'50px',
                        'margin-left': '5px'}),

                html.Div([
                    html.Div("Currency", 
                        style={
                            'display': 'block',
                        }),

                    dcc.Dropdown(
                        id="entry-currency",
                        options=[{"label": i, "value": i} for i in df['currency'].unique()],
                        value=df['currency'].unique()[0],
                        clearable=False
                    ),
                ], style={'width': '10%', 'display': 'inline-block', 'float':'left'}),

                html.Div([

                    html.Div("Note", 
                        style={
                            'display': 'block',
                        }),

                    dcc.Input(
                        id="entry-note",
                        type='text',
                    ),
                ], style={'width': '10%', 'display': 'inline-block', 'margin-right':'50px'}),

                html.Div([
                    html.Div(". ", 
                        style={
                            'display': 'block',
                        }),
                    html.Button("Enter", 
                                id='entry-enter', 
                                n_clicks=0,
                                disabled = True)  
                ], style={'display':'inline-block', 'float':'right'}),


                html.Br(),
                dash_table.DataTable(
                        id='entry-preview-table-add',
    #                             data=df[display_columns].iloc[::-1].to_dict('records'),
                        columns=[{"name": i, "id": i} for i in utils.display_columns],
                        editable=True,
                        page_size=10,
                        style_cell={
                            'minWidth': 80, 'maxWidth': 250, 'width': 80
                        },
                        row_deletable=True,
                ),


                html.Br(),

                html.B('Sum:', id='entry-add-sum-text', style={'display': 'inline-block', "margin-right": "20px",}),
                html.Div(id='entry-add-sum-value', style={'display': 'inline-block'}),

                html.Br(),
                html.Button('Save to Database', 
                            id='entry-save-add', 
                            n_clicks=0, 
                            style={'display':'block'},
                            disabled=True),
                
                html.Br(),
                html.Br(),
                html.Br(),
            ])
        ]),

        dcc.Tab(label='Remove/Edit Entry', children=[
            html.Div([
                #---------- From ---------
                html.Div(
                    utils_plotly.date_month_year_dropdown(
                        "From",
                        {
                            "id_date": "start-date-entry-remove",
                            "id_month": "start-month-entry-remove",
                            "id_year": "start-year-entry-remove"
                        },
                        {
                            "value_date": utils.last_day_date,
                            "value_month": utils.last_day_month,
                            "value_year": utils.last_day_year,
                        }
                    ), style={'width': '50%', 'display': 'inline-block'}
                ),
                #---------- To ---------
                html.Div(
                    utils_plotly.date_month_year_dropdown(
                        "To",
                        {
                            "id_date": "end-date-entry-remove",
                            "id_month": "end-month-entry-remove",
                            "id_year": "end-year-entry-remove",
                        },
                        {
                            "value_date": utils.last_day_date,
                            "value_month": utils.last_day_month,
                            "value_year": utils.last_day_year,
                        }
                    ), style={'width': '50%', 'display': 'inline-block'}
                ),
                
                # --------
            ]),
                
            dash_table.DataTable(
                    id='entry-remove-table',
                    data=df[utils.display_columns].to_dict('records'),
                    columns=[{"name": i, "id": i} for i in utils.display_columns],
                    merge_duplicate_headers=True,
                    editable=True,
                    row_deletable=True,
                    fixed_rows={'headers': True},
                    style_table={'height': 300},
                    style_cell={
                        'minWidth': 80, 'maxWidth': 250, 'width': 95
                    }
                ),

            html.Br(),

            html.B('Sum:', id='entry-remove-sum-text', style={'display': 'inline-block', "margin-right": "20px",}),
            html.Div(id='entry-remove-sum-value', style={'display': 'inline-block'}),

            html.Br(),

            html.Button(
                'Save to Database', 
                id='entry-save-remove', 
                n_clicks=0, 
                style={'display':'block'}
                ),
        ])
    ]),

])

# add row to preview table in add entry
@app.callback(
    Output('entry-preview-table-add', 'data'),
    Input('entry-enter', 'n_clicks'),
    State('entry-preview-table-add', 'data'),
    State('entry-preview-table-add', 'columns'),
    State('entry-date', 'date'),
    State('entry-transaction-type', 'value'),
    State('entry-category', 'value'),
    State('entry-sub-category', 'value'),
    State('entry-amount', 'value'),
    State('entry-currency', 'value'),
    State('entry-note', 'value'),
    State('entry-in-out', 'value'))
def add_row_to_preview_table(n_clicks, rows, columns,
            date, transaction_type, category, sub_category, amount, currency, note, in_out):
    sign = ''
    if in_out == "Cash Out":
        sign = '-'
        
    date = date.split('T')[0]
    [year, month, day] = map(int, date.split('-'))
    weekday = datetime.date(year, month, day).strftime('%A')
    
    if note == None:
        note = ''
    
    if n_clicks > 0:
        new_entry_df = pd.DataFrame({
                            'date' : f"{date}",
                            'date_of_week' : f"{weekday}",
                            'currency' : f"{currency}",
                            'transaction_type' : f"{transaction_type}",
                            'category' : f"{category}",
                            'sub_category' : f"{sub_category}",
                            'amount' : f"{sign}{amount}",
                            'note' : f"{note}"
                        }, index=[0])
        
        if rows == None:
            sum_df = new_entry_df
        else: 
            sum_df = pd.DataFrame.from_records(rows)
            sum_df = sum_df.append(new_entry_df)
        
        sum_df['amount'] = sum_df['amount'].str.replace(',', '')
        sum_df['amount'] = sum_df['amount'].astype('int64')
        sum_df['amount'] = sum_df['amount'].map('{:,d}'.format)
        
        return sum_df.to_dict("records")

# save to database in add entry
@app.callback(
    Output('entry-db-table', 'data'),
    Input('entry-save-add', 'n_clicks'),
    Input('entry-preview-table-add', 'data'),
    Input('entry-preview-table-add', 'columns'))
    
def save_new_entry(n_clicks_add, rows_add, columns_add):
    if n_clicks_add > 0: 
        rows = rows_add
        new_entry_df = pd.DataFrame(rows, columns=[c['name'] for c in columns_add])
        database_df = init_database.init_database(database_name)
        # remove , seperator in amount column
        new_entry_df.amount = new_entry_df.amount.str.replace(',', '')
        # append to original db
        database_df = database_df.append(new_entry_df)
        
        database_df['Date'] = pd.to_datetime(database_df['date'])
        database_df.sort_values(by=['Date'], inplace=True)
        database_df.drop(columns = ["Date"], inplace=True)
        
        database_df.to_csv(database_name, index=False)
        
    return database_df[utils.display_columns].iloc[::-1].to_dict('records')

# save to database in add entry
# @app.callback(
#     Output('entry-db-table', 'data'),
#     Input('entry-save-add', 'n_clicks'),
#     State('entry-preview-table-add', 'data'))
    
# def update_entry_table(
#                       n_clicks_remove, rows_remove, 
#                        ):
        
#     if n_clicks_remove > 0: 
#         rows = rows_remove
#         old_entry = df.copy()
#         old_entry['date'] = pd.to_datetime(old_entry['date'])
#         start_day = f"{start_year}-{start_month}-{start_date}"
#         end_day = f"{end_year}-{end_month}-{end_date}"

#         old_entry = old_entry[(old_entry['date'] >= start_day) & 
#                                               (old_entry['date'] <= end_day)]

#         old_entry['date'] = old_entry['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
        
#         new_entry = pd.DataFrame.from_records(rows).iloc[:-1]
        
        
#         database_df = pd.read_csv(database_name)
#         database_df = pd.concat([old_entry, database_df]).drop_duplicates(keep=False)

#         database_df = database_df.append(new_entry)
        
#         database_df['Date'] = pd.to_datetime(database_df['date'])
#         database_df.sort_values(by=['Date'], inplace=True)
#         database_df.drop(columns = ["Date"], inplace=True)
        
#         database_df.to_csv(database_name, index=False)
#     return database_df[utils.display_columns].iloc[::-1].to_dict('records')


# refresh entry note after saving
@app.callback(
    Output('entry-note', 'value'),
    Input('entry-save-add', 'n_clicks'))
def add_row(n_clicks):
    if n_clicks > 0:
        return ''
    
# update category list when transaction type changes
@app.callback(
    Output("entry-category", "options"), 
    [Input("entry-transaction-type", "value")]
)
def create_list_for_transaction_category(transaction_type):
    transaction_category = df[df['transaction_type'] == transaction_type]['category'].unique().tolist()
    
    return [{"label": i, "value": i} for i in transaction_category]

# update sub-category list when category changes
@app.callback(
    Output("entry-sub-category", "options"), 
    [Input("entry-transaction-type", "value"),
     Input("entry-category", "value")]
)
def create_list_for_transaction_sub_category(transaction_type, category):
    transaction_sub_category = df[(df['transaction_type'] == transaction_type) & ((df['category'] == category))]['sub_category'].unique().tolist()
    
    return [{"label": i, "value": i} for i in transaction_sub_category]

# update transaction type when cash-out
@app.callback(
    Output("entry-transaction-type", "value"), 
    [Input("entry-in-out", "value")]
)
def update_transaction_type_when_cash_out(cash_in_out):
    if cash_in_out == 'Cash Out':
        return 'Assets'
    else:
        return 'Expenses'

# update amount when cash-out or enter
@app.callback(
    Output("entry-amount", "value"), 
    [Input("entry-in-out", "value"),
    Input("entry-preview-table-add", "data"),
    Input("entry-preview-table-add", "columns"),
    Input('entry-save-add', 'n_clicks')]
)
def update_amount_when_cash_out(cash_in_out, rows, columns, n_clicks):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    df.amount = df.amount.str.replace(',', '')
    df.amount = df.amount.astype('int32')
    if n_clicks > 0:
        return ''
    elif cash_in_out == 'Cash Out':
        return df.amount.sum()
    else:
        return None

# enable/disable enter button before amount is filled
@app.callback(
    Output("entry-enter", "disabled"), 
    [Input("entry-sub-category", "value"),
     Input("entry-category", "value"),
     Input("entry-amount", "value")]
)
def enable_entry_enter_button(sub_category, category, amount):
    if (sub_category == None) or (category==None) or (amount==None):
        return True
    else:
        return False

# disable save to database button in add when there is entry
@app.callback(
    Output("entry-save-add", "disabled"), 
    [Input("entry-preview-table-add", "data")]
)
def enable_entry_enter_button(rows):
    if rows == None:
        return True
    else:
        return False

# display remove/edit table that is editable
@app.callback(
    Output("entry-remove-table", "data"), 
    [Input("start-date-entry-remove", "value"), 
     Input("start-month-entry-remove", "value"),
     Input("start-year-entry-remove", "value"), 
     Input("end-date-entry-remove", "value"),
     Input("end-month-entry-remove", "value"), 
     Input("end-year-entry-remove", "value"),]
)
def display_daily_expenses(start_date, start_month, start_year,
                           end_date, end_month, end_year):
    
    transaction_df = df.copy()
    transaction_df['date'] = pd.to_datetime(transaction_df['date'])
    start_day = f"{start_year}-{start_month}-{start_date}"
    end_day = f"{end_year}-{end_month}-{end_date}"

    transaction_df = transaction_df[(transaction_df['date'] >= start_day) & (transaction_df['date'] <= end_day)]
    
    transaction_df['date'] = transaction_df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
    # cast from float to int to format
    transaction_df['amount'] = transaction_df['amount'].astype('int64')
    transaction_df['amount'] = transaction_df['amount'].map('{:,d}'.format)
    return transaction_df.to_dict('records')

# update amount sum in add entry
@app.callback(
    Output("entry-add-sum-value", "children"), 
    [Input("entry-preview-table-add", "data"),
    Input("entry-preview-table-add", "columns"),]
)
def display_total_sum_add(rows, columns):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    df.amount = df.amount.str.replace(',', '')
    df.amount = df.amount.astype('int32')
    return html.Div(f' {"{:,}".format(df.amount.sum())} VND')

# update amount sum in remove entry
@app.callback(
    Output("entry-remove-sum-value", "children"), 
    [Input("entry-remove-table", "data"),
    Input("entry-remove-table", "columns"),]
)
def display_total_sum_remove(rows, columns):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    df.amount = df.amount.str.replace(',', '')
    df.amount = df.amount.astype('int32')
    return html.Div(f' {"{:,}".format(df.amount.sum())} VND')