from logging import PlaceHolder, disable
from dash_bootstrap_components._components.DropdownMenu import DropdownMenu
from dash_bootstrap_components._components.DropdownMenuItem import DropdownMenuItem
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

# import our app
from app import app

# access our data using a relative path
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# Load data from data folder
df_annual_ttls = pd.read_csv(DATA_PATH.joinpath('annual_totals.csv'))
df_full = pd.read_csv(DATA_PATH.joinpath(
    'allegations_precinct_address_included.csv'))

# Drop 2020 because data is incomplete
df_full = df_full[df_full.year_received < 2020]

# Set mapbox key
# Access mapbox api using mapbox access token
with open("../mapbox_token", 'r') as f:
    mapbox_key = f.read().strip()

# Create General Layout format to reuse
margins = {'l': 30, 'r': 30, 't': 20, 'b': 20}
legend_title = {'text': ''}
# fig.update_layout(margin = margins)
legend_details = {'orientation': 'h',
                  'bgcolor': 'rgb(246, 246, 244)', 'x': 0.3, 'title': legend_title}
# fig.update_layout(legend=legend_details)
# paper_bgcolor='rgb(25, 26, 26)'
general_layout = go.Layout(template='seaborn', plot_bgcolor='rgba(0,0,0,0)',
                           margin=margins, paper_bgcolor='rgb(246, 246, 244)', legend=legend_details)

layout = html.Div([
    dbc.Row([dbc.Col(
            dcc.Graph(id='animated_annual_map'),
            width={'size': 7, 'offset': 1},
            className='object-container'),
        dbc.Col(
        dbc.FormGroup(
            [
                # dbc.Label("Choose a bunch"),
                dbc.Checklist(
                    options=[
                        {'label': 'Abuse of Authority Complaints',
                         'value': 'Abuse of Authority'},
                        {'label': 'Discourtesy Complaints',
                         'value': 'Discourtesy'},
                        {'label': 'Use of Force Complaints',
                         'value': 'Force'},
                        {'label': 'Offensive Language Complaints',
                         'value': 'Offensive Language'},
                    ],
                    value=['Abuse of Authority', 'Discourtesy',
                           'Force', 'Offensive Language'],
                    id="map-input",
                    switch=True,
                ),
            ]
        ),
        id='map-input-container',
        width={'size': 2},
        className='object-container',
    )
    ]),
    dbc.Row([
        dbc.Col(
            # Graphs chosen
            dcc.Graph(id='user_selected_bar_graph'),
            width={'size': 6, 'offset': 1},
            className='object-container'
        ),
        dbc.Col([
            # Select year for visualizations
            dbc.Row(
                dbc.Col(
                    dbc.FormGroup(
                        [
                            html.Div(
                                [
                                    dbc.Input(type="number", list=list(range(
                                        1989, 2020)), min=1989, max=2020, id="year-input", value=None, placeholder='Enter year...'),
                                ],
                                className='input-element'

                            )
                        ]
                    ),
                )

            ),
            dbc.Row(
                dbc.Col(
                    # Filterning options (filter by borough or by precinct)
                    dbc.FormGroup(
                        [
                            # dbc.Label("Choose Filter"),
                            dbc.RadioItems(
                                options=[
                                    {'label': 'All data', 'value': None},
                                    {"label": "Filter by Precinct",
                                        "value": 'precinct'},
                                    {"label": "Filter by Borough",
                                        "value": 'borough'},
                                    # {"label": "Filter by Zip Code",
                                    #     "value": 'zc'},
                                ],
                                value=None,
                                id="graphs-filter",
                                inline=True,
                                className='input-element',

                            ),
                        ],
                    )
                    # width={'size': 2, 'offset': 1}
                )

            ),
            dbc.Row(
                dbc.Col(
                    # Select Precinct input
                    html.Div(
                        [
                            dbc.Input(type="number", list=list(
                                range(int(df_full['precinct'].min()), int(df_full['precinct'].max()))), step=1, max=int(df_full['precinct'].max()), min=int(df_full['precinct'].min()), disabled=True, placeholder='Enter Precinct...', id="precinct-input",),
                        ],
                        className='input-element'

                    )
                )

            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        # Select Borough Menu
                        [dbc.Select(
                            options=[
                                {"label": "Brooklyn", "value": 'Brooklyn'},
                                {"label": "Bronx", "value": 'Bronx'},
                                {"label": "Manhattan", "Value": "Manhattan"},
                                {"label": "Queens", "Value": "Queens"},
                                {"label": "Staten Island",
                                    "Value": "Staten Island"}
                            ],
                            placeholder="Select Borough...",
                            id="boro-selection",
                            disabled=True,
                            className='form-control',

                        )],
                        className='input-element select'
                    ),

                )

            ),
            dbc.Row(
                dbc.Col(
                    # Graph Selection
                    dbc.FormGroup(
                        [
                            dbc.RadioItems(
                                options=[
                                    {'label': 'Complaint Totals',
                                        'value': 'totals'},
                                    {'label': 'Complainant and Officer Genders',
                                        'value': 'genders'},
                                    {'label': 'Complainant and Officer Ethnicities',
                                     'value': 'ethnicities'}
                                ],
                                value='totals',
                                id="bar_graph_selector",
                                inline=False,

                            ),
                        ],
                        className='input-element',
                    )
                )

            ),

        ],
            width={'size': 3},
            className='object-container'
        ),
    ]
    ),

    html.Br(),
    html.Div(id='officer_info_input_div', children=[
        dbc.Row([
            # Officer Info input
            dbc.Col(

                dbc.FormGroup(
                    [
                        dbc.Input(placeholder='Officer First Name', id='officer_fn',
                                  value=None, type='text', className='input-element'),

                    ],
                ),
                width=3,
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Input(placeholder='Officer Last Name', id='officer_ln',
                                  value=None, type='text', className='input-element'),
                    ],
                ),
                width=3
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.RadioItems(
                            options=[
                                {'label': 'Complaint Types by Year',
                                 'value': 'complaint_types_annual'},
                                {"label": 'Complainant Ethnicities by Year',
                                 "value": 'ethnicities_annual'},
                                {"label": "Ethnicities of Complainants Overall",
                                 "value": 'ethnicities'},
                                {"label": "Civilian Complaint Review Board Rulings",
                                 "value": 'ccrb'},

                                # {"label": "Filter by Zip Code",
                                #     "value": 'zc'},
                            ],
                            value='complaint_types_annual',
                            id="officer-graphs-filter",
                            inline=True,
                            className='input-element',

                        ),
                    ],
                )

            )
        ]
            # width={'size': 2, 'offset': 1}


        ),
    ],
        className='object-container'),
    html.Div(id='officer_figs_container',
             children=[
                 dbc.Row([

                     dbc.Col(
                         dcc.Graph(id='officer_data_table'),
                         width={'size': 4},
                         className='object-container'
                     ),
                     dbc.Col(
                         dcc.Graph(id='officer_data_graph'),
                         width={'size': 7},
                         className='object-container'
                     )
                 ],

                 )
             ]

             )


]
)
# Callback for displaying officer info graphs


