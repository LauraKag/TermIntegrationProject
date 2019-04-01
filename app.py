# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 19:56:15 2019

@author: laura
"""
#%%
import dash
#import base64
#import datetime
#import io
import dash_core_components as dcc
import dash_html_components as html
import psycopg2 as pg
import pandas as pd
import plotly.graph_objs as go
import collections
import dash_table
import dash_table_experiments as dt
#import json
import plotly
from dash.dependencies import Input, Output,State
import numpy as np

#from dash.exceptions import PreventUpdate

#conn = pg.connect("postgres://svaoxmufmplmsu:8a40bddf7d6d4bd1bec788f91feacdbdcb0404d83aeda1ac6b40410340eea95b@ec2-75-101-131-79.compute-1.amazonaws.com:5432/d62btbprhf4ja3")

#NEW=pd.read_sql_query('select * from "Finaldata"', conn)
#NEW=NEW.iloc[1:]

NEW = pd.read_csv('C:/Users/laura/OneDrive/Desktop/Finaldata.csv', sep=',')
NEW1=NEW.dropna(subset=['Service'])

NEW2=NEW1[['Domain', 'Month raised', 'Service', 'Incident ID', 'RESO']]
NEW3=NEW2[pd.notnull(NEW2['Month raised'])]
NEW3.columns=['Domain','Month raised','Service','Incident ID','Resolution time']
#df1 = df[pd.notnull(df['SERVICE'])]
#df2=df1[['DOMAIN', 'Month raised', 'SERVICE', 'CI Name', 'Reliability','Real Availability Application']]
#df2=df2[pd.notnull(df2['Month raised'])]
#df2.columns=['Domain', 'Month raised', 'Service' , 'Application' , 'Application Reliability', 'Application Availability']
#df2 = df2.drop_duplicates()

AppsinService=NEW.dropna(subset=['Service'])
array = ['Critical', 'High']
Appsincritical=AppsinService.loc[AppsinService['Priority'].isin(array)]
Apps=Appsincritical['CI Name'].unique()
Apps=Apps.tolist()
Apps.sort()


#%% Set Up Layout 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.config['suppress_callback_exceptions']=True

app.layout = html.Div([

     html.Div([
            html.Div(
                html.Img(src='http://www.aviacionnews.com/blog/wp-content/uploads/2015/08/IAG-Logo.png')
                ,style={"float":"top-left","height":"60%"})
            ]
            ),
    html.Div([ 
        dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Incidences', value='tab-1-example'),
        dcc.Tab(label='Applications', value='tab-2-example'),
        dcc.Tab(label='Services', value='tab-3-example'),
        ]),
        html.Div(id='tabs-content-example')

    ])
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab1_layout
    elif tab == 'tab-2-example':
        return tab2_layout
    elif tab== 'tab-3-example':
        return tab3_layout
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



tab1_layout = html.Div([
        html.Div([
            html.Div([
                html.H3('Incidence Volumes'),
                dcc.RadioItems(
                    id='VolumesInc',
                    options=[{'label': 'January', 'value': 'January'},
                    {'label': 'February', 'value': 'February'},
                    {'label': 'March', 'value': 'March'},
                    {'label': 'April', 'value': 'April'},
                    {'label': 'May', 'value': 'May'},
                    {'label': 'June', 'value': 'June'}],
                    value='January',labelStyle={'display': 'inline-block'}),
            dcc.Graph( id="VolumesInc-graph-app")
            ],className='six columns'),
            html.Div([
                html.H3('Incidence Distribution'),
                dcc.RadioItems(
                    id='IncDistribution',
                    options=[{'label': 'January', 'value': 'January'},
                    {'label': 'February', 'value': 'February'},
                    {'label': 'March', 'value': 'March'},
                    {'label': 'April', 'value': 'April'},
                    {'label': 'May', 'value': 'May'},
                    {'label': 'June', 'value': 'June'}],
                    value='January',labelStyle={'display': 'inline-block'}),
            dcc.Graph( id="IncDistribution-graph-app")
            ],className='six columns')
            
    ], className='row'),

     html.Div([
            html.Div([
                html.H3('Resolution Rates'),
                dcc.RadioItems(
                    id='Resolution',
                    options=[{'label': 'January', 'value': 'January'},
                    {'label': 'February', 'value': 'February'},
                    {'label': 'March', 'value': 'March'},
                    {'label': 'April', 'value': 'April'},
                    {'label': 'May', 'value': 'May'},
                    {'label': 'June', 'value': 'June'}],
                    value='January',labelStyle={'display': 'inline-block'}),
            dcc.Graph( id="Resolution-graph-app")
            ],className='six columns'),
            html.Div([
                html.H3('Incidence Volumes per Tower'),
                dcc.RadioItems(
                    id='TowerInc',
                    options=[{'label': 'January', 'value': 'January'},
                    {'label': 'February', 'value': 'February'},
                    {'label': 'March', 'value': 'March'},
                    {'label': 'April', 'value': 'April'},
                    {'label': 'May', 'value': 'May'},
                    {'label': 'June', 'value': 'June'}],
                    value='January',labelStyle={'display': 'inline-block'}),
            dcc.Graph( id="TowerInc-graph-app")
            ],className='six columns')
            
    ], className='row'),

    html.Div([
            html.Div([
                html.H3('Trend of Incidence Volumes'),
                                dcc.Graph(
                                    figure=go.Figure(
                        data=[
                            go.Scatter(
                                y=[14, 21, 15, 32, 22, 27],
                                x=['January','February','March','April','May','June'],
                                name='Critical',
                                
                            ),
                            go.Scatter(
                                y=[296, 319, 369, 422, 372, 346],
                                x=['January','February','March','April','May','June'],
                                name='High',
                                
                                
                            ),
                            go.Scatter(
                                y=[2303, 2255, 2407, 2463, 2439, 2639],
                                x=['January','February','March','April','May','June'],
                                name='Medium',
                                
                                
                            ),
                            go.Scatter(
                                y=[4345, 3462, 3518, 3467, 3460, 3648],
                                x=['January','February','March','April','May','June'],
                                name='Low',
                                
                                
                            ),
                            go.Scatter(
                                y=[4199, 3561, 3675, 3594, 3657, 3227],
                                x=['January','February','March','April','May','June'],
                                name='Access related',
                                
                                
                            )
                        ],
                        layout=go.Layout(
                            title='Trend of Incidence Volumes',
                            showlegend=True,
                            
                        )
                    ),
                    style={'height': 500},
                    id='my-graph'
                )
        ], className='six columns'),

                html.Div([
                      html.H3('Trend of MTTR'),
                                    dcc.Graph(
                                        figure=go.Figure(
                            data=[
                                go.Scatter(
                                    y=[7, 3, 2, 5, 10, 11],
                                    x=['January','February','March','April','May','June'],
                                    name='Critical',
                                    
                                ),
                                go.Scatter(
                                    y= [26, 21, 35, 19, 30, 30],
                                    x=['January','February','March','April','May','June'],
                                    name='High',
                                    
                                    
                                ),
                                go.Scatter(
                                    y=[108, 130, 139, 147, 141, 133],
                                    x=['January','February','March','April','May','June'],
                                    name='Medium',
                                    
                                    
                                ),
                                go.Scatter(
                                    y=[134, 156, 146, 142, 133, 134],
                                    x=['January','February','March','April','May','June'],
                                    name='Low',
                                    
                                    
                                ),
                                go.Scatter(
                                    y=[12, 12, 9, 8, 5, 6],
                                    x=['January','February','March','April','May','June'],
                                    name='Access related',
                                    
                                    
                                )
                            ],
                            layout=go.Layout(
                                title='Trend of MTTR',
                                showlegend=True,
                               
                            )
                        ),
                        style={'height': 500},
                        id='other-graph'
                    )
        ], className='six columns')

    ],className='row'),

    #html.Div([
       # dcc.Upload(
      #  id='upload-data',
      #  children=html.Div([
      #      'Drag and Drop or ',
      #      html.A('Select Files')
      #  ]),
      #  style={
      #      'width': '100%',
      #      'height': '60px',
      #      'lineHeight': '60px',
      #      'borderWidth': '1px',
      #      'borderStyle': 'dashed',
      #      'borderRadius': '5px',
      #      'textAlign': 'center',
      #      'margin': '10px'
     #   },
        # Allow multiple files to be uploaded
        #multiple=True
   # ),
  #  html.Div(id='output-data-upload'),
#],className="row")

        ])

tab2_layout=html.Div([
    html.Div([
            html.Div([
                html.H3('Reliability for Critical and High Incidences'),
                dcc.Dropdown(
                    id='Reliability',
                    options=[{'label':name, 'value':name} for name in Apps],
                    value='CKI'),
            dcc.Graph( id="reliability-graph-app")
            ],className='six columns'),
            html.Div([
                html.H3('Availability for Critical and High Incidences'),
                dcc.Dropdown(
                    id='availabilityApp',
                    options=[{'label':name, 'value':name} for name in Apps],
                    value='CKI'),
            dcc.Graph( id="availability-graph-app")
            ],className='six columns')
            
    ], className='row'),

     html.Div([
            html.Div([
                html.H3('MTTRs for Critical, High, Medium and Low Incidences'),
                dcc.Dropdown(
                    id='MTTRs',
                    options=[{'label':name, 'value':name} for name in Apps],
                    value='CKI'),
            dcc.Graph( id="mttr-graph-app")
            ],className='six columns'),
            html.Div([
                html.H3('Number of Critical, High, Medium and Low Incidences'),
                dcc.Dropdown(
                    id='Numbers',
                    options=[{'label':name, 'value':name} for name in Apps],
                    value='CKI'),
            dcc.Graph( id="numbers-graph-app")
            ],className='six columns')
            
    ], className='row'),

    html.Div([
            html.Div([
                html.H3('Reliabilities for Critical and High Incidences'),
                dcc.RadioItems(
                    id='ReliabilityAll',
                    options=[{'label': 'January', 'value': 'January'},
                    {'label': 'February', 'value': 'February'},
                    {'label': 'March', 'value': 'March'},
                    {'label': 'April', 'value': 'April'},
                    {'label': 'May', 'value': 'May'},
                    {'label': 'June', 'value': 'June'}],
                    value='January',labelStyle={'display': 'inline-block'}),
            dcc.Graph( id="reliabilities-graph-app")
            ],className='six columns'),
            html.Div([
                html.H3('Availabilities for Critical and High Incidences'),
                dcc.RadioItems(
                    id='availabilityAppAll',
                    options=[{'label': 'January', 'value': 'January'},
                    {'label': 'February', 'value': 'February'},
                    {'label': 'March', 'value': 'March'},
                    {'label': 'April', 'value': 'April'},
                    {'label': 'May', 'value': 'May'},
                    {'label': 'June', 'value': 'June'}],
                    value='January',labelStyle={'display': 'inline-block'}),
            dcc.Graph( id="availabilities-graph-app")
            ],className='six columns')
            
    ], className='row'),


    html.Div([
        html.H3('MTTRs for Critical and High Incidences'),
        dcc.RadioItems(
            id='MTTRsAll',
            options=[{'label': 'January', 'value': 'January'},
            {'label': 'February', 'value': 'February'},
            {'label': 'March', 'value': 'March'},
            {'label': 'April', 'value': 'April'},
            {'label': 'May', 'value': 'May'},
            {'label': 'June', 'value': 'June'}],
            value='January',labelStyle={'display': 'inline-block'}),
        dcc.Graph( id="MTTRsAll-graph-app")
        ],className='row'),

    html.Div([
        html.H3('Critical and High Incidence Volumes'),
        dcc.RadioItems(
            id='VolumesAppAll',
            options=[{'label': 'January', 'value': 'January'},
            {'label': 'February', 'value': 'February'},
            {'label': 'March', 'value': 'March'},
            {'label': 'April', 'value': 'April'},
            {'label': 'May', 'value': 'May'},
            {'label': 'June', 'value': 'June'}],
            value='January',labelStyle={'display': 'inline-block'}),
        dcc.Graph( id="VolumesAppAll-graph-app")
        ],className='row')


            ], style={"border-radius":"gray 3px"})
   


tab3_layout=html.Div([

    html.Div([

        html.Div([
                html.H3('Service Reliability for Critical Incidences'),
                dcc.Dropdown(
                    id="reliability",
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
                ],value='.COM'
            ), 
            dcc.Graph( id="reliability-graph")
            ],className='six columns'),

            html.Div([
                html.H3('Service Availability for Critical Incidences'),
                dcc.Dropdown(
                    id="availability",
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
                ],value='.COM'
            ), 
            dcc.Graph( id="availability-graph")
            ],className='six columns')

    ], className ='row'),
    
    html.Div([
        html.Div([
            html.H3('All Services - Reliability'),
            dcc.RadioItems(
                    id="AllReliability",
                options=[
                    {'label': 'January', 'value': 'January'},
                    {'label': 'February', 'value': 'February'},
                    {'label': 'March', 'value': 'March'},
                    {'label': 'April', 'value': 'April'},
                    {'label': 'May', 'value': 'May'},
                    {'label': 'June', 'value': 'June'},
                ], value='January', labelStyle={'display': 'inline-block'})
        ]),
        dcc.Graph( id="allreliabilities")
    ], className='row'),

    html.Div([
        html.Div([
            html.H3('All Services - Availability'),
            dcc.RadioItems(
                    id="AllAvailability",
                options=[
                    {'label': 'January', 'value': 'January'},
                    {'label': 'February', 'value': 'February'},
                    {'label': 'March', 'value': 'March'},
                    {'label': 'April', 'value': 'April'},
                    {'label': 'May', 'value': 'May'},
                    {'label': 'June', 'value': 'June'},
                ], value='January',labelStyle={'display': 'inline-block'})
        ]),
        dcc.Graph( id="allavailabilities")
    ], className='row'),

    html.Div([
        html.Div([
            html.H3('Number of Critical and High Incidences'),
            dcc.RadioItems(
                    id="NumberHIGH",
                options=[
                    {'label': 'January', 'value': 'January'},
                    {'label': 'February', 'value': 'February'},
                    {'label': 'March', 'value': 'March'},
                    {'label': 'April', 'value': 'April'},
                    {'label': 'May', 'value': 'May'},
                    {'label': 'June', 'value': 'June'},
                ], value='January',labelStyle={'display': 'inline-block'})
        ]),
        dcc.Graph( id="numberHIGH")
    ], className='row'),

    
    html.Div([
        html.Div([
                html.H4('Service Information'),
                dt.DataTable(
                    rows=NEW3.to_dict('records'),
                    columns=NEW3.columns,
                    #editable=True,
                    row_selectable=True,
                    filterable=True,
                    sortable=True,
                    selected_row_indices=[],
                    id='datatable-gapminder'
                ),
                html.Div(id='selected-indexes')
                #,
                #html.Div([
                  # dcc.Graph(id='graph-gapminder'),
                #],className="container") 
                ])
    ], className='row')

#], style={"background-color":"gray"})
])

@app.callback(
   Output(component_id='VolumesInc-graph-app', component_property='figure'),
   [Input(component_id='VolumesInc', component_property='value')])
def Incidence_volumes(value):
    Incidencemonth=NEW[NEW['Month raised']==value]
    WithoutSSI=Incidencemonth[Incidencemonth['Assigned Group']!="SSI"]
    WithSSI=Incidencemonth[Incidencemonth['Assigned Group']=="SSI"]
    Numbers=[]

    SelectAppcritical=WithoutSSI[WithoutSSI['Priority']=='Critical']
    countedcritical=SelectAppcritical[['Incident ID']].count()
    countedcritical.tolist()
    countedcritical=countedcritical[0]
    Numbers.append(countedcritical)

    SelectApphigh=WithoutSSI[WithoutSSI['Priority']=='High']
    countedhigh=SelectApphigh[['Incident ID']].count()
    countedhigh.tolist()
    countedhigh=countedhigh[0]
    Numbers.append(countedhigh)

    SelectAppmedium=WithoutSSI[WithoutSSI['Priority']=='Medium']
    countedmedium=SelectAppmedium[['Incident ID']].count()
    countedmedium.tolist()
    countedmedium=countedmedium[0]
    Numbers.append(countedmedium)
    
    
    SelectApplow=WithoutSSI[WithoutSSI['Priority']=='Low']
    countedlow=SelectApplow[['Incident ID']].count()
    countedlow.tolist()
    countedlow=countedlow[0]
    Numbers.append(countedlow) 
    
    countedSSI=WithSSI[['Incident ID']].count()
    countedSSI.tolist()
    countedSSI=countedSSI[0]
    Numbers.append(countedSSI)
    
    return ({'data': [
                {'x': ["Critical","High","Medium","Low","Access related"], 'y': Numbers, 'type': 'bar',
        'marker':{'color': ['purple','red','#52AF2B','#3871D7','#F97E05']}}
                
            ],
            'layout': {
                'title': "Incidence Volumes for {} in 2018".format(value)
            }
        }
    )

@app.callback(
   Output(component_id='IncDistribution-graph-app', component_property='figure'),
   [Input(component_id='IncDistribution', component_property='value')])
def Incidence_volumes(value):
    Incidencemonth=NEW[NEW['Month raised']==value]
    WithoutSSI=Incidencemonth[Incidencemonth['Assigned Group']!="SSI"]
    WithSSI=Incidencemonth[Incidencemonth['Assigned Group']=="SSI"]
    Numbers=[]

    SelectAppcritical=WithoutSSI[WithoutSSI['Priority']=='Critical']
    countedcritical=SelectAppcritical[['Incident ID']].count()
    countedcritical.tolist()
    countedcritical=countedcritical[0]
    Numbers.append(countedcritical)

    SelectApphigh=WithoutSSI[WithoutSSI['Priority']=='High']
    countedhigh=SelectApphigh[['Incident ID']].count()
    countedhigh.tolist()
    countedhigh=countedhigh[0]
    Numbers.append(countedhigh)

    SelectAppmedium=WithoutSSI[WithoutSSI['Priority']=='Medium']
    countedmedium=SelectAppmedium[['Incident ID']].count()
    countedmedium.tolist()
    countedmedium=countedmedium[0]
    Numbers.append(countedmedium)
    
    
    SelectApplow=WithoutSSI[WithoutSSI['Priority']=='Low']
    countedlow=SelectApplow[['Incident ID']].count()
    countedlow.tolist()
    countedlow=countedlow[0]
    Numbers.append(countedlow) 
    
    countedSSI=WithSSI[['Incident ID']].count()
    countedSSI.tolist()
    countedSSI=countedSSI[0]
    Numbers.append(countedSSI)
    
    return ({'data': [
                {'values': Numbers,
                 'labels':["Critical","High","Medium","Low","Access related"],
                 'type': 'pie'}],
  
            'layout': {
                'title': "Incidence Distribution for {} in 2018".format(value)
            }
        }
    )


@app.callback(
   Output(component_id='Resolution-graph-app', component_property='figure'),
   [Input(component_id='Resolution', component_property='value')])
def Incidence_MTTRs(value):
    Incidencemonth=NEW[NEW['Month raised']==value]
    WithoutSSI=Incidencemonth[Incidencemonth['Assigned Group']!="SSI"]
    #WithSSI=Incidencemonth[Incidencemonth['Assigned Group']=="SSI"]
    
    MTTRs=[]

    SelectAppcritical=WithoutSSI[WithoutSSI['Priority']=='Critical']
    countedcritical=SelectAppcritical["RESO"].mean()
    countedcritical=round(countedcritical)
    MTTRs.append(countedcritical)

    SelectApphigh=WithoutSSI[WithoutSSI['Priority']=='High']
    countedhigh=SelectApphigh["RESO"].mean()
    countedhigh=round(countedhigh)
    MTTRs.append(countedhigh)

    SelectAppmedium=WithoutSSI[WithoutSSI['Priority']=='Medium']
    countedmedium=SelectAppmedium["RESO"].mean()
    countedmedium=round(countedmedium)
    MTTRs.append(countedmedium)
    
    
    SelectApplow=WithoutSSI[WithoutSSI['Priority']=='Low']
    countedlow=SelectApplow["RESO"].mean()
    countedlow=round(countedlow)
    MTTRs.append(countedlow)
    
    return ({'data': [
                {'x': ["Critical","High","Medium","Low"], 'y': MTTRs, 'type': 'bar',
        'marker':{'color': ['purple','red','#52AF2B','#3871D7']}}
                
            ],
            'layout': {
                'title': "Resolution Rates for {} in 2018".format(value)
            }
        }
    )


@app.callback(
   Output(component_id='TowerInc-graph-app', component_property='figure'),
   [Input(component_id='TowerInc', component_property='value')])
def find_numbers_of_CH_Tower(value):
    Monthsdf=NEW[NEW['Month raised']==value]
    array = ['Critical', 'High']
    AppsinMonthcritical=Monthsdf.loc[Monthsdf['Priority'].isin(array)]
    AppsinMonthA=AppsinMonthcritical['Tower Group'].unique()
    AppsinMonthA=[x for x in AppsinMonthA if str(x) != 'nan']
    AppsinMonthCriticalonly=Monthsdf[Monthsdf['Priority']=='Critical']
    AppsinMonthACritical=AppsinMonthCriticalonly['Tower Group'].unique()
    AppsinMonthACritical=[x for x in AppsinMonthACritical if str(x) != 'nan']
    CriticalIncidences=[] 
    HighIncidences=[]
    for i in AppsinMonthA:
        SortbyApp=AppsinMonthcritical[AppsinMonthcritical['Tower Group']==i]
        Critical=SortbyApp[SortbyApp['Priority']=="Critical"]
        counted=Critical[['Incident ID']].count()
        counted.tolist()
        counted=counted[0]
        CriticalIncidences.append(counted) 
        High=SortbyApp[SortbyApp['Priority']=="High"]
        counted2=High[['Incident ID']].count()
        counted2.tolist()
        counted2=counted2[0]
        HighIncidences.append(counted2)
        CriticalIncidences=list(filter(lambda a: a != 0, CriticalIncidences)) 

        CriticalIncidencesnew=sorted(CriticalIncidences, key=float, reverse=True)
        AppsinMonthACriticalnew = [x for _,x in sorted(zip(CriticalIncidences,AppsinMonthACritical))]
        #AppsinMonthAnew=[x for _,x in sorted(zip(CriticalIncidences,AppsinMonthA))]
        #HighIncidencesnew

       
    return ({'data': [
                {'x': AppsinMonthACriticalnew, 'y': CriticalIncidencesnew, 'type': 'bar', 'name': "Critical" },
                {'x': AppsinMonthA, 'y': HighIncidences, 'type': 'bar', 'name': "High"}
            ],
            'layout': {
                'title': "Incidence Volumes per Tower",
                #'xaxis': {'tickangle':"-90"}
            }
        })





@app.callback(
   Output(component_id='reliability-graph-app', component_property='figure'),
   [Input(component_id='Reliability', component_property='value')])
def update_graph_Reliability(value):
    AppDF=NEW[NEW['CI Name']==value]
    array = ['Critical', 'High']
    AppsinMonthcritical=AppDF.loc[AppDF['Priority'].isin(array)]
    monthscolumn=AppsinMonthcritical['Month raised']
    monthsofApp=monthscolumn.unique()
    months=[x for x in monthsofApp if str(x) != 'nan']
    ReliabilitiesAPP=[]
    for i in months: 
        FilterMonth=AppsinMonthcritical[AppsinMonthcritical['Month raised']==str(i)]
        counted=FilterMonth[['Incident ID']].count()
        counted.tolist()
        counted=counted[0]
        MTTR=FilterMonth['RESO'].mean()
        reliability=(720-MTTR)/counted
        reliability=round(reliability)
        ReliabilitiesAPP.append(reliability)

    return ({'data': [
                {'x': monthsofApp, 'y': ReliabilitiesAPP, 'type': 'bar', 'name': value , 'marker':{'color': 'orange'}},
            ],
            'layout': {
                'title': "Reliability for {} in 2018".format(value)
            }
        }
    )


@app.callback(
   Output(component_id='availability-graph-app', component_property='figure'),
   [Input(component_id='availabilityApp', component_property='value')])
def update_graph_Availability(value):
    AppsinService=NEW.dropna(subset=['Service'])
    AppDF=AppsinService[AppsinService['CI Name']==value]
    array = ['Critical', 'High']
    Appsincritical=AppDF.loc[AppDF['Priority'].isin(array)]
    monthscolumn=Appsincritical['Month raised']
    monthsofApp=monthscolumn.unique()
    months=[x for x in monthsofApp if str(x) != 'nan']
    AvailabilitiesApp=[]
    for i in months: 
        FilterMonth= Appsincritical[Appsincritical['Month raised']==str(i)]
        MTTR=FilterMonth['RESO'].mean()
        availability=(720-MTTR)/720
        roundedav=round(availability,4)
        AvailabilitiesApp.append(roundedav)
          
    return ({'data': [
                {'x': months, 'y': AvailabilitiesApp, 'type': 'scatter', 'name': value},
            ],
            'layout': {
                'title': "Availability for {} in 2018".format(value)
            }
        }
    )

@app.callback(
   Output(component_id='reliabilities-graph-app', component_property='figure'),
   [Input(component_id='ReliabilityAll', component_property='value')])
def update_graph_Reliabilities_App(value):
    AppsinService=NEW.dropna(subset=['Service'])
    MonthDF=AppsinService[AppsinService['Month raised']==value]
    array = ['Critical', 'High']
    AppsinMonthcritical=MonthDF.loc[MonthDF['Priority'].isin(array)]
    AppsinMonth=AppsinMonthcritical['Service'].unique()
    AppsinMonth=[x for x in AppsinMonth if str(x) != 'nan']
    ReliabilitiesforApps=[]
    for i in AppsinMonth:
        AppMonth=AppsinMonthcritical[AppsinMonthcritical['Service']==i]
        counted=AppMonth[['Incident ID']].count()
        counted.tolist()
        counted=counted[0]
        MTTR=AppMonth['RESO'].mean()
        rounded=round(MTTR,2)
        reliability=(720-rounded)/counted
        reliability=round(reliability)
        ReliabilitiesforApps.append(reliability)

    ReliabilitiesforApps=sorted(ReliabilitiesforApps, key=float, reverse=True)
    AppsinMonth = [x for _,x in sorted(zip(ReliabilitiesforApps,AppsinMonth))]
          
    return ({'data': [
                {'x': AppsinMonth, 'y': ReliabilitiesforApps, 'type': 'bar', 'name': value , 'marker':{'color': 'orange'}},
            ],
            'layout': {
                'title': "Reliabilities for {}".format(value)
            }
        }
    )

@app.callback(
   Output(component_id='availabilities-graph-app', component_property='figure'),
   [Input(component_id='availabilityAppAll', component_property='value')])
def update_graph_Availabilities_App(value):
    AppsinService=NEW.dropna(subset=['Service'])
    MonthDF=AppsinService[AppsinService['Month raised']==value]
    array = ['Critical', 'High']
    AppsinMonthcritical=MonthDF.loc[MonthDF['Priority'].isin(array)]
    AppsinMonth=AppsinMonthcritical['Service'].unique()
    AppsinMonth=[x for x in AppsinMonth if str(x) != 'nan']
    AvailabilitiesforApps=[]
    for i in AppsinMonth:
        AppMonth=AppsinMonthcritical[AppsinMonthcritical['Service']==i]
        MTTR=AppMonth['RESO'].mean()
        availability=(720-MTTR)/720
        availability=round(availability,4)
        AvailabilitiesforApps.append(availability)

    AvailabilitiesforApps=sorted(AvailabilitiesforApps, key=float, reverse=True)
    AppsinMonth = [x for _,x in sorted(zip(AvailabilitiesforApps,AppsinMonth))]
 

    return ({'data': [
                    {'x': AppsinMonth, 'y': AvailabilitiesforApps, 'type': 'scatter', 'name': value },
                ],
                'layout': {
                    'title': "Reliabilities for {}".format(value)
                }
            }
        )


@app.callback(
   Output(component_id='mttr-graph-app', component_property='figure'),
   [Input(component_id='MTTRs', component_property='value')])
def update_MTTR(value):
    AppsinService=NEW.dropna(subset=['Service'])
    SelectApp=AppsinService[AppsinService['CI Name']==value]
    AppsMonths=SelectApp['Month raised'].unique()
    AppsMonths=[x for x in AppsMonths if str(x) != 'nan']
    MTTRcritical=[]
    MTTRhigh=[]
    MTTRmedium=[]
    MTTRlow=[]
    for i in AppsMonths:
        SelectAppmonth=SelectApp[SelectApp['Month raised']==i]
        SelectAppmonth=SelectAppmonth[SelectAppmonth['Assigned Group']!="SSI"]
        SelectApplow=SelectAppmonth[SelectAppmonth['Priority']=='Low']
        MTTRlows=SelectApplow['RESO'].mean()
        if str(MTTRlows)=='nan':
            MTTRlow.append(MTTRlows)
        else:
            MTTRlows=round(MTTRlows)
            MTTRlow.append(MTTRlows)
            
        SelectAppmedium=SelectAppmonth[SelectAppmonth['Priority']=='Medium']
        MTTRmediums=SelectAppmedium['RESO'].mean()
        if str(MTTRmediums)=='nan':
            MTTRmedium.append(MTTRmediums)
        else:
            MTTRmediums=round(MTTRmediums)
            MTTRmedium.append(MTTRmediums)
            
        SelectApphigh=SelectAppmonth[SelectAppmonth['Priority']=='High']
        MTTRhighs=SelectApphigh['RESO'].mean()
        if str(MTTRhighs)=='nan':
            MTTRhigh.append(MTTRhighs)
        else:
            MTTRhighs=round(MTTRhighs)
            MTTRhigh.append(MTTRhighs)
            
        SelectAppcritical=SelectAppmonth[SelectAppmonth['Priority']=='Critical']
        MTTRcriticals=SelectAppcritical['RESO'].mean()
        if str(MTTRcriticals)=='nan':
            MTTRcritical.append(MTTRcriticals)
        else:
            MTTRcriticals=round(MTTRcriticals)
            MTTRcritical.append(MTTRcriticals)

    return ({'data': [
                {'x': AppsMonths, 'y': MTTRcritical, 'type': 'bar', 'name': "critical", 'marker':{'color': 'red'}},
                {'x': AppsMonths, 'y': MTTRhigh, 'type': 'bar', 'name': "high", 'marker':{'color': 'orange'}},
                {'x': AppsMonths, 'y': MTTRmedium, 'type': 'bar', 'name': "medium", 'marker':{'color': 'blue'}},
                {'x': AppsMonths, 'y': MTTRlow, 'type': 'bar', 'name': "low", 'marker':{'color': 'green'}}
            ],
            'layout': {
                'title': "MTTRs for {} in 2018".format(value)
            }
        }
    )

@app.callback(
   Output(component_id='numbers-graph-app', component_property='figure'),
   [Input(component_id='Numbers', component_property='value')])
def update_Numbers(value):
    AppsinService=NEW.dropna(subset=['Service'])
    SelectApp=AppsinService[AppsinService['CI Name']==value]
    AppsMonths=SelectApp['Month raised'].unique()
    AppsMonths=[x for x in AppsMonths if str(x) != 'nan']
    Numbercritical=[]
    Numberhigh=[]
    Numbermedium=[]
    Numberlow=[]
    for i in AppsMonths:
        SelectAppmonth=SelectApp[SelectApp['Month raised']==i]
        SelectAppmonth=SelectAppmonth[SelectAppmonth['Assigned Group']!="SSI"]
        SelectApplow=SelectAppmonth[SelectAppmonth['Priority']=='Low']
        countedlow=SelectApplow[['Incident ID']].count()
        countedlow.tolist()
        countedlow=countedlow[0]
        Numberlow.append(countedlow) 
            
        SelectAppmedium=SelectAppmonth[SelectAppmonth['Priority']=='Medium']
        countedmedium=SelectAppmedium[['Incident ID']].count()
        countedmedium.tolist()
        countedmedium=countedmedium[0]
        Numbermedium.append(countedmedium) 

        SelectApphigh=SelectAppmonth[SelectAppmonth['Priority']=='High']
        countedhigh=SelectApphigh[['Incident ID']].count()
        countedhigh.tolist()
        countedhigh=countedhigh[0]
        Numberhigh.append(countedhigh) 

        SelectAppcritical=SelectAppmonth[SelectAppmonth['Priority']=='Critical']
        countedcritical=SelectAppcritical[['Incident ID']].count()
        countedcritical.tolist()
        countedcritical=countedcritical[0]
        Numbercritical.append(countedcritical) 

    return ({'data': [
                {'x': AppsMonths, 'y': Numbercritical, 'type': 'bar', 'name': "critical", 'marker':{'color': 'red'}},
                {'x': AppsMonths, 'y': Numberhigh, 'type': 'bar', 'name': "high", 'marker':{'color': 'orange'}},
                {'x': AppsMonths, 'y': Numbermedium, 'type': 'bar', 'name': "medium", 'marker':{'color': 'blue'}},
                {'x': AppsMonths, 'y': Numberlow, 'type': 'bar', 'name': "low", 'marker':{'color': 'green'}}
            ],
            'layout': {
                'title': "Incidence Volumes for {} in 2018".format(value)
            }
        }
    )

@app.callback(
Output(component_id='VolumesAppAll-graph-app', component_property='figure'),
[Input(component_id='VolumesAppAll', component_property='value')])
def find_numbers_of_CH_App(value):
    Monthsdf=NEW[NEW['Month raised']==value]
    array = ['Critical', 'High']
    AppsinMonthcritical=Monthsdf.loc[Monthsdf['Priority'].isin(array)]
    AppsinMonthA=AppsinMonthcritical['CI Name'].unique()
    AppsinMonthA=[x for x in AppsinMonthA if str(x) != 'nan']
    AppsinMonthCriticalonly=Monthsdf[Monthsdf['Priority']=='Critical']
    AppsinMonthACritical=AppsinMonthCriticalonly['CI Name'].unique()
    AppsinMonthACritical=[x for x in AppsinMonthACritical if str(x) != 'nan']
    CriticalIncidences=[] 
    HighIncidences=[]
    for i in AppsinMonthA:
        SortbyApp=AppsinMonthcritical[AppsinMonthcritical['CI Name']==i]
        Critical=SortbyApp[SortbyApp['Priority']=="Critical"]
        counted=Critical[['Incident ID']].count()
        counted.tolist()
        counted=counted[0]
        CriticalIncidences.append(counted) 
        High=SortbyApp[SortbyApp['Priority']=="High"]
        counted2=High[['Incident ID']].count()
        counted2.tolist()
        counted2=counted2[0]
        HighIncidences.append(counted2)
        CriticalIncidences=list(filter(lambda a: a != 0, CriticalIncidences)) 

        CriticalIncidencesnew=sorted(CriticalIncidences, key=float, reverse=True)
        AppsinMonthACriticalnew = [x for _,x in sorted(zip(CriticalIncidences,AppsinMonthACritical))]
        #AppsinMonthAnew=[x for _,x in sorted(zip(CriticalIncidences,AppsinMonthA))]
        #HighIncidencesnew

       
    return ({'data': [
                {'x': AppsinMonthACriticalnew, 'y': CriticalIncidencesnew, 'type': 'bar', 'name': "Critical" },
                {'x': AppsinMonthA, 'y': HighIncidences, 'type': 'bar', 'name': "High"}
            ],
            'layout': {
                'title': "Critical and High Incidences for ".format(value),
                'xaxis': {'tickangle':"-90"}
            }
        })


@app.callback(
Output(component_id='MTTRsAll-graph-app', component_property='figure'),
[Input(component_id='MTTRsAll', component_property='value')])
def find_MTTRs(value):
    Monthsdf=NEW[NEW['Month raised']==value]
    #array = ['Critical', 'High']
    
    AppsinMonthcritical=Monthsdf[Monthsdf['Priority']=="High"]
    AppsinMonthA=AppsinMonthcritical['CI Name'].unique()
    AppsinMonthA=[x for x in AppsinMonthA if str(x) != 'nan']
    AppsinMonthCriticalonly=Monthsdf[Monthsdf['Priority']=='Critical']
    AppsinMonthACritical=AppsinMonthCriticalonly['CI Name'].unique()
    AppsinMonthACritical=[x for x in AppsinMonthACritical if str(x) != 'nan']
    CriticalIncidences=[] 
    HighIncidences=[]
    for i in AppsinMonthACritical:
        SortbyApp=AppsinMonthCriticalonly[AppsinMonthCriticalonly['CI Name']==i]
        #Critical=SortbyApp[SortbyApp['Priority']=="Critical"]
        counted=SortbyApp["RESO"].mean()
        counted=round(counted,2)
        if counted !=0.0:
            CriticalIncidences.append(counted) 
       
    for i in AppsinMonthA:
        SortbyAppA=AppsinMonthcritical[AppsinMonthcritical['CI Name']==i]
        #High=SortbyAppA[SortbyAppA['Priority']=="High"]
        counted2=SortbyAppA["RESO"].mean()
        counted2=round(counted2,2)
        if counted2!=0.0:
            HighIncidences.append(counted2)
        
        CriticalIncidences=list(filter(lambda a: a != 0, CriticalIncidences)) 
        CriticalIncidencesnew=sorted(CriticalIncidences, key=float, reverse=True)
        AppsinMonthACriticalnew = [x for _,x in sorted(zip(CriticalIncidences,AppsinMonthACritical))]

       
    return ({'data': [
                {'x': AppsinMonthACriticalnew, 'y': CriticalIncidencesnew, 'type': 'bar', 'name': "Critical" },
                {'x': AppsinMonthA, 'y': HighIncidences, 'type': 'bar', 'name': "High"}
            ],
            'layout': {
                'title': "MTTRs for ".format(value),
                'xaxis': {'tickangle':"-90"}
            }
        })











@app.callback(
   Output(component_id='reliability-graph', component_property='figure'),
   [Input(component_id='reliability', component_property='value')])
def update_graph_Reliability(value):
    ServiceDF=NEW[NEW['Service']==value]
    array = ['Critical', 'High']
    ServicesinMonthcritical=ServiceDF.loc[ServiceDF['Priority'].isin(array)]
    monthscolumn=ServicesinMonthcritical['Month raised']
    monthsofService=monthscolumn.unique()
    months=[x for x in monthsofService if str(x) != 'nan']
    Reliabilities=[]
    for i in months: 
        FilterMonth= ServicesinMonthcritical[ServicesinMonthcritical['Month raised']==str(i)]
        counted=FilterMonth[['Incident ID']].count()
        counted.tolist()
        counted=counted[0]
        MTTRser=FilterMonth['RESO'].mean()
        rounded=round(MTTRser,2)
        reliability=(720-MTTRser)/counted
        reliability=round(reliability)
        Reliabilities.append(reliability)

    return ({'data': [
                {'x': months, 'y': Reliabilities, 'type': 'bar', 'name': value , 'marker':{'color': 'orange'}},
            ],
            'layout': {
                'title': "Reliability for {} in 2018".format(value)
            }
        }
    )

@app.callback(
   Output(component_id='availability-graph', component_property='figure'),
   [Input(component_id='availability', component_property='value')])
def update_graph_Availability(value):
    ServiceDF=NEW[NEW['Service']==value]
    array = ['Critical', 'High']
    ServicesinMonthcritical=ServiceDF.loc[ServiceDF['Priority'].isin(array)]
    monthscolumn=ServicesinMonthcritical['Month raised']
    monthsofService=monthscolumn.unique()
    months=[x for x in monthsofService if str(x) != 'nan']
    Availabilities=[]
    for i in months: 
        FilterMonth= ServicesinMonthcritical[ServicesinMonthcritical['Month raised']==str(i)]
        MTTRser=FilterMonth['RESO'].mean()
        availabilitySer=(720-MTTRser)/720
        roundedav=round(availabilitySer,4)
        Availabilities.append(roundedav)
          
    return ({'data': [
                {'x': months, 'y': Availabilities, 'type': 'scatter', 'name': value},
            ],
            'layout': {
                'title': "Availability for {} in 2018".format(value)
            }
        }
    )



@app.callback(
   Output(component_id='allreliabilities', component_property='figure'),
   [Input(component_id='AllReliability', component_property='value')])
def update_graph_Reliabilities(value):
    MonthDF=NEW[NEW['Month raised']==value]
    array = ['Critical', 'High']
    ServicesinMonthcritical=MonthDF.loc[MonthDF['Priority'].isin(array)]
    ServicesinMonth=ServicesinMonthcritical['Service'].unique()
    ServicesinMonth=[x for x in ServicesinMonth if str(x) != 'nan']
    ReliabilitiesforServices=[]
    for i in ServicesinMonth:
        ServiceMonth=ServicesinMonthcritical[ServicesinMonthcritical['Service']==i]
        counted=ServiceMonth[['Incident ID']].count()
        counted.tolist()
        counted=counted[0]
        MTTRser=ServiceMonth['RESO'].mean()
        rounded=round(MTTRser,2)
        reliability=(720-rounded)/counted
        reliability=round(reliability)
        ReliabilitiesforServices.append(reliability)

    ReliabilitiesforServices=sorted(ReliabilitiesforServices, key=float, reverse=True)
    ServicesinMonth = [x for _,x in sorted(zip(ReliabilitiesforServices,ServicesinMonth))]
          
    return ({'data': [
                {'x': ServicesinMonth, 'y': ReliabilitiesforServices, 'type': 'bar', 'name': value , 'marker':{'color': 'orange'}},
            ],
            'layout': {
                'title': "Reliabilities for {}".format(value)
            }
        }
    )

@app.callback(
   Output(component_id='allavailabilities', component_property='figure'),
   [Input(component_id='AllAvailability', component_property='value')])
def update_graph_Availabilities(value):
    MonthDF=NEW[NEW['Month raised']==value]
    array = ['Critical', 'High']
    ServicesinMonthcritical=MonthDF.loc[MonthDF['Priority'].isin(array)]
    ServicesinMonthA=ServicesinMonthcritical['Service'].unique()
    ServicesinMonthA=[x for x in ServicesinMonthA if str(x) != 'nan']
    AvailabilitiesforServices=[] 
    for i in ServicesinMonthA:
        ServiceMonthA=ServicesinMonthcritical[ServicesinMonthcritical['Service']==i]
        MTTRser=ServiceMonthA['RESO'].mean()
        availabilitySer=(720-MTTRser)/720
        roundedav=round(availabilitySer,4)
        AvailabilitiesforServices.append(roundedav)
    
    AvailabilitiesforServices=sorted(AvailabilitiesforServices, key=float, reverse=True)
    ServicesinMonthA = [x for _,x in sorted(zip(AvailabilitiesforServices,ServicesinMonthA))]
          
    return ({'data': [
                {'x': ServicesinMonthA, 'y': AvailabilitiesforServices, 'type': 'bar', 'name': value},
            ],
            'layout': {
                'title': "Availabilities for {}".format(value)
            }
        }
    )





@app.callback(
    Output('datatable-gapminder', 'selected_row_indices'),
    [Input('graph-gapminder', 'clickData')],
    [State('datatable-gapminder', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices

#@app.callback(
  #  Output('graph-gapminder', 'figure'),
  #  [Input('datatable-gapminder', 'rows'),
  #   Input('datatable-gapminder', 'selected_row_indices')])
#def update_figure(rows, selected_row_indices):
    #dff = pd.DataFrame(rows)
    #fig = plotly.tools.make_subplots(
       # rows=2, cols=1,
      #  subplot_titles=('Original Availability', 'New Availability'),
      #  shared_xaxes=True)
    #marker = {'color': ['#0074D9']*len(dff)}
    #for i in (selected_row_indices or []):
       # marker['color'][i] = '#FF851B'
    #trace1=go.Scatter(
       # x=[1,2,3],
       # y= [1,2,3],
    #)
    #trace2=go.Scatter(
      #  x=[1,2,3],
      #  y= [4,5,6],
    #)
    
    #fig['layout']['showlegend'] = False
    #fig['layout']['height'] = 800
    #fig['layout']['margin'] = {
        #'l': 40,
        #'r': 10,
        #'t': 60,
       # 'b': 200
    #}
    #fig['layout']['yaxis3']['type'] = 'log'
    #data=[trace1,trace2]
    #layout = go.Layout(
      #title="Original - Manually corrected Availability"
    #)
    
    #fig=go.Figure(data=data,layout=layout)
    #return fig





@app.callback(
Output(component_id='numberHIGH', component_property='figure'),
[Input(component_id='NumberHIGH', component_property='value')])
def find_numbers_of_CH_Service(value):
    Monthsdf=NEW[NEW['Month raised']==value]
    array = ['Critical', 'High']
    AppsinMonthcritical=Monthsdf.loc[Monthsdf['Priority'].isin(array)]
    AppsinMonthA=AppsinMonthcritical['Service'].unique()
    AppsinMonthA=[x for x in AppsinMonthA if str(x) != 'nan']
    AppsinMonthCriticalonly=Monthsdf[Monthsdf['Priority']=='Critical']
    AppsinMonthACritical=AppsinMonthCriticalonly['Service'].unique()
    AppsinMonthACritical=[x for x in AppsinMonthACritical if str(x) != 'nan']
    CriticalIncidences=[] 
    HighIncidences=[]
    for i in AppsinMonthA:
        SortbyApp=AppsinMonthcritical[AppsinMonthcritical['Service']==i]
        Critical=SortbyApp[SortbyApp['Priority']=="Critical"]
        counted=Critical[['Incident ID']].count()
        counted.tolist()
        counted=counted[0]
        CriticalIncidences.append(counted) 
        High=SortbyApp[SortbyApp['Priority']=="High"]
        counted2=High[['Incident ID']].count()
        counted2.tolist()
        counted2=counted2[0]
        HighIncidences.append(counted2)
        CriticalIncidences=list(filter(lambda a: a != 0, CriticalIncidences)) 

        CriticalIncidencesnew=sorted(CriticalIncidences, key=float, reverse=True)
        AppsinMonthACriticalnew = [x for _,x in sorted(zip(CriticalIncidences,AppsinMonthACritical))]
        #AppsinMonthAnew=[x for _,x in sorted(zip(CriticalIncidences,AppsinMonthA))]
        #HighIncidencesnew

       
    return ({'data': [
                {'x': AppsinMonthACriticalnew, 'y': CriticalIncidencesnew, 'type': 'bar', 'name': "Critical" },
                {'x': AppsinMonthA, 'y': HighIncidences, 'type': 'bar', 'name': "High"}
            ],
            'layout': {
                'title': "Critical and High Incidences ",
                'xaxis': {'tickangle':"-90"}
            }
        })


    
app.css.append_css({
   'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


if __name__ == '__main__':
    app.run_server(debug=True)

