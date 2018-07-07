import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import os
from dash.dependencies import Input, Output

mannschaft = pd.read_csv('https://raw.githubusercontent.com/MaanasSathaye/DieMannschaft/master/DieMannschaftRecord.csv')

countrycodes = pd.DataFrame(dict(Opponent = ['Albania', 'Algeria', 'Argentina','Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Brazil', 'Bulgaria', 'Cameroon', 'Canada', 'Chile', 'China PR', 'Colombia', 'Costa Rica', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Ecuador', 'England', 'Faroe Islands', 'Finland', 'France', 'Georgia', 'Ghana', 'Gibraltar', 'Greece', 'Guatemala', 'Hungary', 'Iceland', 'Iran', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kuwait', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Malaysia', 'Malta', 'Mexico', 'Netherlands', 'Northern Ireland', 'Norway', 'Paraguay', 'Poland', 'Portugal', 'Republic of Ireland', 'Romania', 'Russia', 'San Marino', 'Saudi Arabia', 'Scotland', 'Serbia', 'Serbia and Montenegro', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland', 'Thailand', 'Tunisia', 'Turkey', 'Ukraine', 'United Arab Emirates', 'United States', 'Uruguay', 'Uzbekistan', 'Wales'],
                                 code = ['ALB', 'DZA', 'ARG', 'ARM', 'AUS', 'AUT', 'AZE', 'BLR', 'BEL', 'BIH', 'BRA', 'BGR', 'CMR', 'CAN', 'CHL', 'CHN', 'COL', 'CRI', 'HRV', 'CYP', 'CZE', 'DNK', 'ECU', 'GBR', 'FRO', 'FIN', 'FRA', 'GEO', 'GHA', 'GIB', 'GRC', 'GTM', 'HUN', 'ISL', 'IRN', 'ISR', 'ITA', 'CIV', 'JAM', 'JPN', 'JOR', 'KAZ', 'KWT', 'LVA', 'LIE', 'LTU', 'LUX', 'MKD', 'MYS', 'MLT', 'MEX', 'NLD', 'NIR', 'NOR', 'PRY', 'POL', 'PRT', 'RIR', 'ROU', 'RUS', 'SMR', 'SAU', 'SCO', 'SRB', 'SAM', 'SGP', 'SVK', 'SVN', 'ZAF', 'SOK', 'ESP', 'SWE', 'CHE', 'THA', 'TUN', 'TUR', 'UKR', 'ARE', 'USA', 'URY', 'UZB', 'WAL']))


mannschaft = pd.merge(mannschaft, countrycodes, on = 'Opponent')


opponent = mannschaft['Opponent'].unique()
location = mannschaft['Location'].unique()
result = mannschaft['Result'].unique()
GG = mannschaft['German Goals'].unique()
OG = mannschaft['Opponent Goals'].unique()

mannschaft['Date'] = mannschaft['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())


#map
df = pd.read_csv('https://raw.githubusercontent.com/MaanasSathaye/DieMannschaft/master/DieMannschaftRecord.csv')
df.head()

df['text'] = df['Opponent'] + '' + df['Location'] + ', ' + df['Result']

scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
       [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]

data = [ dict(
              type = 'scattergeo',
              locationmode = 'world',
              text = df['text'],
              mode = 'markers',
              marker = dict(
                            size = 8,
                            opacity = 0.8,
                            reversescale = True,
                            autocolorscale = False,
                            symbol = 'square',
                            line = dict(
                                        width=1,
                                        color='rgba(102, 102, 102)'
                                        ),
                            colorscale = scl,
                            colorbar=dict(
                                          title="Incoming flightsFebruary 2011"
                                          )
                            ))]

layout = dict(
              title = 'Die Mannschaft<br>(Hover for detailed info)',
              autosize = True,
              width=1280,
              height=720,
              colorbar = True,
              geo = dict(
                         scope='world',
                         projection=dict( type='equirectangular' ),
                         showland = True,
                         showcountries = True,
                         landcolor = "rgb(250, 250, 250)",
                         subunitcolor = "rgb(217, 217, 217)",
                         countrycolor = "rgb(217, 217, 217)",
                         countrywidth = 0.5,
                         subunitwidth = 0.5
                         ),
              )

fig = dict( data=data, layout=layout )

#end_map





app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.layout  = html.Div([
                        dcc.Graph(id='graph', figure=fig)
                        ])

if __name__ == '__main__':
    app.run_server(debug=True)

