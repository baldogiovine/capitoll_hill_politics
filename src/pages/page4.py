import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import json
import networkx as nx
import plotly.express as px
import os
import matplotlib.pyplot as plt
cmap = plt.get_cmap('viridis')

#setting the path to call datasets and images 
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
dname = dname.replace("\\", "/")
os.chdir(dname)

dash.register_page(__name__, name='Relationships')


# Read CSV data
data_files = os.listdir('data')
keywords = [f[10:-4] for f in data_files if f.startswith('community_') and f.endswith('.csv')]

# Convert the CSV files to dataframes
result_dfs_edge_betweenness = {}

for keyword in keywords:
    result_dfs_edge_betweenness[keyword] = pd.read_csv(f"data/community_{keyword}.csv")

layout = dbc.Container([
    # Rest of your layout code...
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='keyword-dropdown',
                options=[{"label": kw, "value": kw} for kw in result_dfs_edge_betweenness.keys()],
                value=keywords[0],
                clearable=False,
            ),
        ], width={'size':6, 'offset':3}, style={'marginBottom': '30px'})
    ]),

    # Rest of your layout code...
], fluid=True)
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Unraveling Relationships: A Keyword-Centric Network',
                    style={'textAlign': 'center', 'font-weight': 'bold', 'color': 'black', 'marginBottom': '30px'}),
            html.P("""Step into the network of discourse. Here, we illuminate the complex web spun by communities as 
            they engage with different keywords. Our graph, rooted in edge betweenness, reveals the intricate connections between communities. 
            Select a keyword from the dropdown menu below and let the exploration begin!",
                   """,
                    style={'textAlign': 'center', 'color': 'black', 'font-size': '20px', 'marginBottom': '20px'}),

        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='keyword-dropdown',
                options=[{"label": kw, "value": kw} for kw in result_dfs_edge_betweenness.keys()],
                value=keywords[0],
                clearable=False,
            ),
        ], width={'size': 6, 'offset': 3}, style={'marginBottom': '30px'})
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='network-graph'),
        ], width=12)
    ], style={'marginBottom': '30px'}),

    dbc.Row([
        dbc.Col([
            dcc.Link('Eager for more insights? Return to the main page', href='/')
        ], width=12, style={'textAlign': 'center', 'marginBottom': '30px', 'marginTop': '30px'}),
    ]),
], fluid=True)


def get_most_active_user(df, modularity_class):
    # Filter dataframe for specific modularity class
    df_filtered = df[(df['SourceModularity'] == modularity_class) |
                     (df['TargetModularity'] == modularity_class)]

    # Count the number of posts for each user
    user_counts = df_filtered['originalUsernamePost'].value_counts()

    # The most active user is the one with the most posts
    most_active_user = user_counts.idxmax()

    return most_active_user


def create_network_graph(keyword, df):
    # Group the data by SourceModularity and TargetModularity
    grouped = df.groupby(['SourceModularity', 'TargetModularity'])
    filtered_groups = [(name, group) for name, group in grouped if name[0] != name[1]]

    # Create a NetworkX graph from the filtered DataFrame
    G = nx.from_pandas_edgelist(
        pd.concat([group for _, group in filtered_groups]),
        'SourceModularity',
        'TargetModularity',
        edge_attr=['agreement', 'edge_bet'],  # Add 'agreement' and 'edge_bet' attributes
        create_using=nx.DiGraph()
    )
    pos = nx.spring_layout(G, seed=42)

    # Colors for nodes and edges
    colors = {-1: "red", 1: "green"}
    edge_colors = [colors[G.edges[edge]['agreement']] for edge in G.edges]  # Get color for each edge
    size = [G.edges[edge]['edge_bet'] * 10 for edge in G.edges]

    nodes = list(G.nodes)
    # Create a dictionary mapping each node to a color from the colormap
    node_colors = {node: cmap(i / len(nodes)) for i, node in enumerate(nodes)}
    # Create node trace
    node_trace = go.Scatter(
        x=tuple(pos[node][0] for node in G.nodes),  # Convert to tuple
        y=tuple(pos[node][1] for node in G.nodes),  # Convert to tuple
        text=[get_most_active_user(df, node) for node in G.nodes],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            color=[node_colors[node] for node in G.nodes],  # Use node_colors
            size=size,
            line_width=2
        )
    )
    # Create edge trace
    edge_traces = []

    for edge in G.edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_color = colors[G.edges[edge]['agreement']]

        edge_trace = go.Scatter(
            x=[x0, x1, None],  # List of x-coordinates
            y=[y0, y1, None],  # List of y-coordinates
            line=dict(width=0.5, color=edge_color),  # Line color for this edge
            hoverinfo='none',
            mode='lines'
        )

        edge_traces.append(edge_trace)
    # Create a Plotly figure
    fig = go.Figure(
        data=[*edge_traces, node_trace],  # Unpack edge_traces and add node_trace
        layout=go.Layout(
            title=f'Network Graph for Keyword "{keyword}"',
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )

    return fig

# Define the callback for updating the network graph
@callback(
    Output('network-graph', 'figure'),
    Input('keyword-dropdown', 'value')
)
def update_graph(selected_keyword):
    # Get the DataFrame for the selected keyword
    df = result_dfs_edge_betweenness[selected_keyword]

    # Create the network graph for the selected keyword
    figure = create_network_graph(selected_keyword, df)

    return figure
