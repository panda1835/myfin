import dash_html_components as html
import dash_core_components as dcc
import datetime

import utils

dropdown_option_month = [
    {"label": 'January'  , "value": '01'},
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
    {"label": 'December' , "value": '12'}
]

def date_month_year_dropdown(title, id_dict, value_dict):
    id_date = id_dict['id_date']
    id_month = id_dict['id_month']
    id_year = id_dict['id_year']

    value_date = value_dict['value_date']
    value_month = value_dict['value_month']
    value_year = value_dict['value_year']

    return [
        html.Div(title, 
                style={
                    'width': '10%', 
                    'height':'50%',
                    'display': 'block',
#                       'border': '3px solid green',
                }
        ),
        
        html.Div([
            dcc.Dropdown(
                id=id_date,
                options=[{"label": str(i).zfill(2), "value": str(i).zfill(2)} for i in range(1, 32)],
                value=value_date,
                clearable=False
            ),
        ], style={'width': '15%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id=id_month,
                options=dropdown_option_month,
                value=value_month,
                clearable=False
            ),
        ], style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id=id_year,
                options=[{"label": i  , "value": i} for i in range(int(utils.first_day_year), datetime.datetime.now().year+1)],
                value=value_year,
                clearable=False
            ),
        ], style={'width': '25%', 'display': 'inline-block'})
    ]


def month_year_dropdown(id_dict, value_dict):
    id_month = id_dict['id_month']
    id_year = id_dict['id_year']

    value_month = value_dict['value_month']
    value_year = value_dict['value_year']

    return [
        html.Div([
            dcc.Dropdown(
                id=id_month,
                options=dropdown_option_month,
                value=value_month,
                clearable=False
            ),
        ], style={'width': '18%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id=id_year,
                options=[{"label": i, "value": i} for i in range(int(utils.first_day_year), datetime.datetime.now().year+1)],
                value=value_year,
                clearable=False
            ),
        ], style={'width': '10%', 'display': 'inline-block'}),  
    ]

def type_category_subcategory_dropdown(id_dict, value_dict):

    id_type = id_dict['id_type']
    id_category = id_dict['id_category']
    id_subcategory = id_dict['id_subcategory']

    value_type = value_dict['value_type']
    value_category = value_dict['value_category']
    value_subcategory = value_dict['value_subcategory']

    return [
        html.Div([
            html.Div("Type", 
                    style={'width': '10%', 
                        'height':'50%',
                        'display': 'block',
                    }),
            
            dcc.Dropdown(
                id=id_type,
                options=[{"label": i, "value": i} for i in utils.transaction_list],
                value=value_type,
                clearable=False
            ),
        ], style={'width': '10%', 'display': 'inline-block'}),

        html.Div([
            html.Div("Category", 
                    style={'width': '10%', 
                        'height':'50%',
                        'display': 'block',
                    }),
            
            dcc.Dropdown(
                id=id_category,
                value=value_category,
                clearable=False
            ),
        ], style={'width': '20%', 'display': 'inline-block'}),

        html.Div([
            
            html.Div("Sub-category", 
                    style={
                        'display': 'block',
                    }),
            
            dcc.Dropdown(
                id=id_subcategory,
                value=value_subcategory,
                clearable=False
            ),
        ], style={'width': '20%', 'display': 'inline-block'})
    ]
            