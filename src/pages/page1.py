import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
from pages.navbar import header_menu, CONTENT_STYLE

dash.register_page(__name__, path='/', name='Homepage')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("TwitterPolitics: A Journey into Digital Discourse", style={"textAlign": "center", "margin-top": "2rem", 'font-weight': 'bold', 'color': 'black'}),
            html.H3(
                """
                From lively debates to the rise of polarizing opinions, Twitter has been the stage for political conversations. We invite you on an exploration to unearth the impact of keywords on these digital interactions and the intriguing patterns they reveal.
                """,
                className="lead",
                style={"marginTop": "40px", "fontSize": "20px", "textAlign": "center"},
            ),
            html.Br(),
            html.H2('The Stages of Our Investigation', style={'textAlign': 'center', 'font-weight': 'bold', 'color': 'black'}),
            html.Br(),
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.Img(src=r'assets/twitter_funnel copia.png', alt='image', height="100%", width="100%")
        ], width=6),
        dbc.Col([
            html.Br(),
            html.H4("""Our focus converges on three distinct yet interconnected levels:"""),
            html.Br(),
            html.H5("""1. Twitter Network:"""),
            html.P(
                """Our journey starts with a broad overview of the Twitter network, encapsulating a pivotal four-month period - from the onset of the presidential debates in October 2020 to the day following the Capitol Hill riot on January 6th, 2021."""),
            html.P(
                "This initial phase offers a wealth of insights about the general debate on Twitter, including key metrics like the most active and mentioned users."),
            html.Br(),
            html.H5("""2. Inter-Communities:"""),
            html.P(
                """As we delve deeper, we turn our attention to the interplay between communities. Leveraging the Greedy Modularity Community algorithm, we've identified user communities based on the most common keywords."""),
            html.P(
                "Our primary objective here is to gauge the polarization level of the political discourse across these communities."),
            html.Br(),
            html.H5("""3. Intra-Communities:"""),
            html.P(
                """Finally, we zoom in to examine the intra-community dynamics. Is there a pattern of homophily influencing members within the same community? Do similar communities exhibit similar levels of agreement?"""),
        ], width=6)
    ], style={'marginTop': '30px', 'marginBottom': '30px'}),

    dbc.Row([
        dbc.Col([
            html.H4(children="Ready to dive into our findings? Proceed to the next sections!",
                    style={'textAlign': 'center', 'font-weight': 'bold', 'color': 'black'})], width={'size': 12})
    ], style={'marginTop': '30px', 'marginBottom': '40px'}),

], style= CONTENT_STYLE, fluid=True)
