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

    expected_output = {
        datetime.date(2020, 11, 30): {
            'reportId': datetime.date(2020, 11, 30),
            'countryStatistics': {
                'investmentOneCountry': pytest.approx(66.66, abs=1e-2),
                'investmentThreeCountries': 100.0
            },
            'originatorStatistics': {
                'investmentOneOriginator': pytest.approx(66.66, abs=1e-2),
                'investmentFiveOriginators': 100.0
            },
            'overallInvestment': 225.0,
            'loanParts': 5,
        }
    }
    assert expected_output == diversification.generate_report_per_date(input_data_frame)
