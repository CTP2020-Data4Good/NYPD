import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pathlib

# import our app
from app import app

# access our data using a relative path
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# Load data from data folder
df_annual_ttls = pd.read_csv(DATA_PATH.joinpath('annual_totals.csv'))
df_full = pd.read_csv(DATA_PATH.joinpath('allegations_202007271729.csv'))

layout = html.Div([
    # Will base multiple figures on this input slider
    # Slider year selector
    dcc.Slider(
        id='year-slider',
        # Min set to earliest year in our data
        min=df_annual_ttls['year_received'].min(),
        # Max set to latest year in our data
        max=df_annual_ttls['year_received'].max(),
        # Initial value is min
        value=df_annual_ttls['year_received'].min(),
        marks={str(year): str(year)
               for year in df_annual_ttls['year_received'].unique()},
        step=None
    ),
    # Graph showing number of each type of complaint for selected year
    dcc.Graph(id='annual_totals_fado'),

    # Bar Graph showing ethnic distribution of complainants and officers
    dcc.Graph(id='annual_totals_ethnicity'),

    # Bar Graph showing gender distribution of complainants and officers
    dcc.Graph(id='annual_totals_gender')
])


# Callback for complaint type numbers by year bar graph
@app.callback(
    Output('annual_totals_fado', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_year):
    filtered_df = df_annual_ttls[df_annual_ttls.year_received == selected_year]
    # Drop unsubstantiated_or_exnrtd since it's not relevant to this graph
    filtered_df.drop(['unsubstantiated_or_exnrtd',
                      'substantiated_(any)'], axis=1, inplace=True)
    # Drop year since we don't want it in this visualization, it's assumed from input
    filtered_df.drop('year_received', axis=1, inplace=True)
    # Transpose so we don't have to work with wideform df
    filtered_df = filtered_df.T
    # Reset index
    filtered_df.reset_index(inplace=True)
    # Name our columns so we can reference them easily when creating figure
    filtered_df.columns = ['fado_type', 'total']
    # Sort the df by total
    filtered_df.sort_values('total', ascending=False, inplace=True)
    # Build the visualization, using this filtered_df
    fig = px.bar(filtered_df, x='fado_type', y='total', )

    return fig


# Callback for ethnicity distribution for selected year
@app.callback(
    Output('annual_totals_ethnicity', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_year):
    # Get data for selected year
    filtered_df = df_full[df_full['year_received'] == selected_year]
    # Fill null values with "unknown"
    filtered_df['complainant_ethnicity'].fillna('Unknown', inplace=True)
    filtered_df['mos_ethnicity'].fillna('Unknown', inplace=True)
    # Collect information about complainant ethnicity in dataframe
    comp_eth = filtered_df['complainant_ethnicity'].value_counts()
    comp_eth = pd.DataFrame(comp_eth)
    comp_eth = comp_eth.reset_index()
    comp_eth.columns = ['comp_ethnicity', 'comp_eth_count']
    # Collect information about officer ethnicity in datafram
    mos_ethnicity = filtered_df['mos_ethnicity'].value_counts()
    mos_ethnicity = pd.DataFrame(mos_ethnicity)
    mos_ethnicity = mos_ethnicity.reset_index()
    mos_ethnicity.columns = ['mos_ethnicity', 'mos_eth_count']

    # Join the two to get a df with both officer and complainant ethnicity by year
    filtered_df = comp_eth.join(mos_ethnicity)

    # Build figure based on selected year
    fig = go.Figure(data=[go.Bar(name="Complainant Ethnicity",
                                 x=filtered_df['comp_ethnicity'],
                                 y=filtered_df['comp_eth_count']),
                          go.Bar(name="Officer Ethnicity", x=filtered_df['mos_ethnicity'],
                                 y=filtered_df["mos_eth_count"])
                          ])
    fig.update_layout(barmode='group')

    return fig


# Callback for gender distribution for selected year
@app.callback(
    Output('annual_totals_gender', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_year):
    # Get data for selected year
    filtered_df = df_full[df_full['year_received'] == selected_year]
    # Fill null values with "unknown"
    filtered_df['complainant_gender'].fillna('Unknown', inplace=True)
    filtered_df['mos_gender'].fillna('Unknown', inplace=True)
    # Collect information about complainant ethnicity in dataframe
    comp_gender = filtered_df['complainant_gender'].value_counts()
    comp_gender = pd.DataFrame(comp_gender)
    comp_gender = comp_gender.reset_index()
    comp_gender.columns = ['comp_gender', 'comp_gender_count']
    # Collect information about officer ethnicity in datafram
    mos_gender = filtered_df['mos_gender'].value_counts()
    mos_gender = pd.DataFrame(mos_gender)
    mos_gender = mos_gender.reset_index()
    mos_gender.columns = ['mos_gender', 'mos_gender_count']

    # Join the two to get a df with both officer and complainant ethnicity by year
    filtered_df = comp_gender.join(mos_gender)

    # Build figure based on selected year
    fig = go.Figure(data=[go.Bar(name="Complainant Gender",
                                 x=filtered_df['comp_gender'],
                                 y=filtered_df['comp_gender_count']),
                          go.Bar(name="Officer Gender", x=filtered_df['mos_gender'],
                                 y=filtered_df["mos_gender_count"])
                          ])
    fig.update_layout(barmode='group')

    return fig
# app.layout = html.Div([
#     html.H1("Annual Data Page"),

#     dcc.Dropdown(
#         id='years-dropdown',
#         options=[
#             {'label': '1985', 'value': 1985},
#             {'label': '1986', 'value': 1986},
#             {'label': '1987', 'value': 1987}
#         ],
#         value=1985,  # initial selected value
#         multi=False,
#         style={'width': '40%'}

#     ),
#     html.Div(id='output-container'), # Where the output will go
# ])
