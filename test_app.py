# -*- coding: utf-8 -*-
"""
Created on Mon May 28 13:11:08 2018

@author: droes
"""


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd



#%%
app = dash.Dash(__name__)

data_frame = pd.read_csv('property_database.csv')


app.layout = html.Div([
    html.Div(    
        dcc.Tabs(
            tabs=[
                {'label': 'Property Price Map', 'value': 1},
                {'label': 'Property Price Prediction', 'value': 2},
                {'label': 'Data visualization', 'value': 3} 
            ],
            value=2,
            id='tabs',
            vertical=True,
            style={
                'height': '100vh',
                'borderRight': 'thin lightgrey solid',
                'textAlign': 'left'
            }
        ),
        style={'width': '20%', 'float': 'left'}
    ),
    html.Div(
            html.Div(id='tab-output'),
            style={'width': '80%', 'float': 'right'}
    ),
    
], style={
    'width': '80%',
    'fontFamily': 'Sans-Serif',
    'margin-left': 'auto',
    'margin-right': 'auto'
})

@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):
    if value == 3:
        return html.Div([
            html.Div(
                    dcc.Dropdown(
                        options = [
                                {'label': 'Total Space (m2)', 'value': 1},
                                {'label': 'Total volume (m3)', 'value': 2},
                                {'label': '' }],
                        multi = True,
                        value = 1
                            )
            )
                    ])
        
    elif value == 1:
        return html.Div([
                html.H3('Property price map'),
                html.Div(id='text-content'),
                dcc.Graph(id='map', figure={
                    'data': [{
                        'lat': data_frame['Latitude'],
                        'lon': data_frame['Longitude'],
                        'marker': {
                            'color': data_frame['Price'],
                            'size': 8,
                            'opacity': 0.6
                        },
                        'type': 'scattermapbox'
                    }],
                    'layout': {
                        'mapbox': {
                            'accesstoken': 'pk.eyJ1IjoiZHJvZXNqIiwiYSI6ImNqaHFiYTBoZzAwMXUzN3F0dXBhOXMwY3IifQ.tgd10h6uc8XViS1NZMcPnw'
                        },
                    'hovermode': 'closest',
                    'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}
                }
            })
        ])

    elif value == 2:
        html.Div([
                html.H3('predictor tab')
        ])
                
        
       
        
        


if __name__ == '__main__':
    app.run_server(debug=True)