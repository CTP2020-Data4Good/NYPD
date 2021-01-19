from dash_bootstrap_components._components.CardBody import CardBody
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import dash
import pathlib
# import our app
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath(
    'allegations_202007271729.csv'))

# df = pd.read_csv('NYPD/DashApp/datasets/allegations_202007271729.csv')
PAGE_SIZE = 27

layout = html.Div([
    html.Div(className="jumbotron",
             children=[
                 html.H1("Visualizing and Understanding NYPD Misconduct Data",
                         className="display-3"),
                 html.Hr(className="my-4"),

                 dbc.Row([
                     # project description
                     dbc.CardDeck([
                         dbc.Card(className="card text-white bg-primary mb-6", style={"max-width": "60rem"},
                                  children=[
                             dbc.CardBody(children=[
                                 html.H3("What is NYPD Complaint Navigator?",
                                          className="card-header"),
                                 html.Div(className="card-body",
                                          children=[
                                              html.P("Due to an upsurge in advocacy against police misconduct and for transparency, in the summer of 2020 New York State repealed laws  which had for years denied the public access to NYPD disciplinary records. The reform resulted in the release of a database featuring 12,000 civilian complaints of police misconduct, including tens of thousands of allegations. NYPD Complaint Navigator is a data visualization \"dashboard\" application, that enables users to filter and analyze this newly available data. This application is intended as a tool for community members, activists, and policy makers to facilitate the understanding and exploration of this data. We hope that this tool can be especially useful to communities impacted by police misconduct.", className="card-text"),
                                              html.P(["NYPD Complaint Navigator is a student project developed by Computer Science Students at the City University of New York as part of the", html.A(' CUNY Tech Prep Program', href="https://cunytechprep.nyc/"), ". To view the code for this project or contribute to improving it, visit the project ", html.A(
                                                  "github", href="https://github.com/CTP2020-Data4Good/NYPD"), " page."]),
                                          ]
                                          ),

                             ]),

                         ],
                         ),
                         dbc.Card(className="card text-white bg-primary mb-6", style={"max-width": "60rem"},
                                  children=[dbc.CardBody([
                                      html.H3("About the Data",
                                              className="card-header"),
                                      html.Div(className="card-body",
                                               children=[
                                                   html.P(
                                                       ["The data used in this application is downloaded from ProPublica's", html.A(" Data Store", href="https://www.propublica.org/datastore/dataset/civilian-complaints-against-new-york-city-police-officers"), ". The data features:"], className="card-text"),
                                                   html.Ul([
                                                       html.Li("12,000 unique complaints filed against 4,000 active duty officers, and over 30,000 distinct allegations."
                                                               ),
                                                       html.Li(
                                                           "Civilian complaints dating back to 1985."
                                                       ),
                                                       html.Li(
                                                           "Demographic information associated with each allegation, including complainant and officer ethnicity and gender, precincts associated with each complaint, and Civilian Review Board outcome."
                                                       )]
                                                   ),
                                                   html.P(
                                                       "These details are used to create the visualizations provided here. Users of this application can search for a specific officer and view a summary and visualizations based on data from allegation made against the given officer. More details about the data can be found at the project github page and at ProPublica's website. ",
                                                   ),

                                               ]
                                               ),
                                  ]), ],
                                  ),
                     ],),
                 ], justify="center"),

                 html.Br(id="space-in-between"),

                 dbc.Row([
                     # data
                         dbc.Card(className="card text-white bg-primary mb-6", style={"max-width": "124rem"},
                                  children=[dbc.CardBody([
                                      html.Div(
                                          "The Data", className="card-header"),
                                      html.Div(className="card-body",
                                               children=[
                                                   dash_table.DataTable(
                                                       id='table-sorting-filtering',
                                                       columns=[
                                                           {'name': i, 'id': i, 'deletable': True} for i in sorted(df.columns)
                                                       ],
                                                       page_current=0,
                                                       page_size=PAGE_SIZE,
                                                       page_action='custom',

                                                       filter_action='custom',
                                                       filter_query='',

                                                       sort_action='custom',
                                                       sort_mode='multi',
                                                       sort_by=[],
                                                       style_table={
                                                           'overflowX': 'auto', 'height': '450px', 'overflowY': 'auto'},
                                                       style_header={
                                                           'backgroundColor': 'rgb(230, 230, 230)',
                                                           'fontWeight': 'bold'
                                                       },
                                                       style_cell={
                                                           'color': '#2C3F50',
                                                           'font-family': 'sans-serif'
                                                       }
                                                   ),
                                               ],
                                               ),
                                  ]), ],
                                  ), ]),

                 html.Br(id="space-in-between"),

             ],
             #  "font-weight": "lighter"
             ),
], style={'margin': 'auto', 'width': '90%'},)

# for officer
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(
    Output('table-sorting-filtering', 'data'),
    Input('table-sorting-filtering', "page_current"),
    Input('table-sorting-filtering', "page_size"),
    Input('table-sorting-filtering', 'sort_by'),
    Input('table-sorting-filtering', 'filter_query'))
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    page = page_current
    size = page_size
    return dff.iloc[page * size: (page + 1) * size].to_dict('records')
