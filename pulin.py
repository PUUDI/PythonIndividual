# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 23:28:01 2021

@author: Pulin
"""

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import date

app = dash.Dash(__name__)
#Reading the data from source
df = pd.read_excel('owid-covid-data.xlsx' ,sheet_name='Sheet1', usecols="A,B,C,D,E,F,H,I,AU,AZ,K")

#Filtering the data for World
df_world = df.loc[df['location'] == "World"]

dfc = df.groupby(by = 'continent').mean().reset_index()

dfd_world = df_world.groupby(by = 'date').sum().reset_index()

#data = dict(labels = ['hosp_patients', 'icu_patients','new_deaths'] , values = dfd[dfd['date']=='2021-09-18'][['hosp_patients', 'icu_patients','new_deaths']].values.tolist()[0])

#Default figure for line plot 01
fig1 = px.line( x =dfd_world['date'], y = dfd_world['new_cases'] , title = "New cases Summary")

#Default figure for line plot 02
fig2 = px.line(dfd_world, x ='date', y = ['new_cases' , 'total_cases'] , title = "New cases Summary")

#Default Figure for line plot


#fig3 = px.funnel(data, x = 'values', y = 'labels')

app.layout = html.Div([html.Div([
        dcc.Dropdown(
            id='dropdown_line1',
            options=[
                {'label': 'Total Cases', 'value':'total_cases'},
                {'label': 'New Cases', 'value':'new_cases'},
                {'label': 'New Deaths', 'value':'new_deaths'},
                {'label': 'Total Deaths', 'value':'total_deaths'}],
            value="total_cases" ),
    
        dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2021, 5, 19),
                initial_visible_month=date(2021, 1, 1),
                start_date = date(2021 ,1,1),
                end_date=date(2021, 1, 12),
                end_date_placeholder_text = "End Date",
                first_day_of_week = 1,
                display_format = 'MMM Do, YYYY',
                day_size = 50
                )
                ]),
    
            
    dcc.Graph(id = 'line1', figure = fig1),
    
    html.Div(id = 'howard'),
    
    dcc.Graph(id = 'scatter' , figure = fig2),
    
    dcc.Graph(id = 'line2', figure = fig2)])


@app.callback(
    Output('line1', 'figure'),
    Input('dropdown_line1','value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))

def line1(var , start_date , end_date):
    
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
    
    fig1 = px.line(x =dfd_world['date'], y = dfd_world[var])
 
    fig1.update_layout(
    title=title1,
    xaxis_title="Date",
    yaxis_title=var_title,
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
        )
    )
    return fig1
    
    
    
@app.callback(
    
    Input('my-date-picker-range', 'start_date'))

def line2(start_date):
    print(start_date)
    # =============================================================================
# #=============================================================================
#    if (var == 'location'):
#          dfc = df.groupby(by = 'location').mean().reset_index()
#          fig = px.scatter(x = dfc['population'], y = dfc['gdp_per_capita'], color = dfc['location'], size = dfc['total_cases_per_million'],hover_name = dfc['location'])
#          #return fig
#      else:
#          dfc = df.groupby(by = 'continent').mean().reset_index()
#          fig = px.scatter(x = dfc['population'], y = dfc['gdp_per_capita'], color = dfc['continent'], size = dfc['total_cases_per_million'],hover_name = dfc['continent'])
#          #return fig
#      return fig
# #=============================================================================
# =============================================================================
    


if __name__ == '__main__':
    app.run_server(port = 8020, debug = False)