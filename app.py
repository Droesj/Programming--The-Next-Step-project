# -*- coding: utf-8 -*-
"""
Created on Mon May 28 13:11:08 2018

@author: droesj
"""

# import libraries
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
#import dash_table_experiments as dt
import pandas as pd
import numpy as np
from textwrap import dedent
import plotly.graph_objs as go
from sklearn import linear_model


#Load data
data_frame = pd.read_csv(r'property_database_final.csv', sep = ";")
data_frame.rename( columns={'Unnamed: 0':'Property number'}, inplace=True )

#delete some extreme values
data_frame = data_frame[data_frame["Surface (m²)"]< 1000]
data_frame = data_frame[data_frame["Total volume (m³)"]< 20000]

#Need this to display map
mapbox_access_token = 'pk.eyJ1IjoiZHJvZXNqIiwiYSI6ImNqaHFiYTBoZzAwMXUzN3F0dXBhOXMwY3IifQ.tgd10h6uc8XViS1NZMcPnw'

#Part of the not working neighbourhood price map
# neighbourhood_data_url = 'https://kaart.amsterdam.nl/datasets/datasets-item/t/buurtcombinatiegrenzen-1/export/json'
neighbourhood_data = pd.read_json('geojson_amsterdam.json')
neighbourhoods = []


#load data for Neighbourhood map (that does not work yet)
mean = data_frame.groupby(["Neighbourhood"],).mean()["Price"]
for nh in range(len(neighbourhood_data['features'])):
    neighbourhood = neighbourhood_data['features'][nh]['properties']['naam']
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
                        tabs=[{'label': 'Information tab', 'value':0},
                              {'label': 'Property Price Map', 'value': 1},
                              #{'label': 'Property Aspect predictor', 'value': 2},
                              {'label': 'Property Price Prediction', 'value': 3},
                              {'label': 'Data visualization', 'value': 4} ,
                              {'label': 'Data Table', 'value': 5}
                        ],
            value=0,
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

# Main callback function for the main content
                
                
@app.callback(Output('tab-output', 'children'), 
              [Input('tabs', 'value')])
def display_tab_content(value):
    
    if value == 0:
        #Introduction page with markdown text
        return html.Div([html.Div(dcc.Markdown(dedent('''
                               ### Welcome!
                               
                               ##### This dashboard containins the data of {} properties in Amsterdam.
                               
                               ##### Data is scraped from [Pararius.nl](https://www.pararius.nl) using a slow scraper
                               ##### which you can find at [my Github]( https://github.com/Droesj)
                               
                               ##### Use the Tabs to the left to navigate to different properties, 
                               ##### you can use the submenus to pick out different options. 
                               ##### Currently you can find:
                                    
                               * A property price map with interactive slider and hover functions
                               * a housing price predictor *(under construction)*
                               * Some data visualization *(under construction)*
                               * A table with the raw data
                               
                               ##### Hope you enjoy it!
                
                
                                '''.format(len(data_frame)))
                    ), style ={'width':'80%',
                             'marginBottom': 50,
                             'marginTop': 20,
                             'margin-left': 'auto',
                             'margin-right': 'auto'}
                  )                           
                ])
    
    
    
    
    
    if value == 3:
        #prediction tab, sadly the predictor itself does not work yet...
        return html.Div([
            html.Div(#Dropdown menu at the top
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
                    #Slider 1
            html.Div(id = 'dynamic-prediction-input-surface', 
                     style ={'width':'80%',
                             'marginBottom': 50,
                             'marginTop': 20,
                             'margin-left': 'auto',
                             'margin-right': 'auto'}),
                    #Slider 2
            html.Div(id = 'dynamic-prediction-input-volume',
                     style ={'width':'80%',
                             'marginBottom': 50,
                             'marginTop': 20,
                             'margin-left': 'auto',
                             'margin-right': 'auto'}),
                    #Slider 3
            html.Div(id = 'dynamic-prediction-input-rooms',
                     style ={'width':'80%',
                             'marginBottom': 50,
                             'marginTop': 20,
                             'margin-left': 'auto',
                             'margin-right': 'auto'}),
                    #OPtion selector for house type
            html.Div(id = 'dynamic-prediction-input-type',
                     style ={'marginBottom': 50,
                             'marginTop': 20,
                             'margin-left': 'auto',
                             'margin-right': 'auto'}),
            #Button to fire callback
            html.Button('Submit', id='button',
                        ),
                        #outpur
            html.Div(id = 'price-prediction-output', 
                     children = "select values and press submit",
                     )
                    ])
        #Display the price map
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
                #this contains the map
                html.Div(id = 'map-container',
                         style={'width': '70%'} ),
                html.H4('Select Price range',
                        style = {'width': '70%',
                                 'textAlign': 'center' }),         
                #Price slider
                html.Div(
                        dcc.RangeSlider(id = 'pricerange-map',
                                min = min(data_frame.Price),
                                max = max(data_frame.Price),
                                value = [min(data_frame.Price), max(data_frame.Price)],
                                ),
                        style = {'width': '70%'}),
                html.Div(id = 'pricerange-text',
                         style = {'width': '70%',
                                  'textAlign': 'center'})
                
        ]),
    
    #this is not there
    elif value == 2:
        return html.Div([html.H4('Predict the price of your desired property!'),
                html.Div(id = 'Predictor-tab')
        ])
    #Data viz tab, both plots are not working yet...
    elif value == 4:
        return html.Div([
                html.H3('Data vizualization tab, choose option below', ),
                dcc.Dropdown(id = 'data-viz-menu',
                             options = [
                                     {'label': 'Average price map', 'value': 1},
                                     {'label': 'Graphs', 'value' :2},
                                     {'label': 'add something', 'value':3}
                                     ]),
                    html.Div(id = 'data-viz-content',
                            )
        ])
    #Raw data table, might change this into an interactive one
    elif value == 5:
        return html.Div([html.Table(
                [html.Tr([html.Th(col) for col in data_frame.columns])] + 
                [html.Tr([
                        html.Td(data_frame.iloc[i][col]) for col in data_frame.columns
                        ]) for i in range(min(len(data_frame), len(data_frame)))])
                    ])
    


