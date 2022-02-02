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
import init_database

with open('data.json','r') as f:
    data = json.load(f)
    database_name = data['constant']['DATABASE_NAME']

df = init_database.init_database(database_name)

layout = html.Div([
    html.H1("Add New Entry"),
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
                    
    html.Br(),

    dcc.RadioItems(
        id='entry-radio-button',
        options=[
            {'label': 'Add New Entry', 'value': 'add'},
            {'label': 'Remove Entry', 'value': 'remove'}
        ],
        value='add',
        labelStyle={'display': 'inline-block'}
    ),

    html.Br(),
    # ---

    html.Div(id='entry-option-display'),
])

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
            sum_df = pd.DataFrame.from_records(rows).iloc[:-1]
            sum_df = sum_df.append(new_entry_df)
            
        sum_df['amount'] = sum_df['amount'].astype('int64')
        sum_df = sum_df.append(sum_df.sum(numeric_only=True), ignore_index=True)
    
        sum_df.loc[len(sum_df)-1, 'date'] = 'Sum'
        
        return sum_df.to_dict("records")

# save to database add
@app.callback(
    Output('entry-db-table', 'data'),
    Input('entry-save-add', 'n_clicks'),
    State('entry-preview-table-add', 'data'),
    
    Input('entry-save-remove', 'n_clicks'),
    State('entry-preview-table-remove', 'data'),
    State("entry-start-date-remove", "value"), 
     State("entry-start-month-remove", "value"),
     State("entry-start-year-remove", "value"), 
     State("entry-end-date-remove", "value"),
     State("entry-end-month-remove", "value"), 
     State("entry-end-year-remove", "value"))
    
def update_entry_table(n_clicks_add, rows_add,
                      n_clicks_remove, rows_remove, 
                       start_date, start_month, start_year,
                       end_date, end_month, end_year):
     
    if n_clicks_add > 0: 
        rows = rows_add
        new_entry_df = pd.DataFrame.from_records(rows).iloc[:-1]
        database_df = pd.read_csv(database_name)
        database_df = database_df.append(new_entry_df)
        
        database_df['Date'] = pd.to_datetime(database_df['date'])
        database_df.sort_values(by=['Date'], inplace=True)
        database_df.drop(columns = ["Date"], inplace=True)
        
        database_df.to_csv(database_name, index=False)
        
    if n_clicks_remove > 0: 
        rows = rows_remove
        old_entry = df.copy()
        old_entry['date'] = pd.to_datetime(old_entry['date'])
        start_day = f"{start_year}-{start_month}-{start_date}"
        end_day = f"{end_year}-{end_month}-{end_date}"

        old_entry = old_entry[(old_entry['date'] >= start_day) & 
                                              (old_entry['date'] <= end_day)]

        old_entry['date'] = old_entry['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
        
        new_entry = pd.DataFrame.from_records(rows).iloc[:-1]
        
        
        database_df = pd.read_csv(database_name)
        database_df = pd.concat([old_entry, database_df]).drop_duplicates(keep=False)

        database_df = database_df.append(new_entry)
        
        database_df['Date'] = pd.to_datetime(database_df['date'])
        database_df.sort_values(by=['Date'], inplace=True)
        database_df.drop(columns = ["Date"], inplace=True)
        
        database_df.to_csv(database_name, index=False)
    return database_df[utils.display_columns].iloc[::-1].to_dict('records')


# refresh entry (amount) after saving
@app.callback(
    Output('entry-amount', 'value'),
    Input('entry-save-add', 'n_clicks'))
def add_row(n_clicks):
    if n_clicks > 0:
        return ''
    
# refresh entry (note) after saving
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

# display remove preview table and update sum when table changes
@app.callback(
    Output("entry-preview-table-remove", "data"), 
    [Input("entry-start-date-remove", "value"), 
     Input("entry-start-month-remove", "value"),
     Input("entry-start-year-remove", "value"), 
     Input("entry-end-date-remove", "value"),
     Input("entry-end-month-remove", "value"), 
     Input("entry-end-year-remove", "value"),
#      Input('entry-preview-table-remove', 'data_previous'),
#      State('entry-preview-table-remove', 'data')
    ]
)
def display_remove_preview_table(start_date, start_month, start_year,
                                 end_date, end_month, end_year,
#                                  data_previous, data
                                ):
      
    
    remove_preview_df = df.copy()
    remove_preview_df['date'] = pd.to_datetime(remove_preview_df['date'])
    start_day = f"{start_year}-{start_month}-{start_date}"
    end_day = f"{end_year}-{end_month}-{end_date}"

    remove_preview_df = remove_preview_df[(remove_preview_df['date'] >= start_day) & 
                                          (remove_preview_df['date'] <= end_day)]

    remove_preview_df['date'] = remove_preview_df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
    # update sum when table changes
#     if data_previous != data:
#         remove_preview_df = pd.DataFrame.from_records(data).iloc[:-1]
    
    
    remove_preview_df = remove_preview_df.append(remove_preview_df.sum(numeric_only=True), ignore_index=True)
    
    remove_preview_df.loc[len(remove_preview_df)-1, 'date'] = 'Sum'
    
    return remove_preview_df.to_dict('records')
    


# add entry radio button
@app.callback(
    Output("entry-option-display", "children"), 
    [Input("entry-radio-button", "value")]
)
def display_add_remove_panel(value):
    if value == 'add':
        return html.Div([
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

            html.Button('Save to Database', 
                        id='entry-save-add', 
                        n_clicks=0, 
                        style={'display':'block'},
                        disabled=True),
            
            html.Br(),
            html.Br(),
            html.Br(),
        ])
            
    else:
        return html.Div([

            html.Div([
                html.Div("From", 
                         style={'width': '10%', 
                                'height':'50%',
                                'display': 'block',
                         }),

                html.Div([
                    dcc.Dropdown(
                        id="entry-start-date-remove",
                        options=[{"label": str(i).zfill(2), "value": str(i).zfill(2)} for i in range(1, 32)],
                        value=utils.today_date.zfill(2),
                        clearable=False
                    ),
                ], style={'width': '20%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Dropdown(
                        id="entry-start-month-remove",
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
                        id="entry-start-year-remove",
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
                        id="entry-end-date-remove",
                        options=[{"label": str(i).zfill(2), "value": str(i).zfill(2)} for i in range(1, 32)],
                        value=utils.today_date,
                        clearable=False
                    ),
                ], style={'width': '10%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Dropdown(
                        id="entry-end-month-remove",
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
                        id="entry-end-year-remove",
                        options=[{"label": i  , "value": i} for i in range(int(utils.first_day_year), datetime.datetime.now().year+1)],
                        value=utils.first_day_year,
                        clearable=False
                    ),
                ], style={'width': '10%', 'display': 'inline-block'})
            ], style={'width': '50%', 'display': 'inline-block'}),


            html.Br(),
            dash_table.DataTable(
                    id='entry-preview-table-remove',
                    columns=[{"name": i, "id": i} for i in utils.display_columns],
                    editable=True,
                    fixed_rows={'headers': True},
                    style_table={'height': 400},
                    style_cell={
                        'minWidth': 80, 'maxWidth': 250, 'width': 80
                    },
                    row_deletable=True,
               ),


            html.Br(),

            html.Button('Save to Database', id='entry-save-remove', n_clicks=0, style={'display':'block'}),
            
            html.Br(),
        ])