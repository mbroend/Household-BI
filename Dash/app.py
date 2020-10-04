# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
df = pd.read_csv('../data/export.csv',delimiter=';', header=None, names=['Date','Date1','Post','Value','Acc_Value'])
df.drop(columns=['Date1'],inplace=True)
df.Value = df.Value.str.replace('.','').str.replace(',','.').astype('float64')
df.Acc_Value = df.Acc_Value.str.replace('.','').str.replace(',','.').astype('float64')
df['DateTime'] = pd.to_datetime(df.Date, dayfirst=True)
df.sort_values('DateTime',inplace= True)
df['Category'] = np.select([df['Post'].str.contains(r'(?i)(netto)') |
                            df['Post'].str.contains(r'(?i)(rema)') |
                            df['Post'].str.contains(r'(?i)(føtex)') |
                            df['Post'].str.contains(r'(?i)(meny)') |
                            df['Post'].str.contains(r'(?i)(lidl)') |
                            df['Post'].str.contains(r'(?i)(superb)')
                            ,
                            df['Post'].str.contains(r'(?i)(mobility)') |
                            df['Post'].str.contains(r'(?i)(dsb)') |
                            df['Post'].str.contains(r'(?i)(kombardo)') |
                            df['Post'].str.contains(r'(?i)(billeje)') |
                            df['Post'].str.contains(r'(?i)(easypark)') |
                            df['Post'].str.contains(r'(?i)(parkering)') |
                            df['Post'].str.contains(r'(?i)(lej1lig)') |
                            df['Post'].str.contains(r'(?i)(diesel)') |
                            df['Post'].str.contains(r'(?i)(benzin)') |
                            df['Post'].str.contains(r'(?i)(one2move)') |
                            df['Post'].str.contains(r'(?i)(molslinien)') |
                            df['Post'].str.contains(r'(?i)(færge)') |
                            df['Post'].str.contains(r'(?i)(storebælt)') |
                            df['Post'].str.contains(r'(?i)(norwegian)') |
                            df['Post'].str.contains(r'(?i)(bil^[a-zA-Z])')
                            ,
                            df['Post'].str.contains(r'(?i)(ikea)') |
                            df['Post'].str.contains(r'(?i)(silvan)') |
                            df['Post'].str.contains(r'(?i)(stark)')
                            ,
                            df['Post'].str.contains(r'(?i)(elgiganten)')
                            ,
                            df['Post'].str.contains(r'(?i)(gave)')
                            ,
                            df['Post'].str.contains(r'(?i)(wolt)') |
                            df['Post'].str.contains(r'(?i)(pizza)')
                           ],
                           ['Dagligvarer', 'Transport', 'Bolig', 'Elektronik', 'Gave', 'Takeout'],
                           default = 'Andet'

                          )

dg = df.query('Value < 0').groupby([pd.Grouper(key='DateTime', freq='1M'),'Category']).sum() # groupby each 1 month
dg.reset_index(inplace=True)
dg.DateTime= dg.DateTime.dt.strftime('%Y-%B')
dg.Value = dg.Value*-1
# see https://plotly.com/python/px-arguments/ for more options
df2 = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df2, x="Fruit", y="Amount", color="City", barmode="group")

fig2 = px.line(df, x="DateTime", y="Acc_Value", hover_data=['Post','Value'], title='Life expectancy in Canada')
fig3 = px.bar(dg, x="DateTime", y="Value", color='Category',title='Udgifter')
app.layout = html.Div(children=[
    html.H1(children='Household BI'),

    html.Div(children='''
        Many moneyz
    '''),

    dcc.Graph(
        id='acc-value',
        figure=fig2
    ),
    dcc.Graph(
        id='expenditures',
        figure=fig3
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
