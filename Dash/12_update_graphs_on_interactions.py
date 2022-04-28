import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import json
import numpy as np

app = dash.Dash()

df = pd.read_csv('../Data/mpg.csv')

app.layout = html.Div([
                html.Div([dcc.Graph(id='mpg-scatter',
                            figure={
                                'data':[go.Scatter(
                                    x=df['model_year']+1900,
                                    y=df['mpg'],
                                    text=df['name'],
                                    hoverinfo='text+y+x',
                                    mode='markers'
                                    )],
                                'layout':go.Layout(title="MPG Data",
                                                    xaxis={'title':'Model Year'},
                                                    yaxis={'title':'MPG'},
                                                    hovermode='closest')
                            }
                )], style={'width':'50%','display':'inline-block'}),
                html.Div([
                    dcc.Graph(id='mpg_line',
                                figure={'data':[go.Scatter(x=[0,1], y=[0,1], mode='lines')],
                                        'layout':go.Layout(title='Acceleration',margin={'l':0})}
                    )

                ], style={'width':'20%','height':'50%','display':'inline-block'}),

                html.Div([
                    dcc.Markdown(id='mpg-stats')


                ], style={'width':'20%','height':'50%','display':'inline-block'})


])

@app.callback(Output('mpg_line','figure'), [Input('mpg-scatter', 'hoverData')])
def callback_graph(hoverData):
    v_index = hoverData['points'][0]['pointIndex']
    figure = {'data':[go.Scatter(x=[0,1],
                      y=[0,60/df.iloc[v_index]['acceleration']],
                      mode='lines',
                      line={'width':2*df.iloc[v_index]['cylinders']}
    )],
                'layout':go.Layout(title=df.iloc[v_index]['name'],
                                    xaxis={'visible':False},
                                    yaxis={'visible':False,'range':[0,60/df['acceleration'].min()]},
                                    margin={'l':0},
                                    height=300)}
    return figure

@app.callback(Output('mpg-stats','children'),
            [Input('mpg-scatter', 'hoverData')])
def callback_stats(hoverData):
    v_index = hoverData['points'][0]['pointIndex']
    stats="""
    {} cylinders
    {}cc displacement
    0 to 60mpn in {} seconds
    """.format(df.iloc[v_index]['cylinders'],df.iloc[v_index]['displacement'],df.iloc[v_index]['acceleration'])

    return stats

if __name__ == '__main__':
    app.run_server()