@app.callback(
    Output('officer_data_graph', 'figure'),
    [Input('officer_fn', 'value'), Input(
        'officer_ln', 'value'), Input('officer-graphs-filter', 'value')]
)
def update_figure(first, last, filter):
    # Filter dataframe for officer data
    condition1 = df_full.first_name == first.capitalize()
    condition2 = df_full.last_name == last.capitalize()
    df_officer = df_full[condition1 & condition2]
    # Todo return alert that there is no one with that name in the datafram if df_officer is empty

    if filter == 'ethnicities':
        officer_ethnicity_grp = df_officer.groupby(
            ['complainant_ethnicity']).size()
        officer_ethnicity_grp = officer_ethnicity_grp.reset_index()
        officer_ethnicity_grp.rename(columns={0: '#_complaints'}, inplace=True)
        labels = list(officer_ethnicity_grp.complainant_ethnicity)
        values = list(officer_ethnicity_grp['#_complaints'])
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3,
                                     title='Ethnicities of Complainants for Selected Officer', titleposition='top center')])
    elif filter == 'ccrb':
        # Group by year, borough, and get count
        officer_ethnicity_outcome_grp = df_officer.groupby(
            by=['complainant_ethnicity', 'unsubstantiated/exonerated'],).size()
        # get dataframe from groupby object
        officer_ethnicity_outcome_grp = officer_ethnicity_outcome_grp.reset_index()
        # Change name of size(count) column to #_complaints
        officer_ethnicity_outcome_grp.rename(
            columns={0: '#_complaints'}, inplace=True)
        # Change text to clarify for user
        condition = officer_ethnicity_outcome_grp['unsubstantiated/exonerated'] == True
        condition2 = officer_ethnicity_outcome_grp['unsubstantiated/exonerated'] == False
        officer_ethnicity_outcome_grp['unsubstantiated/exonerated'].where(
            condition, 'Substantiated', inplace=True)
        officer_ethnicity_outcome_grp['unsubstantiated/exonerated'].where(
            condition2, 'Unsubstantiated/Exonerated', inplace=True)
        # Create figure
        labels = {'unsubstantiated/exonerated': 'Civilian Complaint Review Board Ruling',
                  '#_complaints': 'No. of Complaints', 'complainant_ethnicity': 'Complainant Ethnicity'}
        fig = px.bar(officer_ethnicity_outcome_grp, x="complainant_ethnicity", y="#_complaints",
                     color="unsubstantiated/exonerated", barmode="group",
                     labels=labels)
    elif filter == 'complaint_types_annual':
        # Group by year, borough, and get count
        officer_year_comptype_grp = df_officer.groupby(
            by=['year_received', 'fado_type'],).size()
        # get dataframe from groupby object
        officer_year_comptype_grp = officer_year_comptype_grp.reset_index()
        # Change name of size(count) column to #_complaints
        officer_year_comptype_grp.rename(
            columns={0: '#_complaints'}, inplace=True)
        # Create and show line plot
        fig = px.scatter(officer_year_comptype_grp, x="year_received",
                         y="#_complaints", color="fado_type", size='#_complaints')
    elif filter == 'ethnicities_annual':
        # Group by year, borough, and get count
        officer_year_ethnicity_grp = df_officer.groupby(
            by=['year_received', 'complainant_ethnicity'],).size()
        # get dataframe from groupby object
        officer_year_ethnicity_grp = officer_year_ethnicity_grp.reset_index()
        # Change name of size(count) column to #_complaints
        officer_year_ethnicity_grp.rename(
            columns={0: '#_complaints'}, inplace=True)
        # Create and show line plot
        fig = px.scatter(officer_year_ethnicity_grp, x="year_received",
                         y="#_complaints", color="complainant_ethnicity", size='#_complaints')

    fig.layout = general_layout
    return fig


