# This our landing page
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# Connect to main app.py file for app and for server
from app import app
from app import server

# Connect to any other app pages from apps folder
from apps import predictions, annual

app.layout = html.Div([
    html.Div([
        html.H1("Understanding and Predicting NYPD Misconduct",),
        dcc.Link('NYPD Complaints By Year', href='/apps/annual'),
        dcc.Link('Predicting NYPD Complaints', href='/apps/predictions')
    ], className="row"),
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
