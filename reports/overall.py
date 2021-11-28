import datetime
import pandas
from logger import logger
from marketplace import marketplace
from . import calculator


def generate_report_per_date(df_investiments):
    overall_report_per_date = {}
    for date in df_investiments[marketplace.FILE_DATE].unique():
        overall_report_per_date[datetime.datetime.date(pandas.to_datetime(date))] = generate_report(
            df_investiments[df_investiments[marketplace.FILE_DATE] == date])

    return overall_report_per_date


def generate_report(investment_raw_data):
    overall_report = {}
    overall_report['RawDataHash'] = calculator.get_raw_data_hash(investment_raw_data)
    overall_report['Data'] = investment_raw_data
    overall_report['TotalInvestment'] = calculator.get_total_investment(investment_raw_data)
    overall_report['NumberLoanParts'] = calculator.get_number_loan_parts(investment_raw_data)
    overall_report['DataByCountry'] = calculator.get_percentage_investment_by_country(investment_raw_data)
    overall_report['DataByLoanOriginator'] = calculator.get_percentage_investment_by_originator(investment_raw_data)

    return overall_report


def print_report_per_date(overall_report):
    logger.info("*****************************")
    logger.info("**** Overall Investments ****")
    logger.info("*****************************")
    for date, overall_data in sorted(overall_report.items()):
        logger.info(f"Overall Investments on {date}")
        logger.info(f"|- Raw data hash: {overall_data['RawDataHash']}")
        logger.info(f"|- Overall Investment: {overall_data['TotalInvestment']:.2f}€")
        logger.info("|- Investment by Country")
        logger.info(overall_data['DataByCountry'])
        logger.info("|- Investment by Loan Originator")
        logger.info(overall_data['DataByLoanOriginator'])