# Callback for displaying officer info in a table


@ app.callback(
    Output('officer_data_table', 'figure'),
    [Input('officer_fn', 'value'), Input(
        'officer_ln', 'value')]
)
def update_figure(first, last):
    # Filter dataframe for officer data
    condition1 = df_full.first_name == first.capitalize()
    condition2 = df_full.last_name == last.capitalize()
    df_officer = df_full[condition1 & condition2]
    # Create table with general data about officer
    # Group by year, fado_type, and get count
    officer_year_comptype_grp = df_officer.groupby(
        by=['year_received', 'fado_type'],).size()
    # get dataframe from groupby object
    officer_year_comptype_grp = officer_year_comptype_grp.reset_index()
    # Change name of size(count) column to #_complaints
    officer_year_comptype_grp.rename(columns={0: '#_complaints'}, inplace=True)
    # Create table with the data and return figure
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Year', 'Complaint Type', "No. Complaints"],
                    align='left'),
        cells=dict(values=[officer_year_comptype_grp.year_received, officer_year_comptype_grp.fado_type,
                           officer_year_comptype_grp['#_complaints']],
                   fill_color='lavender',
                   align='left'),
        columnwidth=[2, 4, 2]
    )
    ])
    fig.layout = general_layout
    return fig


@ app.callback(
    Output('animated_annual_map', 'figure'),
    [Input('map-input', 'value')]
)
def update_figure(categories):
    # Group by year, borough, precinct
    df_cat = df_full[df_full.year_received > 1986]
    # filter dataframe based on selected categories
    df_cat = df_cat[df_full['fado_type'].isin(categories)]
    precinct_grp = df_cat.groupby(by=['year_received', 'borough',
                                      'precinct', 'long', 'lat', 'fado_type'],).size()
    # Get dataframe from groupby object
    precinct_grp = precinct_grp.reset_index()
    # Change name of size(count) column to #_complaints
    precinct_grp.rename(columns={0: '#_complaints'}, inplace=True)
    # Order dataframe by year
    precinct_grp.sort_values('year_received', inplace=True)

    # Create labels dictionary for hover info
    labels = {'precinct': 'Precinct',
              'year_received': 'Complaint Year',
              '#_complaints': 'No. Complaints',
              'borough': 'Borough'}
    # Create list of columns that would appear upon hovering, using the labels above
    hover_data = {'precinct': True, 'year_received': True, 'borough': True, '#_complaints': True,
                  'long': False, 'lat': False}

    # Create scatter mapbox using same dataframe
    fig = px.scatter_mapbox(precinct_grp, lat="lat", lon="long",
                            size='#_complaints',
                            labels=labels, hover_data=hover_data, opacity=0.6,
                            animation_frame='year_received', color='fado_type', zoom=8.5,)
    fig.update_layout(mapbox_style="light",
                      mapbox_accesstoken=mapbox_key)
    fig.layout.template = 'seaborn'
    fig.layout.paper_bgcolor = 'rgb(246, 246, 244)'
    # 'rgb(202, 210, 211)'
    margins = {'l': 10, 'r': 10, 't': 20, 'b': 0}
    legend_title = {'text': ''}
    fig.update_layout(margin=margins)
    # 'bgcolor': 'rgb(52, 51, 50)' legend
    legend_details = {'orientation': 'h',  'x': 0.4,
                      'bgcolor': 'rgb(246, 246, 244)', 'title': legend_title}
    fig.update_layout(legend=legend_details)

    return fig

