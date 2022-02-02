import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

import create_plot
import utils
import init_database

df = init_database.init_database()

# read info page
with open('info_page.md', 'r') as f:
    info_content = f.read()

layout = html.Div([
    html.Div([
        dcc.Markdown(info_content)
    ])
])