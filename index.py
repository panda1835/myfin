import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output

from app import app
from apps import accounts, entry, information, overview, transaction

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
        html.H2("Sidebar", className="display-sidebar"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/overview", active="exact"),
                dbc.NavLink("Transactions", href="/transaction", active="exact"),
                dbc.NavLink("Accounts", href="/accounts", active="exact"),
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


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/accounts':
        return accounts.layout
    elif pathname == '/entry':
        return entry.layout
    elif pathname == '/information':
        return information.layout
    elif pathname == '/overview':
        return overview.layout
    elif pathname == '/':
        return overview.layout
    elif pathname == '/transaction':
        return transaction.layout
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
