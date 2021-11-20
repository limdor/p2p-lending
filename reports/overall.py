import datetime
from collections import defaultdict
import pandas
from logger import logger
from marketplace import marketplace
from . import calculator


def compute_total_investment(investment_raw_data):
    return investment_raw_data[marketplace.OUTSTANDING_PRINCIPAL].sum()


def generate_report_per_date(df_investiments):
    overall_report_per_date = defaultdict(datetime.datetime)
    for date in sorted(df_investiments[marketplace.FILE_DATE].unique()):
        overall_report_per_date[datetime.datetime.date(pandas.to_datetime(date))] = generate_report(
            df_investiments[df_investiments[marketplace.FILE_DATE] == date])

    return overall_report_per_date


def generate_report(investment_raw_data):
    overall_report = {}
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
    for date, overall_data in overall_report.items():
        logger.info(f"Overall Investments on {date}")
        logger.info(f"|- Overall Investment: {overall_data['TotalInvestment']:.2f}€")
        logger.info("|- Investment by Country")
        logger.info(overall_data['DataByCountry'])
        logger.info("|- Investment by Loan Originator")
        logger.info(overall_data['DataByLoanOriginator'])