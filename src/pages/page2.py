import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import os


#setting the path to call datasets and images 
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
dname = dname.replace("\\", "/")
os.chdir(dname)

dash.register_page(__name__, name='6th of January')

# Assuming you have a DataFrame named df
# For demonstration purposes, I'm using a sample DataFrame
most_actimel = pd.read_csv("data/most_actimel.csv")
most_mentos = pd.read_csv("data/most_mentos.csv")



@callback(
    [Output(component_id='users_barplot', component_property='figure')],
    [Input(component_id='dummy-input', component_property='value')]
)

def update_output(dummy_value):
    # Top 5 Keywords Bar Plot
    users_barplot = insights_plot
    return users_barplot

def create_most_plot():
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Most Active Users", "Most Mentioned Users"))

    fig.add_trace(
        go.Bar(x=most_actimel.most_active_users, y=most_actimel.value),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=most_mentos.most_mentioned_users, y=most_mentos.value),
        row=1, col=2
    )

    fig.update_layout(
        showlegend=False,

    )

    return fig


#most_active_users, most_mentioned_users = extract_insights(df)
insights_plot = create_most_plot()

layout=dbc.Container([

    # Eye-catching title
    dbc.Row([
        dbc.Col([
            html.H1('The 6th of January: Decoding Democracy Through Twitter',
                    style={'textAlign': 'center', "color" : "black", 'font-weight': 'bold'}),
            html.P("""What if we told you that the heartbeat of democracy could be traced in 280 characters or less? 
            From October 2020 to January 2021, we delved into the vibrant and volatile world of Twitter to dissect the discourse around the infamous U.s. presidential election of 2020. 
            Welcome to a digital exploration that uncovers the unexpected and confronts the unimaginable.""",
                   style={'textAlign': 'center', "color" :"black", 'font-size': '20px'})
        ], width=12)
    ]),

    # Visually striking image
    dbc.Row([
        dbc.Col([
            html.Img(src=r'assets/Poster_Unleash_def.png', alt='image', style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '70%'}),
            html.P("""
                    This infographic provides a deep investigation of Twitter activity during the critical period from October 2020 to January 6, 2021. This period marked a crucial time in U.S. politics, witnessing an unprecedented level of discourse on the digital stage. The focus of our analysis is on the ego networks of Twitter, which represent intricate structures of interaction centered around influential individuals, or 'egos'. These influencers play a significant role in shaping the dialogue within their networks, thereby influencing the patterns of agreement and disagreement that were particularly noticeable during this remarkable time. 
                    The first visualization in our study provides an insightful snapshot of these ego networks, illuminating the nature of political conversations in the online space during this crucial period. Our analysis aims to shed light on the dynamics of these discussions, thereby contributing to a broader understanding of the significant role social media plays in shaping public opinion and influencing political discourse.
                """, style={'textAlign': 'center', "color": "black", 'font-size': '16px'})
        ], width=12)
    ], align="center"),

    html.Div(style={'height':'30px'}),

    # Data Insights title
    dbc.Row([
        dbc.Col([
            html.H3('Insights from the Digital Battlefield', style={'textAlign': 'center', "color" : "black", 'font-weight': 'bold'}),
            html.P("Beyond the hashtags and retweets, Twitter holds a mirror to society. Our analysis reveals startling patterns and influential actors who steer the currents of conversation.")
        ], width=12)
    ]),

    # Data Insights
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=insights_plot),
            html.P("Step into the heart of the conversation with these key insights:", style={'textAlign': 'center', "color" :"black", 'font-size': '20px'}),
        ],width={'size':8, 'offset':2,'order':1}),
    ]),

    html.Div(style={'height':'30px'}),

    # Back to main page link
    dbc.Row([
        dbc.Col([
            dcc.Link('Venture Back to Main Page', href='/', style={'textAlign': 'center', 'display': 'block', 'color': 'blue'})
        ], width=12)
    ]),

    html.Div(style={'height':'30px'}),

    dbc.Row([
        dbc.Col([dcc.Input(id='dummy-input', type='hidden', value='dummy')], width=12)
    ])
])
