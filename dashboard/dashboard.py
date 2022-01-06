import base64
import io
import datetime
import dash
import pandas
import charts
from marketplace import iuvo
from marketplace import mintos
import p2p

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dash.html.Div(
    [
        dash.dcc.Store(id='investment-raw-data'),
        dash.html.Div([dash.html.H1('Monthly Report')]),
        dash.html.Div(
            [
                dash.dcc.Upload(
                    id='datatable-upload',
                    children=dash.html.Div(
                        [
                            'Drag and Drop or ',
                            dash.html.A('Select Files')
                        ]),
                    style={
                        'width': '100%', 'height': '60px', 'lineHeight': '60px',
                        'borderWidth': '1px', 'borderStyle': 'dashed',
                        'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
                    },
                    multiple=True
                ),
                dash.dash_table.DataTable(id='datatable-upload-container'),
            ]),
        dash.html.Div(
            [
                dash.html.Div(
                    [dash.dcc.Graph(id='piechart-PlatformOriginator')],
                    style={'width': '100%'},
                ),
                dash.html.Div(
                    [dash.dcc.Graph(id='piechart-CounyryPlatformOriginator')],
                    style={'width': '100%'},
                ),
            ],
            style={'columnCount': '2'},
            className="flex-container",
            ),
    ],
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
              dash.dependencies.Output('piechart-CounyryPlatformOriginator', 'figure'),
              dash.dependencies.Input('investment-raw-data', 'data'))
def update_graphs(investment_raw_data):
    investment_raw_dataframe = pandas.read_json(investment_raw_data, orient='split')
    fig1 = charts.piechart_PlatformOriginator(investment_raw_dataframe)
    fig2 = charts.piechart_CountryPlatformOriginator(investment_raw_dataframe)
    return fig1, fig2


if __name__ == '__main__':

    # app.server.logger.addHandler(handler)
    app.run_server(debug=False)