# Callback for complaint type numbers by year bar graph


@ app.callback(
    Output('user_selected_bar_graph', 'figure'),
    [Input('year-input', 'value'), Input('graphs-filter', 'value'), Input('bar_graph_selector', 'value'),
     Input('boro-selection', 'value'), Input('precinct-input', 'value')]
)
def update_figure(selected_year,  filter, selection, boro, precinct):
    # Determin filter
    if filter == 'precinct':
        df_tmp = df_full[df_full.precinct == precinct]
    elif filter == 'boro':
        df_tmp = df_full[df_full.borough == boro]
    else:
        df_tmp = df_full

    if selection == 'totals':
        # Callback for complaint type numbers by year bar graph
        if selected_year == None:
            filtered_df = df_annual_ttls
            filtered_df = df_annual_ttls.drop(
                ['unsubstantiated_or_exnrtd', 'substantiated_(any)', 'year_received'], axis=1)
            filtered_df = pd.DataFrame(filtered_df.sum())
            filtered_df.reset_index(inplace=True)
            filtered_df.columns = ['fado_type', 'total']
            filtered_df.sort_values('total', ascending=False, inplace=True)
            fig = px.bar(filtered_df, x='fado_type', y='total', )

        else:
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
    elif selection == 'genders':
        # Callback for gender distribution for selected year
        # Get data for selected year
        if selected_year == None:
            filtered_df = df_tmp
        else:
            filtered_df = df_tmp[df_tmp['year_received'] == selected_year]
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
        # fig.update_layout(barmode='group')
    elif selection == 'ethnicities':
        # Callback for ethnicity distribution for selected year
        # Get data for selected year
        if selected_year == None:
            filtered_df = df_tmp
        else:
            filtered_df = df_tmp[df_tmp['year_received'] == selected_year]
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

    fig.layout = general_layout
    fig.update_layout(barmode='group')

    return fig

### Callback for layout and visual adjustments######
# Callback to disable precinct input unless precinct filtering is selected


@app.callback(
    Output('precinct-input', 'disabled'),
    [Input('graphs-filter', 'value')]
)
def adjust_input(filter):
    if filter == 'precinct':
        return False
    else:
        return True

# Callback to disable borough input unless borough filtering is selected


@app.callback(
    Output('boro-selection', 'disabled'),
    [Input('graphs-filter', 'value')]
)
def adjust_input(filter):
    if filter == 'borough':
        return False
    else:
        return True

 # Callback to hide figure containers for officer info until input is given


@ app.callback(
    Output('officer_figs_container', 'style'),
    [Input('officer_fn', 'value'), Input(
        'officer_ln', 'value')]
)
def hide_container(fn, ln):
    if fn is not None and ln is not None:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


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
