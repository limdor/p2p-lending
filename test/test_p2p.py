import datetime
from unittest.mock import patch
import pandas
from p2p import get_latest_report_date, filter_investment_files_by_newest_date, \
    read_marketplace_files, generate_overall_report_per_date


def test_get_latest_report_date():
    input_data = {
        datetime.date.fromisoformat("2021-11-01") : "path1.xls",
        datetime.date.fromisoformat("2021-12-01") : "path2.xls",
        datetime.date.fromisoformat("2021-08-01") : "path3.xls",
        datetime.date.fromisoformat("2021-04-01") : "path4.xls",
        datetime.date.fromisoformat("2021-02-01") : "path5.xls",
        datetime.date.fromisoformat("2021-01-01") : "path6.xls",
    }
    assert datetime.date.fromisoformat("2021-12-01") == get_latest_report_date(input_data)


@patch('p2p.os.walk')
def test_read_marketplace_files_iuvo(os_walk):
    os_walk.return_value = [
        ('/iuvo', ('',), (
            'MyInvestments-20201130.xlsx',
            'MyInvestments-20201231.xlsx',
            '20201130-current-investments.xlsx',
            '20210630-current-investments.xlsx',
            'OtherFile.xlsx',
        ))
    ]
    output_data = {
        datetime.date.fromisoformat("2020-11-30"): "/iuvo/MyInvestments-20201130.xlsx",
        datetime.date.fromisoformat("2020-12-31"): "/iuvo/MyInvestments-20201231.xlsx",
    }
    assert output_data == read_marketplace_files("dummy/folder", "iuvo")


@patch('p2p.os.walk')
def test_read_marketplace_files_mintos(os_walk):
    os_walk.return_value = [
        ('/mintos', ('',), (
            'MyInvestments-20201130.xlsx',
            'MyInvestments-20201231.xlsx',
            '20201130-current-investments.xlsx',
            '20210630-current-investments.xlsx',
            'OtherFile.xlsx',
        ))
    ]
    output_data = {
        datetime.date.fromisoformat("2020-11-30"): "/mintos/20201130-current-investments.xlsx",
        datetime.date.fromisoformat("2021-06-30"): "/mintos/20210630-current-investments.xlsx",
    }
    assert output_data == read_marketplace_files("dummy/folder", "mintos")


def test_filter_investment_files_by_newest_date():
    input_data = {
        'platform_A' : {
            datetime.date.fromisoformat("2021-11-01") : "path1.xls",
            datetime.date.fromisoformat("2021-12-01") : "path2.xls",
        },
        'platform_B' : {
            datetime.date.fromisoformat("2021-11-01") : "path1.xls",
            datetime.date.fromisoformat("2021-12-01") : "path2.xls",
            datetime.date.fromisoformat("2022-01-01") : "path3.xls",
        },
    }
    output_data = {
        'platform_A' : {
            datetime.date.fromisoformat("2021-12-01") : "path2.xls",
        },
        'platform_B' : {
            datetime.date.fromisoformat("2022-01-01") : "path3.xls",
        },
    }
    assert output_data == filter_investment_files_by_newest_date(input_data)


def test_generate_overall_report_per_date():
    input_data = {
        'Country': {
            0: 'Poland', 1: 'Spain', 2: 'Poland', 3: 'Spain', 4: 'Poland'
        },
        'Loan originator': {
            0: 'Sun Finance', 1: 'Creamfinance', 2: 'Creditstar', 3: 'Creamfinance', 4: 'Creditstar'
        },
        'Outstanding principal': {
            0: 50.0, 1: 75.0, 2: 10.0, 3: 75.0, 4: 15.0
        },
        'Investment platform': {
            0: 'mintos', 1: 'mintos', 2: 'mintos', 3: 'mintos', 4: 'mintos'
        },
        'Date': {
            0: datetime.date(2020, 11, 30), 1: datetime.date(2020, 11, 30),
            2: datetime.date(2020, 11, 30), 3: datetime.date(2020, 11, 30),
            4: datetime.date(2020, 11, 30)
        }
    }
    input_data_frame = pandas.DataFrame(input_data)

    input_files = {
        'mintos': {
            datetime.date(2021, 6, 30): './data/mintos/20210630-current-investments.xlsx',
            datetime.date(2020, 11, 30): './data/mintos/20201130-current-investments.xlsx'
        },
        'iuvo': {
            datetime.date(2020, 11, 30): './data/iuvo/MyInvestments-20201130.xlsx',
            datetime.date(2021, 6, 30): './data/iuvo/MyInvestments-20210630.xlsx'
        }
    }
    overall_report_per_date = generate_overall_report_per_date(input_data_frame, input_files)

    expected_overall_report_per_date = {
        datetime.date(2020, 11, 30): {
            'Data': input_data_frame,
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
            'Data': pandas.DataFrame({
                'Country': {},
                'Loan originator': {},
                'Outstanding principal': {},
                'Investment platform': {},
                'Date': {}
            }),
            'DataByCountry': pandas.DataFrame({
                'Outstanding principal': {},
                'Percentage': {}
            }),
            'DataByLoanOriginator': pandas.DataFrame({
                'Outstanding principal': {},
                'Percentage': {}
            }),
            'TotalInvestment': 0,
            'NumberLoanParts': 0
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
