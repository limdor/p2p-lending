import datetime
from unittest.mock import patch
from marketplace import iuvo, mintos
from datacollection.datacollection import read_marketplace_files, get_latest_report_date, filter_investment_files_by_newest_date

@patch('datacollection.datacollection.os.walk')
def test_read_marketplace_files_iuvo(os_walk):
    os_walk.return_value = [
        ('/iuvo', ('',), (
            'MyInvestments-20201130.xlsx',
            'MyInvestments-20201231.xlsx',
            '20210630-current-investments.xlsx',
            'OtherFile.xlsx',
        ))
    ]
    output_data = {
        datetime.date.fromisoformat("2020-11-30"): "/iuvo/MyInvestments-20201130.xlsx",
        datetime.date.fromisoformat("2020-12-31"): "/iuvo/MyInvestments-20201231.xlsx",
    }
    assert output_data == read_marketplace_files("dummy/folder", iuvo.META_DATA)


@patch('datacollection.datacollection.os.walk')
def test_read_marketplace_files_mintos(os_walk):
    os_walk.return_value = [
        ('/mintos', ('',), (
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
    assert output_data == read_marketplace_files("dummy/folder", mintos.META_DATA)

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


def test_filter_investment_files_by_newest_date_returns_newest_date_independent_of_the_other_platform():
    input_data = {
        'platform_A' : {
            datetime.date.fromisoformat("2021-11-01") : "A/path1.xls",
            datetime.date.fromisoformat("2021-12-01") : "A/path2.xls",
        },
        'platform_B' : {
            datetime.date.fromisoformat("2021-11-01") : "B/path1.xls",
            datetime.date.fromisoformat("2021-12-01") : "B/path2.xls",
            datetime.date.fromisoformat("2022-01-01") : "B/path3.xls",
        },
    }
    output_data = {
        'platform_A' : {
            datetime.date.fromisoformat("2021-12-01") : "A/path2.xls",
        },
        'platform_B' : {
            datetime.date.fromisoformat("2022-01-01") : "B/path3.xls",
        },
    }
    assert output_data == filter_investment_files_by_newest_date(input_data)


def test_filter_investment_files_by_newest_date():
    input_data = {
        'platform_A' : {
            datetime.date.fromisoformat("2021-11-01") : "A/path1.xls",
            datetime.date.fromisoformat("2021-12-01") : "A/path2.xls",
        },
        'platform_B' : {
            datetime.date.fromisoformat("2021-12-01") : "B/path2.xls",
            datetime.date.fromisoformat("2021-11-01") : "B/path1.xls",
        },
    }
    output_data = {
        'platform_A' : {
            datetime.date.fromisoformat("2021-12-01") : "A/path2.xls",
        },
        'platform_B' : {
            datetime.date.fromisoformat("2021-12-01") : "B/path2.xls",
        },
    }
    assert output_data == filter_investment_files_by_newest_date(input_data)
