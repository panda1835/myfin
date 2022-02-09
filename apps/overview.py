import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import calendar
import datetime

from app import app

import create_plot
import utils
import utils_plotly
import init_database

df = init_database.init_database()

def layout():
    return html.Div([
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
        
        # --------- From ---------
        html.Div(
            utils_plotly.date_month_year_dropdown(
                "From",
                {
                    "id_date": "start-date-pie",
                    "id_month": "start-month-pie",
                    "id_year": "start-year-pie"
                },
                {
                    "value_date": utils.first_day_date.zfill(2),
                    "value_month": utils.first_day_month,
                    "value_year": utils.first_day_year
                }
            ), style={'width': '50%', 'display': 'inline-block'}
        ),
        #---------- To ---------
        html.Div(
            utils_plotly.date_month_year_dropdown(
                "To",
                {
                    "id_date": "end-date-pie",
                    "id_month": "end-month-pie",
                    "id_year": "end-year-pie"
                },
                {
                    "value_date": utils.today_date,
                    "value_month": utils.today_month,
                    "value_year": utils.today_year,
                }
            ), style={'width': '50%', 'display': 'inline-block'}
        ),
            
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

