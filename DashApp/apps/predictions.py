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
# import our app
from app import app

#import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
confusion_matrix, f1_score, roc_auc_score, make_scorer)
from sklearn.model_selection import GridSearchCV 
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

#import our data
prediction_model = pickle.load(open('test_classifier.pkl', 'rb'))

#import df to get the options
df = pd.read_csv('allegations_precinct_address_included.csv')


#dropdown options
unique_mos = df['unique_mos_id'].unique()
complaints_id = df['complaint_id'].unique()
allegation_info = df['allegation'].unique()
precinct_id = df['precinct'].unique()
complaints_age = df['complainant_age_incident'].unique()

layout = html.Div([
    html.H1("Prediction based on NYPD Classifier Model", style={'text-align':'center'}),
    html.Div(["Complaints Id: ", dcc.Input(id='complaints_ids', type='number')]),
    html.Br(),
    html.Div(["Mos Id: ", dcc.Input(id='unique_mosid', type='number')]),
    html.Br(),
    html.Div(["Allegation Information: ", dcc.Input(id='allegation_infos', type='number')]),
    html.Br(),
    html.Div(["Precinct Id: ", dcc.Input(id='precinct_ids', type='number')]),
    html.Br(),
    html.Div(["Complaints Ages: ", dcc.Input(id='complaints_ages', type='number')]),
    html.Br(),
    html.Div(id='prediction_results'),
])

#call back
@ app.callback(
    Output(component_id='prediction_results', component_property='children'),
    Input(component_id='complaints_ids', component_property='value'),
    Input(component_id='unique_mosid', component_property='value'),
    Input(component_id='allegation_infos', component_property='value'),
    Input(component_id='precinct_ids', component_property='value'),
    Input(component_id='complaints_ages', component_property='value')
)

def show_factors(complaint_Id, unique_mosId, allegation_Info, precinct_Id, complaints_Age):
    if complaint_Id is None and unique_mosId is None and allegation_Info is None and precinct_Id is None and complaints_Age is None:
        raise dash.exceptions.PreventUpdate
    else:
        update_prediction(complaint_Id, unique_mosId, allegation_Info, precinct_Id, complaints_Age)

def update_prediction(complaint_Id, unique_mosId, allegation_Info, precinct_Id, complaints_Age):
    my_prediction = [[complaint_Id, unique_mosId, allegation_Info, precinct_Id, complaints_Age]]
    sc = StandardScaler()
    my_pred = sc.fit_transform(my_prediction)
    pred = prediction_model.predict(my_pred)
    if pred == 0:
        return 'Predict decision of the given condition is Exonerated'
    else:
        return 'Predict decision of the given condition is Unsubstantiated'


'''   html.Label(["Choose a complaint's id number ", dcc.Dropdown(id='complaints_ids',
    options = [{'label': c, 'value' : c} for c in complaints_id],
    multi = False]),

    html.Label(["Choose a mos id number ", dcc.Dropdown(id='unique_mosid',
    options = [{'label': m, 'value' : m} for m in unique_mos],
    multi = False]),

    html.Label(["Choose an allegation information ", dcc.Dropdown(id='allegation_infos',
    options = [{'label': a, 'value' : a} for a in allegation_info],
    multi = False]),

    html.Label(["Choose a precinct id number ", dcc.Dropdown(id='precinct_ids',
    options = [{'label': p, 'value' : p} for p in precinct_id],
    multi = False]),

    html.Label(["Choose a complaint's age ", dcc.Dropdown(id='complaints_ages',
    options = [{'label': i, 'value' : i} for i in complaints_age],
    multi = False]), '''