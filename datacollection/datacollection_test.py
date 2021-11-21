import datetime
from unittest.mock import patch
from marketplace import iuvo, mintos
from datacollection.datacollection import read_marketplace_files

@patch('datacollection.datacollection.os.walk')
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
    assert output_data == read_marketplace_files("dummy/folder", iuvo.META_DATA)


@patch('datacollection.datacollection.os.walk')
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
    assert output_data == read_marketplace_files("dummy/folder", mintos.META_DATA)
