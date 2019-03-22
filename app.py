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




conn = pg.connect("postgres://svaoxmufmplmsu:8a40bddf7d6d4bd1bec788f91feacdbdcb0404d83aeda1ac6b40410340eea95b@ec2-75-101-131-79.compute-1.amazonaws.com:5432/d62btbprhf4ja3")

a = pd.read_sql_query('select "Incident ID" from "JanJunData" limit 1;', conn)

app = dash.Dash(__name__)
server = app.server



app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


@app.callback(dash.dependencies.Output('display-value', 'children'), [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)