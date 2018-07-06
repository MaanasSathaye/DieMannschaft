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

mannschaft = pd.read_csv('https://raw.githubusercontent.com/MaanasSathaye/DieMannschaft/master/DieMannschaftRecord.csv').drop('X', axis=1)

opponent = mannschaft['opponent'].unique()
location = mannschaft['location'].unique()
result = mannschaft['result'].unique()
GG = mannschaft['German Goals'].unique()
OG = mannschaft['Opponent Goals'].unique()

countrycodes = pd.DataFrame(dict(country = ['Albania', 'Algeria', 'Argentina','Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Brazil', 'Bulgaria', 'Cameroon', 'Canada', 'Chile', 'China PR', 'Colombia', 'Costa Rica', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Ecuador', 'England', 'Faroe Islands', 'Finland', 'France', 'Georgia', 'Ghana', 'Gibraltar', 'Greece', 'Guatemala', 'Hungary', 'Iceland', 'Iran', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kuwait', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Malaysia', 'Malta', 'Mexico', 'Netherlands', 'Northern Ireland', 'Norway', 'Paraguay', 'Poland', 'Portugal', 'Republic of Ireland', 'Romania', 'Russia', 'San Marino', 'Saudi Arabia', 'Scotland', 'Serbia', 'Serbia and Montenegro', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland', 'Thailand', 'Tunisia', 'Turkey', 'Ukraine', 'United Arab Emirates', 'United States', 'Uruguay', 'Uzbekistan', 'Wales'],
                                 code = ['ALB', 'DZA', 'ARG', 'ARM', 'AUS', 'AUT', 'AZE', 'BLR', 'BEL', 'BIH', 'BRA', 'BGR', 'CMR', 'CAN', 'CHL', 'CHN', 'COL', 'CRI', 'HRV', 'CYP', 'CZE', 'DNK', 'ECU', 'GBR', 'FRO', 'FIN', 'FRA', 'GEO', 'GHA', 'GIB', 'GRC', 'GTM', 'HUN', 'ISL', 'IRN', 'ISR', 'ITA', 'CIV', 'JAM', 'JPN', 'JOR', 'KAZ', 'KWT', 'LVA', 'LIE', 'LTU', 'LUX', 'MKD', 'MYS', 'MLT', 'MEX', 'NLD', 'NIR', 'NOR', 'PRY', 'POL', 'PRT', 'RIR', 'ROU', 'RUS', 'SMR', 'SAU', 'SCO', 'SRB', 'SAM', 'SGP', 'SVK', 'SVN', 'ZAF', 'SOK', 'ESP', 'SWE', 'CHE', 'THA', 'TUN', 'TUR', 'UKR', 'ARE', 'USA', 'URY', 'UZB', 'WAL']))

mannschaft = pd.merge(mannschaft, countrycodes, on='country')

mannschaft['Date'] = mannschaft['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())

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




if __name__ == '__main__':
    app.run_server(debug=True)

