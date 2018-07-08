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
locations = mannschaft['Location'].unique()
result = mannschaft['Result'].unique()
GG = mannschaft['German Goals'].unique()
OG = mannschaft['Opponent Goals'].unique()

mannschaft['Date'] = mannschaft['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())

dates = [np.sort(mannschaft['Date'].unique())[0], np.sort(mannschaft['Date'].unique())[-1]]

countries = ['Albania', 'Algeria', 'Argentina','Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Brazil', 'Bulgaria', 'Cameroon', 'Canada', 'Chile', 'China PR', 'Colombia', 'Costa Rica', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Ecuador', 'England', 'Faroe Islands', 'Finland', 'France', 'Georgia', 'Ghana', 'Gibraltar', 'Greece', 'Guatemala', 'Hungary', 'Iceland', 'Iran', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kuwait', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Malaysia', 'Malta', 'Mexico', 'Netherlands', 'Northern Ireland', 'Norway', 'Paraguay', 'Poland', 'Portugal', 'Republic of Ireland', 'Romania', 'Russia', 'San Marino', 'Saudi Arabia', 'Scotland', 'Serbia', 'Serbia and Montenegro', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland', 'Thailand', 'Tunisia', 'Turkey', 'Ukraine', 'United Arab Emirates', 'United States', 'Uruguay', 'Uzbekistan', 'Wales']

types = ['Wins, Losses, Draws, Ref Nation']

####### CHOROPLETH DATA
def makeChoropleth(dates, types, countries, location):
    
    chorodata = mannschaft.loc[(mannschaft['Date'] >= dates[0]) & (mannschaft['Date'] <= dates[1]) &
                               (mannschaft['Opponent'].isin(types)) & (mannschaft['Location'].isin(locations))].copy()
        
    chorodata = chorodata.groupby(['code', 'Opponent']).sum()['German Goals'].reset_index()
    chorodata = pd.merge(mannschaft[['code', 'Opponent']].drop_duplicates().reset_index().drop('index', axis = 1),
                        chorodata, on=['code', 'Opponent'], how='outer')
   
    chorodata = chorodata.loc[chorodata['Opponent'].isin(countries)]
   
    data = [
           go.Choropleth(
                         locations = chorodata['code'],
                         z = chorodata['German Goals'],
                         colorscale = 'Viridis',
                         zmin = 0,
                         zmax = mannschaft.groupby('Opponent').sum()['German Goals'].max()
                         )
           ]
   
    layout = go.Layout(
                      title = 'I do not know',
                      geo = dict(
                                 center = dict(lon = -60, lat = -12),
                                 projection = dict(scale = 2)
                                 )
                      )
   
    return go.Figure(data = data, layout = layout)
####### END CHOROPLETH DATA



#####random

app.layout = html.Div([
                       html.Div([
                                 html.H2('Zika Explorer'),
                                 html.Div([], className = 'one column'),
                                 html.Div([
                                           html.Div([
                                                     html.P('Country')
                                                     ], className = 'row'),
                                           html.Div([
                                                     dcc.Dropdown(
                                                                  id = 'countryPicker',
                                                                  options = [{'label': i, 'value': i} for i in mannschaft['Opponent'].unique()],
                                                                  multi = True,
                                                                  value = mannschaft['Opponent'].unique()
                                                                  )
                                                     ], className = 'row')
                                           
                                           ], className = 'seven columns'),
                                 html.Div([
                                           html.Div([
                                                     html.P('Result')
                                                     ], className = 'row'),
                                           html.Div([
                                                     dcc.Dropdown(
                                                                  id = 'reportTypePicker',
                                                                  options = [{'label': i, 'value': i} for i in mannschaft['Result'].unique()],
                                                                  multi = True,
                                                                  value = mannschaft['Result'].unique()
                                                                  )
                                                     ], className = 'row')
                                           ], className = 'three columns'),
                                 html.Div([], className = 'one column')
                                 ], className = 'row'),
                       html.Div([
                                 html.Div([
                                           dcc.Graph(id = 'countryMap', figure = makeChoropleth(dates, types, countries, locations))
                                           ], className = 'six columns'),
                                 html.Div([
                                           dcc.Graph(id = 'subMap', figure = makeScatterMap(dates, types, countries, locations),
                                                     selectedData = subMapSelected)
                                           ], className = 'six columns')
                                 ], className = 'row'),
                       html.Div([
                                 dcc.Graph(id = 'timeSeriesGraph',
                                           figure = makeTimeSeriesGraph(dates, types, countries, locations),
                                           selectedData = timeseriesSelected)
                                 ], className = 'row')
                       ])
####end random

def makeScatterMap(dates, types, countries, locations):
    
    scattermapdata = mannschaft.loc[(mannschaft['Date'] >= dates[0]) & (mannschaft['Date'] <= dates[1]) &
                              (mannschaft['Result'].isin(types)) & (mannschaft['Location'].isin(countries))].copy()
        
    scattermapdata = scattermapdata.groupby(['location', 'lat', 'lon']).sum()['value'].reset_index()
                              
    scattermapdata['text'] = scattermapdata.apply(lambda x: x['location'] + ': ' + str(x['German Goals']) ,axis = 1)
    scattermapdata['opacity'] = scattermapdata['location'].apply(lambda x: 1 if x in locations else 0.2)
    scattermapdata['width'] = scattermapdata['location'].apply(lambda x: 1 if x in locations else 0)
                              
    data = [
              go.Scattergeo(
                            lat = scattermapdata['lat'],
                            lon = scattermapdata['lon'],
                            text = scattermapdata['text'],
                            hoverinfo = 'text',
                            marker = dict(
                                          color = scattermapdata['value'],
                                          colorscale = 'Viridis',
                                          opacity = scattermapdata['opacity'],
                                          line = dict(
                                                      width = scattermapdata['width']
                                                      )
                                          )
                            )
              ]
                              
    layout = go.Layout(
                     title = 'Zika Cases by Municipality',
                     dragmode = 'lasso',
                     geo = dict(
                                center = dict(lon = -60, lat = -12),
                                projection = dict(scale = 2)
                                )
                     )
  
    fig = go.Figure(data = data, layout = layout)
                              
    return fig



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
              font = dict(family = "Times New Roman", size = 18, color='#DD0000'),
              title ='Die Mannschaft<br>(Hover for detailed info)',
              autosize = True,
              width=1280,
              height=720,
              colorbar = True,
              geo = dict(
                         scope='world',
                         projection=dict( type='equirectangular' ),
                         showland = True,
                         showcountries = True,
                         landcolor = "rgb(350, 350, 350)",
                         subunitcolor = "rgb(217, 217, 217)",
                         countrycolor = "rgb(117, 117, 117)",
                         countrywidth = 0.5,
                         subunitwidth = 0.5
                         ),
              )

