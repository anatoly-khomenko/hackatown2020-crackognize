import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd

# build app
app = dash.Dash(__name__)

# link external stylesheet
data = pd.read_csv("data.csv")

fig = px.scatter_mapbox(data, lat="Latitude", lon="Longitude", hover_name="BOROUGH", hover_data=["EMPLACEMENT"],
                        size='NBR_PLA', color_discrete_sequence=["fuchsia"], zoom=10, height=500, width=820)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# fig.show()

app.layout = html.Div(className="main",
                      children=[html.H1(className="app-header", children="Road Crack Visualization App"),
                                html.Div(className="title-bar",
                                         children=html.Div(className='app-bar', children=[
                                             html.Div(className='title', children=
                                             '''Montreal Road Distress Map ''')
                                         ])
                                         ),
                                html.Div(className='main-container', children=[
                                    dcc.Graph(id='dash_graph',
                                              figure=fig
                                              ),
                                    html.Div(
                                        className="right-container",
                                        children=[
                                            html.Div(className="severity-div",
                                                     children=[html.H3("Severity: "),
                                                               dcc.Dropdown(
                                                                   id='ddseverity',
                                                                   style={'height': '30px', 'width': '150px', },
                                                                   options=[
                                                                       {'label': 'select', 'value': 'select'},
                                                                       {'label': 'Very Severe', 'value': 'severe'},
                                                                       {'label': 'Moderate', 'value': 'moderate'},
                                                                       {'label': 'Light', 'value': 'light'}
                                                                   ],
                                                                   value='none'
                                                               ),
                                                               html.Button('Submit', className='button',
                                                                           style={'height': '35px', 'width': '120px', })
                                                               ]),

                                        ]
                                    ),

                                ])
                                ])


@app.callback(
    dash.dependencies.Output('dash_graph', 'figure'),
    [dash.dependencies.Input('ddseverity', 'value')])
def update_graph(value):
    if (value == 'light'):
        temp_df = data[data['NBR_PLA'] <= 20]
    elif (value == 'moderate'):
        temp_df = data[(data['NBR_PLA']>20)&(data['NBR_PLA']<=70)]
    elif (value == 'severe'):
        temp_df = data[data['NBR_PLA'] > 70]
    else:
        temp_df = data
    fig = px.scatter_mapbox(temp_df, lat="Latitude", lon="Longitude", hover_name="BOROUGH", hover_data=["EMPLACEMENT"],
                            size=temp_df['NBR_PLA'], color_discrete_sequence=["fuchsia"], zoom=10, height=500, width=820)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
