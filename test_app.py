# -*- coding: utf-8 -*-
"""
Created on Mon May 28 13:11:08 2018

@author: droesj
"""

#%%
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
#import dash_table_experiments as dt
import pandas as pd
from textwrap import dedent




data_frame = pd.read_csv(r'property_small_database.csv', sep = ";")
data_frame.rename( columns={'Unnamed: 0':'Property number'}, inplace=True )


app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True
app.layout = html.Div([
        html.H1('Pararius.nl property analysis'),
        html.Div(
                dcc.Tabs(
                        tabs=[{'label': 'Property Price Map', 'value': 1},
                              {'label': 'Property Aspect predictor', 'value': 2},
                              {'label': 'Property Price Prediction', 'value': 3},
                              {'label': 'Data visualization', 'value': 4} ,
                              {'label': 'Data Table', 'value': 5}
                        ],
            value=1,
            id='tabs',
            vertical=True,
            style={
                'height': '100vh',
                'borderRight': 'thin lightgrey solid',
                'textAlign': 'center'
            }
        ),
        style={'width': '17%', 'float': 'left'}
    ),
    html.Div(
            html.Div(id='tab-output'),
            style={'width': '83%', 'float': 'right'}
    ),
    
], style={
    'width': '83%',
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
                html.H1('Property price map',
                        style = {'width': '100%',
                                 'textAlign': 'center' }),
                html.Div(id='text-content',
                         style={'width': '70%',
                                'textAlign': 'center'}
                         ),
                html.Div(id='property-details',
                         style={'width': '30%', 
                                'float': 'right',
                                'margin-left': '10px'}),
                dcc.Graph(id='map', figure={
                    'data': [{
                        'lat': data_frame['Latitude'],
                        'lon': data_frame['Longitude'],
                        'marker': {
                            'color': data_frame['Price'],
                            'size': 11,
                            'opacity': 0.7,
                            'colorscale': 'Jet',
                            'colorbar': {
                                    'thicknessmode': 'fraction',
                                    'title': 'Price range',
                                    'titlefont': {'family':'Sans-Serif', 'size': 17},
                                    'ticks': 'outside',
                                    'nticks': 20,
                                    'xanchor': 'right',
                                    'x': 1.02,
                                    'outlinewidth': 0,
                                    'tickfont':{'family':'Sans-Serif','size': 14},
                                    'xpad': 0,
                                    
                                    }
                        },
                        'text': data_frame['Street'],
                        'customdata': data_frame['Property number'],
                        'type': 'scattermapbox',
                        
                    }],
                    'layout': {
                        'autosize': True,
                        'mapbox': {
                            'center':{'lat':52.35211, 'lon': 4.88773},
                            'zoom': 10.8,
                            'accesstoken': 'pk.eyJ1IjoiZHJvZXNqIiwiYSI6ImNqaHFiYTBoZzAwMXUzN3F0dXBhOXMwY3IifQ.tgd10h6uc8XViS1NZMcPnw'
                        },
                        'hovermode': 'closest',
                        'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}
                    }
                },
                style={'width': '70%'}),
                
        ]),
    

    elif value == 2:
        return html.Div([
                html.Div('Predictor tab')
        ])
    elif value == 4:
        return html.Div([
                html.Div('Data viz tab')
        ])
    elif value == 5:
        return html.Div([html.Table(
                [html.Tr([html.Th(col) for col in data_frame.columns])] + 
                [html.Tr([
                        html.Td(data_frame.iloc[i][col]) for col in data_frame.columns
                        ]) for i in range(min(len(data_frame), len(data_frame)))])
                    ])
    
                
    
@app.callback(
        dash.dependencies.Output('text-content', 'children'),
        [dash.dependencies.Input('map', 'hoverData')]
        )
        
def update_text(hoverData):
    s = data_frame[data_frame['Property number'] == hoverData['points'][0]['customdata']]
    return html.H3(
            '{}'.format(
                    s.iloc[0]['Street'],
                    )
            )          

@app.callback(
        dash.dependencies.Output('property-details', 'children'),
        [dash.dependencies.Input('map', 'hoverData')]
        )
        
def update_details(hoverData):
    s = data_frame[data_frame['Property number'] == hoverData['points'][0]['customdata']]
    return dcc.Markdown(dedent('''
                        ### Price: €{},- 
                        
                        ###### Property type: {}
                        
                        ###### Neigbourhood: {}
                        
                        ###### Year built: {}

                        ###### Total Surface: {}m² 
                        
                        ###### Total volume: {}m³
                        
                        ###### Number of (bed)rooms: {} ({}) 
                        
                        ###### Garden: {}
                                                
                        ###### [Link to page]({})
                        '''.format(
                        '{0:,}'.format(s.iloc[0]['Price']),
                        s.iloc[0]['Type'],
                        s.iloc[0]['Neighbourhood'],
                        s.iloc[0]['Year built'],
                        s.iloc[0]['Surface (m²)'],
                        s.iloc[0]['Total volume (m³)'],
                        s.iloc[0]['Number of rooms'],
                        s.iloc[0]['Number of bedrooms'],
                        s.iloc[0]['Garden'].lstrip("'[").rstrip("]'"),
                        s.iloc[0]['Link']
                        )))
    
        
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})       


if __name__ == '__main__':
    app.run_server(debug=True)