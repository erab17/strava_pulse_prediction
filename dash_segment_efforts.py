# create dash dash board with dash and plotly libraries 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

import sqlite3
import pandas as pd

# get data from acitivities table in strava.db
conn = sqlite3.connect('strava.db')
df = pd.read_sql_query("SELECT * FROM segment_efforts", conn)
conn.close()

# create dash app
app = dash.Dash(__name__)

# create a drop down with with the unique names in segment_name column
segment_names = df['segment_name'].unique()
segment_names = [{'label': i, 'value': i} for i in segment_names]

# create layout
app.layout = html.Div([
    html.H1('Strava Dashboard', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis',
                options=[{'label': i, 'value': i} for i in df.columns],
                value='distance'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='yaxis',
                options=[{'label': i, 'value': i} for i in df.columns],
                value='moving_time'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='graph'),
    html.Div([
        dcc.Dropdown(
            id='segment_name',
            options=segment_names,
            value='Boulder Creek Trail'
        )
    ]),
    dcc.Graph(id='segment_graph')
], style={'width': '49%'})

# create callback for graph
@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='xaxis', component_property='value'),
    Input(component_id='yaxis', component_property='value')]
)
def update_graph(xaxis_name, yaxis_name):
    return {
        'data': [go.Scatter(
            x=df[xaxis_name],
            y=df[yaxis_name],
            text=df['segment_name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            # add code so graph size is not more than 70% of screen width and height 


            xaxis={'title': xaxis_name},
            yaxis={'title': yaxis_name},
            margin={'l': 80, 'b': 40, 't': 10, 'r': 10},
            hovermode='closest'
        )
    }

# create callback for segment graph
@app.callback(
    Output(component_id='segment_graph', component_property='figure'),
    [Input(component_id='segment_name', component_property='value')]
)
def update_segment_graph(segment_name):
    dff = df[df['segment_name'] == segment_name]
    return {
        'data': [go.Scatter(
            x=dff['start_date'],
            y=dff['elapsed_time'],
            text=dff['segment_name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={'title': 'start_date'},
            yaxis={'title': 'Elapsed Time'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
