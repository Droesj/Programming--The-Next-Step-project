# -*- coding: utf-8 -*-
"""
Created on Mon May 28 11:57:34 2018

@author: Sjoerd Evelo
"""
#%%

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd



#%%
app = dash.Dash()

#data_frame = pd.read_csv('property_database.csv')


app.layout = html.Div([
    html.Div(    
        dcc.Tabs(
            tabs=[
                {'label': 'Data visuaization', 'value': 1},
                {'label': 'Prediction', 'value': 2}
            ],
            value=1,
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
    )
], style={
    'width': '80%',
    'fontFamily': 'Sans-Serif',
    'margin-left': 'auto',
    'margin-right': 'auto'
})




#%%

app = dash.Dash()

app.layout = html.Div([
    html.Label('Dropdown'),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    ),

    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['MTL', 'SF'],
        multi=True
    ),

    html.Label('Radio Items'),
    dcc.RadioItems(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    ),

    html.Label('Checkboxes'),
    dcc.Checklist(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        values=['MTL', 'SF']
    ),

    html.Label('Text Input'),
    dcc.Input(value='MTL', type='text'),

    html.Label('Slider'),
    dcc.Slider(
        min=0,
        max=9,
        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
        value=5,
    ),
], style={'columnCount': 2})

if __name__ == '__main__':
    app.run_server(debug=True)