
import sys
import datetime
import pytest
from p2p import get_latest_report_date, filter_investment_files_by_date

INPUT_DATA = {
    datetime.date.fromisoformat("2021-11-01") : "path1.xls",
    datetime.date.fromisoformat("2021-12-01") : "path2.xls",
    datetime.date.fromisoformat("2021-08-01") : "path3.xls",
    datetime.date.fromisoformat("2021-04-01") : "path4.xls",
    datetime.date.fromisoformat("2021-02-01") : "path5.xls",
    datetime.date.fromisoformat("2021-01-01") : "path6.xls",
}


def test_get_latest_report_date():
    assert datetime.date.fromisoformat("2021-12-01") == get_latest_report_date(INPUT_DATA)


def test_filter_investment_files_by_date_all():
    assert  INPUT_DATA == filter_investment_files_by_date(INPUT_DATA,kind='all')


def test_filter_investment_files_by_date_newest():
    plaftorm_data = { 
        'platform_A' : INPUT_DATA, 
        'platform_B' : INPUT_DATA, 
    }
    filtered_data = { 
        'platform_A' : { datetime.date.fromisoformat("2021-12-01") : "path2.xls" },
        'platform_B' : { datetime.date.fromisoformat("2021-12-01") : "path2.xls" },
        }
    assert  filtered_data == filter_investment_files_by_date(plaftorm_data,kind='newest')


def test_filter_investment_files_by_date_list():
    plaftorm_data = { 
        'platform_A' : INPUT_DATA, 
    }
    filtered_data = { 
        'platform_A' : { 
            datetime.date.fromisoformat("2021-12-01") : "path2.xls",
            datetime.date.fromisoformat("2021-08-01") : "path3.xls",
            datetime.date.fromisoformat("2021-02-01") : "path5.xls",
        }
    }
    dates_to_filter = [
        datetime.date.fromisoformat("2021-12-01"),
        datetime.date.fromisoformat("2021-08-01"),
        datetime.date.fromisoformat("2021-02-01"),
        ]
    assert  filtered_data == filter_investment_files_by_date(plaftorm_data,dates=dates_to_filter)


if __name__ == "__main__":
    sys.exit(pytest.main(['-rA',__file__]))

