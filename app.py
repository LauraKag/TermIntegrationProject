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

from dash.dependencies import Input, Output

conn = pg.connect("postgres://svaoxmufmplmsu:8a40bddf7d6d4bd1bec788f91feacdbdcb0404d83aeda1ac6b40410340eea95b@ec2-75-101-131-79.compute-1.amazonaws.com:5432/d62btbprhf4ja3")

df = pd.read_sql_query('select * from "JanJunData" limit 10;', conn)






#%% Set Up Layout 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

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
        return html.Div([
            html.H3('Tab content 1'),
            dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [3, 1, 2],
                        'type': 'bar'
                    }]
                }
            )
        ])
    elif tab == 'tab-2-example':
        return html.Div([
            html.H3('Tab content 2'),
            generate_table(df)
            ])

    elif tab== 'tab-3-example':
        return html.Div([
            html.H3('Tab content 2')
        ])
        
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


if __name__ == '__main__':
    app.run_server(debug=True)