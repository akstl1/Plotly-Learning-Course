import dash
from dash import html
from dash import dcc


app=dash.Dash()

app.layout = html.Div([

                html.Label('Dropdown'),
                dcc.Dropdown(options=[{'label':'New York City',
                                        'value':'NYC'},
                                        {'label':'San Francisco',
                                        'value':'SF'}],
                            value='SF') #default
])
