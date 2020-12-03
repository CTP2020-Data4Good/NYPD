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
                 html.H3("Visualizing and Predicting NYPD Misconduct",
                         className="display-3"),
                 html.P("This is a parapgraph of intro of the members who work on it if needed",
                        className="lead"),
                 html.Hr(className="my-4"),

                 dbc.Row([
                     # projext description
                     dbc.Col([
                         html.Div(className="card text-white bg-primary mb-6", style={"max-width": "60rem"},
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
                     ], width=5),

                     # why
                     dbc.Col([
                         html.Div(className="card text-white bg-primary mb-6", style={"max-width": "60rem"},
                                  children=[
                             html.Div("Why this project?",
                                      className="card-header"),
                             html.Div(className="card-body",
                                      children=[
                                          html.H2("Why this project?",
                                                  className="card-title"),
                                          html.P(
                                              "1. Help improve the understanding of police misconduct at a time when the issue is of interest and concern to much of the public", className="card-text"),
                                          html.Br(),
                                          html.P(
                                              "2. Examine a trove of data that was previously unavailable to the public to see what we can learn from it and what it can help us to predict", className="card-text"),
                                          html.Br(),
                                          html.P(
                                              "3. Provide a clarifying and easy to use dashboard for anyone to use to understand the data and learn about their local precincts", className="card-text"),
                                      ]
                                      ),
                         ],
                         ),
                     ], width=5),
                 ], justify="center"),

                 html.Br(id="space-in-between"),

                 dbc.Row([
                     # data
                     dbc.Col([
                         html.Div(className="card text-white bg-primary mb-6", style={"max-width": "150rem"},
                                  children=[
                             html.Div("Our Data", className="card-header"),
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
                         ],
                         ),
                     ], width={"size": 10, "offset": 1},),
                 ]),

                 html.Br(id="space-in-between"),

                 dbc.Row([
                     # NYPD Complaints By Year
                     dbc.Col([
                         html.Div(className="card text-white bg-primary mb-6", style={"max-width": "60rem", "text-align": "center"},
                                  children=[
                             html.Div("NYPD Complaints By Year",
                                      className="card-header"),
                             html.Div(className="card-body",
                                      children=[
                                          html.H2("NYPD Complaints By Year",
                                                  className="card-title"),
                                          html.P("something to introduce the feature ",
                                                 className="card-text"),
                                          dbc.Button("NYPD Complaints By Year",
                                                     className="btn btn-secondary btn-lg",
                                                     href='/apps/annual',
                                                     size="lg"),
                                      ]
                                      ),
                         ],
                         ),
                     ], width=5),

                     # Machine Learning Model
                     dbc.Col([
                         html.Div(className="card text-white bg-primary mb-6", style={"max-width": "60rem", "text-align": "center"},
                                  children=[
                             html.Div("Machine Learning Model",
                                      className="card-header"),
                             html.Div(className="card-body",
                                      children=[
                                          html.H2("Machine Learning Model",
                                                  className="card-title"),
                                          html.P("something to introduce the feature ",
                                                 className="card-text"),
                                          dbc.Button("NYPD Complaints By Year",
                                                     className="btn btn-secondary btn-lg",
                                                     href='/apps/predictions',
                                                     size="lg"),
                                      ]
                                      ),
                         ],
                         ),
                     ], width=5),
                 ], justify="center"),

             ], style={"marginTop": 0, "marginBottom": 0, "fontSize": 15, },
             #  "font-weight": "lighter"
             ),
])

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
