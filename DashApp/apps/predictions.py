from dash_bootstrap_components._components.DropdownMenu import DropdownMenu
from dash_bootstrap_components._components.DropdownMenuItem import DropdownMenuItem
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pandas.io.formats import style
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pathlib
import pickle
import dash
from sklearn.preprocessing import StandardScaler
# import our app
from app import app

PATH = pathlib.Path(__file__).parent
MODELS_PATH = PATH.joinpath("../ml_models").resolve()
DATA_PATH = PATH.joinpath("../datasets").resolve()

# Load data from data folder
prediction_model = pickle.load(
    open(MODELS_PATH.joinpath('gradient_boost_classifier.pkl'), 'rb'))
# # import our data
# prediction_model = pickle.load(
#     open('../gradient_boost_classifier.pkl', 'rb'))

# import df to get the options
df = pd.read_csv(DATA_PATH.joinpath(
    'classification_model_test.csv'))
# df = pd.read_csv('NYPD/classification_model_test.csv')


# dropdown options
case_year_receive = df['year_received'].unique()
case_year_close = df['year_closed'].unique()
different_fado_types = df['fado_type'].unique()
allegation_information = df['allegation'].unique()
precinct_id = df['precinct'].unique()
officer_gender = df['mos_gender'].unique()

# layout

layout = html.Div([
    html.Div(className="jumbotron",
             children=[
                 dbc.Row([
                     # projext description
                     dbc.Col([
                         html.Div(className="card text-white bg-primary mb-6", style={"max-width": "60rem", "height": "50rem"},
                                  children=[
                             html.Div("Project Description",
                                      className="card-header"),
                             html.Div(className="card-body",
                                      children=[
                                          html.H2("Project Description",
                                                  className="card-title"),
                                          html.P("We will build a dashboard application to facilitate the visualization of 33K data points of NYPD misconduct complaints and the forecasting of future rates of complaints. The application will facilitate navigation and understanding of the data and provides clarifying visualization customized for user inquiry. The dashboard will use maps and various graphs to help users understand data spanning from 1985-2020 and all NYPD precincts. In addition to visualizing data, the application will highlight predictive features in the data and include a forecasting feature which will be built using Scikit Learn. The application will seek to use regression to forecast the number of future complaints for a given precinct. ", className="card-text"),
                                      ]
                                      ),
                         ],
                         ),
                     ], width={'size': 3}),

                     # why
                     dbc.Col([
                         html.Div(className="card text-white bg-primary mb-6", style={"max-width": "100rem", "height": "50rem"},
                                  children=[
                             html.Div("Prediction model",
                                      className="card-header"),
                             html.Div(className="card-body",
                                      children=[
                                          dbc.Row(
                                              [
                                                  dbc.Col(
                                                      html.P("Choose the case starting year:"), md=12),
                                                  dbc.Col([
                                                      dcc.Slider(
                                                          min=min(
                                                              case_year_receive),
                                                          max=max(
                                                              case_year_receive),
                                                          value=min(
                                                              case_year_receive),
                                                          id='case_year_receive',
                                                          marks={
                                                              str(year): {
                                                                  "label": str(year),
                                                                  "value": year,

                                                              } for year in case_year_receive
                                                          },), ],
                                                          md=12,
                                                          ),
                                                  dbc.Col(html.Hr()),
                                                  dbc.Col(
                                                      html.P("Choose the case closing year:"), md=12),
                                                  dbc.Col([
                                                      dcc.Slider(
                                                          min=min(
                                                              case_year_close),
                                                          max=max(
                                                              case_year_close),
                                                          value=min(
                                                              case_year_close),
                                                          id='case_year_close',
                                                          marks={
                                                              str(year): {
                                                                  "label": str(year),
                                                                  "value": year,

                                                              } for year in case_year_close
                                                          },), ],
                                                          md=12,
                                                          ),
                                              ]
                                          ),

                                          dbc.Row(html.Hr()),
                                          dbc.Row(
                                              [
                                                  dbc.Col(
                                                      html.P("Choose the fado type:"), md=6),
                                                  dbc.Col(
                                                      html.P("Choose the allegation type:"), md=6),
                                                  dbc.Col([
                                                      dcc.Dropdown(
                                                          id='different_fado_types',
                                                          options=sorted([{'label': c, 'value': c} for c in different_fado_types],
                                                                         key=lambda x: x['label']),
                                                          multi=False,
                                                          style={
                                                              "color": "#2D3E50"}
                                                      )], md=6,
                                                  ),

                                                  dbc.Col([
                                                      dcc.Dropdown(
                                                          id='allegation_information',
                                                          options=sorted([{'label': d, 'value': d} for d in allegation_information],
                                                                         key=lambda x: x['label']),
                                                          multi=False,
                                                          style={
                                                              "color": "#2D3E50"}
                                                      )], md=6,
                                                  ),
                                              ]
                                          ),
                                          dbc.Row(html.Hr()),
                                          dbc.Row(
                                              [
                                                  dbc.Col(
                                                      html.P("Choose the officer's gender:"), md=6),
                                                  dbc.Col(
                                                      html.P("Choose the precinct id:"), md=6),
                                                  dbc.Col([
                                                      dcc.Dropdown(
                                                          id='officer_gender',
                                                          options=sorted([{'label': f, 'value': f} for f in officer_gender],
                                                                         key=lambda x: x['label']),
                                                          multi=False,
                                                          style={
                                                              "color": "#2D3E50"}
                                                      )], md=6,
                                                  ),
                                                  dbc.Col([
                                                      dcc.Dropdown(
                                                          id='precinct_id',
                                                          options=sorted([{'label': e, 'value': e} for e in precinct_id],
                                                                         key=lambda x: x['label']),
                                                          multi=False,
                                                          style={
                                                              "color": "#2D3E50"}
                                                      )], md=6,
                                                  ),
                                              ]
                                          ),
                                          html.Hr(),
                                          html.Div("The results: ",
                                                   style={"text-align": "center", "font-size": "larger", "font-weight": "bold"}),
                                          html.Div(id='prediction_results',
                                                   style={"text-align": "center"}),
                                      ]
                                      ),
                         ],
                         ),
                     ], width={'size': 9}),
                 ]),
             ], style={"marginTop": 0, "marginBottom": 0, "fontSize": 15, },
             )
])

