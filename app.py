# -*- coding: utf-8 -*-
"""
Created on Mon May 28 13:11:08 2018

@author: droesj
"""


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
#import dash_table_experiments as dt
import pandas as pd
from textwrap import dedent
import plotly.graph_objs as go


mapbox_access_token = 'pk.eyJ1IjoiZHJvZXNqIiwiYSI6ImNqaHFiYTBoZzAwMXUzN3F0dXBhOXMwY3IifQ.tgd10h6uc8XViS1NZMcPnw'

data_frame = pd.read_csv(r'property_database_final.csv', sep = ";")
data_frame.rename( columns={'Unnamed: 0':'Property number'}, inplace=True )
data_frame = data_frame[data_frame.Price < 2500000]
data_frame = data_frame[data_frame["Surface (m²)"]< 1000]
data_frame = data_frame[data_frame["Total volume (m³)"]< 20000]


neighbourhood_data_url = 'https://kaart.amsterdam.nl/datasets/datasets-item/t/buurtcombinatiegrenzen-1/export/json'
neighbourhood_data = pd.read_json(neighbourhood_data_url)
neighbourhoods = []


#load data for Neighbourhood map
mean = data_frame.groupby(["Neighbourhood"],).mean()["Price"]
for nh in range(len(neighbourhood_data['features'])):
    neighbourhood = neighbourhood_data['features'][nh]['properties']['NAAM']
    if neighbourhood not in list(set(data_frame["Neighbourhood"])):
        continue
    else:
        geo_data = neighbourhood_data['features'][nh]['properties']['locatie']
        neighbourhoods.append({'Neighbourhood': neighbourhood,
                               'Geo_data': geo_data,
                               'Mean price':mean[neighbourhood]
                               })

    nh_data_frame = pd.DataFrame(neighbourhoods)

    
    
    
#initialize the app    
app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})
    
#create basic layout
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
            style={'width': '83%', 
                   'float': 'right',
                   }
    ),
    
], style={
    'width': '83%',
    'fontFamily': 'Arial',
    'margin-left': 'auto',
    'margin-right': 'auto'
})

