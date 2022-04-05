import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('../Data/gapminderDataFiveYear.csv')

app=dash.Dash()

year_options = []
for year in df["year"].unique():
    year_options.append({'label':str(year),'value':year})

app.layout = html.Div([
                    dcc.Graph(id='graph'),
                    dcc.Dropdown(id='year-picker', options=year_options)

])

if __name__ == '__main__':
    app.run_server()
