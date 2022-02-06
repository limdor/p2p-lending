import base64
import io
import datetime
import dash
import pandas
import charts
import components
import layouts
from marketplace import iuvo
from marketplace import marketplace
from marketplace import mintos
import p2p
import tables


external_stylesheets = [
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'p2p-lending'
app.config.suppress_callback_exceptions = True

app.layout = dash.html.Div(
    [
        dash.html.Div(
            [
                dash.dcc.Store(id='investment-raw-data'),
                dash.html.Div(
                    [
                        dash.html.H1(
                            children='P2P-LENDING',
                            style={
                                'color':'#4b4b4b',
                                'height': '7vh',
                                'lineHeight': '7vh',
                                },
                        ),
                    ],
                    className='header',
                    style={
                        'textAlign': 'center',
                        },
                    ),
                dash.html.Div(
                    id='body-content',
                    children=[
                        dash.html.Div(
                            [
                                dash.dcc.Upload(
                                    id='datatable-upload',
                                    children=[dash.html.P('Drop/Upload Files')],
                                    className='col border',
                                    style={
                                        'margin': '10px',
                                        'height': '80vh',
                                        'lineHeight': '80vh',
                                        'textAlign': 'center',
                                        'box-shadow': 'rgba(17, 17, 26, 0.05) 0px 1px 0px, rgba(17, 17, 26, 0.1) 0px 0px 8px',
                                        },
                                    multiple=True,
                                    ),
                            ],
                            className='row row-cols-1',
                            ),
                    ]),
            ],
            className="container",
            style={
                'max-width': '960px',
                'margin-left': 'auto',
                'margin-right': 'auto',
                'margin-bot': 'auto',
                },
        )
    ],
    className='body',
    style={
        'margin': '0',
        'padding': '0',
        },
)


@app.callback(dash.dependencies.Output('body-content', 'children'),
            dash.dependencies.Input('datatable-upload', 'filename'),
            prevent_initial_call=True)
def render_body(filename):
    if filename is None:
        raise dash.exceptions.PreventUpdate

    return dash.html.Div(
            [
                dash.html.Div(id='text-date'),
                dash.dcc.Tabs(
                [
                    dash.dcc.Tab(
                            id='report-overall',
                            label='Overall Report',
                            style={
                                'padding': '6px',
                                },
                            selected_style={
                                'padding': '6px',
                                }
                            ),
                    dash.dcc.Tab(
                            id='report-diversification',
                            label='Diversification Report',
                            style={
                                'padding': '6px',
                                },
                            selected_style={
                                'padding': '6px',
                                }
                            ),
                    dash.dcc.Tab(
                        label='Graphs & Tables',
                        children=[
                            dash.html.Div(
                                [
                                    components.figure_card_half_row('piechart-CounyryPlatformOriginator'),
                                    components.figure_card_half_row('table-DataByCountry'),
                                ],
                                className="row row-cols-1 row-cols-md-2 row-cols-lg-2",
                                ),
                            dash.html.Div(
                                [
                                    components.figure_card_half_row('piechart-PlatformOriginator'),
                                    components.figure_card_half_row('table-DataByPlatform'),
                                ],
                                className="row row-cols-1 row-cols-md-2 row-cols-lg-2",
                                ),
                            ],
                        style={
                            'padding': '6px',
                            },
                        selected_style={
                            'padding': '6px',
                            }
                        ),
                    dash.dcc.Tab(
                        label='Raw Data',
                        children=[
                            dash.html.Div(
                                [
                                    components.figure_card_full_row('table-AllRawData'),
                                ],
                                className="row row-cols-1",
                                ),
                            ],
                        style={
                            'padding': '6px',
                            },
                        selected_style={
                            'padding': '6px',
                            }
                        )
                ],
                style={
                    'height': 'fit-content',
                    }
                )
            ],
            className='container',
            style = {
                'textAlign': 'center',
            }
            )


@app.callback(dash.dependencies.Output('investment-raw-data', 'data'),
              dash.dependencies.Input('datatable-upload', 'contents'),
              dash.dependencies.State('datatable-upload', 'filename'),
              prevent_initial_call=True)
def update_output(list_of_contents, list_of_names):
    if list_of_names is None:
        raise dash.exceptions.PreventUpdate
    list_dataframes = []
    for file_name, contents in zip(list_of_names, list_of_contents):
        _, content_string = contents.split(',')
        for investment_platform in [mintos.META_DATA, iuvo.META_DATA]:
            match = investment_platform.filename_regexp.search(file_name)
            if match:
                report_date = datetime.date.fromisoformat(f"{match.group('year')}-{match.group('month')}-{match.group('day')}")
                list_dataframes.append(
                    p2p.get_dataframe_from_excel(
                        io.BytesIO(base64.b64decode(content_string)),
                        report_date,
                        investment_platform,
                    )
                )
    investment_raw_data = pandas.concat(list_dataframes)
    return investment_raw_data.to_json(orient='split')


@app.callback(dash.dependencies.Output('text-date', 'children'),
              dash.dependencies.Output('piechart-PlatformOriginator', 'figure'),
              dash.dependencies.Output('table-DataByPlatform', 'figure'),
              dash.dependencies.Output('piechart-CounyryPlatformOriginator', 'figure'),
              dash.dependencies.Output('table-DataByCountry', 'figure'),
              dash.dependencies.Output('table-AllRawData', 'figure'),
              dash.dependencies.Output('report-diversification', 'children'),
              dash.dependencies.Output('report-overall', 'children'),
              dash.dependencies.Input('investment-raw-data', 'data'),
              prevent_initial_call=True)
def update_graphs(investment_raw_data):
    investment_raw_dataframe = pandas.read_json(investment_raw_data, orient='split')
    date = layouts.DateReport(investment_raw_dataframe)
    fig1 = charts.piechart_OriginatorCountry(investment_raw_dataframe)
    fig2 = tables.table_DataByOriginator(investment_raw_dataframe)
    fig3 = charts.piechart_CountryOriginator(investment_raw_dataframe)
    fig4 = tables.table_DataByCountry(investment_raw_dataframe)
    fig5 = tables.table_RawData(investment_raw_dataframe,columns_excluded=[marketplace.FILE_DATE])
    layout1 = layouts.DiversificationReport(investment_raw_dataframe)
    layout2 = layouts.OverallReport(investment_raw_dataframe)
    return date, fig1, fig2, fig3, fig4, fig5, layout1, layout2


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=False)
