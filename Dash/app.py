# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from datetime import date

import plotly.express as px


import pandas as pd
import numpy as np
from scripts.data_wrangling import load_data

#external_stylesheets = ['css/style.css']
#c    'background': '#111111',
#    'text': '#7FDBFF'
#}
app = dash.Dash(__name__,title='Household Analytics')#, external_stylesheets=external_stylesheets)


df,df2,dg = load_data()
def bar_style(fig):
    fig.update_xaxes(showgrid=False,title='')
    fig.update_yaxes(title='')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    return

fig2 = px.line(df, x="DateTime",
                y="Acc_Value", hover_data=['Post','Value'],
                title='Akkumuleret værdi over tid')
fig3 = px.bar(dg, x="DateTime", y="Value", color='Category',title='Udgifter fordelt på kategorier')
fig3.update_xaxes(showgrid=False)
fig3.update_yaxes(showgrid=False)
fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)')
bar_style(fig3)

cardstyle = {'borderRadius': '5px',
'backgroundColor':'#f9f9f9',
'margin':'10px',
'padding': '15px',
'position': 'relative',
'boxShadow': '2px 2px 2px lightgrey'}

unique_months = dg['DateTime'].drop_duplicates().reset_index(drop=True)
max_slider_steps = unique_months.shape[0]-1

budget_layout = html.Div(#className='container',
children=[
html.Div(children = [
    html.Div(
        className='row flex',
        children=[
            html.Div(
                className = 'four columns',
                children=[
                    html.Div(className = 'mini_container', id='filters', children =[
                    html.P('Vælg dato interval'),
                    html.Div(className = 'slider_container', children = [
                    dcc.RangeSlider(
    id='month-slider',
    min = 0,
    max = max_slider_steps,
    step = None,
    marks = {key: {'label':value[0:max_slider_steps],'style':{'transform': 'rotate(-45deg)','font-size':'8px','left':str(100/max_slider_steps*(key)-100/max_slider_steps    )+'%'}} for (key, value) in dict(unique_months).items()},
    value = [max_slider_steps-6,max_slider_steps]
    #className = 'rotate'
    )]),
    html.Div(id='slider-output-container'),
                        dcc.DatePickerRange(id='date-picker-range',
                                min_date_allowed=date(1995, 8, 5),
                                max_date_allowed=date(2030, 12, 31),
                                start_date = date(2020, 1, 1),
                                end_date=date(2020, 12, 31),
                                display_format='DD/MM/YYYY',
                          #'background-color': '#f9f9f9'}
                            #
                            )
                                ])
                    ]),
            html.Div(
                className='eight columns',
                children = [
                    html.Div(className = 'row container-display', children = [
                        html.Div(className = 'mini_container', id = 'card1',
                            children = [
                                html.H6(id='lastest-expense',children=['FLASHY CARD']),
                                html.P('Total forbrug seneste måned')
                            ]),
                        html.Div(className = 'mini_container', id ='card2',
                                children = [
                                    html.H6(id='percentile-groc',children=['0']),
                                    html.P('Dagligvarerandel seneste måned')
                                ]),
                    ]),
                    html.Div(className = 'mini_container',
                        children = [
                        dcc.Graph(id='expenditures',figure=fig3)
                        ])
                ])
        ]),
    html.Div(
        className='row flex',
        children=[
        html.Div(
            className='twelve columns',
            children = [
            html.Div(className = 'mini_container', children =[
            ''' Vælg dato interval ''',

                dcc.DatePickerRange(id='date-picker-range',
                        min_date_allowed=date(1995, 8, 5),
                        max_date_allowed=date(2030, 12, 31),
                        start_date = date(2020, 1, 1),
                        end_date=date(2020, 12, 31),
                        display_format='DD/MM/YYYY',

                        ),

                        dcc.Graph(id='acc-value',figure=fig2,
                        style = {'background-color': '#f9f9f9'})
                    ])

    ])
])
])
])


app.layout = html.Div(children=[
    html.H1(children='Household BI'),
    html.Div([
        dcc.Location(id="url"),
        html.Div([
            dcc.Link('Budget', href="/Budget"),
            dcc.Link('Aktier', href="/Aktier"),
            dcc.Link('Crowdlending', href="/Crowdlending")
        ]),
        html.Div(id='content-field-in-app-layout')
    ])
])

app.config['suppress_callback_exceptions']=True
@app.callback(
    Output(component_id='acc-value', component_property='figure'),
    [Input(component_id='date-picker-range', component_property='start_date'),
    Input(component_id='date-picker-range', component_property='end_date')]
)
def update_output_div(start_date,end_date):
    return px.line( df[(df['DateTime']>=start_date)&(df['DateTime']<=end_date)],
                    x = 'DateTime',
                    y = 'Acc_Value',
                    hover_data=['Post','Value'],
                    title='Akkumuleret værdi over tid'
                )

@app.callback(
    [Output('expenditures', component_property='figure'),
     Output('lastest-expense', component_property='children'),
     Output('percentile-groc', component_property='children')
    ],
    [Input('month-slider', 'value')])

def update_output(value):
    selected_months = unique_months.loc[value[0]:value[1]]
    fig = px.bar(dg[dg['DateTime'].isin(selected_months)],
                x="DateTime", y="Value",
                color='Category',title='Udgifter fordelt på kategorier')
    bar_style(fig)
    lastest_month = unique_months.loc[value[1]]
    latest_expense = dg[dg['DateTime'] == lastest_month]['Value'].sum()
    percentile_groc = 100*dg[(dg['DateTime'] == lastest_month) & (dg['Category'] == 'Dagligvarer')]['Value']/latest_expense
    percentile_groc = round(percentile_groc,1)
    return fig, latest_expense, percentile_groc

@app.callback(Output('content-field-in-app-layout', 'children'),
[Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/Budget":
   	    return budget_layout
    elif pathname == "/":
        return budget_layout
    elif pathname == "/Aktier":
   	    return Marketing_layout
    elif pathname == "/Crowdlending":
   	    return Finance_layout
    else:
   	    return Error_display_layout

if __name__ == '__main__':
    app.run_server(debug=True,port=8080,host='0.0.0.0')
