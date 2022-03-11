from unicodedata import category
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json

import utils
import init_database

df = init_database.init_database()

with open("category.json", 'r') as f:    
    category_dict = json.load(f)

def generate_subcategory(asset_category, asset_subcategory):
    return html.Div([
            # amount
            html.Div([
                html.P(asset_subcategory),
                html.B([
                    f"{df[(df['transaction_type'] == 'Assets') & (df['category'] == asset_category) & (df['sub_category'] == asset_subcategory)]['amount'].sum():,} {category_dict['Assets']['Categories'][asset_category]['Sub-categories'][asset_subcategory]['Unit'][0]}"
                    ])
            ], style={'display':'inline-block', 
                        "height": "30px", 
                        "text-align": "right",
                        "float":"right",
                        }),
            
            html.Hr(
                className="dashed"
            ),
            
        ], style={
            "width":"200px",
            "height":"80px",
            "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)", 
            "border-radius": "5px",
            "padding": "20px 20px",
            'display':'inline-block',
            "margin-right": "20px",
            "margin-bottom": "20px"
        })

def generate_category(asset_category):
    return html.Div([html.H2(asset_category)] + 
        [
        generate_subcategory(asset_category, asset_subcategory) for asset_subcategory in category_dict['Assets']['Categories'][asset_category]['Sub-categories'].keys()       
    ])

def layout():
    return html.Div([
        generate_category(asset_category) for asset_category in category_dict['Assets']['Categories'].keys()
    ])

