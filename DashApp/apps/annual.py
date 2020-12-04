from logging import PlaceHolder, disable
from dash_bootstrap_components._components.DropdownMenu import DropdownMenu
from dash_bootstrap_components._components.DropdownMenuItem import DropdownMenuItem
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
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

# Datafram cleanup
# Drop 2020 because data is incomplete
df_full = df_full[df_full.year_received < 2020]
df_full.drop_duplicates(inplace=True)
df_unique_complaints = df_full.drop_duplicates(
    subset='complaint_id', inplace=False)

# Data for later reference
precincts = list(df_unique_complaints.precinct.unique())

# Set mapbox key
# Access mapbox api using mapbox access token
with open("./mapbox_token", 'r') as f:
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
            [dbc.Row(
                dbc.Col(
                    html.Div(
                        # Select Borough Menu
                        [dbc.Select(
                            options=[
                                {"label": "Types of complaints",
                                 "value": 'complaint_types'},
                                {"label": "Complainant Ethnicity",
                                    "value": 'ethnicity'},
                                {"label": "Complainant Gender", "value": "gender"},
                            ],
                            placeholder="Select visualizations...",
                            id="map-filter",
                            className='form-control',
                            value='complaint_types'

                        )],
                        className='input-element select'
                    ),
                ),
            ),
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
                    className='input-element'
            ),
                dbc.Checklist(
                    options=[
                        {'label': 'Black',
                         'value': 'Black'},
                        {'label': 'Hispanic',
                         'value': 'Hispanic'},
                        {'label': 'White',
                         'value': 'White'},
                        {'label': 'Other Race',
                         'value': 'Other Race'},
                    ],
                    value=['Black', 'Hispanic',
                           'White', 'Other Race'],
                    id="map-ethnicity",
                    switch=True,
                    inline=True,
                    className='input-element'
            ),
                dbc.Checklist(
                    options=[
                        {'label': 'Male',
                         'value': 'Male'},
                        {'label': 'Female',
                         'value': 'Female'},
                        {'label': 'Unknown',
                         'value': 'Not described'},
                        {'label': 'Transwoman (MTF)',
                         'value': 'Transwoman (MTF)'},
                        {'label': 'Transman (FTM)',
                         'value': 'Transman (FTM)'}

                    ],
                    value=['Male',
                           'Female'],
                    id="map-gender",
                    switch=True,
                    inline=True,
                    className='input-element'
            ),
            ]
        ),
        id='map-input-container',
        width={'size': 3},
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
                            dbc.Input(type="number", list=precincts, max=int(df_full['precinct'].max()), min=int(
                                df_full['precinct'].min()), disabled=True, placeholder='Enter Precinct...', id="precinct-input",),
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
                                {"label": "Manhattan", "value": "Manhattan"},
                                {"label": "Queens", "value": "Queens"},
                                {"label": "Staten Island",
                                    "value": "Staten Island"}
                            ],
                            placeholder="Select Borough...",
                            id="boro-selection",
                            disabled=True,
                            className='form-control',

                        )],
                        className='input-element select'
                    ),
                ),
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
                                value='ethnicities',
                                id="bar_graph_selector",
                                inline=False,

                            ),
                        ],
                        className='input-element',
                    )
                )

            ),

        ],
            width={'size': 4},
            className='object-container'
        ),
    ]
    ),

    html.Br(),
    dbc.Col(id='officer_info_input_div', children=[
        dbc.Row([
            # Officer Info input
            dbc.Col(
                dbc.Form([
                    dbc.FormGroup([
                        dbc.Col([dbc.Input(placeholder='Officer First Name', id='officer_fn',
                                           value=None, type='text', className='input-element',),
                                 dbc.Input(placeholder='Officer Last Name', id='officer_ln',
                                           value=None, type='text', className='input-element',),
                                 dbc.FormFeedback(
                                     "Officer not found in database. ", valid=False),
                                 dbc.FormFeedback("Officer found.", valid=True)
                                 ], width={'size': 12}),

                    ],
                    ),
                    dbc.Col(html.Button('Search', id='officer-search',
                                        n_clicks=0, className='input-element btn btn-primary'), width=2)],
                    inline=True
                ),
                width=6
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
                                {"label": "Civilian Complaint Review Board Rulings by Complainant Ethnicity",
                                 "value": 'ccrb'},
                            ],
                            value='complaint_types_annual',
                            id="officer-graphs-filter",
                            inline=True,
                            className='input-element',

                        ),
                    ],
                ),
                width=6

            )
        ]

        ),
        dbc.Row()
    ],
        className='object-container',
        width={'size': 10, 'offset': 1}),
    html.Div(id='officer_figs_container',
             children=[
                 dbc.Row([

                     dbc.Col(
                         dcc.Graph(id='officer_data_table'),
                         width={'size': 3, 'offset': 1},
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


@ app.callback(
    Output('officer_data_graph', 'figure'),
    [Input('officer-search', 'n_clicks'), Input('officer-graphs-filter', 'value'), State('officer_fn', 'value'), State(
        'officer_ln', 'value')]
)
def update_figure(n_clicks, filter, first, last):
    # Filter dataframe for officer data
    condition1 = df_full.first_name == first.capitalize()
    condition2 = df_full.last_name == last.capitalize()
    df_officer = df_full[condition1 & condition2]
    condition3 = df_officer.board_disposition.isin(
        ['Unsubstantiated', 'Exonerated'])
    df_officer['unsubstantiated/exonerated'] = condition3
    # Todo return alert that there is no one with that name in the datafram if df_officer is empty

    if filter == 'ethnicities':
        officer_ethnicity_grp = df_officer.groupby(
            ['complainant_ethnicity']).size()
        officer_ethnicity_grp = officer_ethnicity_grp.reset_index()
        officer_ethnicity_grp.rename(
            columns={0: '#_complaints'}, inplace=True)
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
    [Input('officer-search', 'n_clicks'), State('officer_fn', 'value'), State(
        'officer_ln', 'value')]
)
def update_figure(n_clicks, first, last):
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
    fig.update_layout(width=350)
    return fig


@ app.callback(
    Output('animated_annual_map', 'figure'),
    [Input('map-input', 'value'), Input('map-filter', 'value'),
        Input('map-ethnicity', 'value'), Input('map-gender', 'value')]
)
def update_figure(categories, filter, ethnicities, genders):
    if filter == 'complaint_types':
        # Group by year, borough, precinct
        df_cat = df_unique_complaints[df_unique_complaints.year_received > 1986]
        # filter dataframe based on selected categories
        df_cat = df_cat[df_cat['fado_type'].isin(categories)]
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
    elif filter == 'ethnicity':
        # Group by precinct year, ethnicity
        precinct_grp_ethnicity = df_unique_complaints.groupby(
            by=['year_received', 'precinct', 'complainant_ethnicity', 'address', 'long', 'lat', ],).size()
        precinct_grp_ethnicity = precinct_grp_ethnicity.reset_index()
        # Change name of size(count) column to #_complaints
        precinct_grp_ethnicity.rename(
            columns={0: '#_complaints'}, inplace=True)
        # condition = precinct_grp_ethnicity['complainant_ethnicity'] != 'Refused'
        # precinct_grp_ethnicity['complainant_ethnicity'].where(condition, )
        # Order dataframe by year

        if 'White' in ethnicities or 'Other Race' in ethnicities:
            ethnicities.append('Unknown')
            precinct_grp_ethnicity = precinct_grp_ethnicity[precinct_grp_ethnicity.year_received > 1998]

        condition = precinct_grp_ethnicity['complainant_ethnicity'].isin(
            ethnicities)
        precinct_grp_ethnicity = precinct_grp_ethnicity[condition]
        precinct_grp_ethnicity.sort_values(
            by=['year_received', 'precinct', 'complainant_ethnicity'])

        labels = {'complainant_ethnicity': 'Complainant Ethnicity',
                  'precinct': 'Precinct',
                  'year_received': 'Complaint Year',
                  '#_complaints': 'No. Complaints'}
        # Create list of columns that would appear upon hovering, using the labels above
        hover_data = {'precinct': True, 'year_received': True, 'complainant_ethnicity': True, '#_complaints': True,
                      'long': False, 'lat': False}
        # Create scatter mapbox using same dataframe
        fig = px.scatter_mapbox(precinct_grp_ethnicity, lat="lat", lon="long",
                                size='#_complaints', color=precinct_grp_ethnicity.complainant_ethnicity,
                                labels=labels, hover_data=hover_data, opacity=0.6,
                                animation_frame='year_received', animation_group='complainant_ethnicity', zoom=9)
    elif filter == 'gender':
        # Group by precinct year, gender
        precinct_grp_gender = df_unique_complaints.groupby(
            by=['year_received', 'precinct', 'complainant_gender', 'address', 'long', 'lat', ],).size()
        precinct_grp_gender = precinct_grp_gender.reset_index()
        # Change name of size(count) column to #_complaints
        precinct_grp_gender.rename(columns={0: '#_complaints'}, inplace=True)
        # Order dataframe by year
        precinct_grp_gender.sort_values(
            by=['year_received', 'precinct', 'complainant_gender'])
        precinct_grp_gender = precinct_grp_gender[precinct_grp_gender.year_received > 1998]
        if 'Not described' in genders:
            precinct_grp_gender = precinct_grp_gender[precinct_grp_gender.year_received > 2003]
        if 'Transwoman (MTF)' in genders:
            precinct_grp_gender = precinct_grp_gender[precinct_grp_gender.year_received > 2015]
        if 'Transman (FTM)' in genders:
            precinct_grp_gender = precinct_grp_gender[precinct_grp_gender.year_received > 2016]
        condition = precinct_grp_gender['complainant_gender'].isin(
            genders)
        precinct_grp_gender = precinct_grp_gender[condition]
        # Create labels dictionary for hover info
        labels = {'complainant_gender': 'Complainant Gender',
                  'precinct': 'Precinct',
                  'year_received': 'Complaint Year',
                  '#_complaints': 'No. Complaints'}
        # Create list of columns that would appear upon hovering, using the labels above
        hover_data = {'precinct': True, 'year_received': True, 'complainant_gender': True, '#_complaints': True,
                      'long': False, 'lat': False}
        # Create scatter mapbox using same dataframe
        fig = px.scatter_mapbox(precinct_grp_gender, lat="lat", lon="long",
                                size='#_complaints', color=precinct_grp_gender.complainant_gender,
                                labels=labels, hover_data=hover_data, opacity=0.6,
                                animation_frame='year_received', animation_group='complainant_gender', zoom=9)

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
        df_tmp = df_unique_complaints[df_unique_complaints.precinct == precinct]
    elif filter == 'borough':
        df_tmp = df_unique_complaints[df_unique_complaints.borough == boro]
    else:
        df_tmp = df_unique_complaints
    if selected_year != None:
        df_tmp = df_tmp[df_tmp.year_received == selected_year]

    if selection == 'totals':
        # Callback for complaint type numbers by year bar graph
        filtered_df = pd.DataFrame(df_tmp.fado_type.value_counts())
        filtered_df.reset_index(inplace=True)
        filtered_df.rename(
            columns={'index': 'Complaint Type', 'fado_type': 'No. Complaints'}, inplace=True)
        filtered_df.sort_values(
            by='No. Complaints', ascending=False, inplace=True)
        fig = px.bar(filtered_df, x='Complaint Type', y='No. Complaints', )

    elif selection == 'genders':
        # Callback for gender distribution for selected year

        # Fill null values with "unknown"
        filtered_df = df_tmp
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
        # if selected_year == None:
        #     filtered_df = df_tmp
        # else:
        #     filtered_df = df_full[df_full['year_received'] == selected_year]

        # Fill null values with "unknown"
        filtered_df = df_tmp
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
    if selection == 'genders':
        fig.update_layout(legend={'orientation': 'v'})
    return fig


### Callback for layout and visual adjustments######
# Callback to disable precinct input unless precinct filtering is selected


@ app.callback(
    Output('map-gender', 'options'),
    [Input('map-filter', 'value')]
)
def adjust_input(filter):
    if filter == 'complaint_types' or filter == 'ethnicity':
        return [
            {'label': 'Male',
             'value': 'Male', 'disabled': True},
            {'label': 'Female',
             'value': 'Female', 'disabled': True},
            {'label': 'Unknown',
             'value': 'Not described', 'disabled': True},
            {'label': 'Transwoman (MTF)',
             'value': 'Transwoman (MTF)', 'disabled': True},
            {'label': 'Transman (FTM)',
             'value': 'Transman (FTM)', 'disabled': True},

        ]
    elif filter == 'gender':
        return [
            {'label': 'Male',
             'value': 'Male'},
            {'label': 'Female',
             'value': 'Female'},
            {'label': 'Unknown',
             'value': 'Not described'},
            {'label': 'Transwoman (MTF)',
             'value': 'Transwoman (MTF)'},
            {'label': 'Transman (FTM)',
             'value': 'Transman (FTM)'},

        ]


@ app.callback(
    Output('map-ethnicity', 'options'),
    [Input('map-filter', 'value')]
)
def adjust_input(filter):
    if filter == 'complaint_types' or filter == 'gender':
        return [
            {'label': 'Black',
             'value': 'Black', 'disabled': True},
            {'label': 'Hispanic',
             'value': 'Hispanic', 'disabled': True},
            {'label': 'White',
             'value': 'White', 'disabled': True},
            {'label': 'Other Race',
             'value': 'Other Race', 'disabled': True},
        ]
    elif filter == 'ethnicity':
        return [
            {'label': 'Black',
             'value': 'Black'},
            {'label': 'Hispanic',
             'value': 'Hispanic'},
            {'label': 'White',
             'value': 'White'},
            {'label': 'Other Race',
             'value': 'Other Race'},
        ]


@ app.callback(
    Output('map-input', 'options'),
    [Input('map-filter', 'value')]
)
def adjust_input(filter):

    if filter == 'ethnicity' or filter == 'gender':
        return [
            {'label': 'Abuse of Authority Complaints',
                'value': 'Abuse of Authority', 'disabled': True},
            {'label': 'Discourtesy Complaints',
                'value': 'Discourtesy', 'disabled': True},
            {'label': 'Use of Force Complaints',
                'value': 'Force', 'disabled': True},
            {'label': 'Offensive Language Complaints',
                'value': 'Offensive Language', 'disabled': True},
        ]
    elif filter == 'complaint_types':
        return [
            {'label': 'Abuse of Authority Complaints',
             'value': 'Abuse of Authority'},
            {'label': 'Discourtesy Complaints',
             'value': 'Discourtesy'},
            {'label': 'Use of Force Complaints',
             'value': 'Force'},
            {'label': 'Offensive Language Complaints',
             'value': 'Offensive Language'},
        ]


# Callback to disable precinct input unless precinct filter is selected
@ app.callback(
    Output('precinct-input', 'disabled'),
    [Input('graphs-filter', 'value')]
)
def adjust_input(filter):
    if filter == 'precinct':
        return False
    else:
        return True

# Callback to disable borough input unless borough filtering is selected


@ app.callback(
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
    Output('officer_fn', 'valid'), Output('officer_fn', 'invalid'),
    Output('officer_ln', 'valid'), Output('officer_ln', 'invalid'),
    [Input('officer-search', 'n_clicks'), State('officer_fn', 'value'), State(
        'officer_ln', 'value')]
)
def hide_container(n_clicks, first, last):
    condition1 = df_full.first_name == first.capitalize()
    condition2 = df_full.last_name == last.capitalize()
    df_officer = df_full[condition1 & condition2]
    if len(df_officer) > 0:
        return {'display': 'block'}, True, False, True, False
    else:
        return {'display': 'none'}, False, True, False, True
