import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
import os

#setting the path to call datasets and images 
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
dname = dname.replace("\\", "/")
os.chdir(dname)

HEADER_STYLE = {
    "width": "100%",
    "height": "4rem",
    "padding": "0.5rem 1rem",
    "background-color": "#1da1f2",
    "display": "flex",
    "align-items": "center",
    "justify-content": "space-between",
    "box-shadow": "0 4px 6px 0 rgba(0, 0, 0, 0.2)",
}

CONTENT_STYLE = {
    "margin-top": "4rem",  # Adjust this value to match the height of your header
}


navbar_menu = dbc.Nav(
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

header_menu = html.Div(
    [
        html.Div([
            html.Img(src='assets/twitter_logo.png', alt="Twitter Logo",
                     style={"width": "2rem", "height": "2rem"}),
        ], style={"flex": "1"}),
        html.Div([
            navbar_menu
        ], style={"flex": "2"}),
        html.Div([
            html.Span(" ", style={"width": "2rem", "height": "2rem"})
        ], style={"flex": "1"}),
    ],
    style=HEADER_STYLE,
    className="sidebar",
)
