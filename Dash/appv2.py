# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from datetime import date

import plotly.express as px


import pandas as pd
import numpy as np
from scripts.data_wrangling import load_data

#external_stylesheets = ['css/style.css']
#c    'background': '#111111',
#    'text': '#7FDBFF'
#}
app = dash.Dash(__name__,title='Household Analytics',external_stylesheets=[dbc.themes.SLATE])#, external_stylesheets=external_stylesheets)


df,df2,dg = load_data()
def bar_style(fig):
    fig.update_xaxes(showgrid=False,title='')
    fig.update_yaxes(title='')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(legend_font={'color':'#aaa'})
    fig.update_xaxes(title_font={'color':'#aaa'})
    fig.update_xaxes(tickfont={'color':'#aaa'})
    fig.update_traces(textposition='outside')
    return

fig2 = px.line(df, x="DateTime",
                y="Acc_Value", hover_data=['Post','Value'],
                title='Akkumuleret værdi over tid')
fig_expenses = px.bar(dg, x="DateTime", y="Value", color='Category',title='Udgifter fordelt på kategorier',text='Value')
bar_style(fig_expenses)

#cardstyle = {'borderRadius': '5px',
#'backgroundColor':'#f9f9f9',
#'margin':'10px',
#'padding': '15px',
#'position': 'relative',
#'boxShadow': '2px 2px 2px lightgrey'}

unique_months = dg['DateTime'].drop_duplicates().reset_index(drop=True)
max_slider_steps = unique_months.shape[0]-1

budget_layout = html.Div(#className='container',
children=[
html.Div(children = [
    dbc.Row(children=[
        dbc.Col(
            html.Div(
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
                            )
                    ]),
                    dcc.Dropdown(options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'Montreal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                        ],
                        value=['MTL', 'NYC'], multi=True
                    )
                    ])
            ]),
            width=4),
            dbc.Col(
            html.Div(
                children = [
                    html.Div(className = 'row container-display', children = [
                        html.Div(className = 'mini_container', #id = 'card1',
                            children = [
                                html.H6(id='lastest-expense',children=['FLASHY CARD']),
                                html.P('Total forbrug seneste måned')
                            ]),
                        html.Div(className = 'mini_container', #id ='card2',
                                children = [
                                    html.H6(id='percentile-groc',children=['0']),
                                    html.P('Dagligvarerandel seneste måned')
                                ]),
                    ]),
                    html.Div(className = 'mini_container',
                        children = [
                        dcc.Graph(id='expenditures',figure=fig_expenses)
                        ])
                ]), width=8)
                ]
        ),


    dbc.Row(
    dbc.Col(
        html.Div(
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

    ]))
)
])
])


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Fælleskort", href="/Faelles",id="page-1-link")),
        dbc.NavItem(dbc.NavLink("Aktier", href="/Aktier",id="page-2-link")),
        dbc.NavItem(dbc.NavLink("Crowdlending", href="/Crowdlending",id="page-3-link")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Household BI",
    brand_href="/",
    color="primary",
    dark=True,
    #id="page-1-link",
    fluid=True
)

Error_display_layout = html.Div('Du er helt på afveje makker')

faelles_layout = html.Div(id='faelles-container', children = [
        dbc.Row(html.H2('Fælleskortet')),
        dbc.Row(children=[
            dbc.Col(width=4,children=[
                dbc.Card(
                    dbc.CardBody(
                        html.Div(children = [
                            html.H4('Filtrering'),
                            dcc.RangeSlider(
                                id='month-slider',
                                min = 0,
                                max = max_slider_steps,
                                step = None,
                                marks = {key: {'label':value[0:max_slider_steps],'style':{'transform': 'rotate(-45deg)','font-size':'8px','left':str(100/max_slider_steps*(key)-100/max_slider_steps    )+'%'}} for (key, value) in dict(unique_months).items()},
                                value = [max_slider_steps-6,max_slider_steps]
                                )
                    ]))
                )
            ]
        ),
        dbc.Col(width=8, children=[
            dbc.Row(children=[
                dbc.Col(dbc.Alert(color="secondary", className="close", children=[
                    html.H6(id='ban-latest-total',children=['0']),
                    html.P('Seneste måneds udgifter'),
                    ])
        ),
        dbc.Col(dbc.Alert(color="secondary", className="close",
        children=[html.H6(id='ban-latest-groc',children=['0']),
                  html.P('Seneste måneds dagligvarer')])
            )
            ]),
            dbc.Row(dbc.Card(
                        dbc.CardBody(dcc.Graph(id='expenditures',figure=fig_expenses))
                    )
            ),
        ]
        )
    ]
        )
    
   
    ])
    

app.layout = html.Div(children = 
    [dcc.Location(id="url", refresh=False),navbar,
     dbc.Container(html.Div(id='content-field-in-app-layout'))
])


@app.callback(Output('content-field-in-app-layout', 'children'),
[Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/Faelles":
   	    return faelles_layout
    elif pathname == "/":
        return budget_layout
    elif pathname == "/Aktier":
   	    return aktier_layout
    elif pathname == "/Crowdlending":
   	    return crowdlending_layout
    else:
   	    return Error_display_layout



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
     Output('ban-latest-total', component_property='children'),
     Output('ban-latest-groc', component_property='children')
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
    return fig, round(latest_expense,1), percentile_groc



if __name__ == '__main__':
    app.run_server(debug=True,port=8080,host='0.0.0.0')