fig = dict( data=data, layout=layout )

#end_map



def makeTimeSeriesGraph(dates, types, countries, locations):
    
    timeseriesdata = mannschaft.loc[(mannschaft['Result'].isin(types)) & (mannschaft['Opponent'].isin(countries)) &
                              (mannschaft['Location'].isin(locations))]
        
    timeseriesdata = timeseriesdata.groupby('Date').sum()['German Goals'].reset_index().sort_values('Date')
  
    timeseriesdata = pd.merge(pd.DataFrame(mannschaft['Date']).drop_duplicates().reset_index().drop('index', axis = 1),
                            timeseriesdata, on = 'Date', how = 'outer')
    timeseriesdata = timeseriesdata.sort_values('Date').fillna(0)
  
    timeseriesdata['color'] = timeseriesdata['Date'].apply(
                                                                lambda x: 'rgba(68,6,83,1)' if (x >= dates[0]) & (x <= dates[1]) else 'rgba(68,6,83,0.2)')
  
    data = [
          go.Bar(
                 x = timeseriesdata['Date'],
                 y = timeseriesdata['German Goals'],
                 marker = dict(
                               color = timeseriesdata['color']
                               )
                 )
          ]
  
    layout = go.Layout(title = 'Reports over time', dragmode = 'select', showlegend = False, hovermode = 'closest')
                              
    return go.Figure(data = data, layout = layout)


app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.layout  = html.Div([
                        dcc.Graph(id='graph', figure=fig)
                        ])

if __name__ == '__main__':
    app.run_server(debug=True)
