import datetime
from p2p import get_latest_report_date, filter_investment_files_by_newest_date

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