@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_tab_content(value):
    if value == 3:
        return html.Div([
            html.Div(
                    dcc.Dropdown(id = 'prediction-menu',
                        options = [
                                {'label': 'Total Surface (m2)', 'value': 'space'},
                                {'label': 'Total volume (m3)', 'value': 'volume'},
                                {'label': 'Number of rooms', 'value': 'rooms'},
                                #{'label': 'Neighbourhood', 'value': 'nh'},
                                {'label': 'property type', 'value': 'type'},
                                ],
                        multi = True,
                        value = 1
                            )),
            html.Div(id = 'dynamic-prediction-input-surface', 
                     style ={'width':'80%',
                             'marginBottom': 50,
                             'marginTop': 20,
                             'margin-left': 'auto',
                             'margin-right': 'auto'}),
            html.Div(id = 'dynamic-prediction-input-volume',
                     style ={'width':'80%',
                             'marginBottom': 50,
                             'marginTop': 20,
                             'margin-left': 'auto',
                             'margin-right': 'auto'}),
            html.Div(id = 'dynamic-prediction-input-rooms',
                     style ={'width':'80%',
                             'marginBottom': 50,
                             'marginTop': 20,
                             'margin-left': 'auto',
                             'margin-right': 'auto'}),
            html.Div(id = 'dynamic-prediction-input-type',
                     style ={'marginBottom': 50,
                             'marginTop': 20,
                             'margin-left': 'auto',
                             'margin-right': 'auto'}),
            html.Button('Submit', id='button',
                        style = {
                             'horizontalAllign': 'middle'}),
            html.Div(id = 'price-prediction-output', 
                     children = "select values and press submit",
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
                            'color': data_frame.Price,
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
                            'accesstoken': mapbox_access_token
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
                html.Div('Data viz tab'),
                dcc.Dropdown(id = 'data-viz-menu',
                             options = [
                                     {'label': 'average price map', 'value': 1},
                                     {'label': 'graphs', 'value' :2},
                                     {'label': 'add something', 'value':3}
                                     ]),
                    html.Div(id = 'data-viz-content')
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

@app.callback(
        dash.dependencies.Output('dynamic-prediction-input-surface', 'children'),
        [dash.dependencies.Input('prediction-menu', 'value')]
        )
def display_prediction_input_surface(values):
    
    if 'space' in values:
        min_surf = min(data_frame["Surface (m²)"])
        max_surf = max(data_frame["Surface (m²)"])
        return html.Div([
                html.H4('Total surface Slider'),
                dcc.Slider(id = 'surface-slider',
                           min = min_surf,
                           max = max_surf,
                           value = 50,
                           step = 1,
                           marks = {str(i):'{}'.format(i) for i in range(min_surf,max_surf,10)}
                           )
                ])

@app.callback(
        dash.dependencies.Output('dynamic-prediction-input-volume', 'children'),
        [dash.dependencies.Input('prediction-menu', 'value')]
        )
def display_prediction_input_volume(values):
    if 'volume' in values:
        min_vol = min(data_frame["Total volume (m³)"])
        max_vol = max(data_frame["Total volume (m³)"])
        return html.Div([
                html.H4('Total Volume Slider'),
                dcc.Slider(id = 'volume-slider',
                           min = min_vol,
                           max = max_vol,
                           value = 250,
                           step = 1,
                            marks = {str(i):'{}'.format(i) for i in range(min_vol,max_vol,100)},
                           )
                ])
@app.callback(
        dash.dependencies.Output('dynamic-prediction-input-rooms', 'children'),
        [dash.dependencies.Input('prediction-menu', 'value')]
        )
def display_prediction_input_rooms(values):
    if 'rooms' in values:
        min_room = min(data_frame['Number of rooms'])
        max_room = max(data_frame['Number of rooms'])
        return html.Div([
                html.H4('Desired number of rooms'),
                dcc.Slider(id = 'room-slider',
                           min = min_room,
                           max = max_room,
                           value = 2,
                           step = 1,
                           marks = {str(i):'{}'.format(i) for i in range(min_room,max_room)},
                           )
                ])
@app.callback(
        dash.dependencies.Output('dynamic-prediction-input-type', 'children'),
        [dash.dependencies.Input('prediction-menu', 'value')]
        )

def display_prediction_input_type(values):        
    if 'type' in values:
        type_list = list(set(data_frame["Type"]))
        return html.Div([
                html.H4('Property type'),
                dcc.RadioItems(id = 'property-type',
                options = [{'label':type_list[0],'value' : 1},
                           {'label':type_list[1],'value' : 2},
                           {'label':type_list[2],'value' : 3},
                           {'label':type_list[3],'value' : 4},
                           {'label':type_list[4],'value' : 5},
                           {'label':type_list[5],'value' : 6},
                           ]
                )           
        ])


@app.callback(
        dash.dependencies.Output('price-prediction-output', 'children'),
        [dash.dependencies.Input('Button', 'n_clicks')],
        [dash.dependencies.State('dynamic-prediction-input-surface', 'value'),
         ])

def Price_predictor(n_clicks, value):
    return  html.H4('The input value was{} and the button was clicked {} times'.format(
            value,
            n_clicks))



@app.callback(
        dash.dependencies.Output('data-viz-content', 'children'),
        [dash.dependencies.Input('data-viz-menu', 'value')]
        )

def data_viz_input(value):  
    if value == 1:
        return 
    dcc.Graph(id = 'map_2',
              figure = {
                      'data':[{
                              'scattermapbox': {
                                      'lat':45.5017,
                                      'lon':-73.5673,
                                      'mode': 'markers',},
                              'color': nh_data_frame['Mean price']
                                 }],
                    'layout': {
                        'autosize': True,
                        'mapbox': {
                            'layers' :{'sourcetype': 'geojson',
                                       'source': 'https://kaart.amsterdam.nl/datasets/datasets-item/t/buurtcombinatiegrenzen-1/export/json',
                                       'type':'fill',
                                       'color': nh_data_frame['Mean price']
                                       },
                            'center':{'lat':52.35211, 'lon': 4.88773},
                            'zoom': 10.8,
                            'accesstoken': mapbox_access_token}
                        }
                        }
                         )
    if value == 2:
        return 
    dcc.Graph(id = 'scatterplot',
              figure = {
                      'data':[
                              go.Scatter(
                                      x = data_frame["Surface (m²)"],
                                      y = data_frame.Price,
                                      mode= 'markers',
                                      opacity = 0.7,
                                      marker = {'size': 10,
                                                'color': data_frame.Neighbourhood}
                                 )],
                    'layout': {go.Layout(
                            xaxis={'title': 'Surface (m²)'},
                            yaxis={'title': 'Price in Euro'},
                            hovermode='closest'
                        )}
                        }
                        )


if __name__ == '__main__':
    app.run_server(debug=True)

