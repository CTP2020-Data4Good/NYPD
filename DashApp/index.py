# This our landing page
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


# Connect to main app.py file for app and for server
from app import app
from app import server

# Connect to any other app pages from apps folder
from apps import annual, about


app.layout = html.Div(id='nav',
                      children=[dbc.NavbarSimple(className='navbar navbar-expand-lg navbar-dark bg-primary', id='navbarColor01', children=[
                          dbc.NavItem(dbc.NavLink(
                              'About', className='nav-item', id='about', href='/apps/about', ), className='nav-item'), ], color="primary", dark=True, brand="NYPD Complaints Navigator", brand_href='index',
                      ),
                          # When link is clicked, the href value populates pathname param here
                          dcc.Location(id='url', refresh=False, pathname=''),
                          # App pages will be returned to be rendered int his div
                          html.Div(id='page-content', children=[]),
                      ])

home_layout = html.Div(id='home_layout', className="jumpotron",
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
                       )


@app.callback(
    Output(component_id='page-content', component_property='children'),
    [Input(component_id='url', component_property='pathname',)]
)
def display_page(pathname):
    if pathname == '/apps/about':
        return about.layout
    else:
        return annual.layout


if __name__ == '__main__':
    app.run_server(debug=False)
