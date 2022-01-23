import dash
from reports import diversification


def DiversificationReport(investment_raw_dataframe):
    report = diversification.generate_report('dashboard',investment_raw_dataframe)
    return dash.html.Div(
            [
                dash.html.P(f"The portfolio consists of at least 100 different loan parts: {report['loanParts']:d}",className='text-center border',style={'lineHeight': '8vh'}),
                dash.html.P(f"No more than 50% of loans are issued in 3 (or less) countries: {report['countryStatistics']['investmentThreeCountries']:.2f}%",className='text-center border',style={'lineHeight': '8vh'}),
                dash.html.P(f"No more than 33% of loans are issued in any single country: {report['countryStatistics']['investmentOneCountry']:.2f}%",className='text-center border',style={'lineHeight': '8vh'}),
                dash.html.P(f"No more than 50% of loans are issued by 5 (or less) lending companies: {report['originatorStatistics']['investmentFiveOriginators']:.2f}%",className='text-center border',style={'lineHeight': '8vh'}),
                dash.html.P(f"No more than 20% of loans are issued by any single lending company: {report['originatorStatistics']['investmentOneOriginator']:.2f}%",className='text-center border',style={'lineHeight': '8vh'}),
            ],
            className='row row-cols-1',
            style={
                    'height': 'fit-content',
                    'padding': '10px'
                }
            )
