import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd

from app import app
from apps import assets, entry, information, overview, transaction

import init_database
import utils

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/overview", active="exact"),
                dbc.NavLink("Transactions", href="/transaction", active="exact"),
                dbc.NavLink("Assets", href="/assets", active="exact"),
                dbc.NavLink("Entry", href="/entry", active="exact"),
                dbc.NavLink("Information", href="/information", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    sidebar,
    content
])

update_status_counter = 0
entry_layout = entry.layout()
overview_layout = overview.layout()
transaction_layout = transaction.layout()


def update_db():
    global update_status_counter
    global entry_layout
    global overview_layout
    global transaction_layout

    df = init_database.init_database()
    entry.df = df
    overview.df = df
    transaction.df = df

    entry_layout = entry.layout()
    overview_layout = overview.layout()
    transaction_layout = transaction.layout()

    update_status_counter = entry.update_counter

    # declare first date in the df
    utils.first_day_df = pd.to_datetime(df['date']).min()
    utils.first_day_date = utils.first_day_df.strftime("%d")
    utils.first_day_month = utils.first_day_df.strftime("%m")
    utils.first_day_year = utils.first_day_df.strftime("%Y")
    utils.first_day_df = utils.first_day_df.strftime("%Y-%m-%d")

    # declare most recent date in the df
    utils.last_day_df = pd.to_datetime(df['date']).max()
    utils.last_day_date = utils.last_day_df.strftime("%d")
    utils.last_day_month = utils.last_day_df.strftime("%m")
    utils.last_day_year = utils.last_day_df.strftime("%Y")
    utils.last_day_df = utils.last_day_df.strftime("%Y-%m-%d")

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    # global update_status_counter
    if entry.update_counter != update_status_counter:
        update_db()

    if pathname == '/assets':
        return assets.layout

    elif pathname == '/entry':
        return entry_layout

    elif pathname == '/information':
        return information.layout

    elif pathname == '/overview':
        return overview_layout

    elif pathname == '/':
        return overview_layout

    elif pathname == '/transaction':
        return transaction_layout

    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )

if __name__ == '__main__':
    app.run_server(debug=True)
