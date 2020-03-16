import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from open_list_servicer import run_open_list
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df_who = pd.read_csv('data/full_data.csv')
df_open_line_list = run_open_list()
global_fig = px.scatter_geo(df_open_line_list, lat="latitude",lon="longitude", color="country",
                     hover_name="city", size="case", size_max=50,
                     projection="natural earth")





app.layout = html.Div(children=[
    html.H1(children='COVID 19 Dashboard'),

    html.Div(children='''
        Created using plotly dash with Python.
    '''),

    dcc.Input(id='search-country', value='World', type='text'),
    dcc.Input(id='start-date', value='2020-03-01', type='text'),
    dcc.RadioItems(
        id='run-query',
        options=[
            {'label': 'Run Query on Map', 'value': '1'},
            {'label': 'Run Global on Map', 'value': '0'},
        ],
        value='0',
    ),
    # dcc.Input(id='end-date', value='1', type='text'),

    dcc.Graph(
        id='main-graph',
    ),
    dcc.Graph(
        id='map-graph',
    )


    # dcc.Graph(
    #     id='example-graph',
    #     figure={
    #         'data': [
    #             {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
    #             {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
    #         ],
    #         'layout': {
    #             'title': 'Dash Data Visualization'
    #         }
    #     }
    # )
])


@app.callback(
    [Output(component_id='main-graph', component_property='figure'),
     Output(component_id='map-graph', component_property='figure')],
    [
        Input(component_id='search-country', component_property='value'),
        Input(component_id='start-date', component_property='value'),
        Input(component_id='run-query', component_property='value'),
        # Input(component_id='end-date', component_property='value'),
    ]
)
def query_data(country_name, start_date, run_query):
    df_tmp = df_who.query(f"location == '{country_name}' ")
    df_tmp = df_tmp.query(f"date >= '{start_date}' ")

    fig_plot = go.Figure(
        data=[go.Scatter(
            x=list(df_tmp.date),
            y=list(df_tmp.total_cases), line=dict(color="crimson"))],
        layout=dict(title=dict(text="Total confirmed cases")),
    )
    if run_query == "1" and country_name != 'World':
        df_open_query = df_open_line_list.query(f"country == '{country_name}' ")
        fig_map = px.scatter_geo(df_open_query, lat="latitude", lon="longitude", color="province",
                       hover_name="city", size="case", size_max=50,
                       projection="natural earth")
    else:
        fig_map = global_fig
    return fig_plot, fig_map

if __name__ == '__main__':
    app.run_server(debug=True)
