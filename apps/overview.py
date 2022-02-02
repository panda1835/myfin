import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import calendar
import datetime

from app import app

import create_plot
import utils
import init_database

df = init_database.init_database()

layout = html.Div([
    html.Div([
        html.H2(f"Expenses for Necessity in {calendar.month_name[int(utils.today_month)]}"),
                    
        dcc.Graph(figure=create_plot.create_expenses_by_category(df, ['Food', 
                                                            'Drink', 
                                                            'Transportation', 
                                                            'Personal', 
                                                            'Household Items',
                                                            'Fees'], utils.today_month, utils.today_year))

    ], style={'width': '48%', 'display': 'inline-block'}),
    
    # ----------------------- Graph 02 -----------------------
    
    html.Div([
        html.H2(f"Expenses for Entertainment & Education in {calendar.month_name[int(utils.today_month)]}"),
        
        dcc.Graph(figure=create_plot.create_expenses_by_category(df, ['Education',
                                                            'Entertainment'], utils.today_month, utils.today_year))
        
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    # ----------------------- Graph 03 -----------------------
    html.Div([
        html.H2("Monthly Expenses"),
                    
        dcc.Graph(figure=create_plot.create_plot_for_category(df))

    ], style={'width': '48%', 'display': 'inline-block'}),
    
    # ----------------------- Graph 04 -----------------------
    html.Div([
        html.H2("Expenses by Category"),
        
        # ---------
        html.Div([
            html.Div("From", 
                        style={'width': '10%', 
                            'height':'50%',
                            'display': 'block',
#                                   'border': '3px solid green',
                        }),
            
            html.Div([
                dcc.Dropdown(
                    id="start-date-pie",
                    options=[{"label": str(i).zfill(2), "value": str(i).zfill(2)} for i in range(1, 32)],
                    value=utils.first_day_date.zfill(2),
                    clearable=False
                ),
            ], style={'width': '15%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id="start-month-pie",
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
                    value=utils.first_day_month,
                    clearable=False
                ),
            ], style={'width': '30%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id="start-year-pie",
                    options=[{"label": i  , "value": i} for i in range(int(utils.first_day_year), datetime.datetime.now().year+1)],
                    value=utils.first_day_year,
                    clearable=False
                ),
            ], style={'width': '25%', 'display': 'inline-block'})
        ], style={'width': '50%', 'display': 'inline-block'}),
        #----------
        
        html.Div([
            html.Div("To", 
                        style={'width': '10%', 
                            'height':'50%',
                            'display': 'block',
                        }),

            html.Div([
                dcc.Dropdown(
                    id="end-date-pie",
                    options=[{"label": str(i).zfill(2), "value": str(i).zfill(2)} for i in range(1, 32)],
                    value=utils.today_date,
                    clearable=False
                ),
            ], style={'width': '15%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id="end-month-pie",
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
            ], style={'width': '30%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id="end-year-pie",
                    options=[{"label": i  , "value": i} for i in range(int(utils.first_day_year), datetime.datetime.now().year+1)],
                    value=utils.today_year,
                    clearable=False
                ),
            ], style={'width': '25%', 'display': 'inline-block'})
        ], style={'width': '50%', 'display': 'inline-block'}),
            
        dcc.Graph(id='category-pie')
        
    ], style={'width': '48%', 'display': 'inline-block'}),
])


# category pie chart
@app.callback(
    Output("category-pie", "figure"), 
    [Input("start-date-pie", "value"), 
     Input("start-month-pie", "value"),
     Input("start-year-pie", "value"), 
     Input("end-date-pie", "value"),
     Input("end-month-pie", "value"), 
     Input("end-year-pie", "value")]
)
def display_category_pie_chart(start_date, start_month, start_year,
                               end_date, end_month, end_year):

    return create_plot.create_category_pie_chart(df, f"{start_year}-{start_month}-{start_date}", 
                                         f"{end_year}-{end_month}-{end_date}")