#Callback for the pricemap
@app.callback(Output('map-container', 'children'),
              [Input('pricerange-map', 'value')]
              )

def Create_pricemap(values):
    
    df_filtered = data_frame[data_frame.Price.between(values[0],values[1])]
    figure = dcc.Graph(id='map', figure={
                    'data': [{
                        'lat': df_filtered['Latitude'],
                        'lon': df_filtered['Longitude'],
                        'marker': {
                            'color': df_filtered.Price,
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
                        'text': df_filtered['Street'],
                        'customdata': df_filtered['Property number'],
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
                )
    return figure

#Callback that is displayed below the pricerange slider
@app.callback(Output('pricerange-text', 'children'),
              [Input('pricerange-map', 'value')]
              )

def pricerange_text(value):
    return 'Selected minimum price €{},-, maximum price €{},-'.format(
            '{0:,}'.format(value[0]),
            '{0:,}'.format(value[1]))

#Callback that displays the streetname above the map   
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
# Callback that displays all the info next to the map
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
#Callback for surface slider that pops up if selected
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
                           marks = {str(i):'{}'.format(i) for i in range(min_surf,max_surf,25)}
                           )
                ])

# Callback for volume slider
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
                
#Callback for number of rooms slider
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

#Callback for the property type element
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
                ),
                #style ={'margin-left': 20}           
        ])

#Callback for the predictor
@app.callback(
        dash.dependencies.Output('price-prediction-output', 'children'),
        [dash.dependencies.Input('button', 'n_clicks')],
        [dash.dependencies.State('surface-slider', 'value'),
        dash.dependencies.State('volume-slider', 'value'),
        dash.dependencies.State('room-slider', 'value'),
        dash.dependencies.State('property-type', 'value')],
         )

