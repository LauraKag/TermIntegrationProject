# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 19:56:15 2019

@author: laura
"""
#%%

import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2 as pg
import pandas as pd
import plotly.graph_objs as go
import collections

from dash.dependencies import Input, Output

conn = pg.connect("postgres://svaoxmufmplmsu:8a40bddf7d6d4bd1bec788f91feacdbdcb0404d83aeda1ac6b40410340eea95b@ec2-75-101-131-79.compute-1.amazonaws.com:5432/d62btbprhf4ja3")

#df = pd.read_sql_query('select * from "Test_1";', conn)

df = pd.read_csv('C:/Users/laura/OneDrive/Desktop/TermIntegrationProject/Data/NEWNEW5.csv', sep=',')

#%% Set Up Layout 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    html.H1('IBERIA'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Incidences', value='tab-1-example'),
        dcc.Tab(label='Applications', value='tab-2-example'),
        dcc.Tab(label='Services', value='tab-3-example'),
    ]),
    html.Div(id='tabs-content-example')
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab1_layout
    elif tab == 'tab-2-example':
        return html.Div([
            html.H3('Tab content 2'),
            generate_table(df)
            ])

    elif tab== 'tab-3-example':
        return html.Div([
            html.H3('Service Performance'),
            dcc.Dropdown(
                id="input",
            options=[
                {'label': '.COM', 'value': '.COM'},
                {'label': 'BOOKINGS AND INVENTORY SYSTEM', 'value': 'BOOKINGS AND INVENTORY SYSTEM'},
                {'label': 'CHECK IN SYSTEM', 'value': 'CHECK IN SYSTEM'},
                {'label': 'CREW MANAGEMENT', 'value':'CREW MANAGEMENT'},
                {'label': 'FLIGHT DISPATCHING', 'value': 'FLIGHT DISPATCHING'},
                {'label': 'FLIGHT TRACKING AND CONTROL', 'value': 'FLIGHT TRACKING AND CONTROL'},
                {'label': 'LOAD PLAN', 'value': 'LOAD PLAN' },
                {'label': 'MAD-HUB OPERATIONAL MANAGEMENT', 'value': 'MAD-HUB OPERATIONAL MANAGEMENT'},
                {'label': 'MRO SAP', 'value': 'MRO SAP'},
                {'label': 'STATIONS OPERATIONAL MANAGEMENT', 'value': 'STATIONS OPERATIONAL MANAGEMENT'},
                {'label': 'TICKETING SYSTEM', 'value': 'TICKETING SYSTEM'}
            ],value='Service'
        ), dcc.Graph( id="output-graph")
        ],style={'width': '48%', 'float': 'left', 'display': 'inline-block'})

    else:
        return tab1_layout

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


@app.callback(
   Output(component_id='output-graph', component_property='figure'),
   [Input(component_id='input', component_property='value')])
def update_graph(value):
    trace=go.Bar(
            x=['January', 'February', 'March', 'April', 'May', 'June'],
            y= ['123','140','160','180','250','70'],
            name= value,
            marker=go.bar.Marker(
                color='rgb(55, 83, 109)'
            )
        )
            
    return {
        'data': [trace],
        'layout': go.Layout(
                title=value + " -Availability",
                showlegend=True,
                legend=go.layout.Legend(
                    x=0,
                    y=1.0
                ),
                margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
    }


tab1_layout = html.Div([
            html.H3('Tab content 1'),
            generate_table(df)
    
        ])



if __name__ == '__main__':
    app.run_server(debug=True)
