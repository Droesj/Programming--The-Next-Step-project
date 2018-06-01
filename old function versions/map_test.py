# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 02:38:44 2018

@author: S.Evelo
"""

#%%
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
#import dash_table_experiments as dt
import pandas as pd


mapbox_access_token = 'pk.eyJ1IjoiZHJvZXNqIiwiYSI6ImNqaHFiYTBoZzAwMXUzN3F0dXBhOXMwY3IifQ.tgd10h6uc8XViS1NZMcPnw'

data_frame = pd.read_csv(r'property_database_final.csv', sep = ";")
data_frame.rename( columns={'Unnamed: 0':'Property number'}, inplace=True )



#%%
app_2 = dash.Dash()
app_2.config['suppress_callback_exceptions']=True
app_2.layout = html.Div([
        html.Div(id = 'map-container',
                         style={'width': '70%'} ),
                
                dcc.RangeSlider(id = 'pricerange-map',
                                min = min(data_frame.Price),
                                max = max(data_frame.Price),
                                value = [min(data_frame.Price), max(data_frame.Price)]
                                
    ),
    html.Div(id='output-container-range-slider')
])


@app_2.callback(Output('map-container', 'children'),
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


@app_2.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)





if __name__ == '__main__':
    app_2.run_server(debug=True, port = 8081)




#%%
import pandas as pd

values = [5,15]
r = {'Price': [1,5,10,15,20,30]}

print 
df = pd.DataFrame(r)
#print(df.Price[ df.Price < values[1]  df.Price > values[0]])
#print(r > values[0])

#print(r[values[0]>r<values[1]])


print(df.Price[df.Price.between(values[0],values[1],)])