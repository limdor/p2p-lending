import datetime
from collections import defaultdict
import pandas
from logger import logger
from marketplace import marketplace


def generate_report_per_date(df_investiments):
    overall_report_per_date = defaultdict(datetime.datetime)
    for date in sorted(df_investiments[marketplace.FILE_DATE].unique()):
        overall_report_per_date[datetime.datetime.date(pandas.to_datetime(date))] = generate_report(
            df_investiments[df_investiments[marketplace.FILE_DATE] == date])

    return overall_report_per_date


def generate_report(investment_data):
    overall_report = {}
    overall_report['Data'] = investment_data

    # Overall statistics
    total_invested_by_date = investment_data[marketplace.OUTSTANDING_PRINCIPAL].sum()
    overall_report['TotalInvestment'] = total_invested_by_date
    total_invested_parts = len(investment_data.index)
    overall_report['NumberLoanParts'] = total_invested_parts

    # Statistics by Country
    overall_group_by_country = investment_data.groupby(marketplace.COUNTRY).sum()
    overall_group_by_country = overall_group_by_country.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False)
    overall_group_by_country['Percentage'] = overall_group_by_country[marketplace.OUTSTANDING_PRINCIPAL] / total_invested_by_date
    overall_report['DataByCountry'] = overall_group_by_country

    # Statistics by Loan Originator
    overall_group_by_originator = investment_data.groupby(marketplace.LOAN_ORIGINATOR).sum()
    overall_group_by_originator = overall_group_by_originator.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False)
    overall_group_by_originator['Percentage'] = overall_group_by_originator[marketplace.OUTSTANDING_PRINCIPAL] / total_invested_by_date
    overall_report['DataByLoanOriginator'] = overall_group_by_originator

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
