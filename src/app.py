import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback
from pages.navbar import CONTENT_STYLE, HEADER_STYLE
import os

#setting the path to call datasets and images 
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
dname = dname.replace("\\", "/")
os.chdir(dname)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME], use_pages=True, suppress_callback_exceptions=True)
server = app.server

# define the navbar

navbar_menu = html.Div(
    [
        html.Div([
            html.Img(src='assets/twitter_logo.png', alt="Twitter Logo",
                     style={"width": "2rem", "height": "2rem"}),
        ], style={"flex": "1"}),
        html.Div([
            dbc.Nav(
                [
                    dbc.NavLink(
                        [
                            html.Div(page["name"], className="ms-2"),
                        ],
                        href=page["path"],
                        active="exact",
                        style={"color": "white", "font-weight": "bold"}
                    )
                    for page in dash.page_registry.values()
                ],
                style={"display": "flex", "justify-content": "center", "align-items": "center"},
            )
        ], style={"flex": "2"}),
        html.Div([
            html.Span(" ", style={"width": "2rem", "height": "2rem"})
        ], style={"flex": "1"}),
    ],
    style=HEADER_STYLE,
    className="sidebar",
)

# layout for all the pages
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col([
                    navbar_menu,
                    ], width={'size':12}, align="center"
                )
            ]
        ),

        html.Hr(),
        dbc.Row(
            [
                dbc.Col([
                    dash.page_container
                ])
            ])
        ], fluid=True, style=CONTENT_STYLE
        )

if __name__ == '__main__':
    app.run_server(debug=True)
