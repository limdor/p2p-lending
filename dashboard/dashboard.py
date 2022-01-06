import base64
import io
import dash
import pandas
import charts

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


def parse_excel_fiels(contents, _):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    # Assume that the user uploaded a CSV file
    return pandas.read_csv(
        io.StringIO(decoded.decode('utf-8'))).to_json(orient='split')


@app.callback(dash.dependencies.Output('investment-raw-data', 'data'),
              dash.dependencies.Input('datatable-upload', 'contents'),
              dash.dependencies.State('datatable-upload', 'filename'))
def update_output(contents, filename):
    if contents is None:
        # PreventUpdate prevents ALL outputs updating
        raise dash.exceptions.PreventUpdate
    investment_raw_data = parse_excel_fiels(contents, filename)
    return investment_raw_data


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
