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

# import our data
prediction_model = pickle.load(
    open('../gradient_boost_classifier.pkl', 'rb'))

# import df to get the options
df = pd.read_csv('datasets/allegations_202007271729.csv')


# dropdown options
case_year_receive = df['year_received'].unique()
case_year_close = df['year_closed'].unique()
different_fado_types = df['fado_type'].unique()
allegation_information = df['allegation'].unique()
precinct_id = df['precinct'].unique()
officer_gender = df['mos_gender'].unique()

# layout
PREDICTION = [
    dbc.CardHeader(html.H5("Prediction for NYPD Classification model")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-bigrams-comps",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-bigrams_comp",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.P("Choose the case starting year:"), md=12),
                            dbc.Col([
                                    dcc.Slider(
                                        min=min(case_year_receive),
                                        max=max(case_year_receive),
                                        value=min(case_year_receive),
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
                                        min=min(case_year_close),
                                        max=max(case_year_close),
                                        value=min(case_year_close),
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
                            dbc.Col(html.P("Choose the fado type:"), md=6),
                            dbc.Col(
                                html.P("Choose the allegation type:"), md=6),
                            dbc.Col([
                                    dcc.Dropdown(
                                        id='different_fado_types',
                                        options=sorted([{'label': c, 'value': c} for c in different_fado_types],
                                                       key=lambda x: x['label']),
                                        multi=False
                                    )], md=6,
                                    ),

                            dbc.Col([
                                    dcc.Dropdown(
                                        id='allegation_information',
                                        options=sorted([{'label': d, 'value': d} for d in allegation_information],
                                                       key=lambda x: x['label']),
                                        multi=False
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
                                        multi=False
                                    )], md=6,
                                    ),
                            dbc.Col([
                                    dcc.Dropdown(
                                        id='precinct_id',
                                        options=sorted([{'label': e, 'value': e} for e in precinct_id],
                                                       key=lambda x: x['label']),
                                        multi=False
                                    )], md=6,
                                    ),
                        ]
                    ),
                    html.Hr(),
                    html.Div("The results: ",
                             style={"text-align": "center"}),
                    html.Div(id='prediction_results',
                             style={"text-align": "center"}),
                ], type="default",
            )
        ], style={"marginTop": 0, "marginBottom": 0, "fontSize": 15, "font-weight": "lighter"},
    )
]

BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(PREDICTION)), ], style={"marginTop": 30}),
    ],
    className="mt-12",
)

layout = html.Div(children=[BODY])
# layout = html.Div([
#     # html.Label('Choose a the year of case received: '),
#     # dcc.Dropdown(
#     #     id='case_year_receive',
#     #     options = [{'label': a, 'value' : a} for a in case_year_receive],
#     #     multi = False
#     # ),

#     # html.Label('Choose a the year of case closed: '),
#     # dcc.Dropdown(
#     #     id='case_year_close',
#     #     options = [{'label': b, 'value' : b} for b in case_year_close],
#     #     multi = False
#     # ),

#     # html.Label('Choose a fado type: '),
#     # dcc.Dropdown(
#     #     id='different_fado_types',
#     #     options = [{'label': c, 'value' : c} for c in different_fado_types],
#     #     multi = False
#     # ),

#     # html.Label('Choose the allegation information: '),
#     # dcc.Dropdown(
#     #     id='allegation_information',
#     #     options = [{'label': d, 'value' : d} for d in allegation_information],
#     #     multi = False
#     # ),

#     # html.Label('Choose a precinct location id: '),
#     # dcc.Dropdown(
#     #     id='precinct_id',
#     #     options = [{'label': e, 'value' : e} for e in precinct_id],
#     #     multi = False
#     # ),

#     # html.Label('Choose the officer\'s gender: '),
#     # dcc.Dropdown(
#     #     id='officer_gender',
#     #     options = [{'label': f, 'value' : f} for f in officer_gender],
#     #     multi = False
#     # ),
#     #---------------
#     html.Label(["Choose a the year of case received:",
#     dcc.Dropdown(
#         id='case_year_receive',
#         options = sorted([{'label': a, 'value' : a} for a in case_year_receive],
#         key = lambda x: x['label']),
#         multi = False
#     )]),

#     html.Label(["Choose a the year of case closed: ",
#     dcc.Dropdown(
#         id='case_year_close',
#         options = sorted([{'label': b, 'value' : b} for b in case_year_close],
#         key = lambda x: x['label']),
#         multi = False
#     )]),

#     html.Label(["Choose a fado type: ",
#      dcc.Dropdown(
#         id='different_fado_types',
#         options = sorted([{'label': c, 'value' : c} for c in different_fado_types],
#         key = lambda x: x['label']),
#         multi = False
#     )]),

#     html.Label(["Choose the allegation information: ",
#      dcc.Dropdown(
#         id='allegation_information',
#         options = sorted([{'label': d, 'value' : d} for d in allegation_information],
#         key = lambda x: x['label']),
#         multi = False
#     )]),

#     html.Label(["Choose a precinct location id: ",
#      dcc.Dropdown(
#         id='precinct_id',
#         options = sorted([{'label': e, 'value' : e} for e in precinct_id],
#         key = lambda x: x['label']),
#         multi = False
#     )]),

#     html.Label(["Choose the officer\'s gender: ",
#      dcc.Dropdown(
#         id='officer_gender',
#         options = sorted([{'label': f, 'value' : f} for f in officer_gender],
#         key = lambda x: x['label']),
#         multi = False
#     )]),


#     # html.Label(["Choose a complaint's age ", dcc.Dropdown(id='complaints_ages',
#     # options = [{'label': i, 'value' : i} for i in complaints_age],
#     # multi = False)]),
#     # html.H1("Prediction based on NYPD Classifier Model", style={'text-align':'center'}),
#     # html.Div(["Complaints Id: ", dcc.Input(id='complaints_ids', type='number')]),
#     # html.Br(),
#     # html.Div(["Mos Id: ", dcc.Input(id='unique_mosid', type='number')]),
#     # html.Br(),
#     # html.Div(["Allegation Information: ", dcc.Input(id='allegation_infos', type='number')]),
#     # html.Br(),
#     # html.Div(["Precinct Id: ", dcc.Input(id='precinct_ids', type='number')]),
#     # html.Br(),
#     # html.Div(["Complaints Ages: ", dcc.Input(id='complaints_ages', type='number')]),
#     html.Br(),
#     html.Div(id='prediction_results'),
# ], )

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
def update_prediction(case_year_receive, case_year_close, different_fado_types, allegation_information, precinct_id, officer_gender):
    if case_year_receive is None and case_year_close is None and different_fado_types is None and allegation_information is None and precinct_id is None and officer_gender is None:
        raise dash.exceptions.PreventUpdate

    def transfer_fado_type_to_int(different_fado_types):
        if different_fado_types == 'Abuse of Authority':
            return 1
        elif different_fado_types == 'Discourtesy':
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

    different_fado_types = transfer_fado_type_to_int(different_fado_types)
    allegation_information = transfer_allegation_to_int(allegation_information)
    officer_gender = transfer_gender_int(officer_gender)

    my_prediction = [[case_year_receive, case_year_close, different_fado_types,
                      allegation_information, precinct_id, officer_gender]]
    sc = StandardScaler()
    my_pred = sc.fit_transform(my_prediction)
    pred = prediction_model.predict(my_pred)
    if pred == 0:
        return 'Predict decision of the given condition is substantiated'
    else:
        return 'Predict decision of the given condition is Unsubstantiated or Exonerated'
