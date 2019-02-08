
# -*- coding: utf-8 -*-

import dash

import dash_core_components as dcc

import dash_html_components as html

import pandas as pd

################################




#imagine this data has been passed from the database

data = pd.DataFrame(data=[{'x': [1, 2, 3], 'y': [4, 1, 2], 'name': 'SF'},
{'x': [1, 2, 3], 'y': [2, 4, 5], 'name': 'MT'}])

data = data.set_index('name')

#creating app

app = dash.Dash()


# Boostrap CSS.

app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})  # noqa: E501


app.layout = html.Div(

    html.Div([

        html.Div(

            [
                html.H1(children='Hello World',

                        className='two columns'),

                html.Img(

                    src="http://test.fulcrumanalytics.com/wp-content/uploads/2015/10/Fulcrum-logo_840X144.png",

                    className='three columns',

                    style={

                        'height': '9%',

                        'width': '9%',

                        'float': 'right',

                        'position': 'relative',

                        'margin-top': 10,

                    },

                ),

                html.Div(children='''

                        Dash: A web application framework for Python.

                        ''',

                        className='nine columns'

                )

            ], className="row"

        ),



        html.Div(
            [
                html.Div(
                    [
                        html.P('Choose City:'),

                        dcc.Checklist(

                                id = 'Cities',

                                options=[

                                    {'label': 'San Francisco', 'value': 'SF'},

                                    {'label': 'Montreal', 'value': 'MT'}

                                ],

                                values=['SF', 'MT'],

                                labelStyle={'display': 'inline-block'}

                        ),

                    ],

                    className='six columns',

                    style={'margin-top': '10'}

                ),

            ], className="row"

        ),



        html.Div(

            [

            html.Div([

                dcc.Graph(

                    id='example-graph',                    
                    
                )

                ], className= 'six columns'),



            html.Div([

                dcc.Graph(

                    id='example-graph-2'
                )

                ], className= 'six columns')

            ], 
				className="row")

    ], className='ten columns offset-by-one')

)

@app.callback(

    dash.dependencies.Output('example-graph', 'figure'),

    [dash.dependencies.Input('Cities', 'values')])

def update_image_src(selector):
		type='bar'
		
		data0 = []
		
		for i, subs in enumerate(selector):
			if 'SF'==subs:

				data_temp = data.iloc[i].to_dict()

				data_temp.update({'type': type, 'name': 'SF'})

				data0.append(data_temp)

			if 'MT'==subs:
				data_temp = data.iloc[i].to_dict()

				data_temp.update({'type': type, 'name': 'MT'})

				data0.append(data_temp)
		
		figure = {
			
			'data': data0,

			'layout': {

					'title': 'Graph 1',

					'xaxis' : dict(

						title='x Axis',

						titlefont=dict(

						family='Courier New, monospace',

						size=20,

						color='#7f7f7f'

					)),

					'yaxis' : dict(

						title='y Axis',

						titlefont=dict(

						family='Helvetica, monospace',

						size=20,

						color='#7f7f7f'

				))

			}

		}
		return figure


@app.callback(

    dash.dependencies.Output('example-graph-2', 'figure'),

    [dash.dependencies.Input('Cities', 'values')])

def update_image_src(selector):
	type='line'
	data0=[]
	for i, subs in enumerate(selector):
		if 'SF'==subs:

			data_temp = data.iloc[i].to_dict()

			data_temp.update({'type': type, 'name': 'SF'})

			data0.append(data_temp)

		if 'MT'==subs:
			data_temp = data.iloc[i].to_dict()

			data_temp.update({'type': type, 'name': 'MT'})

			data0.append(data_temp)

	figure = {

		'data': data0,

		'layout': {

			'title': 'Graph 2',

			'xaxis' : dict(

			title='x Axis',

			titlefont=dict(

			family='Courier New, monospace',

			size=20,

			color='#7f7f7f'

			)),

			'yaxis' : dict(

			title='y Axis',

			titlefont=dict(

			family='Helvetica, monospace',

			size=20,

			color='#7f7f7f'

		))

		}

	}
	return figure



if __name__ == '__main__':

    app.run_server(debug=True)