# call back


@ app.callback(
    Output(component_id='prediction_results', component_property='children'),
    Input(component_id='case_year_receive', component_property='value'),
    Input(component_id='case_year_close', component_property='value'),
    Input(component_id='different_fado_types', component_property='value'),
    Input(component_id='allegation_information', component_property='value'),
    Input(component_id='precinct_id', component_property='value'),
    Input(component_id='officer_gender', component_property='value')
)
def update_prediction(case_year_receive, case_year_close, fado_type, allegation_information, precinct_id, officer_gender):
    if case_year_receive is None and case_year_close is None and fado_type is None and allegation_information is None and precinct_id is None and officer_gender is None:
        raise dash.exceptions.PreventUpdate

    def transfer_fado_type_to_int(fado_type):
        if fado_type == 'Abuse of Authority':
            return 1
        elif fado_type == 'Discourtesy':
            return 2
        else:
            return 3

    def transfer_allegation_to_int(allegation_information):
        if allegation_information == 'Physical force':
            return 2
        elif allegation_information == 'Word':
            return 10
        elif allegation_information == 'Stop':
            return 6
        elif allegation_information == 'Search (of person)':
            return 5
        elif allegation_information == 'Frisk':
            return 1
        elif allegation_information == 'Premises entered and/or searched':
            return 3
        elif allegation_information == 'Refusal to provide name/shield number':
            return 4
        elif allegation_information == 'Vehicle search':
            return 8
        elif allegation_information == 'Threat of arrest':
            return 7
        else:
            return 9

    def transfer_gender_int(officer_gender):
        if officer_gender == 'M':
            return 2
        else:
            return 1

    fado_type = transfer_fado_type_to_int(fado_type)
    allegation_information = transfer_allegation_to_int(allegation_information)
    officer_gender = transfer_gender_int(officer_gender)

    my_prediction = [[case_year_receive, case_year_close, fado_type,
                      allegation_information, precinct_id, officer_gender]]
    sc = StandardScaler()
    my_pred = sc.fit_transform(my_prediction)
    pred = prediction_model.predict(my_pred)
    if pred == 0:
        return 'Predict decision of the given condition is substantiated'
    else:
        return 'Predict decision of the given condition is Unsubstantiated or Exonerated'
