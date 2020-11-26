# This our landing page
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


# Connect to main app.py file for app and for server
from app import app
from app import server

# Connect to any other app pages from apps folder
from apps import predictions, annual


app.layout = html.Div([
    html.Div([
        html.Nav(className='navbar navbar-expand-lg navbar-dark bg-primary', id='navbarColor01',
                 children=[html.A('NYPD Complaints Navigator',
                                  className='navbar-brand', href='index'),
                           html.Div(className='collapse navbar-collapse',
                                    children=[
                                        html.Ul(className='navbar-nav mr-auto',
                                                children=[
                                                    html.Li(
                                                        dcc.Link(
                                                            'NYPD Complaints By Year', className='nav-link', href='/apps/annual'), className='nav-item',),
                                                    html.Li(dcc.Link(
                                                        'Machine Learning Model', className='nav-link', href='/apps/predictions', ), className='nav-item')

                                                ]

                                                )
                                    ])]
                 ),
    ],),
    html.Div(className="jumpotron",
             children=[
                 html.H1('Welcome!'),
                 html.P('This is our welcome message and explaination',
                        className='lead'),
                 html.P(className='lead',
                        children=[dcc.Link('NYPD Complaints By Year', className='btn btn-primary btn-lg',
                                           href='/apps/annual'),
                                  dcc.Link('Machine Learning Model', className='btn btn-primary btn-lg', href='/apps/predictions', )]
                        )
             ]
             ),
    # When link is clicked, the href value populates pathname param here
    dcc.Location(id='url', refresh=False, pathname=''),
    # App pages will be returned to go inside that list
    html.Div(id='page-content', children=[]),
    html.Br(),
])


@app.callback(
    Output(component_id='page-content', component_property='children'),
    [Input(component_id='url', component_property='pathname',)]
)
def display_page(pathname):
    if pathname == '/apps/annual':
        return annual.layout
    if pathname == '/apps/predictions':
        return predictions.layout
    else:
        return "404"


if __name__ == '__main__':
    app.run_server(debug=False)
