import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('../Data/gapminderDataFiveYear.csv')
print(df.head())
app=dash.Dash()

year_options = []
for year in df["year"].unique():
    year_options.append({'label':str(year),'value':year})

app.layout = html.Div([
                    dcc.Graph(id='graph'),
                    dcc.Dropdown(id='year-picker', options=year_options,
                    value=df['year'].min())
])

@app.callback(Output('graph', 'figure'),
                [Input('year-picker','value')])

def update_figure(selected_year):
    filtered_df = df[df["year"]==selected_year]

    traces = []
    for continent_name in filtered_df['continent'].unique():
        df_by_continent = filtered_df[filtered_df["continent"]==continent_name]
        traces.append(go.Scatter(
            x = df_by_continent["gdpPercap"],
            y = df_by_continent["lifeExp"],
            mode='markers',
            opacity=0.7,
            marker={'size':15},
            name=continent_name
        ))

    return {'data':traces,
            'layout':go.Layout(title='My Plot',
                                xaxis={'title': 'GDP Per Cap', 'type':'log'},
                                yaxis={'title':'Life Expectancy'})}

if __name__ == '__main__':
    app.run_server()
