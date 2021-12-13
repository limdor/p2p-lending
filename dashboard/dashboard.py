import base64
import dash
import io
import pandas
import plotly.express

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dash.html.Div([
        dash.html.Div([
            dash.html.H1('Monthly Report'),
        ]),
        dash.html.Div([
            dash.dcc.Upload(
                id='datatable-upload',
                children = dash.html.Div([
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
        dash.html.Div([
            dash.html.Div([
                    dash.dcc.Graph(id='datatable-upload-graph-1'),
                ],
                style={'width': '100%'},
            ),
            dash.html.Div([
                    dash.dcc.Graph(id='datatable-upload-graph-2'),
                ],
                style={'width': '100%'},
            ),
        ],
        style={'columnCount': '2'},
        className="flex-container"),
    ],
)

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    # Assume that the user uploaded a CSV file
    return pandas.read_csv(
        io.StringIO(decoded.decode('utf-8')))


@app.callback(dash.dependencies.Output('datatable-upload-graph-1', 'figure'),
              dash.dependencies.Output('datatable-upload-graph-2', 'figure'),
              dash.dependencies.Input('datatable-upload', 'contents'),
              dash.dependencies.State('datatable-upload', 'filename'))
def update_output(contents, filename):

    if contents is None:
        # PreventUpdate prevents ALL outputs updating
        raise dash.exceptions.PreventUpdate
    
    df = parse_contents(contents, filename)
    
    df2 = df.groupby(['Investment platform','Loan originator'],as_index=False).sum()
    
    fig = plotly.express.sunburst(
            df2,
            path = ['Investment platform','Loan originator'],
            values = 'Outstanding principal',
            labels = ''
        )
    fig.update_traces(textinfo="label+percent entry")
    
    fig.update_layout(
        grid= dict(columns=1, rows=1),
        margin = dict(t=0, l=0, r=0, b=0)
    )
    
    df3 = df.groupby(['Country','Investment platform','Loan originator'],as_index=False).sum()
    
    fig2 = plotly.express.sunburst(
            df3,
            path = ['Country','Investment platform','Loan originator'],
            values = 'Outstanding principal',
            labels = ''
        )
    
    fig2.update_traces(textinfo="label+percent parent")
    
    fig2.update_layout(
        grid= dict(columns=1, rows=1),
        margin = dict(t=0, l=0, r=0, b=0)
    )

    return fig, fig2


if __name__ == '__main__':

    #app.server.logger.addHandler(handler)
    app.run_server(debug=False) 