def Price_predictor(n_clicks,surf_value, volume_value, room_value, property_type):
    pred_df = data_frame
    types = list(set(pred_df["Type"]))
    pred_df["Type"] = pred_df["Type"].map({str(t):'{}'.format(i) for i, t in enumerate(types)})
    clf = linear_model.LinearRegression()
    features = ["Surface (m²)","Total volume (m³)",
                'Number of rooms',"Type"]
    X_sel = pred_df[features]
    clf.fit(X = X_sel, y = pred_df.Price) 
    if surf_value == 0:
        price = 'hello'
    else:
        
        predictors = np.array([surf_value,volume_value,room_value,property_type])
    
        price = clf.predict(predictors.reshape(1,-1))[0]
    return  'the value was €{},- and the button was clicked {} times'.format(
            price,
            n_clicks)

#Callback for the data viz tab
@app.callback(
        Output('data-viz-content', 'children'),
        [Input('data-viz-menu', 'value')]
        )

def data_viz_input(value):  
    if value == 1:
        #This was supposed to be a map with the prices for all the neighbourhoods, unfortunaltely does not display anything
        nh_map =  dcc.Graph(id = 'map_2',
                            figure = {
                                    'data':[{
                                            'scattermapbox': {
                                                    'lat':45.5017,
                                                    'lon':-73.5673,
                                                    'mode': 'markers'
                                                    },
                                                    'color': nh_data_frame['Mean price'],
                                                    'type': 'scattermapbox'
                                                    }
                                            ],
                    'layout': {
                            'autosize': True,
                            'mapbox': {
                            'layers' :{
                                    'sourcetype': 'geojson',
                                    'source': 'https://kaart.amsterdam.nl/datasets/datasets-item/t/buurtcombinatiegrenzen-1/export/json',
                                    'type':'fill',
                                    'color': nh_data_frame['Mean price']
                                    },
                            'center':{
                                    'lat':52.35211, 
                                    'lon': 4.88773
                                    },
                                    'zoom': 10.8,
                            'accesstoken': mapbox_access_token
                            }
                            }
                            }
                            )
        return nh_map
    
    if value == 2:
        #Scatterplot to display some relations, couldnt get it working, 
        #plan was to extend to an interactive plot where you can choose what feature to compare with the price
        text = html.Div(id = 'scatterplot_text')
        menu = dcc.Tabs(tabs=[
                {'label': 'Surface (m²)', 'value':0},
                {'label': 'Volume (m³)', 'value': 1},
                {'label': 'number of rooms', 'value': 2},
                {'label': 'number of bedrooms', 'value': 3},
                {'label': 'Year built', 'value': 4}],
                    id = 'scattermenu',
                    value = 0
                    )
                                
        graph = html.Div(id = 'scatterplot')
        slider = dcc.RangeSlider(id = 'pricerange-scatterplot',
                                min = min(data_frame.Price),
                                max = max(data_frame.Price),
                                value = [min(data_frame.Price), max(data_frame.Price)],
                                ),
        
        output = html.Div([menu,graph])             
        return output


@app.callback(
        Output('scatterplot', 'children'),
        [Input('scattermenu', 'value')
        #,Input('pricerange-scatterplot','value')
        ]
        )

def scatterplot_data(value):
    #df_filtered = data_frame[data_frame.Price.between(values[0],values[1])]
    if value == 0:
        X = data_frame["Surface (m²)"]
        title = "Surface (m²)"
    if value == 1: 
        X = data_frame["Total volume (m³)"]
        title = "Total volume (m³)"
    if value == 2:
        X = data_frame["Number of rooms"]
        title = "Number of rooms"
    if value == 3:
        X = data_frame["Number of bedrooms"]
        title = "Number of bedrooms"
    if value == 4:
        X = data_frame["Year built"]
        title = "Year built"
    
    scatter_graph = dcc.Graph(id = 'scatter_graph',
                              figure = {
                                      'data':[
                                              go.Scatter(
                                                      x = X,
                                                      y = data_frame.Price,
                                                      mode= 'markers',
                                                      opacity = 0.7,
                                                      marker = {'size': 10,
                                                                'line': {'width': 0.5, 'color': 'white'}
                                                                },
                                                      name = data_frame.Street
                                                      )
                                              ],
                                      'layout': (go.Layout(
                                              xaxis={'title': title},
                                              yaxis={'title': 'Price in Euro'},
                                              hovermode='closest')
                                      )
                                      }
                                      )
    return scatter_graph
    

#Run server!
if __name__ == '__main__':
    app.run_server(debug=True, port = 8080)

