
import sys
import datetime
import pytest
from p2p import get_latest_report_date

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

if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
