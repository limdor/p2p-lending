import datetime
import pandas
from logger import logger
from marketplace import marketplace
from . import calculator


def generate_report_per_date(df_investiments):
    diversification_report_per_date = {}
    for date in df_investiments[marketplace.FILE_DATE].unique():
        formated_date = datetime.datetime.date(pandas.to_datetime(date))
        diversification_report_per_date[formated_date] = generate_report(
            formated_date, df_investiments[df_investiments[marketplace.FILE_DATE] == date])

    return diversification_report_per_date


def generate_report(report_id, investment_raw_data):
    diversification_report = {}
    diversification_report['reportId'] = report_id
    diversification_report['RawDataHash'] = calculator.get_raw_data_hash(investment_raw_data)
    diversification_report['overallInvestment'] = calculator.get_total_investment(investment_raw_data)
    diversification_report['loanParts'] = calculator.get_number_loan_parts(investment_raw_data)
    diversification_report['countryStatistics'] = {
        'investmentOneCountry': calculator.get_percentage_top_country(investment_raw_data),
        'investmentThreeCountries': calculator.get_percentage_top_3_countries(investment_raw_data)
    }
    diversification_report['originatorStatistics'] = {
        'investmentOneOriginator': calculator.get_percentage_top_originator(investment_raw_data),
        'investmentFiveOriginators': calculator.get_percentage_top_5_originators(investment_raw_data)
    }

    return diversification_report


def print_report_per_date(diversification_report_per_date):
    logger.info("*********************************")
    logger.info("**** Diversification reports ****")
    logger.info("*********************************")
    for date, report in sorted(diversification_report_per_date.items()):
        logger.info(f"Investments diversification on {date}")
        logger.info(f"|- Raw data hash: {report['RawDataHash']}")
        logger.info(f"|- Diversification Investment: {report['overallInvestment']:.2f}€")
        logger.info(f"|- The portfolio consists of at least 100 different loan parts: {report['loanParts']:d}")
        logger.info("|- Statistics by Country:")
        logger.info(f"   |- No more than 50% of loans are issued in 3 (or less) countries: {report['countryStatistics']['investmentThreeCountries']:.2f}%")
        logger.info(f"   |- No more than 33% of loans are issued in any single country: {report['countryStatistics']['investmentOneCountry']:.2f}%")
        logger.info("|- Statistics by Originator:")
        logger.info(
            f"   |- No more than 50% of loans are issued by 5 (or less) lending companies: {report['originatorStatistics']['investmentFiveOriginators']:.2f}%")
        logger.info(
            f"   |- No more than 20% of loans are issued by any single lending company: {report['originatorStatistics']['investmentOneOriginator']:.2f}%")
