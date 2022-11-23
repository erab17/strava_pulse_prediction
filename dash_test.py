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
df = pd.read_sql_query("SELECT * FROM activities", conn)
conn.close()

# create dash app
app = dash.Dash(__name__)

colors = {'background': '#111111', 'text': '#7FDBFF'}

# create layout
app.layout = html.Div([
    html.H1('Strava Dashboard', style={'textAlign': 'center', 'color': colors['text']}),
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
    dcc.Slider(
        id='year--slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(date): str(date) for date in df['year'].unique()},
        step=None
    ),
    html.Div([
        dcc.Input(id='input-box', type='text'),
        html.Div(id='test_div')
        ])
])

@app.callback(
    Output(component_id='test_div', component_property='children'),
    [Input(component_id='input-box', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

# create callback for graph
@app.callback(
    Output('graph', 'figure'),
    [Input('xaxis', 'value'),
        Input('yaxis', 'value'),
        Input('year--slider', 'value')])
def update_graph(xaxis_name, yaxis_name, year_value):
    dff = df[df['year'] == year_value]
    traces = []
    for activity_type in dff['type'].unique():
        df_by_type = dff[dff['type'] == activity_type]
        traces.append(go.Scatter(
            x=df_by_type[xaxis_name],
            y=df_by_type[yaxis_name],
            text=df_by_type['name'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=activity_type,
            # add additional data to hover over points on graph 
            customdata = df_by_type[['name', 'distance', 'moving_time',
             'type', 'start_date','suffer_score']],
             # add customdata to hovertemplate
            hovertemplate = '<b>%{text}</b><br><br>' +
                            'suffer_score: %{customdata[5]}<br>' +
                            'date: %{customdata[4]}<br>' +
                            'Name: %{customdata[3]}<extra></extra>'
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': xaxis_name},
            yaxis={'title': yaxis_name},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest',
        )

    }

# run app
if __name__ == '__main__':
    app.run_server(debug=True)
    
