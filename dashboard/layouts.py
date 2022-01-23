import dash


def DiversificationReport(investment_raw_dataframe):
    return dash.html.Div(
            [
                dash.html.P(['hola'],className='text-center border',style={'lineHeight': '8vh'}),
                dash.html.P(['hola'],className='text-center border',style={'lineHeight': '8vh'}),
                dash.html.P(['hola'],className='text-center border',style={'lineHeight': '8vh'}),
                dash.html.P(['hola'],className='text-center border',style={'lineHeight': '8vh'}),
                dash.html.P(['hola'],className='text-center border',style={'lineHeight': '8vh'}),
                dash.html.P(['hola'],className='text-center border',style={'lineHeight': '8vh'}),
                dash.html.P(['hola'],className='text-center border',style={'lineHeight': '8vh'}),
            ],
            className='row row-cols-1',
            style={
                    'height': 'fit-content',
                    'padding': '10px'
                }
            )
