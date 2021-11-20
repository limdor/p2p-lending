import datetime
from io import StringIO
import pytest
import pandas
from reports import diversification

def test_diversification_generate_report_per_date():
    input_data = StringIO(
        "Country,Loan originator,Outstanding principal,Investment platform,Date\n"\
        "Poland,Sun Finance,50.0,mintos,2020-11-30\n"\
        "Spain,Creamfinance,75.0,mintos,2020-11-30\n"\
        "Poland,Creditstar,10.0,mintos,2020-11-30\n"\
        "Spain,Creamfinance,75.0,mintos,2020-11-30\n"\
        "Poland,Creditstar,15.0,mintos,2020-11-30\n"\
    )

    input_data_frame = pandas.read_csv(input_data, parse_dates=['Date'])

    input_overall_report = {
        datetime.date(2020, 11, 30): {
            'Data': input_data_frame,
            'DataByCountry': pandas.DataFrame({
                'Outstanding principal': {'Spain': 150.0, 'Poland': 75.0},
                'Percentage': {'Spain': 0.666, 'Poland': 0.333}
            }),
            'DataByLoanOriginator': pandas.DataFrame({
                'Outstanding principal': {
                    'Creamfinance': 100.0, 'Sun Finance': 100.0, 'Creditstar': 25.0
                },
                'Percentage': {
                    'Creamfinance': 0.444, 'Sun Finance': 0.444, 'Creditstar': 0.111
                }
            }),
            'TotalInvestment': 225.0,
            'NumberLoanParts': 5
        },
    }
    expected_output = {
        datetime.date(2020, 11, 30): {
            'reportId': datetime.date(2020, 11, 30),
            'countryStatistics': {
                'investmentOneCountry': pytest.approx(66.66, abs=1e-2),
                'investmentThreeCountries': 100.0
            },
            'originatorStatistics': {
                'investmentOneOriginator': pytest.approx(44.44, abs=1e-2),
                'investmentFiveOriginators': 100.0
            },
            'overallInvestment': 225.0,
            'loanParts': 5,
        }
    }
    assert expected_output == diversification.generate_report_per_date(input_overall_report)
