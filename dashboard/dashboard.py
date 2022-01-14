import base64
import io
import datetime
import dash
import pandas
import charts
import figures
from marketplace import iuvo
from marketplace import mintos
import p2p
import tables


external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': "anonymous"
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.css.config.serve_locally = True

app.layout = dash.html.Div(
    [
        dash.html.Div(
            [
                dash.dcc.Store(id='investment-raw-data'),
                dash.html.Div(
                    [
                        dash.html.H1(
                            'P2P-LENDING',
                            style={'color':'#4b4b4b'},
                        ),
                        dash.html.H2(
                            'Monthly Report',
                        )
                    ],
                    className='header',
                    style={
                        'border-bottom': '1px solid #eee',
                        'text-align': 'center'
                        },
                    ),
                dash.html.Div(
                    [
                        dash.dcc.Upload(
                            id='datatable-upload',
                            children=dash.html.Div(
                                [
                                    dash.html.A('Drop/Upload Files')
                                ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'textAlign': 'center',
                                'lineHeight': '60px',
                                'margin': '10px',
                                'box-shadow': 'rgba(3, 102, 214, 0.3) 0px 0px 0px 3px',
                                },
                            multiple=True
                        ),
                        dash.dash_table.DataTable(id='datatable-upload-container'),
                    ],
                    ),
                dash.html.Div(
                    [
                        dash.html.Div(
                            [
                                dash.dcc.Graph(
                                    id='piechart-CounyryPlatformOriginator',
                                    figure=figures.blank(),
                                    style={
                                        'height': '40vh',
                                    }
                                )
                            ],
                            className="col-sm border",
                            style={
                                'height': 'fit-content',
                                'text-align': 'center',
                                'margin': '10px',
                                'box-shadow': 'rgba(17, 17, 26, 0.05) 0px 1px 0px, rgba(17, 17, 26, 0.1) 0px 0px 8px',
                                },
                        ),
                        dash.html.Div(
                            [
                                dash.dcc.Graph(
                                    id='table-DataByCountry',
                                    figure=figures.blank(),
                                    style={
                                        'height': '40vh',
                                    }
                                )
                            ],
                            className="col-sm border",
                            style={
                                'height': 'fit-content',
                                'text-align': 'center',
                                'margin': '10px',
                                'box-shadow': 'rgba(17, 17, 26, 0.05) 0px 1px 0px, rgba(17, 17, 26, 0.1) 0px 0px 8px',
                                },
                        ),
                    ],
                    className="row",
                    ),
                dash.html.Div(
                    [
                        dash.html.Div(
                            [
                                dash.dcc.Graph(
                                    id='piechart-PlatformOriginator',
                                    figure=figures.blank(),
                                    style={
                                        'height': '40vh',
                                    }
                                )
                            ],
                            className="col-sm border",
                            style={
                                'height': 'fit-content',
                                'text-align': 'center',
                                'margin': '10px',
                                'box-shadow': 'rgba(17, 17, 26, 0.05) 0px 1px 0px, rgba(17, 17, 26, 0.1) 0px 0px 8px',
                                },
                        ),
                        dash.html.Div(
                            [
                                dash.dcc.Graph(
                                    id='table-DataByPlatform',
                                    figure=figures.blank(),
                                    style={
                                        'height': '40vh',
                                    }
                                )
                            ],
                            className="col-sm border",
                            style={
                                'text-align': 'center',
                                'margin': '10px',
                                'box-shadow': 'rgba(17, 17, 26, 0.05) 0px 1px 0px, rgba(17, 17, 26, 0.1) 0px 0px 8px',
                                },
                        ),
                    ],
                    className="row",
                    ),
                dash.html.Div(
                    [
                        dash.html.Div(
                            [
                                dash.dcc.Graph(
                                    id='table-AllRawData',
                                    figure=figures.blank(),
                                    style={
                                        'height': '50vh',
                                    }
                                )
                            ],
                            className="col border",
                            style={
                                'text-align': 'center',
                                'margin': '10px',
                                'box-shadow': 'rgba(17, 17, 26, 0.05) 0px 1px 0px, rgba(17, 17, 26, 0.1) 0px 0px 8px',
                                },
                        ),
                    ],
                    className="row",
                    ),
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
    className='container',
    style={
        'min-width': '100%',
        'min-height': '100%',
        'width': '100%',
        'height': '100%',
        'margin': '0',
        'padding': '0',
        },
)


@app.callback(dash.dependencies.Output('investment-raw-data', 'data'),
              dash.dependencies.Input('datatable-upload', 'contents'),
              dash.dependencies.State('datatable-upload', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is None:
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


@app.callback(dash.dependencies.Output('piechart-PlatformOriginator', 'figure'),
              dash.dependencies.Output('table-DataByPlatform', 'figure'),
              dash.dependencies.Output('piechart-CounyryPlatformOriginator', 'figure'),
              dash.dependencies.Output('table-DataByCountry', 'figure'),
              dash.dependencies.Output('table-AllRawData', 'figure'),
              dash.dependencies.Input('investment-raw-data', 'data'))
def update_graphs(investment_raw_data):
    investment_raw_dataframe = pandas.read_json(investment_raw_data, orient='split')
    fig1 = charts.piechart_OriginatorCountry(investment_raw_dataframe)
    fig2 = tables.table_DataByOriginator(investment_raw_dataframe)
    fig3 = charts.piechart_CountryOriginator(investment_raw_dataframe)
    fig4 = tables.table_DataByCountry(investment_raw_dataframe)
    fig5 = tables.table_AllRawData(investment_raw_dataframe)
    return fig1, fig2, fig3, fig4, fig5


if __name__ == '__main__':
    app.run_server(debug=False)
