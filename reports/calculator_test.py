from io import StringIO
import pytest
import pandas
from reports import calculator

INPUT_RAW_DATA = pandas.read_csv(StringIO(
    "Country,Loan originator,Outstanding principal,Investment platform,Date\n"\
    "Poland,Sun Finance,50.0,mintos,2020-11-30\n"\
    "Spain,Creamfinance,75.0,mintos,2020-11-30\n"\
    "Poland,Creditstar,10.0,mintos,2020-11-30\n"\
    "Spain,Creamfinance,75.0,mintos,2020-11-30\n"\
    "Poland,Creditstar,15.0,mintos,2020-11-30\n"\
    ), parse_dates=['Date'])


def test_get_total_investment():
    expected_output = 225.0
    assert expected_output == calculator.get_total_investment(INPUT_RAW_DATA)


def test_get_number_loan_parts():
    expected_output = 5
    assert expected_output == calculator.get_number_loan_parts(INPUT_RAW_DATA)


def test_get_percentage_investment_by_country():
    expected_output = pandas.read_csv(StringIO(
        "Country,Outstanding principal,Percentage\n"\
        "Spain,150.0,0.666667\n"\
        "Poland,75.0,0.333333\n"), index_col=[0])
    pandas.testing.assert_frame_equal(
        calculator.get_percentage_investment_by_country(INPUT_RAW_DATA),
        expected_output,
        check_names=False, check_index_type=False, check_dtype=False, atol=1e-3)


def test_get_percentage_investment_by_originator():
    expected_output = pandas.read_csv(StringIO(
        "Originator,Outstanding principal,Percentage\n"\
        "Creamfinance,150.0,0.666667\n"\
        "Sun Finance,50.0,0.222222\n"\
        "Creditstar,25.0,0.111111"), index_col=[0])
    pandas.testing.assert_frame_equal(
        calculator.get_percentage_investment_by_originator(INPUT_RAW_DATA),
        expected_output,
        check_names=False, check_index_type=False, check_dtype=False, atol=1e-3)


def test_get_percentage_top_country():
    expected_output = pytest.approx(66.66, abs=1e-2)
    assert expected_output == calculator.get_percentage_top_country(INPUT_RAW_DATA)


def test_get_percentage_top_3_countries():
    expected_output = 100.0
    assert expected_output == calculator.get_percentage_top_3_countries(INPUT_RAW_DATA)


def test_get_percentage_top_originator():
    expected_output = pytest.approx(66.66, abs=1e-2)
    assert expected_output == calculator.get_percentage_top_originator(INPUT_RAW_DATA)


def get_percentage_top_5_originators():
    expected_output = 100.0
    assert expected_output == calculator.get_percentage_top_5_originators(INPUT_RAW_DATA)
