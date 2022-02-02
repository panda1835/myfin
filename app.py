import dash
import dash_bootstrap_components as dbc
from jupyter_dash import JupyterDash

app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css'], 
                suppress_callback_exceptions=True)

# app = JupyterDash(__name__, 
#                 external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css'], 
#                 suppress_callback_exceptions=True)

app.title = 'My Finance Dashboard'

server = app.server