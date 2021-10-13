import datetime
from unittest.mock import patch
from p2p import get_latest_report_date, filter_investment_files_by_newest_date, \
    read_marketplace_files


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
