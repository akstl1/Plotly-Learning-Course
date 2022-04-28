import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = dash.Dash()

nsdq = pd.read_csv('../Data/NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    mydict = {}
    mydict['label']=str(nsdq.loc[tic]["Name"]+' '+tic)
    mydict['value']=tic
    options.append(mydict)

app.layout = html.Div([
                html.H1('Stock Ticker Dashboard'),
                html.Div([
                    html.H3('Enter a stock symbol:', style={'paddingRight':'30px'}),
                    dcc.Dropdown(id='my_stock_picker',value=["TSLA"], multi=True, options=options)
                ],style={'display':'inline-block', 'verticalAlign':'Top', 'width':'30%'})
                ,
                html.Div([html.H3('Select a start and end date:'),
                dcc.DatePickerRange(id='my_date_picker',
                                min_date_allowed = datetime(2015,1,1),
                                max_date_allowed = datetime.today(),
                                start_date = datetime(2018,1,1),
                                end_date = datetime.today()),
                ],style={'display':'inline-block'}),
                html.Div([
                    html.Button(id='submit_button_state', n_clicks=0, children='Submit', style={'fontSize':24,'marginLeft':'30px'}),
                ],style={'display':'inline-block'}),
                dcc.Graph(id='my_graph',
                            figure={'data':[
                                {'x':[1,2], 'y':[3,1]}
                            ], 'layout':{'title':'Default title'}

                            }
                    )

])

@app.callback(Output('my_graph', 'figure'),
              [Input('submit_button_state','n_clicks')],
              [State('my_stock_picker','value'), State('my_date_picker','start_date'), State('my_date_picker','end_date')])

def update_figure_style(n_clicks,stock_ticker, start_date, end_date):
    start = start_date
    end = end_date
    traces = []
    for tic in stock_ticker:
        df = web.get_data_tiingo(tic,start,end,api_key=os.getenv("my_api_key"))
        df.index = df.index.get_level_values('date')
        traces.append({'x':df.index, 'y':df['close'], 'name':tic})
    fig={'data': traces, 'layout':{'title':', '.join(stock_ticker)+' Closeing Prices'}


    }
    return fig



if __name__ == '__main__':
    app.run_server()
