import pandas
import datetime
from logger import logger
from collections import defaultdict
from marketplace import marketplace


def generate_report_per_date(df_investiments, investment_files):
    overall_report = defaultdict(datetime.datetime)
    for date in sorted({date for data_file in investment_files.values() for date in data_file}):
        # Overall statistics
        overall_group_by_date = df_investiments[df_investiments[marketplace.FILE_DATE] == pandas.Timestamp(date)]
        total_invested_by_date = overall_group_by_date[marketplace.OUTSTANDING_PRINCIPAL].sum()
        total_invested_parts = len(overall_group_by_date.index)

        # Statistics by Country
        overall_group_by_country = overall_group_by_date.groupby(marketplace.COUNTRY).sum()
        overall_group_by_country = overall_group_by_country.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False)
        overall_group_by_country['Percentage'] = overall_group_by_country[marketplace.OUTSTANDING_PRINCIPAL] / total_invested_by_date

        # Statistics by Loan Originator
        overall_group_by_originator = overall_group_by_date.groupby(marketplace.LOAN_ORIGINATOR).sum()
        overall_group_by_originator = overall_group_by_originator.sort_values(by=marketplace.OUTSTANDING_PRINCIPAL, ascending=False)
        overall_group_by_originator['Percentage'] = overall_group_by_originator[marketplace.OUTSTANDING_PRINCIPAL] / total_invested_by_date

        # It will be used in the diversification
        overall_report[date] = {
            'Data': overall_group_by_date,
            'DataByCountry': overall_group_by_country,
            'DataByLoanOriginator': overall_group_by_originator,
            'TotalInvestment':  total_invested_by_date,
            'NumberLoanParts': total_invested_parts
        }

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