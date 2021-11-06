import datetime
from io import StringIO
import pandas
from reports import overall

def test_overall_generate_report_per_date():
    input_data = StringIO(
        "Country,Loan originator,Outstanding principal,Investment platform,Date\n"\
        "Poland,Sun Finance,50.0,mintos,2020-11-30\n"\
        "Spain,Creamfinance,75.0,mintos,2020-11-30\n"\
        "Poland,Creditstar,10.0,mintos,2020-11-30\n"\
        "Spain,Creamfinance,75.0,mintos,2020-11-30\n"\
        "Poland,Creditstar,15.0,mintos,2020-11-30\n"\
        "Spain,Creditstar,15.0,mintos,2021-06-30\n"
    )
    input_data_frame = pandas.read_csv(input_data, parse_dates=['Date'])

    overall_report_per_date = overall.generate_report_per_date(input_data_frame)

    expected_overall_report_per_date = {
        datetime.date(2020, 11, 30): {
            'Data': input_data_frame[input_data_frame.index.isin([0,1,2,3,4])],
            'DataByCountry': pandas.DataFrame({
                'Outstanding principal': {'Spain': 150.0, 'Poland': 75.0},
                'Percentage': {'Spain': 0.666, 'Poland': 0.333}
            }),
            'DataByLoanOriginator': pandas.DataFrame({
                'Outstanding principal': {
                    'Creamfinance': 150.0, 'Sun Finance': 50.0, 'Creditstar': 25.0
                },
                'Percentage': {
                    'Creamfinance': 0.666, 'Sun Finance': 0.222, 'Creditstar': 0.111
                }
            }),
            'TotalInvestment': 225.0,
            'NumberLoanParts': 5
        },
        datetime.date(2021, 6, 30): {
            'Data': input_data_frame[input_data_frame.index.isin([5])],
            'DataByCountry': pandas.DataFrame({
                'Outstanding principal': {'Spain': 15.0},
                'Percentage': {'Spain': 1.000}
            }),
            'DataByLoanOriginator': pandas.DataFrame({
                'Outstanding principal': {'Creditstar': 15.0},
                'Percentage': {'Creditstar': 1.000}
            }),
            'TotalInvestment': 15.0,
            'NumberLoanParts': 1
        }
    }

    assert sorted(overall_report_per_date.keys()) == sorted(expected_overall_report_per_date.keys())
    for date, overall_report in overall_report_per_date.items():
        assert sorted(overall_report.keys()) == \
            sorted(expected_overall_report_per_date[date].keys())
        for key, value in overall_report.items():
            if isinstance(value, pandas.core.frame.DataFrame):
                pandas.testing.assert_frame_equal(
                    value, expected_overall_report_per_date[date][key],
                    check_names=False, check_index_type=False, check_dtype=False, atol=1e-3)
            else:
                assert value == expected_overall_report_per_date[date][key]
