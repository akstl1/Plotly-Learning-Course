import dash
from dash import html
from dash import dcc
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = dash.Dash()

app.layout = html.Div([
    dcc.RangeSlider(-5, 6, 1, value=[-3, 2], id='my-range-slider'),
    html.Div(id='output-container-range-slider')
])

@app.callback(
    Output('output-container-range-slider', 'children'),
    [Input('my-range-slider', 'value')])
def update_output(value):
    res=value[0]*value[1]
    return 'The result is {}'.format(res)

if __name__ == '__main__':
    app.run_server(debug=True)
