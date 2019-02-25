# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash_table as dt
import dash_table_experiments as dte


################################
#imagine this data has been passed from the database

path = "C:\\Users\\gauha\\Documents\\Kaggle\\Kaggle Datasets\\Suicide rates world\\master.csv"
df0 = pd.read_csv(path)

#creating app
app = dash.Dash()
#create options for the dropdown element
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


unique_years = list(df0.sort_values('year').year.unique() )
unique_countries = list(df0.sort_values('country').country.unique() )

options_y=[]
for num, x in enumerate(unique_years):
    options_y.append({'label': x, 'value':x })

options_c=[]
for num, x in enumerate(unique_countries):
    options_c.append({'label': x, 'value':x })

#map data preparation
map_input = dict(
    type='choropleth',
    locations=['AZ','CA','VT'],
    locationmode='USA-states',
    #colorscale=['Viridis'],
    z=[10,20,30]
    )
map_layout = dict(geo=dict(scope='usa'))
map_data  = go.Figure(data = [map_input], layout = map_layout)
print(map_data)


#Boostrap CSS.
app.layout = html.Div(
                     html.Div(className='row',
                     style = {'margin-left': 40},
                     children = [
                        html.Div(
                            className = 'ten columns',
                            style = {
                            'margin-top': 10,
                            'margin-bottom': 10,
                            'margin-right':400
                            },
                            children = [
                                html.Div([
                                        html.P(['Choose a country:'],
                                        style =  dict(
                                                   fontFamily = 'Courier New',
                                                   fontSize = '28',
                                                   color = '#7f7f7f')
                                                  )
                                        ]),

                                dcc.Dropdown(
                                            id = 'country_dropdown',
                                            options = options_c,
                                            value = unique_countries[0]
                                              )

                              ]
                            ),

                           html.Div(className='row,',
                                children =[
                                        html.Div(className='four columns',
                                                 style={'margin-top': 20,
                                                        'margin-bottom': 30},
                                                 children=[

                                                        html.Div(
                                                            style={'margin-bottom': 30},
                                                            children =[  html.P(
                                                                    children=['Choose the desired age range:'],
                                                                    style =  dict(
                                                                         fontFamily = 'Courier New',
                                                                         fontSize = '28',
                                                                         color = '#7f7f7f')
                                                                         )
                                                                     ]

                                                                ),

                                                        dt.DataTable(
                                                            id = 'my-table',#'my-table'
                                                            columns = [{"name": i, "id": i} for i in ['age','suicides_no']],
                                                            row_selectable = True,
                                                            style_cell = {
                                                                        'fontWeight': 'bold',
                                                                        'minHeight': '45px'
                                                                        },
                                                            style_cell_conditional = [
                                                                        {
                                                                            'if': {'row_index': 'odd'},
                                                                            'backgroundColor': 'rgb(248, 248, 248)'
                                                                        }
                                                                      ],
                                                            style_header={  'fontFamily': 'Courier New',
                                                                            'backgroundColor': 'white',
                                                                            'fontWeight': 'bold',
                                                                            'fontSize': '18',
                                                                             'color':'#7f7f7f'
                                                                        }
                                                                )
                                                            ]),
                                        html.Div(className='seven columns',
                                                # style={"height" : "90%", "width" : "70%"},
                                                 children = map_data,
                                                 
                                                 style = {  'fontFamily': 'Courier New',
                                                                 'backgroundColor': 'grey',
                                                                 'fontWeight': 'bold',
                                                                 'fontSize': '28',
                                                                  'color':'#7f7f7f'}
                                                 ),
                                           html.Div(className='eleven columns',
                                                children=[dcc.Graph(id='my-graph2')],
                                                style={'margin-left': 40
                                                     }
                                                  )
                                    ]
                             )

                        ])

                    )


@app.callback (
    dash.dependencies.Output(component_id = 'my-table',component_property = 'data'),
    [dash.dependencies.Input(component_id = 'country_dropdown', component_property ='value')]
    )
def update_table(selector):
    country = selector
    df = df0[df0['country'] == country].groupby(['age']).agg(np.sum)['suicides_no'].reset_index().sort_values(['age'])
    data = df.to_dict('records')
    return (data)


@app.callback (
    dash.dependencies.Output(component_id = 'my-graph2',component_property = 'figure'),
    [dash.dependencies.Input(component_id = 'country_dropdown', component_property ='value'),
     dash.dependencies.Input(component_id = 'my-table', component_property ='data'),
     dash.dependencies.Input(component_id = 'my-table', component_property = 'selected_rows')]
    )
def update_plot(country, data_table, table_row_index):

    xnames = df0.sort_values('year')['year'].unique()
    list_of_generations = df0.generation.sort_values().unique().tolist()

    if table_row_index != None:
        age = pd.DataFrame(data_table)['age'].iloc[table_row_index].tolist()
    elif table_row_index == None:
        table_row_index = pd.DataFrame(data_table).index.tolist()
        age = pd.DataFrame(data_table)['age'].iloc[table_row_index].tolist()

    df = df0[(df0['country'] == country) & (df0['age'].isin(age) ) ]

    x = list(  range(min(xnames), max(xnames))   )
    y = df.sort_values('year').groupby(['year','generation']).agg(np.sum).reset_index('generation')[['suicides_no','generation']]

    #sizeref advised by Plotly documentation
    # sizeref = 2. * max(array of size values) / (desired maximum marker size ** 2)
    data = []
    for gen in list_of_generations:
        data.append(
            go.Bar(
                {
                    'x': x,
                    'y': y[y['generation']==gen]['suicides_no'],
                    'visible': True,
                    'hoverinfo': 'text',
                    'text': y[y['generation']==gen]['suicides_no'],
                    'name': 'generation {}'.format(gen)
                }
            )
        )

    layout = dict(title='Suicide volume in {}'.format(country),
                  font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),

                  xaxis=dict(title='year',
                            ticktext = x,
                            tickvals = x),
                  yaxis=dict(title='Number of suicides'
                            ),
                )
    figure = dict(data=data, layout=layout)
    return(figure)





if __name__ == '__main__':
    app.run_server(debug = True)
