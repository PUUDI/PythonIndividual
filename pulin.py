# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 23:28:01 2021
@author: Pulin
"""

import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import json

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#Reading the data from source
df = pd.read_excel('owid-covid-data.xlsx',sheet_name='Sheet1', usecols="A,B,C,D,E,F,H,I,AU,AZ,K,Z")

df['date'] = pd.to_datetime(df['date'])

#Unique value of location column to use in dropdown selector
available_location = df['location'].unique()

#Filtering the data for World
df_world = df.loc[df['location'] == "World"]

df_sl = df.loc[df['location'] == "Sri Lanka"]
saarck_list = ['afghanistan','Bangladesh','Bhutan' ,'India' , 'Nepal' , 'Maldives','Pakistan','Sri Lanka']

df_saarck = df[df.location.isin(saarck_list)]
df_saarck =  df_saarck.groupby(by = 'date').sum().reset_index()
df_asia = df.loc[df['location'] == 'Asia']

#dfc = df.groupby(by = 'continent').mean().reset_index()

dfd_world = df_world.groupby(by = 'date').sum().reset_index()
dfd_sl = df_sl.groupby(by = 'date').sum().reset_index()

#Creating the ROW dataframe for the figure 02


#data = dict(labels = ['hosp_patients', 'icu_patients','new_deaths'] , values = dfd[dfd['date']=='2021-09-18'][['hosp_patients', 'icu_patients','new_deaths']].values.tolist()[0])

#Default figure for line plot 01
fig1 = px.line( x =dfd_world['date'], y = dfd_world['total_cases'] , title = "New cases Summary")

#Default figure for line plot 02
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_world['date'], y=(df_world['total_cases']),
                    mode='lines',
                    name='lines'))
fig2.add_trace(go.Scatter(x=df_sl['date'], y=df_sl['total_cases'],
                    mode='lines',
                    name='lines'))
fig2.add_trace(go.Scatter(x=df_saarck['date'], y=df_saarck['total_cases'],
                    mode='lines',
                    name='lines'))
#fig.add_trace(go.Scatter(x=random_x, y=random_y2,
#                    mode='markers', name='markers'))


#Style for dcc components
buttons_style =  {'background-color': 'White',
            #'height': '200px',
            #width: 200px;
            'font-size':'20px',
            'color': 'Black',
            'textAlign': 'center'
            }


#fig3 = px.funnel(data, x = 'values', y = 'labels')

app.layout = html.Div([
        html.Div([
        dcc.Store(id='intermediate-value'),
        dcc.Store(id='df_cal'),
        
        dbc.Row(dbc.Col(html.H3("COVID-19 DASHBOARD"),
                        width={'size': 6, 'offset': 3},
                        ),
                ),
        
        dbc.Row([
                dbc.Col(dcc.Dropdown(id='dropdown_line1',
                options=[
                {'label': 'Total Cases', 'value':'total_cases'},
                {'label': 'New Cases', 'value':'new_cases'},
                {'label': 'New Deaths', 'value':'new_deaths'},
                {'label': 'Total Deaths', 'value':'total_deaths'}],
                value = 'total_cases',
                style = {
                        'background-color': 'White',
                        'textAlign': 'center'
                        }
                        
                         ),style = buttons_style,

                 width={'size': 2, "offset": 1, 'order': 1}
                 
                         ),
                dbc.Col(dcc.Checklist(id='checklist_fig2',
                options =[
                        {'label':'Rest of the world','value':'ROW'},
                        {'label':'Asia','value':'asia'},
                        {'label':'SAARCK','value':'saarck'}],
                value = 'ROW'
                         ),style =buttons_style,

                 width={'size': 2, "offset":1, 'order': 2}
                 
                         ),

                 dbc.Col(dcc.Dropdown(id='dropdown_line2',
                options=[
                {'label': 'Daily', 'value':'daily'},
                {'label': 'Weekly Average', 'value':'weekly_avg'},
                {'label': 'Monthly Average', 'value':'monthly_avg'},
                {'label': '7-Day Average', 'value':'7day_avg'},
                {'label': '14-Day Average', 'value':'14day_avg'}],
                value = 'daily'
                         ),style = buttons_style,

                 width={'size': 2, "offset": 1, 'order': 3}
                 
                         ),

                dbc.Col(dcc.DatePickerRange(  #The date picker for the figure 1 line plot
                id='my-date-picker-range',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2021, 5, 19),
                initial_visible_month=date(2021, 1, 1),
                start_date = date(2020 ,6,1),
                end_date= date(2020, 7, 16),
                end_date_placeholder_text = "End Date",
                first_day_of_week = 1,
                #display_format = 'MMM Do, YYYY',
                day_size = 50
                        ),style = buttons_style,

                width={'size': 2, "offset": 1, 'order': 4}
                         ),
                    ]
                    ),
        dbc.Row([
                dbc.Col(dcc.Graph(id='line1', figure={}),
                        width=6#, lg={'size': 6,  "offset": 0, 'order': 'first'}
                        ),
                dbc.Col(dcc.Graph(id='scatter', figure={}),
                        width=6#, lg={'size': 6,  "offset": 0, 'order': 'last'}
                        ),
                
                
                ]),
                        
        dbc.Row([
                 dbc.Col(dcc.Dropdown(id='dropdown_figure3',
                options=[{'label': i, 'value': i} for i in available_location],
                value = 'China'
                         ),

                 width={'size': 3, "offset": 0, 'order': 3}
                 
                         ),           
            
                ]),
        dbc.Row([
                dbc.Col(dcc.Graph(id='line2', figure={}),
                        width=6#, lg={'size': 6,  "offset": 0, 'order': 'first'}
                        ),
                dbc.Col(dcc.Graph(id='line3', figure={}),
                        width=6#, lg={'size': 6,  "offset": 0, 'order': 'last'}
                        ),
                
                
                ]),
                        
         dbc.Row([
                dbc.Col(dcc.Graph(id='bar1', figure={},clear_on_unhover=True),
                        width={'size': 6, "offset": 0, 'order': 2}#, lg={'size': 6,  "offset": 0, 'order': 'first'}
                        ),
                dbc.Col(dcc.Graph(id='bar2',  figure={}),
                        width = {'size': 6, "offset": 0, 'order': 1}#, lg={'size': 6,  "offset": 0, 'order': 'last'}
                        ),
                
                
                ])
                
            
                ])
])

                
                
        

@app.callback(
    Output('line1', 'figure'),
    Input('dropdown_line1','value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))

def figure1(var , start_date , end_date):
    
    #df_world = df.loc[df['location'] == "World"]
    
    after_start_date = df_world["date"] >= start_date
    before_end_date = df_world["date"] <= end_date
    
    between_two_dates = after_start_date & before_end_date
    
    df_world_date = df_world.loc[between_two_dates]
    
    dfd_world = df_world_date.groupby(by = 'date').sum().reset_index()
    #Changing the title of the figure
    if var == "total_cases":
        var_title = "Total cases"
    elif var == "new_cases":
        var_title = "New cases"
    elif var == "new_deaths":
        var_title = "New deaths"
    else:
        var_title = "Total deaths"
    
    title1 = "{} summary between {} and {}".format(var_title , start_date , end_date)
    
    fig1 = px.line( x =dfd_world['date'], y = dfd_world[var])    
    
    fig1.update_layout(
    title=title1,
    template='plotly_dark',
    xaxis_title="Date",
    yaxis_title=var_title,
    legend_title="Legend Title"
    )
    
    return fig1
    
    
    
@app.callback(
    Output('scatter', 'figure'),
    Input('checklist_fig2', 'value'),
    Input('dropdown_line1','value'),
    Input('dropdown_line2' , 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('df_cal', 'data'))

def figure2(check_list , var , cal_type , start_date , end_date, s):
    
    df_cal = json.loads(s)
    
    #df_ROW_date = df_cal[0]
    #df_sl_date = df_cal[1]
    #df_asia_date = df_cal[2]
    #df_saarck_date = df_cal[3]
    ##################################3
    
   
        
    #Basic figure with SL line visible and default
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=list(df_cal[1]['date'].values()), y=list(df_cal[1][var].values()),
                    mode='lines',
                    name='lines'))
    #For loop to add the requesting lines to the existing graphs with go.trace
    for data in check_list:
        
        if data == 'ROW':
            fig2.add_trace(go.Scatter(x=list(df_cal[0]['date'].values()), y=list(df_cal[0][var].values()),
                    mode='lines',
                    name='lines'))
        elif data =='asia':
            fig2.add_trace(go.Scatter(x=list(df_cal[2]['date'].values()), y=list(df_cal[2][var].values()),
                    mode='lines',
                    name='lines'))
        elif data =='saarck':
            fig2.add_trace(go.Scatter(x=list(df_cal[3]['date'].values()), y=list(df_cal[3][var].values()),
                    mode='lines',
                    name='lines'))
            
    fig2.update_layout(title="Figure Title",
                  template='plotly_dark')
    
    return(fig2)
    
 
    
    
@app.callback(
    Output('intermediate-value', 'data'),
    Input('dropdown_line1','value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))

def row_data(var , start_date , end_date):   
    
    after_start_date = df_world["date"] >= start_date
    before_end_date = df_world["date"] <= end_date
    
    between_two_dates_ROW = after_start_date & before_end_date 
    
    after_start_date = df_sl["date"] >= start_date
    before_end_date = df_sl["date"] <= end_date
    
    between_two_dates_sl = after_start_date & before_end_date
    
    df_sl_date = df_sl.loc[between_two_dates_sl]
    df_ROW_date = df_world.loc[between_two_dates_ROW]
    
    df_sl_date =  df_sl_date.groupby(by = 'date').sum().reset_index()
    df_ROW_date =  df_ROW_date.groupby(by = 'date').sum().reset_index()
    
    df_sl_date = df_sl_date.set_index('date')
    
    df_ROW_date['new_cases'] = df_ROW_date['new_cases'] - df_ROW_date['date'].map(df_sl_date['new_cases'])
    df_ROW_date['total_cases'] = df_ROW_date['total_cases'] - df_ROW_date['date'].map(df_sl_date['total_cases'])
    df_ROW_date['new_deaths'] = df_ROW_date['new_deaths'] - df_ROW_date['date'].map(df_sl_date['new_deaths'])
    df_ROW_date['total_deaths'] = df_ROW_date['total_deaths'] - df_ROW_date['date'].map(df_sl_date['total_deaths'])
    
    
    #df_ROW_date = df_ROW_date[['date','diff_new_cases','diff_total_cases','diff_new_deaths','diff_total_deaths']]
    
    return(df_ROW_date.to_json(date_format='iso', orient='split'))

@app.callback(
    Output('df_cal', 'data'),
    Input('dropdown_line2','value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('intermediate-value', 'data'))

def cal_type(cal_type , start_date , end_date,jsonified_cleaned_data): 
    
    after_start_date = df_sl["date"] >= start_date
    before_end_date = df_sl["date"] <= end_date
    
    between_two_dates_sl = after_start_date & before_end_date
    ###########################################
    after_start_date = df_saarck["date"] >= start_date
    before_end_date = df_saarck["date"] <= end_date
    
    between_two_dates_saarck = after_start_date & before_end_date
    ###########################################
    after_start_date = df_asia["date"] >= start_date
    before_end_date = df_asia["date"] <= end_date
    
    between_two_dates_asia = after_start_date & before_end_date
    #Filtering by the choosen date range
    
    df_sl_cal = df_sl.loc[between_two_dates_sl]
    df_saarck_cal = df_saarck.loc[between_two_dates_saarck]
    df_asia_cal = df_asia.loc[between_two_dates_asia]
   
    #################################################33
    df_ROW_cal = pd.read_json(jsonified_cleaned_data, orient='split')
    
    
  
    
    df_ROW_i = df_ROW_cal.set_index('date')
    df_sl_i = df_sl_cal.set_index('date')
    df_asia_i = df_asia_cal.set_index('date')
    df_saarck_i = df_saarck_cal.set_index('date')
    
    
    if cal_type == 'weekly_avg':
        
        df_ROW_cal = df_ROW_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("W").mean()
        df_sl_cal = df_sl_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("W").mean()
        df_asia_cal = df_asia_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("W").mean()
        df_saarck_cal = df_saarck_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("W").mean()

    
    elif cal_type  == "monthly_avg":
        df_ROW_cal = df_ROW_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("M").mean()
        df_sl_cal = df_sl_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("M").mean()
        df_asia_cal = df_asia_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("M").mean()
        df_saarck_cal = df_saarck_i[['total_cases','new_cases','new_deaths','total_deaths']].resample("M").mean()

    elif cal_type == '7day_avg':
        df_ROW_cal[['total_cases','new_cases','new_deaths','total_deaths']] = df_ROW_cal[['total_cases','new_cases','new_deaths','total_deaths']].rolling(window=7,min_periods=1).mean()
        df_sl_cal[['total_cases','new_cases','new_deaths','total_deaths']] = df_sl_cal[['total_cases','new_cases','new_deaths','total_deaths']].rolling(window=7,min_periods=1).mean()
        df_asia_cal[['total_cases','new_cases','new_deaths','total_deaths']] = df_asia_cal[['total_cases','new_cases','new_deaths','total_deaths']].rolling(window=7,min_periods=1).mean()
        df_saarck_cal[['total_cases','new_cases','new_deaths','total_deaths']] = df_saarck_cal[['total_cases','new_cases','new_deaths','total_deaths']].rolling(window=7,min_periods=1).mean()
    
    elif cal_type == '14day_avg':
        df_ROW_cal[['total_cases','new_cases','new_deaths','total_deaths']] = df_ROW_cal[['total_cases','new_cases','new_deaths','total_deaths']].rolling(window=14,min_periods=1).mean()
        df_sl_cal[['total_cases','new_cases','new_deaths','total_deaths']] = df_sl_cal[['total_cases','new_cases','new_deaths','total_deaths']].rolling(window=14,min_periods=1).mean()
        df_asia_cal[['total_cases','new_cases','new_deaths','total_deaths']] = df_asia_cal[['total_cases','new_cases','new_deaths','total_deaths']].rolling(window=14,min_periods=1).mean()
        df_saarck_cal[['total_cases','new_cases','new_deaths','total_deaths']] = df_saarck_cal[['total_cases','new_cases','new_deaths','total_deaths']].rolling(window=14,min_periods=1).mean()
    
    df_ROW_cal = df_ROW_cal.reset_index()
    df_sl_cal = df_sl_cal.reset_index()
    df_asia_cal = df_asia_cal.reset_index()
    df_saarck_cal = df_saarck_cal.reset_index()
    
    df_ROW_cal['date'] = df_ROW_cal['date'].astype(str)
    df_sl_cal['date'] = df_sl_cal['date'].astype(str)
    df_asia_cal['date'] = df_asia_cal['date'].astype(str)
    df_saarck_cal['date'] = df_saarck_cal['date'].astype(str)
    
    
    list_df = [df_ROW_cal, df_sl_cal,df_asia_cal,df_saarck_cal]
    s = json.dumps([df.to_dict() for df in list_df])
           
    return(s)



@app.callback(
    Output('line2', 'figure'),
    Input('dropdown_figure3','value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('intermediate-value', 'data'))

def ratio_fun(location , start_date , end_date,jsonified_cleaned_data):     
    
    df['ratio'] = df['new_tests']/df['new_cases'] 
    
    df_loc = df.loc[df['location'] == location]
    df_loc_sl = df.loc[df['location'] == 'Sri Lanka']
    
    #Group by to filter by date range
    df_loc =  df_loc.groupby(by = 'date').sum().reset_index()
    df_loc_sl =  df_loc_sl.groupby(by = 'date').sum().reset_index()
    
    #Filtering by date range
    after_start_date = df_loc["date"] >= start_date
    before_end_date = df_loc["date"] <= end_date
    
    between_two_dates_loc = after_start_date & before_end_date
    ###########################################
    after_start_date = df_loc_sl["date"] >= start_date
    before_end_date = df_loc_sl["date"] <= end_date
    
    between_two_dates_sl = after_start_date & before_end_date
    
    df_loc = df_loc.loc[between_two_dates_loc]
    df_loc_sl = df_loc_sl.loc[between_two_dates_sl]
    
    #Drawing the figure
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df_loc_sl['date'], y=df_loc_sl['ratio'],
                    mode='lines',
                    name='lines'))
    #For loop to add the requesting lines to the existing graphs with go.trace
    
        
    fig3.add_trace(go.Scatter(x=df_loc['date'], y=df_loc['ratio'],
                    mode='lines',
                    name='lines'))
    
    fig3.update_layout(title="Figure Title",
                  template='plotly_dark')
    
    return(fig3)# =============================================================================

@app.callback(
    Output('line3', 'figure'),
    Input('dropdown_figure3','value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('intermediate-value', 'data'))

def figure4(location , start_date , end_date,jsonified_cleaned_data):  
    
    cor = round(df_sl[['new_tests' , 'new_cases']].corr()['new_cases'][0],2)
    
    N = 100000
    
    fig4 = go.Figure(data=go.Scattergl(
    x = df_sl['new_tests'],
    y = df_sl['new_cases'],
    mode='markers',
    marker=dict(
        color=np.random.randn(N),
        colorscale='Viridis',
        line_width=1
    )
    ))

    fig4.add_annotation(x=max(df_sl['new_tests']), y=max(df_sl['new_cases']),
            text= "{}".format(cor),
            font=dict(
            family="Courier New, monospace",
            size=25,
            color="#ff7f0e"
            ),
            showarrow=False,
            arrowhead=1)
    
    fig4.update_layout(title="Figure Title",
                  template='simple_white')
    
    return(fig4)


@app.callback(
    Output('bar1', 'figure'),
    Input('dropdown_figure3','value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('intermediate-value', 'data'),
    Input('bar2', 'hoverData'),
    Input('dropdown_line1','value'))

def bar1(location , start_date , end_date,jsonified_cleaned_data,hover_data,var):  # #=============================================================================
#   
    after_start_date = df["date"] >= start_date
    before_end_date = df["date"] <= end_date
    
    between_two_dates = after_start_date & before_end_date
    df_bar = df.loc[between_two_dates]
    
    
    
    
    df_cross = pd.crosstab(df_bar.date,df_bar.continent, values = df_bar.new_cases , aggfunc = np.sum)
# initiate data list for figure
    trace_index = hover_data["points"][0]["pointIndex"]
    colors = ['lightslategray',] * 6
    colors[trace_index] = 'crimson'
    
    data = []
#use for loop on every zoo name to create bar data
    for index,x in enumerate(df_cross.columns):
        data.append(go.Bar(name=str(x), x=df_cross.index, y=df_cross[x] , marker_color=colors[index]))

    figure = go.Figure(data)
    figure.update_layout(barmode = 'stack')

#For you to take a look at the result use
    #print(hover_data)
    return(figure)
    #if (var == 'location'):
#          dfc = df.groupby(by = 'location').mean().reset_index()
#          fig = px.scatter(x = dfc['population'], y = dfc['gdp_per_capita'], color = dfc['location'], size = dfc['total_cases_per_million'],hover_name = dfc['location'])
@app.callback(
    Output('bar2', 'figure'),
    Input('dropdown_figure3','value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('bar2', 'hoverData'),
    Input('dropdown_line1','value'))

def bar2(location , start_date , end_date,hover_data,var): #          #return fig
    
    after_start_date = df["date"] >= start_date
    before_end_date = df["date"] <= end_date
    
    between_two_dates = after_start_date & before_end_date
    df_bar = df.loc[between_two_dates]
    
    df_bar =  df_bar.groupby(by = 'continent').sum().reset_index()
    #df_bar = df_bar.sort_values(var, ascending=False)
    
    colors = ['lightslategray',] * 6
    #colors[trace_index] = 'crimson'
    
    
    fig = go.Figure(data=[go.Bar(
    y=df_bar['continent'],
    x=df_bar[var],
    orientation='h',
    marker_color=colors # marker color can be a single color value or an iterable
    )])
    
    fig.update_layout(title_text='Least Used Feature')
    
    return(fig)
    #print(trace_index)

    #print(trace_index)       
#          fig = px.scatter(x = dfc['population'], y = dfc['gdp_per_capita'], color = dfc['continent'], size = dfc['total_cases_per_million'],hover_name = dfc['continent'])
#          #return fig
#      return fig
# #=============================================================================
# =============================================================================
    


if __name__ == '__main__':
    app.run_server(port = 8020, debug = False)
