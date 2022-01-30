import dash
from reports import diversification, overall


def conditionalDiv(level_success, text_to_display):
    if level_success < 0.5:
        levelSuccessClass = 'alert-danger'
    elif 0.5 <= level_success < 1.0:
        levelSuccessClass = 'alert-warning'
    else:
        levelSuccessClass = 'alert-success'

    return dash.html.Div(
        [
            dash.html.P(
                text_to_display,
                className='text-center',
                style={
                    'lineHeight': '8vh',
                },
            )
        ],
        className=f'row {levelSuccessClass} border',
        style={
            'height': 'fit-content',
            'margin': '10px',
        }
    )


def infoDiv(text_to_display):
    return dash.html.Div(
        [
            dash.html.P(
                text_to_display,
                className='text-center',
                style={
                    'lineHeight': '8vh',
                },
            )
        ],
        className='row alert-info border',
        style={
            'height': 'fit-content',
            'margin': '10px',
        }
    )


def percentageToSuccessLevel(value, threshold):
    return (1 - ((value - threshold)/(100 - threshold)))


def DiversificationReport(investment_raw_dataframe):
    report = diversification.generate_report('dashboard', investment_raw_dataframe)
    return dash.html.Div(
        [
            conditionalDiv(report['loanParts']/100, f"The portfolio consists of at least 100 different loan parts: {report['loanParts']:d}"),
            conditionalDiv(percentageToSuccessLevel(report['countryStatistics']['investmentThreeCountries'], 50),
                           f"No more than 50% of loans are issued in 3 (or less) countries: {report['countryStatistics']['investmentThreeCountries']:.2f}%"),
            conditionalDiv(percentageToSuccessLevel(report['countryStatistics']['investmentOneCountry'], 33),
                           f"No more than 33% of loans are issued in any single country: {report['countryStatistics']['investmentOneCountry']:.2f}%"),
            conditionalDiv(percentageToSuccessLevel(report['originatorStatistics']['investmentFiveOriginators'], 50),
                           f"No more than 50% of loans are issued by 5 (or less) lending companies: {report['originatorStatistics']['investmentFiveOriginators']:.2f}%"),
            conditionalDiv(percentageToSuccessLevel(report['originatorStatistics']['investmentOneOriginator'], 20),
                           f"No more than 20% of loans are issued by any single lending company: {report['originatorStatistics']['investmentOneOriginator']:.2f}%"),
        ],
        className='container',
        style={
            'height': 'fit-content',
            'padding': '10px'
        }
    )


def OverallReport(investment_raw_dataframe):
    report = overall.generate_report(investment_raw_dataframe)
    return dash.html.Div(
        [
            infoDiv(f"Number of loan parts: {report['NumberLoanParts']:d}"),
            infoDiv(f"Total invested amount: {report['TotalInvestment']:.2f}€"),
            infoDiv(f"Estimated monthly income: {report['EstimatedMonthlyIncome']:.2f}€"),
        ],
        className='container',
        style={
            'height': 'fit-content',
            'padding': '10px'
        }
    )
