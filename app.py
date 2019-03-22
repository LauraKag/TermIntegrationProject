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
import pandas.io.sql as psql
from dash.dependencies import Input, Output, State
import dash_table_experiments as dt
import plotly
import flask
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import os
import plotly.plotly as py
from plotly import graph_objs as go





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


# BUilding the App 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div(
    [
        # header
        html.Div([

            html.Span("IAG FIRST DRAFT", className='app-title'),
            
            html.Div(
                html.Img(src='https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png',height="100%")
                ,style={"float":"right","height":"100%"})
            ],
            className="row header"
            ),

        # tabs
        html.Div([

            dcc.Tabs(
                id="tabs",
                style={"height":"20","verticalAlign":"middle"},
                children=[
                    dcc.Tab(label="Opportunities", value="opportunities_tab"),
                    dcc.Tab(label="Manager's view", value="leads_tab"),
                    dcc.Tab(id="cases_tab",label="IT's views", value="cases_tab"),
                ],
                value="leads_tab",
            )

            ],
            className="row tabs_div"
            ),
       
                
        # divs that save dataframe for each tab
        html.Div(id="opportunities_df", style={"display": "none"}), # CEO tab df
        html.Div(id="leads_df", style={"display": "none"}), # Manager tab df
        html.Div(id="cases_df", style={"display": "none"}), # IT tabs df



        # Tab content
        html.Div(
            children=[
            html.Iframe(
            src = "//plot.ly/~arthur_mf/75.embed",
            style={"width":"500","height":"500","frameborder":"0"}),
            html.Iframe(
            src= "//plot.ly/~arthur_mf/77.embed",
            style={"width":"500", "height":"500","frameborder":"0", "scrolling":"no"}),
            html.Div(generate_table(df), 
            style={"margin-top": "5px","max-height": "350px","overflow-y": "scroll","padding": "8px","background-color": "white","border": "1px solid rgb(200, 212, 227)","border-radius": "3px",},
            ), 
        ],     
        id="tab_content", className="row", style={"margin": "2% 3%","margin-left":"0.5%"}),
        
        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet")
    ],
    className="row",
    style={"margin": "0%"},
)


if __name__ == '__main__':

    app.run_server(debug=True)
    
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
