# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 19:56:15 2019

@author: laura
"""
#%%

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 

import plotly.graph_objs as go






conn = pg.connect("postgres://svaoxmufmplmsu:8a40bddf7d6d4bd1bec788f91feacdbdcb0404d83aeda1ac6b40410340eea95b@ec2-75-101-131-79.compute-1.amazonaws.com:5432/d62btbprhf4ja3")

df = pd.read_sql_query('select * from "JanJunData" limit 20;', conn)


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


@server.route("/dash/<page>")
def pages_route(page):

    df = pd.read_sql_query('select * from "Test1" limit 10 offset {};'.format(page * 10), conn)

    app.layout = html.Div(children=[
        html.H1('Iberia', style={'textAlign': 'center', 'color': '#7FDBFF'}),    
        html.H4(children='Test first table'), generate_table(df),
        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        ),

        html.A
    ])

if __name__ == '__main__':
    app.run_server(debug=True)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
